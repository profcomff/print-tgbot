# Marakulin Andrey https://github.com/Annndruha
# 2023

import logging
import traceback

import psycopg2
from sqlalchemy.exc import SQLAlchemyError
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from src.answers import ans


def errors_solver(func):
    """
    This is decorator for telegram handlers that catches any type of exceptions.
    If exception is possible to solve, this handler send message with exception type.
    Else just log it.
    """

    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await func(update, context)
        except TelegramError as err:
            logging.error(f'TelegramError: {str(err.message)}')
        except (SQLAlchemyError, psycopg2.Error) as err:
            logging.error(err)
            traceback.print_tb(err.__traceback__)
            await context.bot.send_message(chat_id=update.message.chat.id, text=ans["db_err"])
        except Exception as err:
            logging.error(err)
            traceback.print_tb(err.__traceback__)

    return wrapper
