from datetime import datetime as dt, timezone, timedelta
import time
import alpaca_trade_api as tradeapi
import pickle
import pandas as pd
from shared_memory_dict import SharedMemoryDict

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
        def __init__(self, tickers, wallet, positions):
            self.tickers = tickers
            self.wallet = wallet
            self.positions = positions


    def __init__(self, GUID, data_path, data_source, config, sm):
        self.open_orders = SharedMemoryDict(name=sm + "_open_orders", size=2048)
        self.last_filled_orders = SharedMemoryDict(name=sm + "_last_filled_orders", size=2048)
        self.log = None
        self.GUID = GUID
        self.wallet = float(config["start_wallet"])
        self.threshold = float(config["thresh_percent"]) * self.wallet  #   ex, 25,000 * .05 = 125
        self.data_source = data_source
        if config['tickers'] == '':
            self.tickers = []
        else:
            self.tickers = config["tickers"].split(",")
        self.positions = {}
        for t in self.tickers:
            self.positions[t] = (0,0) # Positions stored as tuples (quantity, buy_price)
        self.test = True
        self.buy_qty = {}
        self.prev_rsi = {}
        self.mem_file = data_path + "algo_mem/{}.pkl".format(GUID)
        self.short_selling_enabled = False
        
    def _buy(self, ticker, quantity, type='limit', limit_price=None, block_on_market_order=True):
        price = limit_price
        if type=='market' or self.wallet > price * quantity:
            if not self.test:
                response = self.data_source.submit_order(
                    ticker=ticker,
                    quantity=quantity,
                    side='buy',
                    type=type,
                    limit_price=limit_price,
                    time_in_force='gtc'
                )
                if response['id'] == 0:
                    self.log.warn("[order.py][_buy]: response id==0  Buy Unsuccessful")
                    return
                if type == 'market':
                    time.sleep(1)
                    order_id =response['id']
                    while block_on_market_order and order_id in self.open_orders:
                        time.sleep(.5)
                    price = float(self.last_filled_orders[order_id][1])
            self.positions[ticker] = (self.positions[ticker][0] + quantity, price)
            self.wallet -= price*quantity
            self.log.trade("Limit Buy {} of {} at {} per share".format(ticker, quantity, price))
            self.log.trade("Wallet Value: {}         SPENT -{}".format(self.wallet, price*quantity))
        else:
            self.log.warn(" ! NOT ENOUGH MONEY ! Wallet Value: {}".format(self.wallet))
            
    def _sell(self, ticker, quantity, type='limit', limit_price=None,  block_on_market_order=True):
        price = limit_price
        if self.positions[ticker][0] >= quantity or self.short_selling_enabled:
            if not self.test:
                response = self.data_source.submit_order(
                    ticker=ticker,
                    quantity=quantity,
                    side='sell',
                    type=type,
                    limit_price=limit_price,
                    time_in_force='gtc'
                )
                if response['id'] == 0:
                    self.log.warn("[order.py][_sell]: response id==0  Sell Unsuccessful")
                    return
                if type == 'market':
                    time.sleep(1)
                    order_id =response['id']
                    while block_on_market_order and order_id in self.open_orders:
                        time.sleep(.5)
                    price = float(self.last_filled_orders[order_id][1])
            self.positions[ticker] = (self.positions[ticker][1] - quantity, self.positions[ticker][1])
            self.wallet += price*quantity
            self.log.trade("Limit Sell {} of {} at {} per share".format(ticker, quantity, price))
            self.log.trade("Wallet Value: {}          MADE  +{}".format(self.wallet, price*quantity))
        else:
            self.log.warn(" ! NOT ENOUGH SHARES ! Wallet Value: {}".format(self.wallet))
    
    
    def _cancel_open_orders(self, side='buy'):
        self.log.info("Checking for open orders on {} side".format(side))
        self.log.warn("This method should be rewritten with new open_orders implementation from Stream()".format(side))
        return
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
                self.positions[ticker][0] -= qty
                self.orders.remove(id)
                capital_out -= total_price
            #If the oldest order is a sell
            else:
                self.log.info("Canceling Sell Order Id: {}, Ticker: {}, Shares Returned: {}".format(id, ticker, qty))
                self.data_source.cancel_order(id)
                total_price = qty * limit_price  
                self.wallet -= total_price
                self.positions[ticker][0] += qty
                self.orders.remove(id)
        self.log.info("Finished check for open orders")
    
    def save_algo(self):
        try:
            if self.test: raise Exception("Test mode on. No Saving.")
            fs = open(self.mem_file ,"w+b")
            to_save = self.Memory(self.tickers, self.wallet, self.positions)
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
            self.log.info("Found Memory ||     wallet:{}".format(self.wallet))
            fs.close()
        except Exception as e:
            self.log.warn("Cannot load algo. Creating a mem file...   "   + str(e))
            self.save_algo()
    
    
    def get_total_value(self):
        total_value = self.wallet
        if len(self.tickers) == 0:
            return total_value
        for t in self.tickers:
            ticker_price = self.data_source.get_last_trade(t)["price"]
            try:
                total_value += self.positions[t][0] * ticker_price
            except:
                # supress keyerror if no position for ticker
                pass
        return total_value
        
    
    # takes in list of tickers and safely adds them to the tickers list for this order manager
    # basically also creates entries in the position dict if not already added
    def add_tickers(self, tickers):
        self.log.info("Adding to ticker list: {}".format(tickers))
        for ticker in tickers:
            if ticker not in self.positions:
                self.positions[ticker] = (0,0)
            if ticker not in self.tickers:
                self.tickers.append(ticker)
    
    def refresh_tickers(self):
        self.log.info("Refreshing tickers lists")
        to_remove = self.tickers
        for t in list(self.positions): # if you dont use .keys() it will fail on del
            if self.positions[t][0] != 0:
                to_remove.remove(t)
            else:
                del self.positions[t]
        for t in to_remove:
            self.tickers.remove(t)

        
    def cancel_all_open_orders(self):
        self.log.info("Canceling all Open Orders")
        self._cancel_open_orders('buy')
        self._cancel_open_orders('sell')
        
    def print_details(self):
        if self.test:
            return "Test On"
        else:
            return "Test Off"


class RsiOrderManager(OrderManager):
    def __init__(self, GUID, data_path, data_source, config):
        super().__init__(GUID, data_path, data_source, config)
        self.sell_percent = float(config["sell_percent"])
        self.buy_percent = float(config["buy_percent"])
        for t in self.tickers:
            self.buy_qty[t] = int( (self.wallet*self.buy_percent) / float(self.data_source.get_last_trade(t)["price"]))
            if self.buy_qty[t] < 1:
                self.buy_qty[t] = 1
            self.positions[t][0] = 0
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
    def __init__(self, GUID, data_path, data_source, config):
        super().__init__(GUID, data_path, data_source, config)
        
        
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
    def __init__(self, GUID, data_path, data_source, config, sm):
        super().__init__(GUID, data_path, data_source, config, sm)
        self.short_selling_enabled = True
        
    def rebalance_short(self, proportions):
        self.log.info("Started Rebalancing on Order Manager")
        self.cancel_all_open_orders()
        # Go through each ticker and wallet value. Calculate how much 
        # value of each ticker i should have
        equity = self.get_total_value() * .95 # set aside 5 % at all times
        to_short = []
        to_cover = []
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
                shares_to_short = int((desired_value-current_value)/current_share_price)
                if shares_to_short != 0:
                    to_short.append((t,shares_to_short,"market", current_share_price))
                else:
                    self.log.info("Not enough of a difference to short another share")
            if desired_value < current_value:
                shares_to_cover = int((current_value-desired_value)/current_share_price)
                if shares_to_cover != 0:
                    to_cover.append((t,shares_to_cover,"market", current_share_price))
                else:
                    self.log.info("Not enough of a difference to cover another share")
        
        self.log.info("to_short : {}".format(to_short))
        self.log.info("to_cover  : {}".format(to_cover))
        for short in to_short:
            self._sell(*short)
            # self._sell(*sell)
        for cover in to_cover:
            self._buy(*cover)
            # self._buy(*buy)
    
    def cover_all_percentage(self, percent=.05):
        self.log.info("Placing Cover Orders on all positions at {} projected profit.".format(percent))
        for t in self.positions:
            cur_qty, cur_price  = self.positions[t]
            if cur_price==0:
                cur_price=self.data_source.get_last_trade(t)["price"]
            if cur_qty < 0:
                cur_qty = cur_qty * -1
            try:
                self._buy(t, int(cur_qty), "limit", cur_price*(1.0-percent))
            except TradeException as te:
                raise Exception(te)
            
    def print_details(self):
        return super().print_details() + ", {}".format("placeholder")



class OrderManagerFactory():
    def __init__(self, type="DEFAULT", test='yes'):
        self.type = type
        if test == 'yes':
            self.test = True
        else:
            self.test = False
    def build(self, data_path, data_source, GUID, order_config, sm):
        if self.type == "RSI":
            manager = RsiOrderManager(
                        GUID=GUID,
                        data_path=data_path,
                        data_source=data_source,
                        config=order_config,
                        sm=sm
                        )
        if self.type == "REBALANCING":
            manager = DailyRebalancerOrderManager(
                        GUID=GUID,
                        data_path=data_path,
                        data_source=data_source,
                        config=order_config,
                        sm=sm
                        )
        if self.type == "SHORT":
            manager = ShortOrderManager(
                        GUID=GUID,
                        data_path=data_path,
                        data_source=data_source,
                        config=order_config,
                        sm=sm
                        )
        manager.test = self.test
        return manager
        
    def setType(self, type):
        self.type = type
    