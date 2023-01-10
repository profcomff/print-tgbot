import logging
import telegram
import telegram.ext.filters as filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, \
    CallbackContext

from src.chat import order_print
import config
import src.answers as ans

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Конфиденциальность", callback_data='want_confident')],
                                         [InlineKeyboardButton("Авторизация", callback_data='auth')]])
    await update.message.reply_text(ans.kb_ans['help'], reply_markup=reply_markup, disable_web_page_preview=True)


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == 'want_instruction':
        text = ans.kb_ans['help']
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Конфиденциальность", callback_data='want_confident')],
             [InlineKeyboardButton("Авторизация", callback_data='auth')]])
    elif query.data == 'want_confident':
        text = ans.kb_ans['conf_full']
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("<- Назад", callback_data='want_instruction')],
             [InlineKeyboardButton("Авторизация", callback_data='auth')]])
    else:
        text = ans.val_ans['val_need']
        reply_markup = None

    await query.answer()
    await query.edit_message_text(text=text, reply_markup=reply_markup, disable_web_page_preview=True)
    # await query.edit_message_reply_markup(reply_markup=reply_markup)


# async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="auth")
#     # surname, number = update.message.text.split('/auth ')[1]
#     # print(surname)
#     # print(number)


async def allhand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="etc.")


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

    start_handler = CommandHandler('start', start)
    # command_handler = MessageHandler(filters.COMMAND, botcommand)
    # auth_handler = CommandHandler('auth', auth)
    document_handler = MessageHandler(filters.Document.MimeType('application/pdf'), order_print)
    other_handler = MessageHandler(filters.ALL, allhand)
    buttons_handler = CallbackQueryHandler(button)

    application.add_handler(start_handler)
    # application.add_handler(auth_handler)
    application.add_handler(buttons_handler)
    application.add_handler(document_handler)
    application.add_handler(other_handler)

    application.run_polling()
