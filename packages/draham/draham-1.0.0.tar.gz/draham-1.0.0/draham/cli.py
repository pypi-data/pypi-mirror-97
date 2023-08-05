from configparser import ConfigParser, ParsingError
from pathlib import Path
import os
import click
from .exceptions import ConfigNotFoundError, NoAPIKeyError
from .constants import DEFAULT_SYMBOLS, DEFAULT_CURRENCY
from .draham import Draham
from .utils import print_error, check_config


@click.command()
@click.option('--config', default=os.path.join(Path.home(), '.drahamrc'), help="the path to your config file. Default: $HOME/.drahamrc")
@click.option('--tor', default=False, help="use tor as a proxy to make requests")
@click.option('--detailed', is_flag=True, help="show more detailed information about prices")
def cli(config, tor, detailed):
    parser = ConfigParser()

    try:
        check_config(parser, config)
    except ConfigNotFoundError:
        print_error("Config file not found. Either specify the path to a custom config with --config or create a .drahamrc file inside your home directory")
    except ParsingError:
        print_error("Could not parse config file. Please check its in the correct format.")
    except NoAPIKeyError:
        print_error("API key not found. Please add it to your config file under the [auth] section section as api_key")

    if not parser.has_section('options'):
        symbols = DEFAULT_SYMBOLS
        currency = DEFAULT_CURRENCY
    else:
        symbols = parser['options'].get('symbols', DEFAULT_SYMBOLS)
        currency = parser['options'].get('currency', DEFAULT_CURRENCY)

    api_key = parser['auth']['api_key']
    draham = Draham(api_key, symbols, currency, tor, detailed)
    draham.show_crypto_info()


if __name__ == "__main__":
    cli()
