
from .patent import Patent
import requests


def get(number, language='en'):
    if is_patent(number, language=language):
        return Patent(number)
    raise NotAPatent('That was not a google patent')


def is_patent(number, language='en'):
    return requests.get('https://patents.google.com/patent/' + number + '/' + language).status_code == 200


class NotAPatent(Exception):
    pass
