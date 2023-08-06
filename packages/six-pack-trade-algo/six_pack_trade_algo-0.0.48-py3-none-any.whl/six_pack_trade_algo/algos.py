import pandas as pd
import ta
from ta.utils import dropna
from datetime import datetime as dt, timedelta
import time
import pickle
from heapq import heappush
import datetime
# BDay is business day, not birthday...
from pandas.tseries.offsets import BDay

try:
    from util import AlgoLogger
    print("algo.py dev version")
except Exception as e:
    from six_pack_trade_algo import AlgoLogger
    print("order.py {}".format(e))
    # from six_pack_trade_algo import *
    # from util import AlgoLogger
#
#
#       Classes in algos
#
#           Algo
#           AlgoRsiBb
#
#
'''============================================================================'''
##################################################################################
'''
    This package is responsible for generating buy and sell signals. The input should be data and the output should be a buy, sell, or hold signal. 
    All other functionality relating to how many shares you should buy at what price goes in OrderManger classes. This division is for organizational purposes, 
    not technical reasons. You can in theory write a large class that does all of that.
    
    We also make this abstraction because our DataSource is modular. We can get data from real time sources or from csv files for backtesting. 
    
           main.py
              |
              V
           Algo classes
         /              \
        V                V
    DataSource  <->  OrderManger
        |                  
        V
    Real Data/
    Backtester
'''
##################################################################################
'''============================================================================'''

class Algo:
    def __init__(self, order_manager, data_path, data_source, GUID, config):
        self.log = AlgoLogger(data_path=data_path)
        self.log.set_name(GUID)
        self.data_source = data_source
        self.GUID = GUID
        self.tick_period = int(config["tick_period"])       # the interval of the algo in seconds.
                                                            # if its run every day, the interval is 86400, for example.
        order_manager.log = self.log
        self.order_manager = order_manager

    def run(self):
        self.log.info("STARTED ALGO:  " + self.GUID)
        if not bool(self.data_source.get_clock()["is_open"]):
            self.log.warn("Market is closed")
        else:
            self.log.info("Market is open")
        self.order_manager.load_algo()
        self.log.output()

    def run_end(self):
        self.log.info("Market is closed. Saving wallet data...")
        self.order_manager.save_algo()
        self.log.output()

    def is_test(self):
        return self.order_manager.test

    def print_details(self):
        return ""


class RsiBbAlgo(Algo):
    def __init__ (self, order_manager, data_path, data_source, GUID, config):
        super().__init__(order_manager, data_path, data_source, GUID,  config)
        self.data_points = int(config["data_points"])
        self.stddev = float(config["std_dev"])
        self.rsi_high = float(config["rsi_high"])
        self.rsi_low = float(config["rsi_low"])
        self.bollinger_indicator = {}
        for t in self.order_manager.tickers:
            self.bollinger_indicator[t] = "Middle"

    def run(self, return_dict):
        super().run()
        trades = {}
        while bool(self.data_source.get_clock()["is_open"]):
            for t in self.order_manager.tickers:
                try:
                    trades[t] += [self.data_source.get_last_trade(t)["price"]]
                except Exception as e:
                    trades[t] = [self.data_source.get_last_trade(t)["price"]]
                try:
                    if len(trades[t]) > self.data_points:
                        trades_df = pd.DataFrame(trades[t],columns=['intraday'])
                        rsi = self.generateRsiIndicator(trades_df['intraday'])
                        bollingerBands = self.generateBollingerBands(trades_df['intraday'])
                        try:
                            self.trade(t, bollingerBands, rsi)
                        except Exception as e:
                            self.log.error("Trade error: {}, {}".format(t, e))
                    else:
                        self.log.info("Init trades {}: {}".format(t, 100*len(trades[t])/self.data_points))
                except Exception as e:
                    self.log.error("dataframe issue?: {}".format(e))
            self.log.output()
            self.data_source.step(self.tick_period)
        super().run_end()
        return_dict[self.GUID] = (self.order_manager.wallet, self.order_manager.positions)


    def generateBollingerBands(self, df):
        bollingerBands = ta.volatility.BollingerBands(df, n = self.data_points, ndev=self.stddev)
        return bollingerBands

    def generateRsiIndicator(self, df):
        rsi = ta.momentum.rsi(df, n = self.data_points)
        return rsi

    def trade(self, ticker, bollingerBands, rsi):
        if(bollingerBands.bollinger_hband_indicator().tail(1).iloc[0]):
            self.log.info("Current RSI_BB: {}  is above bollinger bands".format(ticker))
            self.bollinger_indicator[ticker] = "Above"
        elif(bollingerBands.bollinger_lband_indicator().tail(1).iloc[0]):
            self.log.info("Current RSI_BB: {}  is below bollinger bands".format(ticker))
            self.bollinger_indicator[ticker] = "Below"
        else:
            self.log.info("Current RSI_BB: {}  is inbetween bollinger bands; Checking RSIs : {} ".format(ticker, rsi.tail(1).iloc[0]))
            if ((rsi.tail(1).iloc[0] > 50) and (self.bollinger_indicator[ticker] == "Below")) or (rsi.tail(1).iloc[0] > self.rsi_high):
                self.order_manager.buy_shares(ticker)
            elif ((rsi.tail(1).iloc[0] < 50) and (self.bollinger_indicator[ticker] == "Above")) or (rsi.tail(1).iloc[0] > self.rsi_low):
                self.order_manager.sell_proportional(ticker)
            self.bollinger_indicator[ticker] = "Middle"
            
    def print_details(self):
        return "{}, {}, {}, {}".format(self.data_points, self.stddev, self.rsi_high, self.rsi_low)

class MeanReversionBucketsAlgo(Algo):
    def __init__ (self, order_manager, data_path, data_source, GUID, config):
        super().__init__(order_manager, data_path, data_source, GUID,  config)
        self.data_points = int(config["data_points"])
        self.stddev = float(config["std_dev"])
        self.rsi_high = float(config["rsi_high"])
        self.rsi_low = float(config["rsi_low"])
        self.bollinger_indicator = {}
        for t in self.order_manager.tickers:
            self.bollinger_indicator[t] = "Middle"

    def run(self, return_dict):
        super().run()
        trades = {}
        while bool(self.data_source.get_clock()["is_open"]):
            for t in self.order_manager.tickers:
                try:
                    trades[t] += [self.data_source.get_last_trade(t)["price"]]
                except Exception as e:
                    trades[t] = [self.data_source.get_last_trade(t)["price"]]
                try:
                    if len(trades[t]) > self.data_points:
                        trades_df = pd.DataFrame(trades[t],columns=['intraday'])
                        rsi = self.generateRsiIndicator(trades_df['intraday'])
                        bollingerBands = self.generateBollingerBands(trades_df['intraday'])
                        try:
                            self.trade(t, bollingerBands, rsi)
                        except Exception as e:
                            self.log.error("Trade error: {}, {}".format(t, e))
                    else:
                        self.log.info("Init trades {}: {}".format(t, 100*len(trades[t])/self.data_points))
                except Exception as e:
                    self.log.error("dataframe issue?: {}".format(e))
            self.log.output()
            self.data_source.step(self.tick_period)
        super().run_end()
        return_dict[self.GUID] = (self.order_manager.wallet, self.order_manager.positions)

    def generateBollingerBands(self, df):
        bollingerBands = ta.volatility.BollingerBands(df, n = self.data_points, ndev=self.stddev)
        return bollingerBands

    def generateRsiIndicator(self, df):
        rsi = ta.momentum.rsi(df, n = self.data_points)
        return rsi

    def trade(self, ticker, bollingerBands, rsi):
        if(bollingerBands.bollinger_hband_indicator().tail(1).iloc[0]):
            self.log.info("Current RSI_BB: {}  is above bollinger bands".format(ticker))
            self.bollinger_indicator[ticker] = "Above"
        elif(bollingerBands.bollinger_lband_indicator().tail(1).iloc[0]):
            self.log.info("Current RSI_BB: {}  is below bollinger bands".format(ticker))
            self.bollinger_indicator[ticker] = "Below"
        else:
            self.log.info("Current RSI_BB: {}  is inbetween bollinger bands; Checking RSIs : {} ".format(ticker, rsi.tail(1).iloc[0]))
            if ((rsi.tail(1).iloc[0] > 50) and (self.bollinger_indicator[ticker] == "Below")) or (rsi.tail(1).iloc[0] > self.rsi_high):
                self.order_manager.buy_shares(ticker)
            elif ((rsi.tail(1).iloc[0] < 50) and (self.bollinger_indicator[ticker] == "Above")) or (rsi.tail(1).iloc[0] > self.rsi_low):
                self.order_manager.sell_proportional(ticker)
            self.bollinger_indicator[ticker] = "Middle"
            
    def print_details(self):
        return "{}, {}, {}, {}".format(self.data_points, self.stddev, self.rsi_high, self.rsi_low)

class RebalancingAlgo(Algo):
    def __init__ (self, order_manager, data_path, data_source, GUID, config):
        super().__init__(order_manager, data_path, data_source, GUID,config)
        self.ran_today = False
        
    def run(self, return_dict):
        super().run()
        while bool(self.data_source.get_clock()["is_open"]):

            if not self.ran_today:
                proportions = []
                equity = self.order_manager.get_total_value() * .95 # set aside 5 % at all times
                for t in self.order_manager.tickers:
                    proportions.append(1.0/len(self.order_manager.tickers))
                self.order_manager.rebalance(proportions)
                self.log.output()
                # self.data_source.test = True
                self.data_source.step(self.tick_period)
                self.ran_today = True
            self.log.info("Waiting for 5 to keep stream thread alive until end of day")
            time.sleep(5)
        super().run_end()
        return_dict[self.GUID] = (self.order_manager.wallet, self.order_manager.positions)

class ShortAlgo(Algo):
    def __init__ (self, order_manager, data_path, data_source, GUID, config):
        super().__init__(order_manager, data_path, data_source, GUID,config)
        
    def run(self, return_dict):
        super().run()
        while bool(self.data_source.get_clock()["is_open"]) or True:
            print("short algo test")
            shortable_tickers = []
            for asset in self.data_source.list_assets():
                if asset["status"] == True and asset["easy_to_borrow"] == True and asset["shortable"] == True and asset["tradable"] == True:
                    shortable_tickers.append(asset['symbol'])
            equity = self.order_manager.get_total_value() * .95 # set aside 5 % at all times
            # prev buisiness day
            #
            if self.is_test():
                self.log.info("Shortening list to 50 for testing")
                shortable_tickers = shortable_tickers[:50]
            
            percent_change_list = []
            prog = len(shortable_tickers)
            for ticker in shortable_tickers:
                try:
                    prev_b_day = dt.today() - BDay(1)   # buisiness day
                    day_prev_close = self.data_source.historic_agg(ticker, 1, 'day', prev_b_day, prev_b_day)['close'][0]
                    today_close = self.data_source.get_last_trade(ticker)['price']
                    day_percent_change = float(100*(today_close-day_prev_close)/day_prev_close)
                    percent_change_list.append((ticker,day_percent_change))
                    prog-=1
                    self.log.info("Prog: {} {}".format(prog, ticker))
                except Exception as e:
                    self.log.warn("Unable to retreive prev_close or today_close info for {}:      {}".format(ticker, e))
            percent_change_list.sort(key=lambda x:x[1])
            
            # grab the last 10 tickers
            percent_change_list = percent_change_list[-10:]
            # short each ticker based on the price uptick using similar propotion scheme to REBALANCING
            # Also we are only shorting in this scenario
            total_proportion = 0
            for tup in percent_change_list:
                total_proportion += tup[1]
            proportions = {}
            tickers = []
            for tup in percent_change_list:
                tickers.append(tup[0])
                proportions[tup[0]] = tup[1]/total_proportion
            self.order_manager.add_tickers(tickers)
            self.order_manager.rebalance_short(proportions)
                
                
            print(percent_change_list)
            exit()
            self.log.output()
            # self.data_source.test = True
            self.data_source.step(self.tick_period)
            self.ran_today = True

        super().run_end()
        return_dict[self.GUID] = (self.order_manager.wallet, self.order_manager.positions)




class AlgoFactory():
    def __init__(self, type="RSI_BB"):
        self.type = type

        
    def build(self, order_manager, data_path, data_source, GUID, config):
        if self.type == "RSI_BB":
            algo = RsiBbAlgo(
                order_manager=order_manager,
                data_path=data_path,
                data_source=data_source,
                GUID=GUID,
                config=config
                )
        if self.type == "REBALANCING":
            algo = RebalancingAlgo(
                order_manager=order_manager,
                data_path=data_path,
                data_source=data_source,
                GUID=GUID,
                config=config
                )
        if self.type == "SHORT":
            algo = ShortAlgo(
                order_manager=order_manager,
                data_path=data_path,
                data_source=data_source,
                GUID=GUID,
                config=config
                )

        return algo
    def setType(self, type):
        self.type = type
    