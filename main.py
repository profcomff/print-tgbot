import logging
import telegram.ext.filters as filters
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler

import config
from src.handlers import handler_start, handler_about, handler_unknown_command, handler_order_print, handler_doc_error, \
    handler_validate_proff, handler_button

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == '__main__':
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', handler_start))
    application.add_handler(CommandHandler('about', handler_about))
    application.add_handler(MessageHandler(filters.COMMAND, handler_unknown_command))
    application.add_handler(MessageHandler(filters.Document.MimeType('application/pdf'), handler_order_print))
    application.add_handler(MessageHandler(filters.Document.ALL, handler_doc_error))
    application.add_handler(MessageHandler(filters.ALL, handler_validate_proff))
    application.add_handler(CallbackQueryHandler(handler_button))
    application.run_polling()
