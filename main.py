# import asyncio
# import telegram
#
#
#
# # async def main():
# #     bot = telegram.Bot(TOKEN)
# #     async with bot:
# #         print(await bot.get_me())
#
#
# async def main():
#     bot = telegram.Bot(TOKEN)
#     async with bot:
#         updates = await bot.get_updates()
#         print(len(updates)) # .message.from_user.id
#         print(updates[1].message.from_user.id)
#         await bot.send_message(text='Hi Annndruha!', chat_id=updates[1].message.from_user.id)
#
#
# # async def main():
# #     bot = telegram.Bot(TOKEN)
# #     async with bot:
# #         await bot.send_message(text='Hi John!', chat_id=1234567890)
#
# if __name__ == '__main__':
#     asyncio.run(main())


import logging
import telegram
import telegram.ext.filters as filters
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

from src.chat import get_attachments
import config


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


# async def get_attachments(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # update.
#     print(update.message.document.file_name)
#     # await context.bot.send_document(chat_id=update.effective_chat.id, document=open('LICENSE', 'rb'))
#     # await context.bot.getFile(update.message.document)
#     # await telegram.File.download_to_drive(custom_path='files')
#     file_id = update.message.document.file_id
#     new_file = await context.bot.get_file(file_id)
#     await new_file.download_to_drive(custom_path='kek.pdf')
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="Attachment!")

if __name__ == '__main__':
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # start_handler = CommandHandler('kek', start)
    # message_handler = MessageHandler('kek', start)
    command_handler = MessageHandler(filters.COMMAND, start)
    document_handler = MessageHandler(filters.Document.MimeType('application/pdf'), get_attachments)

    application.add_handler(command_handler)
    application.add_handler(document_handler)
    application.run_polling()
