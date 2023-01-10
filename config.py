import configparser

config = configparser.ConfigParser()
config.read('auth.ini')

PDF_PATH = config['settings']['pdf_path']
PRINT_URL = config['print_server']['print_url']
BOT_TOKEN = config['auth_telegram']['bot_token']
