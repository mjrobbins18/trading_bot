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

while True:
    print("")
    print("Checking Price")

    market_data = api.get_barset(symb, 'minute', limit=5)
    close_list = []
    for bar in market_data[symb]:
        close_list.append(bar.c)
    
    close_list = np.array(close_list, dtype=np.float64)
    ma = np.mean(close_list)
    last_price = close_list[4]

    print("Moving Average: " + str(ma))
    print("Last Price: " + str(last_price))

    if ma + 0.01 < last_price and not pos_held:
        print("Buy")
        api.submit_order(
            symbol=symb,
            qty=10,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        pos_held=True
    
    elif ma - 0.01 > last_price and pos_held:
        print("Sell")
        api.submit_order(
            symbol=symb,
            qty=10,
            side='sell',
            type='market',
            time_in_force='gtc'
        )
        pos_held=False

    time.sleep(60)