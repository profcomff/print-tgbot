import json
import requests
import configparser
from urllib.parse import urljoin


config = configparser.ConfigParser()
config.read('auth.ini')
MARKETING_URL = config["logging"]["marketing_url"]
PRINT_URL = config["print_server"]["print_url"]


def pass_if_exc(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as exc:
            print("During marketing following error occured:")
            print(exc)
    return wrapper


@pass_if_exc
def register(**user_info):
    requests.post(
        urljoin(MARKETING_URL, "v1/action"),
        json={
            'user_id': -2,
            'action': 'print bot register',
            'additional_data': json.dumps(user_info),
            'path_from': 'https://vk.com/im',
        }
    )


@pass_if_exc
def register_exc_wrong(**user_info):
    requests.post(
        urljoin(MARKETING_URL, "v1/action"),
        json={
            'user_id': -2,
            'action': 'print bot register exc wrong creds',
            'additional_data': json.dumps(user_info),
            'path_from': 'https://vk.com/im',
        }
    )


@pass_if_exc
def print(**print_info):
    requests.post(
        urljoin(MARKETING_URL, "v1/action"),
        json={
            'user_id': -2,
            'action': 'print bot sent',
            'additional_data': json.dumps(print_info),
            'path_from': 'https://vk.com/im',
            'path_to': urljoin(PRINT_URL, f'/file/{print_info.get("pin")}'),
        }
    )


@pass_if_exc
def print_exc_many(**print_info):
    requests.post(
        urljoin(MARKETING_URL, "v1/action"),
        json={
            'user_id': -2,
            'action': 'print bot sent exc many',
            'additional_data': json.dumps(print_info),
            'path_from': 'https://vk.com/im',
        }
    )


@pass_if_exc
def print_exc_format(**print_info):
    requests.post(
        urljoin(MARKETING_URL, "v1/action"),
        json={
            'user_id': -2,
            'action': 'print bot sent exc format',
            'additional_data': json.dumps(print_info),
            'path_from': 'https://vk.com/im',
        }
    )


@pass_if_exc
def print_exc_other(**print_info):
    requests.post(
        urljoin(MARKETING_URL, "v1/action"),
        json={
            'user_id': -2,
            'action': 'print bot sent exc other',
            'additional_data': json.dumps(print_info),
            'path_from': 'https://vk.com/im',
        }
    )
