from alfa_cli.commands import alfa
from alfa_cli.common.logger import Logger


def main():
    try:
        alfa()
    except Exception as err:
        Logger.error(err)
