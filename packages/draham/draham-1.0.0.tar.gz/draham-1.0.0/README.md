# Draham

![screenshot](screenshot.png)

## Installation

Getting started with draham is very simple. Just install the package via pip

```sh
pip install --user draham
```

## Usage

Because draham pulls its data from the CoinMarketCap API, you will unfortuneraly
need to create a developer account and generate an API KEY.
The basic plan is free and affords you 10K calls per month.

draham requires a configuration file in the `ini` format. By default it will look
for a `.drahamrc` file under your home directory.

Here's how it should look like

```ini
[auth]
api_key=your_api_key_without_quotes
```

other (optional) settings include `symbols` and `currency`.

```ini
[options]
; default symbols are: BTC,BCH,DASH,LTC,ETH,XMR,XRP,BNB
; symbols must be separated by a comma. Quotes are not allowed.
symbols=BTC,ETH,BCH

; default currency is: USD
currency=USD
```

Currently, draham supports the following currencies:

- 🇩🇿  Algerian Dinar (DZD)
- 🇺🇸  US Dollar (USD)
- 🇬🇧  British Pound (GBP)
- 🇪🇺  Euro (EUR)
- 🇦🇺 Australian Dollar (AUD)
- 🇨🇦  Canadian Dollar (CAD)
- 🇯🇵  Japanese Yen (JPY)


## License

This project is distributed under the WTFPL public license.


## Issues and Contributing

Contributions to draham are most welcome. If you encounter bugs, please
report them via issues. You can of course submit fixes and new features via
of merge requests.

If you fork this project on GitHub, I kindly ask you that you credit me as
the original creator of the project.
