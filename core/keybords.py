# Marakulin Andrey @annndruha
# 2021
import json
import logging
import traceback
import requests
import configparser
import psycopg2

import core.answers as ru
import func.vkontakte_functions as vk
import func.database_functions as db


config = configparser.ConfigParser()
config.read('auth.ini')
PRINT_URL = config["print_server"]["print_url"]


def check_auth(user_id):
    if db.get_user(user_id) is not None:
        _, surname, number = db.get_user(user_id)
        r = requests.get(PRINT_URL+'/is_union_member', params=dict(surname=surname, number=number, v=1))
        if r.json():
            return True
        else:
            return False
    else:
        return False


def main_page(user, ans=ru.kb_ans['hey'], attach=None):
    kb = vk.VkKeyboard(one_time=False)

    kb.add_button(ru.kb_ans['inst'], color='primary', payload='{"command":"help"}')
    kb.add_line()
    kb.add_button(ru.kb_ans['conf'], color='primary', payload='{"command":"conf"}')
    vk.send_keyboard(user, kb.get_keyboard(), ans, attach=attach)


def auth_button(user, ans=ru.kb_ans['help']):
    kb = vk.VkKeyboard(inline=True)
    if check_auth(user.user_id):
        kb.add_button(ru.kb_ans['auth'], color='positive', payload='{"command":"auth_true"}')
    else:
        kb.add_button(ru.kb_ans['notauth'], color='negative', payload='{"command":"auth_false"}')
        if ru.kb_ans['help'] == ans:
            ans += ru.val_ans['val_addition']

    vk.send_keyboard(user, kb.get_keyboard(), ans)


def keyboard_browser(user, str_payload):
    try:
        payload = json.loads(str_payload)  # From str to dict
        if payload['command'] == 'start':
            main_page(user)
            auth_button(user)
        if payload['command'] == 'help':
            main_page(user)
            auth_button(user)
        if payload['command'] == 'conf':
            main_page(user, ru.kb_ans['conf_full'])
        if payload['command'] == 'auth_true':
            if check_auth(user.user_id):
                vk.write_msg(user, ru.val_ans['val_already'])
            else:
                vk.write_msg(user, ru.val_ans['val_need'])
                vk.write_msg(user, ru.val_ans['exp_name'])
        if payload['command'] == 'auth_false':
            if check_auth(user.user_id):
                vk.write_msg(user, ru.val_ans['val_already'])
            else:
                vk.write_msg(user, ru.val_ans['val_need'])
                vk.write_msg(user, ru.val_ans['exp_name'])

    except OSError as err:
        raise err
    except psycopg2.Error as err:
        vk.write_msg(user, ru.errors['bd_error'])
        raise err
    except json.decoder.JSONDecodeError as err:
        vk.write_msg(user, ru.errors['print_err'])
        logging.error('JSONDecodeError (message_analyzer), description:')
        traceback.print_tb(err.__traceback__)
        logging.error(str(err.args))
    except Exception as err:
        ans = ru.errors['kb_error']
        vk.write_msg(user, ans)
        logging.error(f'Unknown Exception (keyboard_browser), description:\n{str(err.args)}')
        traceback.print_tb(err.__traceback__)
