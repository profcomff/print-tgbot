# Marakulin Andrey @annndruha
# 2023

import os

import requests
from telegram import Update
from telegram.ext import ContextTypes

from src.answers import ans
import config
import src.database_functions as db


async def get_attachments(update, context):
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


async def check_proff(update, context):
    if db.get_user(update.message.chat.id) is not None:
        vk_id, surname, number = db.get_user(update.message.chat.id)
        r = requests.get(config.PRINT_URL + '/is_union_member', params=dict(surname=surname, number=number, v=1))
        if r.json():
            return vk_id, surname, number

    await context.bot.send_message(chat_id=update.message.chat.id,
                                   text='❌ Документ не будет распечатан. ❌')
    await context.bot.send_message(chat_id=update.message.chat.id,
                                   text=ans['val_need'])


async def order_print(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requisites = await check_proff(update, context)
    if requisites is None:
        return

    pdf_path = await get_attachments(update, context)
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


async def validate_proff(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


def check_auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    if db.get_user(chat_id) is not None:
        _, surname, number = db.get_user(chat_id)
        r = requests.get(config.PRINT_URL + '/is_union_member', params=dict(surname=surname, number=number, v=1))
        if r.json():
            return True
        else:
            return False
    else:
        return False
