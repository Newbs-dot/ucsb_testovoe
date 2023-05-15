from requests import get
import os

API_KEY = os.getenv('API_KEY')
ENDPOINT = os.getenv('ENDPOINT')


async def convert_currencies(currency_rate: float, amount: float):
    if float(amount) < 0:
        raise ValueError('Cannot convert to a negative amount')
    return round(currency_rate * float(amount), 2)


async def get_all_currencies():
    url = f'{ENDPOINT}?apikey={API_KEY}&base_currency=USD'
    responce = get(url).json()['data']
    return responce
