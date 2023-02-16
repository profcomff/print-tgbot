# Marakulin Andrey https://github.com/Annndruha
# 2023

import logging

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler
from telegram.ext.filters import COMMAND, Document, ALL

from src.settings import Settings
from src.handlers import handler_start, handler_help, handler_auth, handler_button_browser, handler_unknown_command, \
    handler_print, handler_mismatch_doctype, handler_register, native_error_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == '__main__':
    settings = Settings()
    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', handler_start))
    application.add_handler(CommandHandler('help', handler_help))
    application.add_handler(CommandHandler('auth', handler_auth))
    application.add_handler(CallbackQueryHandler(handler_button_browser))
    application.add_handler(MessageHandler(COMMAND, handler_unknown_command))
    application.add_handler(MessageHandler(Document.MimeType('application/pdf'), handler_print))
    application.add_handler(MessageHandler(Document.ALL, handler_mismatch_doctype))
    application.add_handler(MessageHandler(ALL, handler_register))
    application.add_error_handler(native_error_handler)
    application.run_polling()
