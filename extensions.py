import requests
import json
from configuration import currency


class ConversionException(Exception):
    pass


class ValueConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversionException(f'Невозможно конвертировать {base} в {base}. Пожалуйста введите разные валюты')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise ConversionException(f'Не удалось конвертировать валюту {quote}')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise ConversionException(f'Не удалось конвертировать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Не удалось конвертировать сумму {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[currency[base]]

        return total_base * amount
