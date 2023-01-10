# Marakulin Andrey @annndruha
# 2021
import logging
import configparser

from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard


config = configparser.ConfigParser()
config.read('auth.ini')

GROUP_ID = config['auth_vk']['group_id']
GROUP_TOKEN = config['auth_vk']['group_token']
API_VERSION = '5.120'

vk = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)  # Auth with community token
longpoll = VkBotLongPoll(vk, group_id=GROUP_ID)  # Create a longpull variable
VkKeyboard = VkKeyboard
VkBotEventType = VkBotEventType


class User:
    def __init__(self, user_id, message, attachments, first_name, last_name):
        self.user_id = user_id
        self.message = message
        self.first_name = first_name
        self.last_name = last_name
        self.attachments = attachments


def reconnect():
    global vk
    global longpoll
    vk = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
    longpoll = VkBotLongPoll(vk, group_id=GROUP_ID)


def user_get(user_id):
    return vk.method('users.get', {'user_ids': user_id})


def write_msg(user, message=None, attach=None, parse_links=False):
    params = {'user_id': user.user_id, 'random_id': get_random_id()}

    if message is not None and attach is not None:
        params['message'] = message
        params['attachment'] = attach
        logging.info(f'[Msg to {user.first_name} {user.last_name}] {message}'.replace('\n', ' '))
    elif message is not None and attach is None:
        params['message'] = message
        logging.info(f'[Msg to {user.first_name} {user.last_name}] {message}'.replace('\n', ' '))
    elif message is None and attach is not None:
        params['attachment'] = attach
    if not parse_links:
        params['dont_parse_links'] = 1

    vk.method('messages.send', params)


def send_keyboard(user, kb, message, attach=None):
    if attach is None:
        vk.method('messages.send',
                  {'user_id': user.user_id,
                   'keyboard': kb,
                   'message': message,
                   'dont_parse_links': 1,
                   'random_id': get_random_id()})
    else:
        vk.method('messages.send',
                  {'user_id': user.user_id,
                   'keyboard': kb,
                   'message': message,
                   'attachment': attach,
                   'dont_parse_links': 1,
                   'random_id': get_random_id()})

    if message is not None:
        logging.info(f'[Msg to {user.first_name} {user.last_name}] {message}'.replace('\n', ' '))
