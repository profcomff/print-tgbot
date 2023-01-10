# Marakulin Andrey @annndruha
# 2023

import os

import requests
from telegram import Update
from telegram.ext import ContextTypes

import src.answers as ans
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
                                   text=ans.print_ans['file_uploaded'].format(update.message.document.file_name))
    return path_to_save


async def check_proff(update, context):
    if db.get_user(update.message.chat.id) is not None:
        vk_id, surname, number = db.get_user(update.message.chat.id)
        r = requests.get(config.PRINT_URL + '/is_union_member', params=dict(surname=surname, number=number, v=1))
        if r.json():
            return vk_id, surname, number
        else:
            await context.bot.send_message(chat_id=update.message.chat.id,
                                           text=ans.val_ans['val_need'])
            await context.bot.send_message(chat_id=update.message.chat.id,
                                           text=ans.val_ans['exp_name'])
    else:
        await context.bot.send_message(chat_id=update.message.chat.id,
                                       text=ans.val_ans['val_need'])
        await context.bot.send_message(chat_id=update.message.chat.id,
                                       text=ans.val_ans['exp_name'])


async def order_print(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requisites = await check_proff(update, context)
    if requisites is None:
        return

    pdf_path = await get_attachments(update, context)
    vk_id, surname, number = requisites
    title = update.message.document.file_name

    # surname = 'Маракулин'# update.message.chat.last_name
    # number = 1018173  # TODO
    pin = None
    if pdf_path is not None:
        r = requests.post(config.PRINT_URL + '/file', json={'surname': surname, 'number': number, 'filename': title})
        if r.status_code == 200:
            pin = r.json()['pin']
            files = {'file': (title, open(pdf_path, 'rb'), 'application/pdf', {'Expires': '0'})}
            rfile = requests.post(config.PRINT_URL + '/file/' + pin, files=files)
            if rfile.status_code == 200:
                await context.bot.send_message(chat_id=update.message.chat.id,
                                               text=ans.print_ans['send_to_print'].format(pin))
                await context.bot.send_message(chat_id=update.message.chat.id,
                                               text=ans.print_ans['qrprint'].format(pin))
                # log.print(
                #     vk_id=vk_id,
                #     surname=surname,
                #     number=number,
                #     pin=pin,
                # )
            else:
                await context.bot.send_message(chat_id=update.message.chat.id,
                                               text=ans.errors['print_err'])
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
                                           text=ans.errors['print_err'])
            # log.print_exc_other(
            #     vk_id=vk_id,
            #     surname=surname,
            #     number=number,
            #     pin=pin,
            #     status_code=r.status_code,
            #     description='Fail on fetching code',
            # )

# def validate_proff(user):
#     if len(user.message.split('\n')) == 2:
#         surname = user.message.split('\n')[0].strip()
#         number = user.message.split('\n')[1].strip()
#
#         r = requests.get(PRINT_URL+'/is_union_member', params=dict(surname=surname, v=1, number=number))
#         data = db.get_user(user.user_id)
#         if r.json() and data is None:
#             db.add_user(user.user_id, surname, number)
#             kb.auth_button(user, ru.val_ans['val_pass'])
#             return True
#         elif r.json() and data is not None:
#             db.update_user(user.user_id, surname, number)
#             kb.auth_button(user, ru.val_ans['val_update_pass'])
#             log.register(
#                 vk_id=user.user_id,
#                 surname=surname,
#                 number=number,
#             )
#             return True
#         elif r.json() is False:
#             vk.write_msg(user, ru.val_ans['val_fail'])
#             vk.write_msg(user, ru.val_ans['exp_name'])
#             log.register_exc_wrong(
#                 vk_id=user.user_id,
#                 surname=surname,
#                 number=number,
#             )
#     else:
#         if db.get_user(user.user_id) is None:
#             vk.write_msg(user, ru.val_ans['val_need'])
#             vk.write_msg(user, ru.val_ans['exp_name'])
#         else:
#             vk.write_msg(user, ru.val_ans['val_update_fail'])
#             vk.write_msg(user, ru.val_ans['exp_name'])
#
#


# async def message_analyzer(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     try:
#         if len(user.message) > 0:
#             for word in ans.ask_help:
#                 if word in user.message.lower():
#                     kb.main_page(user)
#                     kb.auth_button(user)
#                     return
#
#         if len(user.attachments) == 0:
#             if len(user.message) > 0:
#                 validate_proff(user)
#             else:
#                 kb.main_page(user)
#                 kb.auth_button(user)
#         else:
#             requisites = check_proff(user)
#             if requisites is not None:
#                 await order_print(user, requisites)

# except OSError as err:
#     raise err
# except psycopg2.Error as err:
#     vk.write_msg(user, ru.errors['bd_error'])
#     raise err
# except json.decoder.JSONDecodeError as err:
#     vk.write_msg(user, ru.errors['print_err'])
#     logging.error('JSONDecodeError (message_analyzer), description:')
#     traceback.print_tb(err.__traceback__)
#     logging.error(str(err.args))
#     time.sleep(1)
# except Exception as err:
#     ans = ru.errors['im_broken']
#     vk.write_msg(user, ans)
#     logging.error('Unknown Exception (message_analyzer), description:')
#     traceback.print_tb(err.__traceback__)
#     logging.error(str(err.args))

#
# def process_event(event):
#     if event.type == vk.VkBotEventType.MESSAGE_NEW:
#         vk_user = vk.user_get(event.message['from_id'])
#         user = vk.User(event.message['from_id'], event.message['text'],
#                        event.message.attachments, (vk_user[0])['first_name'], (vk_user[0])['last_name'])
#         db.check_and_reconnect()
#         if event.message.payload is not None:
#             kb.keyboard_browser(user, event.message.payload)
#         else:
#             message_analyzer(user)


# def chat_loop():
#     while True:
#         try:
#             vk.reconnect()
#             for event in vk.longpoll.listen():
#                 process_event(event)
#
#         except OSError as err:
#             logging.error('OSError (longpull_loop), description:')
#             traceback.print_tb(err.__traceback__)
#             logging.error(str(err.args))
#             try:
#                 logging.warning('Try to recconnect VK...')
#                 vk.reconnect()
#                 logging.warning('VK connected successful')
#                 time.sleep(1)
#             except VkApiError:
#                 logging.error('Recconnect VK failed')
#                 time.sleep(10)
#
#         except psycopg2.Error as err:
#             logging.error('Database Error (longpull_loop), description:')
#             traceback.print_tb(err.__traceback__)
#             logging.error(err.args)
#             try:
#                 logging.warning('Try to recconnect database...')
#                 db.reconnect()
#                 logging.warning('Database connected successful')
#                 time.sleep(1)
#             except psycopg2.Error:
#                 logging.error('Recconnect database failed')
#                 time.sleep(10)
#
#         except Exception as err:
#             logging.error('BaseException (longpull_loop), description:')
#             traceback.print_tb(err.__traceback__)
#             logging.error(str(err.args))
#             time.sleep(5)
