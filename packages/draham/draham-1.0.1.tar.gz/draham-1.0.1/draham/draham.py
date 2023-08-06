from typing import Union
from datetime import datetime
from .constants import API_BASE_URL, QUOTES_TABLE_HEADER, CURRENCY_SYMBOLS
from .utils import (
    round_percent,
    get_basic_table_columns,
    print_error,
    parse_error
)
from prettytable import PrettyTable  # type: ignore
from requests import Session
from requests.exceptions import ConnectionError, Timeout


class Draham(object):

    def __init__(
            self,
            api_key: str,
            symbols: str,
            currency: str,
            tor: bool = False,
            detailed_view: bool = False,
    ):

        self.symbols: str = symbols
        self.currency: str = currency
        self.currency_symbol: str = CURRENCY_SYMBOLS[currency]
        self.use_tor: bool = tor
        self.detailed_view: bool = detailed_view
        self.api_key: str = api_key
        self.session = Session()

    def show_crypto_info(self):
        quotes: list = self._parse_quotes()
        table: PrettyTable = PrettyTable()

        table.field_names = QUOTES_TABLE_HEADER.values()

        for quote in quotes:
            table.add_row(quote.values())

        now: str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        table.align = 'r'
        table.title = f'Crypto prices as of {now}'
        table.align[QUOTES_TABLE_HEADER['symbol']] = 'l'
        table.sortby = QUOTES_TABLE_HEADER['rank']

        if self.detailed_view:
            print(table)
        else:
            columns: list[str] = get_basic_table_columns()
            print(table.get_string(fields=columns))

    def _parse_quotes(self) -> list[dict]:

        raw_quotes = self._get_raw_quotes()

        final_quotes: list = []

        for symbol, data in raw_quotes.items():
            raw_quote: dict = raw_quotes[symbol]

            _symbol: str = raw_quote['symbol']
            rank: int = raw_quote['cmc_rank']
            circ_supply: float = raw_quote['circulating_supply']
            price_data: dict = raw_quote['quote'][self.currency]
            price: str = f'{self.currency_symbol}{round(price_data["price"], 2)}'
            clean_quote: dict = {
                'rank': rank,
                'symbol': _symbol,
                'price': price,
                'price_1h': round_percent(price_data['percent_change_1h']),
                'price_24h': round_percent(price_data['percent_change_24h']),
                'price_7d': round_percent(price_data['percent_change_7d']),
                'market_cap': self._format_number(price_data['market_cap']),
                'volume_24h': self._format_number(price_data['volume_24h']),
                'circulating_supply': self._format_supply(circ_supply, symbol)
            }

            final_quotes.append(clean_quote)

        return final_quotes

    def _get_raw_quotes(self):
        endpoint: str = '/cryptocurrency/quotes/latest'
        params: dict = {
            'symbol': self.symbols,
            'convert': self.currency
        }
        raw_quotes: Union[dict, None] = self._call_api(endpoint, params=params)
        return raw_quotes

    def _call_api(self, endpoint: str, params=None):
        headers: dict = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key
        }
        url: str = f'{API_BASE_URL}{endpoint}'
        self.session.headers.update(headers)
        self.session.params.update(params)  # type: ignore

        if self.use_tor:
            tor_proxies: dict = {
                'http': 'socks5://localhost:9050',
                'https': 'socks5://localhost:9050'
            }
            self.session.proxies.update(tor_proxies)
        try:
            response = self.session.get(url)
        except ConnectionError:
            conn_error: str = "Could not establish connection to the API. Check your internet connection and try again."  # noqa: E501
            print_error(conn_error)
        except Timeout:
            timeout_error: str = "We're unable to reach the API. The server timed out."
            print_error(timeout_error)

        json_res: dict = response.json()

        if response.status_code == 200:
            return json_res['data']
        else:
            error_message: str = parse_error(json_res, response.status_code)
            print_error(error_message)

    def _format_number(self, value: float, currency=None) -> str:

        result: str = '{:,}'.format(int(value))

        if currency is False:
            return result

        return f'{self.currency_symbol}{result}'

    def _format_supply(self, supply_value: float, symbol: str) -> str:
        val: str = self._format_number(supply_value, currency=False)
        return f'{val} {symbol}'
