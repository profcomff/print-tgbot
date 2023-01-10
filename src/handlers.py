# Marakulin Andrey @annndruha
# 2023

import os
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext

import config
import src.database_functions as db
from src.answers import ans


async def handler_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Конфиденциальность", callback_data='want_confident')]]
    text = ans['help']
    if __auth(update, context) is None:
        text += ans['val_addition']
        keyboard.append([InlineKeyboardButton("Авторизация", callback_data='auth')])

    await update.message.reply_text(text,
                                    reply_markup=InlineKeyboardMarkup(keyboard),
                                    disable_web_page_preview=True)


async def handler_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ans['help'])


async def handler_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == 'want_instruction':
        text = ans['help']
        keyboard = [[InlineKeyboardButton("Конфиденциальность", callback_data='want_confident')]]
        if not __auth(update, context) is None:
            keyboard.append([InlineKeyboardButton("Авторизация", callback_data='auth')])
            text += ans['val_addition']
        reply_markup = InlineKeyboardMarkup(keyboard)

    elif query.data == 'want_confident':
        text = ans['conf_full']
        keyboard = [[InlineKeyboardButton("<- Назад", callback_data='want_instruction')]]
        if __auth(update, context) is None:
            keyboard.append([InlineKeyboardButton("Авторизация", callback_data='auth')])
            text += ans['val_addition']
        reply_markup = InlineKeyboardMarkup(keyboard)

    elif query.data == 'auth':
        text = ans['val_need']
        reply_markup = None
    else:
        text = 'Видимо бот обновился, выполните команду /start'
        reply_markup = None

    await query.answer()
    await query.edit_message_text(text=text, reply_markup=reply_markup, disable_web_page_preview=True)


async def handler_unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Неизвестная команда.\nУ бота лишь две команды: /start /about')


async def handler_mismatch_doctype(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Документы на печать принимаются только в формате PDF')


async def handler_print(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requisites = __auth(update, context)
    if requisites is None:
        await context.bot.send_message(chat_id=update.message.chat.id,
                                       text='❌ Документ не будет распечатан. ❌')
        await context.bot.send_message(chat_id=update.message.chat.id,
                                       text=ans['val_need'])
        return

    pdf_path = await __get_attachments(update, context)
    vk_id, surname, number = requisites
    title = update.message.document.file_name

    pin = None
    if pdf_path is not None:
        r = requests.post(config.PRINT_URL + '/file', json={'surname': surname, 'number': number, 'filename': title})
        if r.status_code == 200:
            pin = r.json()['pin']
            files = {'file': (title, open(pdf_path, 'rb'), 'application/pdf', {'Expires': '0'})}
            rfile = requests.post(config.PRINT_URL + '/file/' + pin, files=files)
            if rfile.status_code == 200:
                await context.bot.send_message(chat_id=update.message.chat.id,
                                               text=ans['send_to_print'].format(pin))
                await context.bot.send_message(chat_id=update.message.chat.id,
                                               text=ans['qrprint'].format(pin))
                # log.print(
                #     vk_id=vk_id,
                #     surname=surname,
                #     number=number,
                #     pin=pin,
                # )
            else:
                await context.bot.send_message(chat_id=update.message.chat.id,
                                               text=ans['print_err'])
                # log.print_exc_other(
                #     vk_id=vk_id,
                #     surname=surname,
                #     number=number,
                #     pin=pin,
                #     status_code=rfile.status_code,
                #     description='Fail on file upload',
                # )
        else:
            await context.bot.send_message(chat_id=update.message.chat.id,
                                           text=ans['print_err'])
            # log.print_exc_other(
            #     vk_id=vk_id,
            #     surname=surname,
            #     number=number,
            #     pin=pin,
            #     status_code=r.status_code,
            #     description='Fail on fetching code',
            # )


async def handler_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat.id

    if len(text.split('\n')) == 2:
        surname = text.split('\n')[0].strip()
        number = text.split('\n')[1].strip()

        r = requests.get(config.PRINT_URL + '/is_union_member', params=dict(surname=surname, v=1, number=number))
        data = db.get_user(update.effective_user.id)
        if r.json() and data is None:
            db.add_user(chat_id, surname, number)
            await context.bot.send_message(chat_id=chat_id, text=ans['val_pass'])
            return True
        elif r.json() and data is not None:
            db.update_user(chat_id, surname, number)
            await context.bot.send_message(chat_id=chat_id, text=ans['val_update_pass'])
            # log.register(
            #     vk_id=user.user_id,
            #     surname=surname,
            #     number=number,
            # )
            return True
        elif r.json() is False:
            await context.bot.send_message(chat_id=chat_id, text=ans['val_fail'])
            # log.register_exc_wrong(
            #     vk_id=user.user_id,
            #     surname=surname,
            #     number=number,
            # )
    else:
        if db.get_user(chat_id) is None:
            await context.bot.send_message(chat_id=chat_id, text=ans['val_need'])
        else:
            await context.bot.send_message(chat_id=chat_id, text=ans['val_update_fail'])


async def __get_attachments(update, context):
    if not os.path.exists(config.PDF_PATH):
        os.makedirs(config.PDF_PATH)
    if not os.path.exists(os.path.join(config.PDF_PATH, str(update.message.chat.id))):
        os.makedirs(os.path.join(config.PDF_PATH, str(update.message.chat.id)))
    path_to_save = os.path.join(config.PDF_PATH, str(update.message.chat.id), update.message.document.file_name)

    file = await context.bot.get_file(update.message.document.file_id)
    await file.download_to_drive(custom_path=path_to_save)
    await context.bot.send_message(chat_id=update.message.chat.id,
                                   text=ans['file_uploaded'].format(update.message.document.file_name))
    return path_to_save


def __auth(update, context):
    chat_id = update.effective_user.id
    if db.get_user(chat_id) is not None:
        tg_id, surname, number = db.get_user(chat_id)
        r = requests.get(config.PRINT_URL + '/is_union_member', params=dict(surname=surname, number=number, v=1))
        if r.json():
            return tg_id, surname, number
