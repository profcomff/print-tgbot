# Marakulin Andrey @annndruha
# 2021
import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('auth.ini')

connection = psycopg2.connect(dbname=config['auth_db']['name'],
                              user=config['auth_db']['user'],
                              password=config['auth_db']['password'],
                              host=config['auth_db']['host'],
                              port=config['auth_db']['port'])


def reconnect():
    global connection
    connection = psycopg2.connect(dbname=config['auth_db']['name'],
                                  user=config['auth_db']['user'],
                                  password=config['auth_db']['password'],
                                  host=config['auth_db']['host'],
                                  port=config['auth_db']['port'])


def check_and_reconnect():
    try:
        cur = connection.cursor()
        cur.execute('SELECT 1')
    except psycopg2.OperationalError:
        reconnect()


def get_user(user_id):
    with connection.cursor() as cur:
        cur.execute('SELECT * FROM printer_bot.vk_users WHERE vk_id=%s;', (user_id,))
        return cur.fetchone()


def add_user(user_id, surname, number):
    with connection.cursor() as cur:
        cur.execute(
            'INSERT INTO printer_bot.vk_users (vk_id,surname,number) VALUES (%s,%s,%s);',
            (user_id, surname, number))
        connection.commit()


def update_user(user_id, surname, number):
    with connection.cursor() as cur:
        cur.execute('UPDATE printer_bot.vk_users SET surname=%s,number=%s WHERE vk_id=%s;',
                    (surname, number, user_id))
        connection.commit()
