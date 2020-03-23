import os
from datetime import datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time

CURRENCY = "TND"

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':CURRENCY
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '39670023-96d0-4320-811b-9918e5be4c37',
}

session = Session()
session.headers.update(headers)

try:
  print()
  print('LISTENING ...')
  print()
  
  already_hit = []

  while True:
      response = session.get(url, params=parameters)
      results = response.json()
      data = results['data']
      ticker_url_pairs = {}
      for currency in data:
          symbol = currency['symbol']
          url = currency['id']
          ticker_url_pairs[symbol] = currency

      with open('alerts.txt') as inp:
          for line in inp:
              ticker,amount = line.split()
              ticker = ticker.upper()
              currency = ticker_url_pairs[ticker]
              name = currency['name']
              last_update = currency['last_updated']
              quotes = currency['quote'][CURRENCY]
              price = quotes['price']

              if float(price) >= float(amount) and ticker not in already_hit:
                  timestamp_string = datetime.fromisoformat(last_update[:-5]).strftime('%B %d, %Y at %I:%M %p')
                  print(name + ' hit ' + amount + ' on ' + timestamp_string)
                  already_hit.append(ticker)
      print('...')
      time.sleep(300)

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)