# Marakulin Andrey https://github.com/Annndruha
# 2023

import logging
from asyncio import to_thread
from html import escape
from io import BytesIO

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import CallbackContext, ContextTypes

from src import marketing
from src.answers import Answers
from src.db import TgUser
from src.errors_solver import errors_solver
from src.log_formatter import log_actor, log_formatter
from src.settings import Settings

ans = Answers()
settings = Settings()
engine = create_engine(url=settings.db_url, pool_pre_ping=True, isolation_level='AUTOCOMMIT')
Session = sessionmaker(bind=engine)
PRINT_API_TIMEOUT = (5, 30)


@errors_solver
@log_formatter
async def handler_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard_base = [[InlineKeyboardButton(ans.about, callback_data='to_about')]]
    text, reply_markup = __change_message_by_auth(update, ans.hello, keyboard_base)
    await update.message.reply_text(text=text, reply_markup=reply_markup, disable_web_page_preview=True)


@errors_solver
@log_formatter
async def handler_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        ans.help.format(limit=settings.MAX_PDF_SIZE_MB), disable_web_page_preview=True, parse_mode=ParseMode('HTML')
    )


@errors_solver
@log_formatter
async def handler_auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requisites = __auth(update)
    if requisites is None:
        await update.message.reply_text(ans.val_need)
    else:
        await update.message.reply_text(ans.val_info.format(*requisites), parse_mode=ParseMode('HTML'))


@errors_solver
@log_formatter
async def handler_button_browser(update: Update, context: CallbackContext) -> None:
    if update.callback_query.data == 'to_hello':
        keyboard_base = [[InlineKeyboardButton(ans.about, callback_data='to_about')]]
        text, reply_markup = __change_message_by_auth(update, ans.hello, keyboard_base)

    elif update.callback_query.data == 'to_about':
        keyboard_base = [[InlineKeyboardButton(ans.back, callback_data='to_hello')]]
        text, reply_markup = __change_message_by_auth(
            update, ans.help.format(limit=settings.MAX_PDF_SIZE_MB), keyboard_base
        )

    elif update.callback_query.data == 'to_auth':
        keyboard_base = [[InlineKeyboardButton(ans.back, callback_data='to_hello')]]
        text, reply_markup = ans.val_need, InlineKeyboardMarkup(keyboard_base)

    elif update.callback_query.data.startswith('print_'):
        await __print_settings_solver(update, context)
        return

    else:
        text, reply_markup = ans.unknown_keyboard_payload, None

    await update.callback_query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        parse_mode=ParseMode('HTML'),
    )


@errors_solver
@log_formatter
async def handler_unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ans.unknown_command)


@errors_solver
@log_formatter
async def handler_print(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requisites = __auth(update)
    if requisites is None:
        await context.bot.send_message(chat_id=update.message.chat.id, text=ans.doc_not_accepted)
        logging.warning(f'{log_actor(update)} try print with no auth')
        return
    document = update.message.document
    filename = document.file_name or 'document.pdf'
    display_filename = escape(filename)
    try:
        filebytes = await __get_attachments(document, context)
        logging.info(f'{log_actor(update)} get attachments OK')
    except FileSizeError:
        await update.message.reply_text(
            text=ans.file_size_error.format(filename=display_filename, limit=settings.MAX_PDF_SIZE_MB),
            reply_to_message_id=update.message.id,
            parse_mode=ParseMode('HTML'),
        )
        logging.warning(f'{log_actor(update)} get attachments FileSizeError')
        return
    except TelegramError:
        await update.message.reply_text(text=ans.download_error, reply_to_message_id=update.message.id)
        logging.warning(f'{log_actor(update)} get attachments download_error')
        return

    r = await to_thread(
        requests.post,
        settings.PRINT_URL + '/file',
        json={'surname': requisites[1], 'number': requisites[2], 'filename': filename, 'source': 'tgbot'},
        timeout=PRINT_API_TIMEOUT,
    )
    if r.status_code == 200:
        pin = r.json()['pin']
        files = {
            'file': (
                filename,
                filebytes.getvalue(),
                'application/pdf',
                {'Expires': '0'},
            )
        }
        r = await to_thread(requests.post, settings.PRINT_URL + '/file/' + pin, files=files, timeout=PRINT_API_TIMEOUT)
        if r.status_code == 200:
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=ans.qr,
                            web_app=WebAppInfo(ans.qr_print.format(settings.PRINT_URL_QR, pin)),
                        )
                    ],
                    [InlineKeyboardButton(ans.kb_print, callback_data=f'print_settings_{pin}')],
                ]
            )
            await update.message.reply_text(
                text=ans.send_to_print.format(display_filename, escape(pin)),
                reply_markup=reply_markup,
                reply_to_message_id=update.message.id,
                disable_web_page_preview=True,
                parse_mode=ParseMode('HTML'),
            )
            logging.info(f'{log_actor(update)} print success')
            await to_thread(
                marketing.print_success,
                tg_id=update.message.chat.id,
                surname=requisites[1],
                number=requisites[2],
                pin=pin,
            )
            return
        if r.status_code == 415:
            await update.message.reply_text(
                text=ans.unreadable_file_error.format(display_filename),
                reply_to_message_id=update.message.id,
                parse_mode=ParseMode('HTML'),
            )
            logging.warning(f'{log_actor(update)} print api 415 UnreadableErr')
            return

    if r.status_code == 413:
        await update.message.reply_text(
            text=ans.print_limit_error.format(display_filename),
            reply_to_message_id=update.message.id,
            parse_mode=ParseMode('HTML'),
        )
        logging.warning(f'{log_actor(update)} print api 413 LimitErr')
        return

    await update.message.reply_text(ans.print_err, reply_to_message_id=update.message.id)
    logging.warning('%s print API returned HTTP %s', log_actor(update), r.status_code)


@errors_solver
@log_formatter
async def handler_mismatch_doctype(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ans.only_pdf)
    await to_thread(marketing.print_exc_format, tg_id=update.message.chat_id)


@errors_solver
@log_formatter
async def handler_other_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ans.err_message_type)


@errors_solver
@log_formatter
async def handler_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat.id

    if text is None or len(text.split('\n')) != 2:
        with Session() as session:
            if session.query(TgUser).filter(TgUser.tg_id == chat_id).one_or_none() is None:
                await context.bot.send_message(chat_id=chat_id, text=ans.val_need)
                logging.warning(f'{log_actor(update)} val_need')
            else:
                await context.bot.send_message(chat_id=chat_id, text=ans.val_update_fail)
                logging.warning(f'{log_actor(update)} val_update_fail')
        return

    surname, number = (line.strip() for line in text.split('\n'))
    is_member = False
    if surname and number:
        response = await to_thread(
            requests.get,
            settings.PRINT_URL + '/is_union_member',
            params=dict(surname=surname, v=1, number=number),
            timeout=PRINT_API_TIMEOUT,
        )
        response.raise_for_status()
        is_member = response.json() is True
    if not is_member:
        await context.bot.send_message(chat_id=chat_id, text=ans.val_fail)
        await to_thread(marketing.register_exc_wrong, tg_id=chat_id, surname=surname, number=number)
        logging.info('%s membership check failed', log_actor(update))
        return

    with Session() as session:
        data: TgUser | None = session.query(TgUser).filter(TgUser.tg_id == update.effective_user.id).one_or_none()
        if data is None:
            session.add(TgUser(tg_id=chat_id, surname=surname, number=number))
            reply, report = ans.val_pass, marketing.register
        else:
            data.surname = surname
            data.number = number
            reply, report = ans.val_update_pass, marketing.re_register
        session.commit()
    await context.bot.send_message(chat_id=chat_id, text=reply)
    await to_thread(report, tg_id=chat_id, surname=surname, number=number)
    logging.info('%s membership saved', log_actor(update))
    return True


async def __print_settings_solver(update: Update, context: CallbackContext):
    _, button, pin = update.callback_query.data.split('_')

    file_url = f'{settings.PRINT_URL}/file/{pin}'
    r = await to_thread(requests.get, file_url, timeout=PRINT_API_TIMEOUT)
    if r.status_code == 200:
        options = r.json()['options']
    else:
        await update.callback_query.message.reply_text(ans.settings_change_fail)
        return

    if button == 'copies':
        options['copies'] = options['copies'] % 5 + 1
    elif button == 'twosided':
        options['two_sided'] = not options['two_sided']
    else:
        await context.bot.answer_callback_query(update.callback_query.id, ans.settings_warning)

    r = await to_thread(requests.patch, file_url, json={'options': options}, timeout=PRINT_API_TIMEOUT)
    if r.status_code != 200:
        await update.callback_query.message.reply_text(ans.settings_change_fail)
        return

    keyboard = [
        [
            InlineKeyboardButton(
                text=ans.qr,
                web_app=WebAppInfo(ans.qr_print.format(settings.PRINT_URL_QR, pin)),
            )
        ],
        [
            InlineKeyboardButton(
                f'{ans.kb_print_copies} {options["copies"]}',
                callback_data=f'print_copies_{pin}',
            )
        ],
        [
            InlineKeyboardButton(
                ans.kb_print_two_side if options['two_sided'] else ans.kb_print_side,
                callback_data=f'print_twosided_{pin}',
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)


def __auth(update):
    with Session() as session:
        data: TgUser | None = session.query(TgUser).filter(TgUser.tg_id == update.effective_user.id).one_or_none()
        if data is not None:
            return data.tg_id, data.surname, data.number


def __change_message_by_auth(update, text, keyboard):
    if __auth(update) is None:
        text += ans.val_addition
        keyboard.append([InlineKeyboardButton(ans.auth, callback_data='to_auth')])
    return text, InlineKeyboardMarkup(keyboard)


class FileSizeError(Exception):
    pass


async def __get_attachments(document, context):
    max_size = settings.MAX_PDF_SIZE_MB * 1024**2
    if document.file_size is not None and document.file_size > max_size:
        raise FileSizeError
    file_info = await context.bot.get_file(document.file_id)
    filebytes = BytesIO()
    await file_info.download_to_memory(filebytes)
    if filebytes.getbuffer().nbytes > max_size:
        raise FileSizeError
    return filebytes
