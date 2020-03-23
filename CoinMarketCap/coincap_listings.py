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
  # print(json.dumps(results , sort_keys=True, indent=4))
  data = results['data']
  for currency in data:
      rank = currency['cmc_rank']
      name = currency['name']
      symbol = currency['symbol']
      print(str(rank) + ':' + name + '(' + symbol + ')')

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)