import logging
import telegram.ext.filters as filters
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler

import config
from src.handlers import handler_start, handler_unknown_command, handler_print, handler_mismatch_doctype, \
    handler_register, handler_button, handler_help, handler_auth, handler_history

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == '__main__':
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', handler_start))
    application.add_handler(CommandHandler('help', handler_help))
    application.add_handler(CommandHandler('auth', handler_auth))
    application.add_handler(CommandHandler('history', handler_history))
    application.add_handler(CallbackQueryHandler(handler_button))
    application.add_handler(MessageHandler(filters.COMMAND, handler_unknown_command))
    application.add_handler(MessageHandler(filters.Document.MimeType('application/pdf'), handler_print))
    application.add_handler(MessageHandler(filters.Document.ALL, handler_mismatch_doctype))
    application.add_handler(MessageHandler(filters.ALL, handler_register))
    application.run_polling()
