import sys
from termcolor import colored
from .constants import QUOTES_TABLE_HEADER
from .exceptions import ConfigNotFoundError, NoAPIKeyError
from configparser import ConfigParser


def check_config(config: ConfigParser, path: str) -> None:
    if len(config.read(path)) == 0:
        raise ConfigNotFoundError

    try:
        config['auth']['api_key']
    except KeyError:
        raise NoAPIKeyError


def print_error(error_message) -> None:
    msg: str = colored(f'[!] ERROR - {error_message}', 'red')
    sys.exit(msg)


def parse_error(response_data: dict, status_code: int) -> str:
    message = response_data['status']['error_message']
    return f'({status_code}) {message}'


def round_percent(value: float) -> str:
    decimal_places: int = 2
    result: str = f'{round(value, decimal_places)}%'

    if value > 0:
        result = colored(f'+{result}', 'green')
    else:
        result = colored(result, 'red')

    return result


def get_basic_table_columns() -> list[str]:
    fields: list[str] = [
        'rank', 'symbol', 'price',
        'price_24h', 'price_7d', 'market_cap'
    ]
    return [QUOTES_TABLE_HEADER[field] for field in fields]
