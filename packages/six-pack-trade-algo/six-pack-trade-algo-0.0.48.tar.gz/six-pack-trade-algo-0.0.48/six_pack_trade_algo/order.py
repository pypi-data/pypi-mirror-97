from datetime import datetime as dt, timezone, timedelta
import time
import alpaca_trade_api as tradeapi
import pickle
import pandas as pd

try:
    from util import AlgoLogger
    print("order.py dev version")
except Exception as e:
    from six_pack_trade_algo import AlgoLogger
    print("order.py {}".format(e))
    
'''============================================================================'''
##################################################################################
'''
    This package is responsible for managing the positions and data of a stock. Everything that doesn't have directly to do with a technical analysis of the stock
    to generate buy or sell signals goes here. This includes figuring out how large each trade should be and what should be traded. The OM classes get data
    from the internet, then passes data along to the Algo classes and receive buy/sell signals back. The OM base class is also responsible for some buy/sell time
    checks as well as managing open orders, and saving the end-of-run (information that is unique to each time the bot is run) algorithm data to be available for the 
    next day. End-of-run information includes the positions for that day as well as net gains or losses during the day. 

    All buy and sell orders should ultimately be submitted using the _buy() and _sell() functions in the base OM class. Currently we only support limit orders.

'''
##################################################################################
'''============================================================================'''

class OrderManager:
    class Memory:
        def __init__(self, tickers, wallet, positions, orders, misc):
            self.tickers = tickers
            self.wallet = wallet
            self.positions = positions
            self.orders = orders


    def __init__(self, GUID, data_path, data_source, config, open_orders):
        self.open_orders = open_orders
        self.log = None
        self.GUID = GUID
        self.wallet = float(config["start_wallet"])
        self.threshold = float(config["thresh_percent"]) * self.wallet  #   ex, 25,000 * .05 = 125
        self.data_source = data_source
        self.tickers = config["tickers"].split(",")
        self.orders = []
        self.positions = {}
        for t in self.tickers:
            self.positions[t] = 0
        self.test = True
        self.buy_qty = {}
        self.init_buy_price = {}
        self.init_buy = {}
        self.prev_rsi = {}
        self.mem_file = data_path + "algo_mem/{}.pkl".format(GUID)
        self.short_selling_enabled = False
        
    def _buy(self, ticker, quantity, price=0, type='limit'):
        self._cancel_open_orders(side='buy')
        if self.wallet > price * quantity:
            if not self.test:
                response = self.data_source.submit_order(
                ticker=ticker,
                quantity=quantity,
                side='buy',
                type=type,
                limit_price=price,
                time_in_force='gtc'
                )
                info = (response['id'])
                self.orders.append(info)
            self.positions[ticker] += quantity
            self.wallet -= price*quantity
            self.log.trade("Limit Buy {} of {} at {} per share".format(ticker, quantity, price))
            self.log.trade("Wallet Value: {}         SPENT -{}".format(self.wallet, price*quantity))
        else:
            self.log.warn(" ! NOT ENOUGH MONEY ! Wallet Value: {}".format(self.wallet))
            
    def _sell(self, ticker, quantity, price=0, type='limit'):
        self._cancel_open_orders(side='sell')
        if self.positions[ticker] >= quantity or self.short_selling_enabled:
            if not self.test:
                response = self.data_source.submit_order(
                ticker=ticker,
                quantity=quantity,
                side='sell',
                type=type,
                limit_price=price,
                time_in_force='gtc'
                )
                info = (response['id'])
                self.orders.append(info)

            self.positions[ticker] -= quantity
            self.wallet += price*quantity
            self.log.trade("Limit Sell {} of {} at {} per share".format(ticker, quantity, price))
            self.log.trade("Wallet Value: {}          MADE  +{}".format(self.wallet, price*quantity))
        else:
            self.log.warn(" ! NOT ENOUGH SHARES ! Wallet Value: {}".format(self.wallet))
    
    def _cancel_open_orders(self, side='buy'):
        self.log.info("Checking for open orders on {} side".format(side))
        capital_out = 0
        # Goes through local order list and updates using live list
        for order in self.orders:
            if self.open_orders.get(order) != None:
                if self.open_orders[order][0] == side:
                    capital_out += self.open_orders[order][1] * self.open_orders[order][2]   #Add up capital_out
            else:
                self.orders.remove(order)
        # If capital out exceeds our threshold we will cancel orders starting from the oldest unitl we have enough open capital
        while capital_out > self.threshold:
            id = self.orders[0]
            side = self.open_orders[id][0]
            qty = self.open_orders[id][1]
            limit_price = self.open_orders[id][2]
            ticker = self.open_orders[id][3]
            #If the oldest order is a buy
            if side == "buy":
                self.log.info("Canceling Buy Order Id: {}, Buy_Capital_out: {}".format(id, capital_out-total_price))
                self.data_source.cancel_order(id)
                total_price = qty * limit_price 
                self.wallet += total_price
                self.positions[ticker] -= qty
                self.orders.remove(id)
                capital_out -= total_price
            #If the oldest order is a sell
            else:
                self.log.info("Canceling Sell Order Id: {}, Ticker: {}, Shares Returned: {}".format(id, ticker, qty))
                self.data_source.cancel_order(id)
                total_price = qty * limit_price  
                self.wallet -= total_price
                self.positions[ticker] += qty
                self.orders.remove(id)
        self.log.info("Finished check for open orders")
    
    def save_algo(self):
        try:
            if self.test: raise Exception("Test mode on. No Saving.")
            fs = open(self.mem_file ,"w+b")
            to_save = self.Memory(self.tickers, self.wallet, self.positions, self.orders, self.misc)
            pickle.dump(to_save,fs)
            fs.close()
            self.log.info("MEM_SAVE SUCCESSFUL")
        except Exception as e:
            self.log.error("Cannot save algo: ")
            self.log.error(e)

    def load_algo(self):
        if self.test: return
        try:
            fs = open(self.mem_file ,"rb")
            from_save = pickle.load(fs)
            if self.tickers != from_save.tickers:
                raise Exception("Incompatable ticker found in mem. Resetting...")
            self.wallet = from_save.wallet
            self.positions = from_save.positions
            self.orders = from_save.orders
            self.log.info("Found Memory ||     wallet:{}".format(self.wallet))
            fs.close()
        except Exception as e:
            self.log.warn("Cannot load algo. Creating a mem file...   "   + str(e))
            self.save_algo()
    
    
    def get_total_value(self):
        total_value = self.wallet
        for t in self.tickers:
            ticker_price = self.data_source.get_last_trade(t)["price"]
            try:
                total_value += self.positions[t] * ticker_price
            except:
                # supress keyerror if no position for ticker
                pass
        return total_value
        
    
    # takes in list of tickers and safely adds them to the tickers list for this order manager
    # basically also creates entries in the position dict if not already added
    def add_tickers(self, tickers):
        for ticker in tickers:
            if ticker not in self.positions:
                self.positions[ticker] = 0
            if ticker not in self.tickers:
                self.tickers.append(ticker)
    
    def print_details(self):
        if self.test:
            return "Test On"
        else:
            return "Test Off"


class RsiOrderManager(OrderManager):
    def __init__(self, GUID, data_path, data_source, config, open_orders):
        super().__init__(GUID, data_path, data_source, config, open_orders)
        self.sell_percent = float(config["sell_percent"])
        self.buy_percent = float(config["buy_percent"])
        for t in self.tickers:
            self.buy_qty[t] = int( (self.wallet*self.buy_percent) / float(self.data_source.get_last_trade(t)["price"]))
            if self.buy_qty[t] < 1:
                self.buy_qty[t] = 1
            self.init_buy_price[t] = 0
            self.init_buy[t] = True # Not used rn
            self.positions[t] = 0
    def sell_proportional(self, ticker):
        try:
            self.log.info("sell_proportional {}".format(ticker))
            pos = self.data_source.get_position(ticker)
            qty = 0
            price = float(self.data_source.get_last_trade(ticker)["price"])
            if int(pos["qty"]) <= 30:
                qty = int(pos["qty"])
            else:
                qty = int(qty*self.sell_percent)
            if qty == 0:
                self.log.info("sell_proportional no shares to sell")
                return
            super()._sell(ticker, qty, price)
            self.log.info("SELL Partial {} shares of {}".format(qty, ticker))
        except Exception as e:
            self.log.error("sell_proportional error: {} ".format(e))

    def buy_shares(self, ticker):
        try:
            self.log.info("buy_shares {}".format(ticker))
            # Make sure that the current wallet value - (buy price * qty + 1%)  > 25,000
            balance = float(self.data_source.get_account()["cash"])
            price = float(self.data_source.get_last_trade(ticker)["price"])
            total_cost = price * float(self.buy_qty[ticker])
            if (balance - (total_cost * 1.01)> 25000.0):
                super()._buy(ticker, self.buy_qty[ticker], price)
                self.log.info("BUY {} shares of {}".format(self.buy_qty[ticker], ticker))
            else:
                raise Exception("Not enough wallet value. Cost:{} / Balance:{}".format(total_cost, balance))
        except Exception as e:
            self.log.error("buy_shares error: {}".format(e))
            
    def print_details(self):
        return super().print_details() + ", {}, {}".format(self.buy_percent, self.sell_percent)

class DailyRebalancerOrderManager(OrderManager):
    def __init__(self, GUID, data_path, data_source, config, open_orders):
        super().__init__(GUID, data_path, data_source, config, open_orders)
        
        
    # proportions is a *normalized* list that describes what percentage of the equity should be allocated to each ticker.
    # the order of proportions should be the same as the order for tickers. the lengths should be the same as well.
    # sum of elements in proportions list should be 1. This is not asserted for due to rounding errors coming about from floating point division
    #
    def rebalance(self, proportions):
        if len(proportions) != len(self.tickers):
            raise Exception("proportions list and tickers list don't have the same number of elements!")
        self.log.info("Started Rebalancing on Order Manager")
        # Go through each ticker and wallet value. Calculate how much 
        # value of each ticker i should have
        equity = self.order_manager.get_total_value() * .95 # set aside 5 % at all times
        to_buy = []
        to_sell = []
        for i, t in enumerate(self.tickers):
            self.log.info("Rebalancing " + t)
            desired_value = proportions[i] * equity
            current_pos = self.data_source.get_position(t)
            # print(current_pos)
            current_value = float(current_pos["market_value"])
            current_share_price = float(current_pos["current_price"])
            if current_share_price == 0:
                current_share_price = self.data_source.get_last_trade(t)["price"]
            
            # first I want to sell.
            # then i want to buy
            self.log.info("Desired : {},   Current : {},     Share Price : {}".format(desired_value, current_value, current_share_price))
            
            if desired_value == current_value:
                continue
            if desired_value > current_value:
                shares_to_buy = int((desired_value-current_value)/current_share_price)
                if shares_to_buy != 0:
                    to_buy.append((t,shares_to_buy,current_share_price))
                else:
                    self.log.info("Not enough of a difference to buy another share")
            if desired_value < current_value:
                shares_to_sell = int((current_value-desired_value)/current_share_price)
                if shares_to_sell != 0:
                    to_sell.append((t,shares_to_sell,current_share_price))
                else:
                    self.log.info("Not enough of a difference to sell another share")
        
        self.log.info("to_sell : {}".format(to_sell))
        self.log.info("to_buy  : {}".format(to_buy))
        for sell in to_sell:
            self._sell(*sell)
        for buy in to_buy:
            self._buy(*buy)
            
            
            
            
            
    def print_details(self):
        return super().print_details() + ", {}".format("placeholder")

class ShortOrderManager(OrderManager):
    def __init__(self, GUID, data_path, data_source, config, open_orders):
        super().__init__(GUID, data_path, data_source, config, open_orders)
        self.short_selling_enabled = True
        
    def rebalance_short(self, proportions):
        self.log.info("Started Rebalancing on Order Manager")
        # Go through each ticker and wallet value. Calculate how much 
        # value of each ticker i should have
        equity = self.get_total_value() * .95 # set aside 5 % at all times
        to_buy = []
        to_sell = []
        for i, t in enumerate(self.tickers):
            self.log.info("Short Rebalancing " + t)
            try:
                desired_value = proportions[t] * equity
            except:
                desired_value = 0
            current_pos = self.data_source.get_position(t)
            # this should always be zero
            # print(current_pos)
            current_value = float(current_pos["market_value"])
            current_share_price = float(current_pos["current_price"])
            if current_share_price == 0:
                current_share_price = self.data_source.get_last_trade(t)["price"]
            
            # first I want to sell.
            # then i want to buy
            self.log.info("Desired : {},   Current : {},     Share Price : {}".format(desired_value, current_value, current_share_price))
            
            if desired_value == current_value:
                continue
            if desired_value > current_value:
                shares_to_buy = int((desired_value-current_value)/current_share_price)
                if shares_to_buy != 0:
                    to_buy.append((t,shares_to_buy,current_share_price))
                else:
                    self.log.info("Not enough of a difference to buy another share")
            if desired_value < current_value:
                shares_to_sell = int((current_value-desired_value)/current_share_price)
                if shares_to_sell != 0:
                    to_sell.append((t,shares_to_sell,current_share_price))
                else:
                    self.log.info("Not enough of a difference to sell another share")
        
        self.log.info("to_sell : {}".format(to_sell))
        self.log.info("to_buy  : {}".format(to_buy))
        for sell in to_sell:
            self._sell(*sell)
        for buy in to_buy:
            self._buy(*buy)
        
    def print_details(self):
        return super().print_details() + ", {}".format("placeholder")



class OrderManagerFactory():
    def __init__(self, type="DEFAULT", test='yes'):
        self.type = type
        if test == 'yes':
            self.test = True
        else:
            self.test = False
    def build(self, data_path, data_source, GUID, order_config, open_orders):
        if self.type == "RSI":
            manager = RsiOrderManager(
                        GUID=GUID,
                        data_path=data_path,
                        data_source=data_source,
                        config=order_config,
                        open_orders = open_orders
                        )
        if self.type == "REBALANCING":
            manager = DailyRebalancerOrderManager(
                        GUID=GUID,
                        data_path=data_path,
                        data_source=data_source,
                        config=order_config,
                        open_orders = open_orders
                        )
        
        if self.type == "SHORT":
            manager = ShortOrderManager(
                        GUID=GUID,
                        data_path=data_path,
                        data_source=data_source,
                        config=order_config,
                        open_orders = open_orders
                        )
        manager.test = self.test
        return manager
        
    def setType(self, type):
        self.type = type
    