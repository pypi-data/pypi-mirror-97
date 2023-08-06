import alpaca_trade_api as tradeapi

import datetime
# BDay is business day, not birthday...
from pandas.tseries.offsets import BDay


api_endpoint = tradeapi.REST(
            key_id="PKUG3R65L13JLJ3YQ11K",
            secret_key="ENXBQr7dtqXY0Rgy9AWT4DHqCNJjTcxQwqhPsqDt",
            base_url="https://paper-api.alpaca.markets"
)
ret = api_endpoint.list_assets()
# print(ret)
# print("---------------------------------")
# print(ret[0])
# ret is list of all assets
# filter for assets that are 
#   shortable
#   tradable
#   easy to borrow
# print(ret)
print(len(ret))
ret_final=[]
for asset in ret:
    if asset.status == 'active' and asset.easy_to_borrow == True and asset.shortable == True and asset.tradable == True:
        ret_final.append(asset.symbol)
print(len(ret_final))
# print(ret_final)

print(api_endpoint.get_clock())
today = datetime.datetime.today()
prev_b_day = today - BDay(1)
print(prev_b_day)
for ticker in ret_final:
    print(ticker)
    print(api_endpoint.get_last_quote(ticker))
    print(api_endpoint.get_last_trade(ticker))
    exit()