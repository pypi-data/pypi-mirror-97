import pandas as pd
from ta.utils import dropna
from datetime import datetime, timedelta
import ta
import time
import argparse
from multiprocessing import Process, Manager
import threading
from openpyxl import load_workbook
import configparser


'''============================================================================'''
##################################################################################
'''




'''
##################################################################################
'''============================================================================'''
try:
    from order import *
    from algos import *
    from util import log as log
    from util import DataSource
    from util import Stream
except:
    from six_pack_trade_algo import *
def main():
    # Load configs according to comand line input
    parser = argparse.ArgumentParser()
    parser.add_argument("--main_config", default="DEFAULT",type=str)
    # parser.add_argument("--strategy_config", default="REBALANCER",type=str)
    # parser.add_argument("--order_config", default="DEFAULT",type=str)
    parser.add_argument('--data_path', default="/home/rbe/AlgoTrader/data/",type=str)
    parser.add_argument('--strategy_config', default=["REB_PAPER_1.0"], nargs='+')
    args = parser.parse_args()
    fs_prefix = args.data_path + "configs/"
    config_list = []
    try:
        main_config = configparser.ConfigParser()
        main_config.read(fs_prefix + "main.cnt")
        main_config = main_config[args.main_config]

        quick_test     = main_config["quick_test"]
        data_path      = main_config["data_path"]
        data_source    = main_config["data_source"]
        api_key_id     = main_config["api_key_id"]
        api_secret_key = main_config["api_secret_key"]
        api_base_url   = main_config["api_base_url"]
        try:
            start_date = main_config["start_date"]
            end_date = main_config["end_date"]
        except Exception as e:
            print("************ No dates found in config for Backtester. Using defaults. ************        ")
            start_date = "2020-06-01"
            end_date = "2020-06-15"

        # algo_config = configparser.ConfigParser()
        # algo_config.read(fs_prefix + "algo.cnt")
        # algo_config = algo_config[args.algo_config]
        
        # order_config = configparser.ConfigParser()
        # order_config.read(fs_prefix + "order_manager.cnt")
        # order_config = order_config[args.order_config]
        
        
        str_config_parser = configparser.ConfigParser()
        for profile in args.strategy_config:
            str_config_parser.read(fs_prefix + "str.cnt")
            str_config = str_config_parser[profile]
            config_list.append(str_config)
        
    except Exception as e:
        print("************ Error loading configs in main. ************        " + str(e))

    # 
    # make the factory
    # 
    algoFactory = AlgoFactory()
    orderManagerFactory = OrderManagerFactory()

    master_wb = load_workbook(filename=data_path + "master.xlsx")
    algo_list = {}
    thread_list = []
    sheet_dict = {}

    return_dict = Manager().dict()

    stream = Stream(
                key_id=api_key_id ,secret_key=api_secret_key,
                base_url=api_base_url
    )
    stream_thread = threading.Thread(target=stream.ws_start, daemon=True)
    stream_thread.start()

    open_orders = stream.get_open_orders()

    i = 2

    for config in config_list:

        data_source = DataSource(
                    key_id=api_key_id ,secret_key=api_secret_key ,
                    base_url=api_base_url, data_source=data_source, tickers=config["tickers"].split(","),
                    start_date=start_date ,end_date=end_date
                    )
        orderManagerFactory.setType(config['type'])
        order_manager = orderManagerFactory.build(
                                GUID=config['guid'],
                                data_path=data_path,
                                data_source=data_source,
                                order_config=config,
                                open_orders = open_orders
                                )
        
        algoFactory.setType(config['type'])
        algo = algoFactory.build(order_manager=order_manager,
                                 data_path=data_path,
                                 data_source=data_source,
                                 GUID=config['guid'],
                                 config=config
                                )

        # Verify test mode
        if quick_test == "no":
            data_source.quick_test = False
            order_manager.quick_test = False
        else:
            data_source.quick_test = True
            order_manager.quick_test = True

        
        # Start the process and correctly set the name
        algo_thread = Process(target=algo.run, name=str(i), args=(return_dict,))
        algo_thread.start()
        
        
        algo_list[config['guid']] = algo
        thread_list.append((config['guid'] ,algo_thread))
        
        
        share_val = 0
        for p in algo.positions:
            share_val += algo.positions[p] * algo.data_source.get_last_trade(p)["price"]
        sheet = master_wb[config['type']]
        try:
            sheet_dict[sheet] += 1
            
        except:
            sheet_dict[sheet] = 1
        d = sheet_dict[sheet]
        sheet[d][0].value = config['guid']
        sheet[d][1].value = order_manager.wallet
        sheet[d][2].value = ', '.join(algo.tickers)
        sheet[d][3].value = algo.tick_period
        sheet[d][4].value = algo.print_details() 
        sheet[d][5].value = order_manager.print_details()
        sheet[d][8].value = share_val
        i+=1
        
    sheet_dict = {}
    # Check if threads are done and save out
    while 0 < len(thread_list):
        remove_list = []
        for g, thread in thread_list:
            if not thread.is_alive():
                i = int(thread.name)
                thread.join()
                algo_finished = algo_list[g]
                ret = return_dict[config_list[i-2]['guid']]
                pos = ret[1]
                total_shares = 0
                for shares in list(pos.values()):
                    total_shares += shares
                share_val = 0
                for p in pos:
                    share_val += pos[p] * algo_finished.data_source.get_last_trade(p)["price"]
                sheet = master_wb[config['type']]
                try:
                    sheet_dict[sheet] += 1
                    
                except:
                    sheet_dict[sheet] = 1
                d = sheet_dict[sheet]
                sheet[d][6].value = ret[0]
                sheet[d][7].value = total_shares
                sheet[d][9].value = share_val
                sheet[d][10].value = share_val + ret[0]
                master_saved = False
                while not master_saved:
                    try:
                        master_wb.save(data_path + "master.xlsx")
                        master_saved = True
                    except Exception as e:
                        print(e)
                        print("CANNOT SAVE TO MASTER")
                        time.sleep(1)
                remove_list.append((config_list[i-2]['guid'],thread))
        for tup in remove_list:
            thread_list.remove(tup)
        time.sleep(1)
            
            
    while algo_finished.data_source.get_clock()["is_open"] and bool(stream.get_open_orders()):
        time.sleep(5)
        print("Keeping process alive for stream thread")
        

if __name__ == "__main__":
    main()
    exit()
