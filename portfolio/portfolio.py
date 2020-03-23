import os
from datetime import datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from prettytable import PrettyTable
from colorama import Fore, Back, Style
import json

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
  response = session.get(url, params=parameters)
  results = response.json()
  data = results['data']
  ticker_url_pairs = {}
  for currency in data:
      symbol = currency['symbol']
      url = currency['id']
      ticker_url_pairs[symbol] = currency
  print()
  print("▂▃▅▇█▓▒░ MY PORTFOLIO ░▒▓█▇▅▃▂")
  print()

  total_value = 0.00
  last_update = 0
  table = PrettyTable(['Asset' , 'Amount Owned' , CURRENCY+' value'  , '1Hour' , '24Hour' , 'Weekly'])
  with open("portfolio.txt") as inp:
      for line in inp:
          ticker, amount = line.split()
          ticker = ticker.upper()
          currency = ticker_url_pairs[ticker]
          name = currency['name']
          last_update = currency['last_updated']
          quotes = currency['quote'][CURRENCY]
          hour_change = quotes['percent_change_1h']
          day_change = quotes['percent_change_24h']
          week_change = quotes['percent_change_7d']
          price = quotes['price']
          value = float(price) * float(amount)

          if hour_change > 0 :
              hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
          else:
              hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

          if day_change > 0 :
              day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
          else:
              day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL

          if week_change > 0 :
              week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
          else:
              week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL

          total_value += value
          value_string = '{:,}'.format(round(value,2))
          
          table.add_row([name + ' (' + ticker + ')' , value_string + ' ' + CURRENCY , str(price) , str(hour_change) , str(day_change) , str(week_change)])

  print(table)
  print()
  total_value_string = '{:,}'.format(round(total_value,2))
  print('Total Value : ' + Back.GREEN + total_value_string + ' ' + CURRENCY + Style.RESET_ALL)
  timestamp_string = datetime.fromisoformat(last_update[:-5]).strftime('%B %d, %Y at %I:%M %p')
  print('Last API update : ' + timestamp_string)
  print()
          

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)