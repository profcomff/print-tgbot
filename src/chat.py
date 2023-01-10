# Marakulin Andrey @annndruha
# 2023

from telegram import Update
from telegram.ext import ContextTypes

import core.answers as ru


async def get_attachments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update.
    print(update.message.document.file_name)
    print(update.message)
    # await context.bot.send_document(chat_id=update.effective_chat.id, document=open('LICENSE', 'rb'))
    # await context.bot.getFile(update.message.document)
    # await telegram.File.download_to_drive(custom_path='files')
    file_id = update.message.document.file_id

    new_file = await context.bot.get_file(file_id)

    # if not os.path.exists(config.PDF_PATH):
    #     os.makedirs(config.PDF_PATH)
    # if not os.path.exists(os.path.join(config.PDF_PATH, str(user.user_id))):
    #     os.makedirs(os.path.join(config.PDF_PATH, str(user.user_id)))
    #
    #
    # await new_file.download_to_drive(custom_path=os.path.join(config.PDF_PATH, str(user.user_id), update.message.document.file_name))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=ru.print_ans['file_uploaded'].format(update.message.document.file_name))

    # vk.write_msg(user, ru.print_ans['file_uploaded'].format(update.message.document.file_name))