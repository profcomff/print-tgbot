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
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, CallbackContext

from src.chat import order_print
import config


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Please choose:', reply_markup=reply_markup)

async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="auth")
    # surname, number = update.message.text.split('/auth ')[1]
    # print(surname)
    # print(number)



async def name(update, context):
    name = update.message.text
    context.bot.send_message(chat_id=update.message.chat_id, text="Nice to meet you, " + name + "!")


async def allhand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb_fruits = ['kek', 'ne kek']
    await context.bot.send_message(chat_id=update.effective_chat.id, text="etc.", reply_markup=kb_fruits)


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

async def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    # command_handler = MessageHandler(filters.COMMAND, botcommand)
    auth_handler = CommandHandler('auth', auth)
    document_handler = MessageHandler(filters.Document.MimeType('application/pdf'), order_print)
    other_handler = MessageHandler(filters.ALL, allhand)

    application.add_handler(start_handler)
    application.add_handler(auth_handler)
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(document_handler)
    application.add_handler(other_handler)

    application.run_polling()