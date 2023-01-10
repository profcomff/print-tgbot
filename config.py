import configparser

config = configparser.ConfigParser()
config.read('auth.ini')

BOT_TOKEN = config['auth_telegram']['bot_token']

PDF_PATH = config['settings']['pdf_path']


MARKETING_URL = config["logging"]["marketing_url"]
PRINT_URL = config['print_server']['print_url']
