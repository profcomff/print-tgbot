import json
import logging
import traceback
from urllib.parse import urljoin

import requests

from src.settings import Settings

settings = Settings()


def pass_if_exc(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as err:
            logging.error(f'Marketing Exception {str(err.args)}, traceback:')
            traceback.print_tb(err.__traceback__)

    return wrapper


@pass_if_exc
def register(**user_info):
    requests.post(
        urljoin(settings.MARKETING_URL, "v1/action"),
        json={
            'user_id': -2,
            'action': 'print tgbot register',
            'additional_data': json.dumps(user_info),
            'path_from': 'https://t.me/',
        }
    )


@pass_if_exc
def re_register(**user_info):
    requests.post(
        urljoin(settings.MARKETING_URL, "v1/action"),
        json={
            'user_id': -2,
            'action': 'print tgbot repeat register',
            'additional_data': json.dumps(user_info),
            'path_from': 'https://t.me/',
        }
    )


@pass_if_exc
def register_exc_wrong(**user_info):
    requests.post(
        urljoin(settings.MARKETING_URL, "v1/action"),
        json={
            'user_id': -2,
            'action': 'print tgbot register exc wrong creds',
            'additional_data': json.dumps(user_info),
            'path_from': 'https://t.me/',
        }
    )


@pass_if_exc
def print_success(**print_info):
    requests.post(
        urljoin(settings.MARKETING_URL, "v1/action"),
        json={
            'user_id': -2,
            'action': 'print tgbot sent',
            'additional_data': json.dumps(print_info),
            'path_from': 'https://t.me/',
            'path_to': urljoin(settings.PRINT_URL, f'/file/{print_info.get("pin")}'),
        }
    )


@pass_if_exc
def print_exc_format(**print_info):
    requests.post(
        urljoin(settings.MARKETING_URL, "v1/action"),
        json={
            'user_id': -2,
            'action': 'print tgbot sent exc format',
            'additional_data': json.dumps(print_info),
            'path_from': 'https://t.me/',
        }
    )
