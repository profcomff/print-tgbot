import logging
import telegram
import telegram.ext.filters as filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, \
    CallbackContext

from src.chat import order_print, validate_proff
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


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Неизвестная команда.\nУ бота лишь две команды: /start /help')


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
    elif query.data == 'auth':
        text = ans.val_ans['val_need']
        reply_markup = None
    else:
        text = 'Видимо бот обновился, выполните команду /start'
        reply_markup = None

    await query.answer()
    await query.edit_message_text(text=text, reply_markup=reply_markup, disable_web_page_preview=True)


async def allhand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await validate_proff(update, context)
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="etc.")



if __name__ == '__main__':
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    application.add_handler(MessageHandler(filters.Document.MimeType('application/pdf'), order_print))
    application.add_handler(MessageHandler(filters.ALL, allhand))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()
