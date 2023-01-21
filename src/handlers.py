# Marakulin Andrey https://github.com/Annndruha
# 2023

import logging
import time
import traceback
from io import BytesIO

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import ContextTypes, CallbackContext

from src import marketing
from src.answers import ans
from src.db import TgUser
from src.settings import get_settings

settings = get_settings()
engine = create_engine(url=settings.DB_DSN, pool_pre_ping=True)
Session = sessionmaker(bind=engine, autocommit=True)
session = Session()


def handler(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await func(update, context)
        except (TelegramError, Exception) as err:
            await context.bot.send_message(chat_id=update.effective_user.id, text=ans['im_broken'])
            logging.error(f'Exception {str(err.args)}, traceback:')
            traceback.print_tb(err.__traceback__)
            time.sleep(2)

    return wrapper


@handler
async def handler_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard_base = [[InlineKeyboardButton(ans['about'], callback_data='to_about')]]
    text, reply_markup = __change_message_by_auth(update, ans['hello'], keyboard_base)
    await update.message.reply_text(text=text,
                                    reply_markup=reply_markup,
                                    disable_web_page_preview=True)


@handler
async def handler_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ans['help'], disable_web_page_preview=True, parse_mode=ParseMode('HTML'))


@handler
async def handler_auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requisites = __auth(update)
    if requisites is None:
        await update.message.reply_text(ans['val_need'])
    else:
        await update.message.reply_text(ans['val_info'].format(*requisites), parse_mode=ParseMode('HTML'))


@handler
async def handler_button_browser(update: Update, context: CallbackContext) -> None:
    if update.callback_query.data == 'to_hello':
        keyboard_base = [[InlineKeyboardButton(ans['about'], callback_data='to_about')]]
        text, reply_markup = __change_message_by_auth(update, ans['hello'], keyboard_base)

    elif update.callback_query.data == 'to_about':
        keyboard_base = [[InlineKeyboardButton(ans['back'], callback_data='to_hello')]]
        text, reply_markup = __change_message_by_auth(update, ans['help'], keyboard_base)

    elif update.callback_query.data == 'to_auth':
        keyboard_base = [[InlineKeyboardButton(ans['back'], callback_data='to_hello')]]
        text, reply_markup = ans['val_need'], InlineKeyboardMarkup(keyboard_base)

    elif update.callback_query.data.startswith('print_'):
        await __print_settings_solver(update, context)
        return

    else:
        text, reply_markup = ans['unknown_keyboard_payload'], None

    await update.callback_query.edit_message_text(text=text,
                                                  reply_markup=reply_markup,
                                                  disable_web_page_preview=True,
                                                  parse_mode=ParseMode('HTML'))


@handler
async def handler_unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ans['unknown_command'])


@handler
async def handler_print(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requisites = __auth(update)
    if requisites is None:
        await context.bot.send_message(chat_id=update.message.chat.id,
                                       text=ans['doc_not_accepted'])
        return
    try:
        filebytes, filename = await __get_attachments(update, context)
    except FileSizeError:
        await update.message.reply_text(text=ans['file_size_error'].format(update.message.document.file_name),
                                        reply_to_message_id=update.message.id,
                                        parse_mode=ParseMode('HTML'))
        return
    except TelegramError:
        await update.message.reply_text(text=ans['download_error'], reply_to_message_id=update.message.id)
        return

    r = requests.post(settings.PRINT_URL + '/file',
                      json={'surname': requisites[1], 'number': requisites[2], 'filename': filename})
    if r.status_code == 200:
        pin = r.json()['pin']
        files = {'file': (filename, filebytes.getvalue(), 'application/pdf', {'Expires': '0'})}
        rfile = requests.post(settings.PRINT_URL + '/file/' + pin, files=files)
        if rfile.status_code == 200:
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text=ans['qr'], web_app=WebAppInfo(ans['qr_print'].format(pin)))],
                 [InlineKeyboardButton(ans['kb_print'], callback_data=f'print_settings_{pin}')]])
            await update.message.reply_text(
                text=ans['send_to_print'].format(update.message.document.file_name, pin),
                reply_markup=reply_markup,
                reply_to_message_id=update.message.id,
                disable_web_page_preview=True,
                parse_mode=ParseMode('HTML'))
            marketing.print_success(tg_id=update.message.chat.id, surname=requisites[1], number=requisites[2])
            return

    await context.bot.send_message(chat_id=update.effective_user.id,
                                   text=ans['print_err'], parse_mode=ParseMode('HTML'))


@handler
async def handler_mismatch_doctype(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ans['only_pdf'])
    marketing.print_exc_format(tg_id=update.message.chat_id)


@handler
async def handler_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat.id
    if text is None:
        if session.query(TgUser).filter(TgUser.tg_id == chat_id).one_or_none() is None:
            await context.bot.send_message(chat_id=chat_id, text=ans['val_need'])
        else:
            await context.bot.send_message(chat_id=chat_id, text=ans['val_update_fail'])
        return

    if len(text.split('\n')) == 2:
        surname = text.split('\n')[0].strip()
        number = text.split('\n')[1].strip()

        r = requests.get(settings.PRINT_URL + '/is_union_member', params=dict(surname=surname, v=1, number=number))
        data: TgUser = session.query(TgUser).filter(TgUser.tg_id == update.effective_user.id).one_or_none()
        if r.json() and data is None:
            session.add(TgUser(tg_id=chat_id, surname=surname, number=number))
            session.flush()
            await context.bot.send_message(chat_id=chat_id, text=ans['val_pass'])
            marketing.register(tg_id=chat_id, surname=surname, number=number)
            return True
        elif r.json() and data is not None:
            data.surname = surname
            data.number = number
            await context.bot.send_message(chat_id=chat_id, text=ans['val_update_pass'])
            marketing.re_register(tg_id=chat_id, surname=surname, number=number)
            return True
        elif r.json() is False:
            await context.bot.send_message(chat_id=chat_id, text=ans['val_fail'])
            marketing.register_exc_wrong(tg_id=chat_id, surname=surname, number=number)
    else:
        if session.query(TgUser).filter(TgUser.tg_id == chat_id).one_or_none() is None:
            await context.bot.send_message(chat_id=chat_id, text=ans['val_need'])
        else:
            await context.bot.send_message(chat_id=chat_id, text=ans['val_update_fail'])


async def __print_settings_solver(update: Update, context: CallbackContext):
    _, button, pin = update.callback_query.data.split('_')

    r = requests.get(settings.PRINT_URL + f'''/file/{pin}''')
    if r.status_code == 200:
        options = r.json()['options']
    else:
        await update.callback_query.message.reply_text(ans['settings_change_fail'])
        return

    if button == 'copies':
        options['copies'] = options['copies'] % 5 + 1
    elif button == 'twosided':
        options['two_sided'] = not options['two_sided']
    else:
        await context.bot.answer_callback_query(update.callback_query.id, ans['settings_warning'])

    r = requests.patch(settings.PRINT_URL + f'''/file/{pin}''', json={'options': options})
    if r.status_code != 200:
        await update.callback_query.message.reply_text(ans['settings_change_fail'])
        return

    keyboard = [
        [InlineKeyboardButton(text=ans['qr'], web_app=WebAppInfo(ans['qr_print'].format(pin)))],
        [InlineKeyboardButton(f'{ans["kb_print_copies"]} {options["copies"]}', callback_data=f'print_copies_{pin}')],
        [InlineKeyboardButton(ans['kb_print_two_side'] if options['two_sided'] else ans['kb_print_side'],
                              callback_data=f'print_twosided_{pin}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)


def __auth(update):
    chat_id = update.effective_user.id
    if session.query(TgUser).filter(TgUser.tg_id == chat_id).one_or_none() is not None:
        tguser: TgUser = session.query(TgUser).filter(TgUser.tg_id == chat_id).one_or_none()
        r = requests.get(settings.PRINT_URL + '/is_union_member',
                         params=dict(surname=tguser.surname, number=tguser.number, v=1))
        if r.json():
            return tguser.tg_id, tguser.surname, tguser.number


def __change_message_by_auth(update, text, keyboard):
    if __auth(update) is None:
        text += ans['val_addition']
        keyboard.append([InlineKeyboardButton(ans['auth'], callback_data='to_auth')])
    return text, InlineKeyboardMarkup(keyboard)


class FileSizeError(Exception):
    pass


async def __get_attachments(update, context):
    if update.message.document.file_size / 1024 ** 2 > settings.MAX_PDF_SIZE_MB:
        raise FileSizeError
    file_info = await context.bot.get_file(update.message.document.file_id)
    filebytes = BytesIO()
    await file_info.download_to_memory(filebytes)
    return filebytes, update.message.document.file_name
