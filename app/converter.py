from requests import get
import os

API_KEY = os.getenv('API_KEY')
ENDPOINT = os.getenv('ENDPOINT')


def get_currency_rate(base_currency:str,to_currency:str):
    url = f'{ENDPOINT}?apikey={API_KEY}&base_currency={base_currency}&currency={to_currency}'
    try:
        responce = get(url).json()['data']
    except:
        raise KeyError('Cannot find ticker')
    return responce[to_currency]

def convert_currencies(currency_rate:float,amount:float):
    if float(amount) < 0:
        raise ValueError('Cannot convert to a negative amount')
    return round(currency_rate * float(amount),2)

def get_all_currencies():
    url = f'{ENDPOINT}?apikey={API_KEY}&base_currency=USD'
    responce = get(url).json()['data']
    return responce

