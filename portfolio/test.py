from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'100',
  'convert':'TND'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '39670023-96d0-4320-811b-9918e5be4c37',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  results = response.json()
  data = results['data']
  ticker_url_pairs = {}
  for currency in data:
      symbol = currency['symbol']
      url = currency['id']
      ticker_url_pairs[symbol] = currency
  print(json.dumps(ticker_url_pairs['BTC'] , sort_keys=True, indent=4))

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)