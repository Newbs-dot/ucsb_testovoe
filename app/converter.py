from requests import get
import os
import redis
#API_KEY = os.getenv('API_KEY')
#ENDPOINT = os.getenv('ENDPOINT')
API_KEY='FCdYqOWk3DgjsyurvwskQNrEyxt5dAnRXdpHbeu4'
ENDPOINT='https://api.freecurrencyapi.com/v1/latest'

def convert_currencies(currency_rate:float,amount:float):
    if float(amount) < 0:
        raise ValueError('Cannot convert to a negative amount')
    return round(currency_rate * float(amount),2)

def get_all_currencies():
    url = f'{ENDPOINT}?apikey={API_KEY}&base_currency=USD'
    responce = get(url).json()['data']
    return responce

