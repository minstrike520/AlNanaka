from .core import Character, Active
from .special_status import Freezed


class NoSuchActef(Exception):
    pass


def burn(char: Character):
    pass


def freeze(_char: Character):
    raise Freezed


dictionary = {
    "burn": {
        "name": "burn",
        "occasion": "initial",
        "time": 3,
        "affect": burn
    },
    "freeze": {
        "name": "freeze",
        "occasion": "initial",
        "time": 2,
        "affect": freeze
    }
}


def get_actef_names():
    return list(dictionary)


def get_actef(actef_name):
    for name, value in dictionary.items():
        if actef_name == name:
            return Active(**value)
    raise NoSuchActef