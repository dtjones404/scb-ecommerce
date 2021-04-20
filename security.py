from os.path import exists
from secrets import token_urlsafe


def get_secret() -> str:
    if not exists("scb.key"):
        with open("scb.key", "w+") as f:
            key = token_urlsafe(64)
            f.write(key)
    with open("scb.key") as f:
        return f.read()
