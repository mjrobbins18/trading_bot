import alpaca_trade_api as tradeapi
import numpy as np
import time
import os
from dotenv import load_dotenv

load_dotenv()


SEC_KEY = os.getenv('SEC_KEY')
PUB_KEY = os.getenv('PUB_KEY')
BASE_URL = os.getenv('BASE_URL')

api = tradeapi.REST(key_id=PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)

symb="TSLA"
pos_held = False
hours_to_test = 2

print("Checking Price")
market_data = api.get_barset(symb, 'minute', limit=(60 * hours_to_test))

close_list = []

for bar in market_data[symb]:
    close_list.append(bar.c)



print("Open:", str(close_list[0]))
print("Close:", str(close_list[60 * hours_to_test -1]))

close_list = np.array(close_list, dtype=np.float64)

startBal = 2000
balance = startBal
buys = 0
sells = 0




for i in range(4, 60 * hours_to_test):
    ma = np.mean(close_list[i-4:i+1])
    last_price = close_list[i]

    print("Moving Average:", str(ma))
    print("Last Price:", str(last_price))

    if ma + 0.01 < last_price and not pos_held:
        print("Buy")
        balance -= last_price
        pos_held = True
        buys += 1
    elif ma - 0.01 > last_price and pos_held:
        print("Sell")
        balance += last_price
        pos_held = False
        sells += 1
    
    print(balance)
    time.sleep(0.01)

print("")
print("Buys:", str(buys))
print("Sells:", str(sells))

if buys > sells:
    balance += close_list[60 * hours_to_test - 1]

print("Final Balance:", str(balance))

print("Profit if held:", str(close_list[60 * hours_to_test - 1]))
print("Profit from algorithm:", str(balance - startBal))