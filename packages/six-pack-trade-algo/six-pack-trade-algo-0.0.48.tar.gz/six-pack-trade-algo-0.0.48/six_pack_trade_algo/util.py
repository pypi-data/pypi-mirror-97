from datetime import datetime, timezone, timedelta
import time
import alpaca_trade_api as tradeapi
#
#
#       Classes in util
#
#           AlgoLogger
#           Backtester
#           Datasource
#           Stream
#
try:
    pass
    print("util.py dev version")
except Exception as e:
    print("util.py {}".format(e))
class AlgoLogger:
    def __init__(self,data_path="", name=""):
        self.to_print = []
        self.error_print = " [  -------- ERROR --------  ] "
        self.trade_print = " [  -------- TRADE --------  ] "
        self.info_print =  " [  -------- INFO  --------  ] "
        self.warn_print =  " [  -------- WARN  --------  ] "
        self.sep =         " [  -----------------------  ] "
        self.fn = data_path + "daily_logs/prog/{}.txt".format(datetime.today().strftime('%Y-%m-%d'))
        if name:
            self.set_name(name)

    def info(self, output):
        self.to_print.append(self.info_print + str(output))
        self.output()
    def trade(self, output):
        self.to_print.append(self.trade_print + str(output))
        self.output()
    def warn(self, output):
        self.to_print.append(self.warn_print + str(output))
        self.output()
    def error(self, output):
        self.to_print.append(self.error_print + str(output))
        self.output()

    def set_name(self, name):
        
        self.error_print = " [ {} {} ][ -------- ERROR -------- ] ".format(name, datetime.now().replace(microsecond=0))
        self.trade_print = " [ {} {} ][ -------- TRADE -------- ] ".format(name, datetime.now().replace(microsecond=0))
        self.info_print =  " [ {} {} ][ -------- INFO  -------- ] ".format(name, datetime.now().replace(microsecond=0))
        self.warn_print =  " [ {} {} ][ -------- WARN  -------- ] ".format(name, datetime.now().replace(microsecond=0))

    def output(self):
        for p in self.to_print:
            print(p)
            try:
                log_file = open(self.fn, 'a')
                log_file.write(p)
                log_file.close()
            except:
                pass
        self.clear_print_buf()
    def output_scr(self):
        i=0
        while i < 4:
            print()
            i+=1
        self.output()
        print(self.sep * 4)
    def clear_print_buf(self):
        self.to_print = []

log = AlgoLogger()

backtest = "backtest"
live = "live"
paper = "paper"
class Backtester():
    #  date will be 'YYYY-MM-DD'
    def __init__(self, api_endpoint, tickers, start_date, end_date):
        self.api_endpoint = api_endpoint
        self.poly = api_endpoint.polygon
        tz = timezone(-timedelta(hours=4))
        self.account = 500000.0
        self.tickers = tickers
        self.is_open = True
        self.start_utc = datetime.fromisoformat(start_date).replace(tzinfo=tz).timestamp()
        self.prev_utc = None
        self.cur_time = self.start_utc
        self.end_utc = datetime.fromisoformat(end_date).replace(tzinfo=tz).timestamp()
        self.positions = {}
        self.algo_done = False
        self.cur_utc = datetime.fromtimestamp(self.cur_time, tz)
        # self.cur_utc = datetime.fromtimestamp(self.cur_time, -timedelta(hours=4))
        self.current_date = "{0:0=4d}".format(self.cur_utc.year)+"-"+"{0:0=2d}".format(self.cur_utc.month)+"-"+"{0:0=2d}".format(self.cur_utc.day)
        self.cur_df = {}
        for t in self.tickers:
            self.positions[t] = 0
        self.update_dataframes()
        self.run()

    # dictates if algo is done overall
    def run(self):
        if self.cur_time >= self.end_utc or self.algo_done:
            self.algo_done = True
            self.is_open = False
            return
        else:
            self.run_step()

    # dictates time between market close and opens
    def run_step(self):
        minute = 60
        self.cur_time += minute
        # if it the market is closed, keep incrementing till open
        while not self.open_hours():
            self.cur_time += minute
            if self.cur_time >= self.end_utc or self.algo_done:
                self.algo_done = True
                self.is_open = False
                return

        # now check that the current data frame is valid for each ticker
        # if the dataframe isn't valid, try to get a new dataframe
        for t in self.tickers:
            valid_df = False
            while not valid_df:
                try:
                    self.cur_df[t].loc[self.cur_utc]
                    valid_df = True
                except:
                    self.cur_time += (minute * 60 * 23)
                    self.open_hours()
                    self.update_dataframes()
                    if self.cur_time >= self.end_utc or self.algo_done:
                        self.algo_done = True
                        self.is_open = False
                        return
        return

    def update_dataframes(self):
        for t in self.tickers:
            self.cur_df[t] = self.poly.historic_agg_v2(t, 1, 'minute', _from=self.current_date, to=self.current_date).df

    def open_hours(self):
        self.cur_utc = datetime.fromtimestamp(self.cur_time, timezone(-timedelta(hours=4)))
        self.current_date = "{0:0=4d}".format(self.cur_utc.year)+"-"+"{0:0=2d}".format(self.cur_utc.month)+"-"+"{0:0=2d}".format(self.cur_utc.day)
        if   (self.cur_utc.hour >= 16 and self.cur_utc.minute >= 0):
            return False
        elif (self.cur_utc.hour >= 9 and self.cur_utc.minute >= 30):
            return True
        else:
            return False
    # def get_date(self):
    #     self.cur_utc = datetime.fromtimestamp(self.cur_time, timezone(-timedelta(hours=4)))
    #     self.current_date = "{0:0=4d}".format(self.cur_utc.year)+"-"+"{0:0=2d}".format(self.cur_utc.month)+"-"+"{0:0=2d}".format(self.cur_utc.day)
    #     return self.current_date
        
    def get_clock(self):
        return {"is_open" : self.is_open}

    def get_last_trade(self, ticker):
        price = self.cur_df[ticker].loc[self.cur_utc]
        ret = {"price" : price["close"]}
        return ret

    def get_position(self, ticker):
        # print("get position")
        price = self.cur_df[ticker].loc[self.cur_utc]["close"]
        qty =  self.positions[ticker]
        # print(price)
        # print(qty)
        
        ret = {"qty" : qty,"current_price" : price, "market_value" : price*qty, }
        return ret

    def get_account(self):
        ret = {"cash" : self.account}
        return ret

    def submit_order(self, ticker, quantity, side, type, limit_price, time_in_force):
        # check using cur_price vs limit_price
        # cur_price = get_last_trade(ticker)
        if side == "buy":
            self.positions[ticker] += quantity
            self.account -= limit_price * quantity

        if side == "sell":
            self.positions[ticker] -= quantity
            self.account += limit_price * quantity
        return

class DataSource:

    def __init__(self, key_id, secret_key, base_url, data_source=backtest, tickers=None, start_date=None, end_date=None):
        self.api_endpoint = tradeapi.REST(
            key_id=key_id,
            secret_key=secret_key,
            base_url=base_url
        )
        self.mode = data_source      # backtest, live, paper
        self.quick_test = True
        if self.mode == backtest:
            self.backtester = Backtester(self.api_endpoint, tickers, start_date, end_date)
        else:
            self.backtester = None


    #
    # tick_perod is in seconds
    #
    def step(self, tick_period):
        if (self.mode == live or self.mode == paper):
                    if self.quick_test:
                        time.sleep(0.5)
                    else:
                        time.sleep(tick_period)
        if (self.mode == backtest):
            self.backtester.run()


    def get_clock(self):
        if (self.mode == backtest):
            return self.backtester.get_clock()
        clk = self.api_endpoint.get_clock()
        ret = {"is_open" : clk.is_open, "timestamp" : clk.timestamp}
        return ret
        
    def get_date(self):
        self.cur_utc = datetime.fromtimestamp(self.get_clock()['timestamp'], timezone(-timedelta(hours=4)))
        self.current_date = "{0:0=4d}".format(self.cur_utc.year)+"-"+"{0:0=2d}".format(self.cur_utc.month)+"-"+"{0:0=2d}".format(self.cur_utc.day)
        return self.current_date

    def get_last_trade(self, ticker):
        if (self.mode == backtest):
            return self.backtester.get_last_trade(ticker)
        trd = self.api_endpoint.get_last_trade(ticker)
        ret = {"price" : trd.price}
        return ret
        
    def get_last_quote(self, ticker):
        if (self.mode == backtest):
            return self.backtester.get_last_quote(ticker)
        qte = self.api_endpoint.get_last_quote(ticker)
        ret = {"price" : qte.price}
        return ret
        
    def get_position(self, ticker):
        if (self.mode == backtest):
            return self.backtester.get_position(ticker)
        try:
            pos =  self.api_endpoint.get_position(ticker)
            qty = pos.qty
            market_value = pos.market_value
            current_price = pos.current_price
        except Exception as e:
            qty = 0
            market_value = 0
            current_price = 0
            log.info("Cannot find position info for {} on Alpaca.".format(ticker))
            
        ret = {"qty" : qty, "market_value" : market_value, "current_price" : current_price }
        return ret

    def get_account(self):
        if (self.mode == backtest):
            return self.backtester.get_account()
        act = self.api_endpoint.get_account()
        ret = {"cash" : act.cash, "equity" : act.equity}
        return ret

    def list_orders(self, side):
        try:
            if (self.mode == backtest):
                return self.backtester.list_orders()
            if (self.mode == paper):
                orders = api_paper.list_orders()
            if (self.mode == live):
                orders = api_live.list_orders()
            valid_orders = []
            for o in orders:
                if o.side == side:
                    info = {"limit_price" : o.limit_price,
                            "qty" : o.qty,
                            "id" : o.id}
                    valid_orders.append(info)
            return valid_orders
        except Exception as e:
            print(e)
            print("list_orders : IMPLEMENT THIS")
            pass

    def submit_order(self, ticker, quantity, side, type, limit_price, time_in_force):
        info = {"limit_price" : 0,
                "qty" : 0,
                "id" : 0}
        try:
            if (self.mode == backtest):
                return self.backtester.submit_order(ticker, quantity, side, type, limit_price, time_in_force)
                            
            response = self.api_endpoint.submit_order(
            symbol=ticker,
            qty=quantity,
            side=side,
            type=type,
            limit_price=limit_price,
            time_in_force=time_in_force
            )
            
            info = {"limit_price" : response.limit_price,
                    "qty" : response.qty,
                    "id" : response.id}
            return info

        except Exception as e:
            log.info("DATA SOURCE ERROR: submit_order()         " + str(e))
            return info
    def cancel_order(self, order_id):
        try:
            if (self.mode == backtest):
                return
            self.api_endpoint.cancel_order(
            order_id=order_id
            )
        except Exception as e:
            log.info("CANCEL ORDER ERROR: cancel_order()        " + str(e))
    
    def list_assets(self):
        try:
            if (self.mode == backtest):
                print("implement this")
                return
            all_assets = self.api_endpoint.list_assets()
            ret = []
            for asset in all_assets:
                ret.append({"symbol" : asset.symbol,
                            "easy_to_borrow" : asset.easy_to_borrow,
                            "shortable" : asset.shortable,
                            "tradable" : asset.tradable,
                            "status" : True if asset.status == 'active' else False
                })
            return ret
        except Exception as e:
            log.info("DATA ERROR: list_assets()        " + str(e))
    
    
    def historic_agg(self, ticker, num, day, start_date , end_date):
        try:
            return self.api_endpoint.polygon.historic_agg_v2(ticker, num, day, _from=start_date, to=end_date).df
        except Exception as e:
            log.error("DATA ERROR: historic_agg()      {}    {}".format(e, ticker))
            raise Exception("invalid agg call {} ".format(ticker))

class Stream:
    class Memory:
        def __init__(self, open_orders):
            self.open_orders = orders_dict


    def __init__(self, key_id, secret_key, base_url, data_path, test):
        self.open_orders = {}
        self.mem_file = data_path + "algo_mem/stream.pkl"
        self.test = test
        try:
            self.conn  = tradeapi.stream2.StreamConn(key_id, secret_key, base_url)
        except Exception as e:
            log.error("CANNOT ESTABLISH WEB SOCKET CONNECTION:          " + str(e))
            raise Exception("Bad stream object. Check provided credentials.")        
        try:
            if self.test:
                return
            fs = open(self.mem_file, "rb")
            from_save = pickle.load(fs)
            self.open_orders = from_save.open_orders
            fs.close()
            log.info("Loading in Stream Contents")
        except Exception as e:
            log.warn("Error loading in stream contents. May just not exist though.  {}".format(e))
        @self.conn.on(r'^trade_updates$')
        async def on_trade_updates(conn, channel, trade):
            log.set_name("UTIL")
            if trade.event == 'new':
                side = trade.order['side']
                symbol = trade.order['symbol']
                id = trade.order['id']
                qty = trade.order['qty']
                limit_price = trade.order['limit_price']
                self.open_orders[id] = (side, qty, limit_price, symbol)
                log.info("New Order - {}  {}  {}, # still open: {}".format(id, symbol, side, len(self.open_orders)))
            elif trade.event == 'canceled':
                id = trade.order['id']
                del self.open_orders[trade.order['id']]
                log.info("Canceled Order - {}, # still open: {}".format(id, len(self.open_orders)))
            elif trade.event == 'fill':
                id = trade.order['id']
                del self.open_orders[trade.order['id']]
                log.info("Filled Order - {}, # still open: {}".format(id, len(self.open_orders)))
            elif trade.event == 'expired':
                id = trade.order['id']
                del self.open_orders[trade.order['id']]
                log.info("Expired Order - {}, # still open: {}".format(id, len(self.open_orders)))
            try:
                if self.test:
                    return
                fs = open(self.mem_file, "w+b")
                to_save = self.Memory(self.open_orders)
                pickle.dump(to_save, fs)
                fs.close()
                log.info("Saving Stream")
            except Exception as e:
                log.error("Stream() error saving contents: {}".format(e))
    def ws_start(self):
        self.conn.run(['trade_updates'])
        # time.sleep(2)
        # Why does this sleep for 2?
    
    def get_num_open(self):
        return len(self.open_orders)

    def get_open_orders(self):
        return self.open_orders
