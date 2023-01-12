# Marakulin Andrey https://github.com/Annndruha
# 2023

import os
import time
import logging
import requests
import traceback

# import psycopg2

from telegram.constants import ParseMode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import config
from src.answers import ans
from src.db import TgUser
from src.settings import get_settings

settings = get_settings()



engine = create_engine(url=settings.DB_DSN)
Session = sessionmaker(bind=engine, autocommit=True)
session = Session()


def handler(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await func(update, context)
        # except psycopg2.Error as err:
        #     logging.error('Database Error (wrapper), description:')
        #     traceback.print_tb(err.__traceback__)
        #     logging.error(err.args)
        #     try:
        #         logging.warning('Try to reconnect database...')
        #         db.reconnect()
        #         logging.warning('Database connected successful')
        #         time.sleep(1)
        #     except psycopg2.Error:
        #         logging.error('Reconnect database failed')
        #         time.sleep(10)

        except Exception as err:
            await context.bot.send_message(
                chat_id=update.effective_user.id, text=ans['im_broken'],
                parse_mode=ParseMode('HTML'))
            logging.error('Exception (wrapper), description:')
            traceback.print_tb(err.__traceback__)
            logging.error(str(err.args))
            time.sleep(5)

    return wrapper


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.error(msg="Exception while handling an update:", exc_info=context.error)
    await context.bot.send_message(
        chat_id=update.effective_user.id, text=ans['im_broken'], parse_mode=ParseMode('HTML'))


@handler
async def handler_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(ans['conf'], callback_data='want_confident')]]
    text = ans['help']
    if __auth(update) is None:
        text += ans['val_addition']
        keyboard.append([InlineKeyboardButton(ans['auth'], callback_data='auth')])
    await update.message.reply_text(text=text,
                                    reply_markup=InlineKeyboardMarkup(keyboard),
                                    disable_web_page_preview=True)


@handler
async def handler_button(update: Update, context: CallbackContext) -> None:
    if update.callback_query.data == 'want_instruction':
        logging.info('button want_instruction pressed')
        text = ans['help']
        keyboard = [[InlineKeyboardButton(ans['conf'], callback_data='want_confident')]]
        if __auth(update) is None:
            keyboard.append([InlineKeyboardButton(ans['auth'], callback_data='auth')])
            text += ans['val_addition']
        reply_markup = InlineKeyboardMarkup(keyboard)

    elif update.callback_query.data == 'want_confident':
        logging.info('button want_instruction pressed')
        text = ans['conf_full']
        keyboard = [[InlineKeyboardButton(ans['back'], callback_data='want_instruction')]]
        if __auth(update) is None:
            keyboard.append([InlineKeyboardButton(ans['auth'], callback_data='auth')])
            text += ans['val_addition']
        reply_markup = InlineKeyboardMarkup(keyboard)

    elif update.callback_query.data == 'auth':
        text = ans['val_need']
        reply_markup = None
    elif update.callback_query.data.startswith('print_'):
        await __print_settings_solver(update)
        return
    else:
        text = ans['unknown_query']
        reply_markup = None

    await update.callback_query.answer()
    logging.info('im here')
    await update.callback_query.edit_message_text(text=text,
                                                  reply_markup=reply_markup,
                                                  disable_web_page_preview=True,
                                                  parse_mode=ParseMode('HTML'))


@handler
async def handler_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ans['help'])


@handler
async def handler_auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requisites = __auth(update)
    if requisites is None:
        await update.message.reply_text(ans['val_need'])
    else:
        tg_id, surname, number = requisites
        await update.message.reply_text(ans['val_info'].format(tg_id, surname, number),
                                        parse_mode=ParseMode('HTML'))


@handler
async def handler_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ans['history_not_implement'])


@handler
async def handler_unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ans['unknown_command'])


@handler
async def handler_mismatch_doctype(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ans['only_pdf'])


async def __print_settings_solver(update):
    _, button, pin = update.callback_query.data.split('_')

    r = requests.get(settings.PRINT_URL + f'''/file/{pin}''')
    if r.status_code == 200:
        options = r.json()['options']
    else:
        await update.callback_query.message.reply_text('Сервер не ответил, попробуйте позже.')
        return

    if button == 'copies':
        options['copies'] = options['copies'] % 5 + 1
    if button == 'twosided':
        options['two_sided'] = not options['two_sided']

    r = requests.patch(settings.PRINT_URL + f'''/file/{pin}''', json={'options': options})
    if r.status_code != 200:
        await update.callback_query.message.reply_text('Сервер не ответил, настройки не изменены, попробуйте позже.')
        return

    keyboard = [[InlineKeyboardButton(f'Копий: {options["copies"]}', callback_data=f'print_copies_{pin}')],
                [InlineKeyboardButton('Двухсторонняя печать' if options['two_sided'] else 'Односторонняя печать',
                                      callback_data=f'print_twosided_{pin}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)


async def handler_print(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requisites = __auth(update)
    if requisites is None:
        await context.bot.send_message(chat_id=update.message.chat.id,
                                       text=ans['doc_not_accepted'])
        await context.bot.send_message(chat_id=update.message.chat.id,
                                       text=ans['val_need'])
        return

    pdf_path, filename = await __get_attachments(update, context)
    if not os.path.exists(pdf_path):
        await update.message.reply_text(text=ans['download_error'], reply_to_message_id=update.message.id)
        return

    r = requests.post(settings.PRINT_URL + '/file',
                      json={'surname': requisites[1], 'number': requisites[2], 'filename': filename})
    if r.status_code == 200:
        pin = r.json()['pin']
        files = {'file': (filename, open(pdf_path, 'rb'), 'application/pdf', {'Expires': '0'})}
        rfile = requests.post(settings.PRINT_URL + '/file/' + pin, files=files)
        if rfile.status_code == 200:
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'Настройки печати', callback_data=f'print_settings_{pin}')]])
            await update.message.reply_text(
                text=ans['send_to_print'].format(update.message.document.file_name, pin, pin),
                reply_markup=reply_markup,
                reply_to_message_id=update.message.id,
                disable_web_page_preview=True,
                parse_mode=ParseMode('HTML'))
            return

    await update.callback_query.edit_message_text(text=ans['print_err'],
                                                  parse_mode=ParseMode('HTML'))


@handler
async def handler_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text  # TODO: ("'NoneType' object has no attribute 'text'",)
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
            # TgUser
            # db.add_user(chat_id, surname, number)
            await context.bot.send_message(chat_id=chat_id, text=ans['val_pass'])
            return True
        elif r.json() and data is not None:
            # db.update_user(chat_id, surname, number)
            # tguser = session.query(TgUser).filter(TgUser.tg_id == chat_id).one_or_none()
            data.surname = surname
            data.number = number
            await context.bot.send_message(chat_id=chat_id, text=ans['val_update_pass'])
            return True
        elif r.json() is False:
            await context.bot.send_message(chat_id=chat_id, text=ans['val_fail'])
    else:
        if session.query(TgUser).filter(TgUser.tg_id == chat_id).one_or_none() is None:
            await context.bot.send_message(chat_id=chat_id, text=ans['val_need'])
        else:
            await context.bot.send_message(chat_id=chat_id, text=ans['val_update_fail'])


async def __get_attachments(update, context):
    if not os.path.exists(settings.PDF_PATH):
        os.makedirs(settings.PDF_PATH)
    if not os.path.exists(os.path.join(settings.PDF_PATH, str(update.message.chat.id))):
        os.makedirs(os.path.join(settings.PDF_PATH, str(update.message.chat.id)))
    path_to_save = os.path.join(settings.PDF_PATH, str(update.message.chat.id), update.message.document.file_name)
    # path_to_save = os.path.join(settings.PDF_PATH, update.message.document.file_unique_id + '.pdf')
    # update.message.document.file_size # TODO: Check size
    file = await context.bot.get_file(update.message.document.file_id)
    await file.download_to_drive(custom_path=path_to_save)
    return path_to_save, update.message.document.file_name  # , update.message.document.file_unique_id


def __auth(update):
    chat_id = update.effective_user.id
    if session.query(TgUser).filter(TgUser.tg_id == chat_id).one_or_none() is not None:
        tguser: TgUser = session.query(TgUser).filter(TgUser.tg_id == chat_id).one_or_none()
        r = requests.get(settings.PRINT_URL + '/is_union_member',
                         params=dict(surname=tguser.surname, number=tguser.number, v=1))
        if r.json():
            return tguser.tg_id, tguser.surname, tguser.number
