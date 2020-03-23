from datetime import datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

CURRENCY = "TND"
url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'
parameters = {
  'convert':CURRENCY
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '39670023-96d0-4320-811b-9918e5be4c37',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)

  active_cryptocurrencies = data['data']['active_cryptocurrencies']
  active_cryptocurrencies_string = '{:,}'.format(active_cryptocurrencies)
  btc_dominance = data['data']['btc_dominance']
  total_market_cap = int(data['data']['quote'][CURRENCY]['total_market_cap'])
  total_market_cap_string = '{:,}'.format(total_market_cap)
  timestamp = data['status']['timestamp'][:-5]

  timestamp_string = datetime.fromisoformat(timestamp).strftime('%B %d, %Y at %I:%M %p')
  
  
  print()
  print("there are currently " + active_cryptocurrencies_string + " active cryptocurrencies.")
  print("the global cap of all cryptocurrencies is: " + total_market_cap_string + " " + CURRENCY)
  print()
  print("this information was last updated on " + timestamp_string)

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)