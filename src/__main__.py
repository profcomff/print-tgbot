# Marakulin Andrey https://github.com/Annndruha
# 2023

import logging

from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler
from telegram.ext.filters import ALL, COMMAND, Document

from src.handlers import (
    handler_auth,
    handler_button_browser,
    handler_help,
    handler_mismatch_doctype,
    handler_print,
    handler_register,
    handler_start,
    handler_unknown_command,
    native_error_handler,
)
from src.settings import Settings


tg_log_handler = logging.FileHandler("tgbot_telegram_updater.log")
tg_log_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
tg_logger = logging.getLogger("telegram.ext._updater")
tg_logger.propagate = False
tg_logger.addHandler(tg_log_handler)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

if __name__ == "__main__":
    settings = Settings()
    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", handler_start))
    application.add_handler(CommandHandler("help", handler_help))
    application.add_handler(CommandHandler("auth", handler_auth))
    application.add_handler(CallbackQueryHandler(handler_button_browser))
    application.add_handler(MessageHandler(COMMAND, handler_unknown_command))
    application.add_handler(MessageHandler(Document.MimeType("application/pdf"), handler_print))
    application.add_handler(MessageHandler(Document.ALL, handler_mismatch_doctype))
    application.add_handler(MessageHandler(ALL, handler_register))
    application.add_error_handler(native_error_handler)
    application.run_polling()
