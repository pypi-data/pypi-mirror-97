# import pandas as pd
# from ta.utils import dropna
# from datetime import datetime, timedelta
# import ta
# import time
# import argparse
# from multiprocessing import Process, Manager
# from openpyxl import load_workbook


# from AlgoTrader.algos.AlgoRsi import AlgoRsi as Algo
# from AlgoTrader.util.AlgoLogger import log
# from algotrader.util import DataSource

print("TEST 0")

# from algos import *
# from util import *


# import six_pack_trade_algo

print("TEST .5")
# from six_pack_trade_algo.algos.AlgoRsi import AlgoRsi as Algo

# import six_pack_trade_algo.util

# from six_pack_trade_algo import log
import alpaca_trade_api as tradeapi
    # api_key_id          = PKNTHH7YSGCEMWMMRRY4
    # api_secret_key      = t4vleKwZhGApgSRyvuExsZS9L2VxRyE4ZAqlX8R1
    # api_base_url        = https://paper-api.alpaca.markets
api_endpoint = tradeapi.REST(
    key_id='PKNTHH7YSGCEMWMMRRY4',
    secret_key='t4vleKwZhGApgSRyvuExsZS9L2VxRyE4ZAqlX8R1',
    base_url='https://paper-api.alpaca.markets'
)

print(api_endpoint.get_account())
print(api_endpoint.get_position("Z"))
print(api_endpoint.get_clock())

# import os
# os.mkdir("$HOME/six_pack_cache/algo_mem")
# 
# 
# # log = AlgoLogger()
# log.info("test")
# log.output()
# print("TEST 2")

# print(api_paper.get_last_trade("BA"))
# print(float(api_paper.get_last_trade("BA").price))