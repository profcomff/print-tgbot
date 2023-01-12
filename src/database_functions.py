# Marakulin Andrey @annndruha
# 2023
import psycopg2
# import settings
from src.settings import get_settings
settings = get_settings()



connection = psycopg2.connect(dsn=settings.DB_DSN)


def reconnect():
    global connection
    connection = psycopg2.connect(dsn=settings.DB_DSN)


def check_and_reconnect():
    try:
        cur = connection.cursor()
        cur.execute('SELECT 1')
    except psycopg2.OperationalError:
        reconnect()


def get_user(user_id):
    with connection.cursor() as cur:
        cur.execute('SELECT * FROM bot_tg_print.tg_users WHERE tg_id=%s;', (user_id,))
        return cur.fetchone()


def add_user(user_id, surname, number):
    with connection.cursor() as cur:
        cur.execute(
            'INSERT INTO bot_tg_print.tg_users (tg_id,surname,number) VALUES (%s,%s,%s);',
            (user_id, surname, number))
        connection.commit()


def update_user(user_id, surname, number):
    with connection.cursor() as cur:
        cur.execute('UPDATE bot_tg_print.tg_users SET surname=%s,number=%s WHERE tg_id=%s;',
                    (surname, number, user_id))
        connection.commit()
