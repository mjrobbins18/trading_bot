import alpaca_trade_api as tradeapi
import os
from dotenv import load_dotenv

load_dotenv()


SEC_KEY = os.getenv('SEC_KEY')
PUB_KEY = os.getenv('PUB_KEY')
BASE_URL = os.getenv('BASE_URL')

api = tradeapi.REST(key_id=PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)


# Buy a stock
api.submit_order(
    symbol='SPY',
    qty=1,
    side='buy',
    type='market',
    time_in_force='gtc'
)

# Sell
api.submit_order(
    symbol='SPY',
    qty=1,
    side='sell',
    type='market',
    time_in_force='gtc'
)