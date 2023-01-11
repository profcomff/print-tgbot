import configparser
import logging

config = configparser.ConfigParser()
config.read('auth.ini')

try:
    BOT_TOKEN = config['auth_telegram']['bot_token']

    PDF_PATH = config['settings']['pdf_path']

    MARKETING_URL = config['logging']['marketing_url']
    PRINT_URL = config['print_server']['print_url']

    DBHOST = config['auth_db']['host']
    DBPORT = config['auth_db']['port']
    DBNAME = config['auth_db']['name']
    DBUSER = config['auth_db']['user']
    DBPASSWORD = config['auth_db']['password']

except KeyError as err:
    logging.error('Did you miss auth.ini?')
