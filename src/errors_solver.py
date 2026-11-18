# Marakulin Andrey https://github.com/Annndruha
# 2023

import logging

import psycopg2
import requests
from sqlalchemy.exc import SQLAlchemyError
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from src.answers import Answers

ans = Answers()


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
            logging.error('TelegramError: %s', err.message)
        except requests.RequestException as err:
            logging.warning('Print API request failed (%s)', type(err).__name__)
            if update.effective_message is not None:
                await update.effective_message.reply_text(ans.print_err)
        except (SQLAlchemyError, psycopg2.Error):
            logging.exception('Telegram user database operation failed')
            if update.effective_message is not None:
                await update.effective_message.reply_text(ans.db_err)
        except Exception:
            logging.exception('Telegram update handling failed')

    return wrapper
