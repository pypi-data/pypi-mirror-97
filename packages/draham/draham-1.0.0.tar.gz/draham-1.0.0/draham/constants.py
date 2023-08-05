API_VERSION: str = 'v1'
API_BASE_URL: str = f'https://pro-api.coinmarketcap.com/{API_VERSION}'

DEFAULT_SYMBOLS: str = 'BTC,BCH,DASH,LTC,ETH,XMR,XRP,BNB'
DEFAULT_CURRENCY: str = 'USD'

QUOTES_TABLE_HEADER: dict = {
    'rank': '🎖  Rank',
    'symbol': '🪙 Symbol',
    'price': '💰 Price ',
    'price_1h': '🕐 1h',
    'price_24h': '🌘 24h',
    'price_7d': '📅 7d',
    'market_cap': '🧢 Market Cap',
    'volume_24h': '🔊 Volume 24h',
    'circulating_supply': '🚜 Circ. Supply',
}

CURRENCY_SYMBOLS: dict = {
    'USD': '$',
    'JPY': '¥',
    'EUR': '€',
    'CAD': '$',
    'AUD': '$',
    'GBP': '£',
    'DZD': 'ج.د ',
}
