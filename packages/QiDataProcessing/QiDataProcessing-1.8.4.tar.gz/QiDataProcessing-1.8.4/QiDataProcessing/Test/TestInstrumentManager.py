import time

import pandas as pd

from QiDataProcessing.BaseBarHelper import BaseBarHelper
from QiDataProcessing.Core.EnumMarket import EnumMarket
from QiDataProcessing.Core.TradingDayHelper import TradingDayHelper
from QiDataProcessing.Instrument.InstrumentManager import InstrumentManager
from QiDataProcessing.QiDataController import QiDataController
import datetime
from QiDataProcessing.Core.EnumBarType import EnumBarType
from QiDataProcessing.QiDataDirectory import QiDataDirectory
from QiDataProcessing.TradingFrame.YfTimeHelper import YfTimeHelper

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

trading_day = datetime.datetime(2019, 10, 13)
tick_path = "\\\\192.168.1.200\\MqData\\futuretick\\Future"
min_path = "\\\\192.168.1.200\\MqData\\futuremin"
day_path = "\\\\192.168.1.200\\MqData\\futureday"

qi_data_directory = QiDataDirectory()
qi_data_directory.trading_day = trading_day
qi_data_directory.future_tick = tick_path
qi_data_directory.future_tick_cache = tick_path
qi_data_directory.future_min = min_path
qi_data_directory.future_day = day_path

qi_data_controller = QiDataController(qi_data_directory)
# 获取交易所代码
exchange_id = qi_data_controller.instrument_manager.get_exchange_id('sc9999')
# 获取期货品种列表
lst_product_ids = qi_data_controller.instrument_manager.get_product_ids(EnumMarket.期货, exchange_id)
# 获取期货主力合约列表
lst_main_contract = qi_data_controller.instrument_manager.get_main_contracts(EnumMarket.期货, exchange_id)
# 获取期货上市日期
listing_date = qi_data_controller.instrument_manager.get_listing_date(EnumMarket.期货, 'fu9999')
# 获取期货活跃日期
active_date = qi_data_controller.instrument_manager.get_active_date(EnumMarket.期货, 'fu9999')

print(exchange_id)
for product_id in lst_product_ids:
    print(product_id)
for main_contract in lst_main_contract:
    print(main_contract)
print(listing_date.strftime('%Y%m%d'))
print(active_date.strftime('%Y%m%d'))
# trading_frame_manager = qi_data_controller.instrument_manager.trading_frame_manager
#
# instrument_id = 'IC2001'
# lst_ic = []
# for instrument_id in qi_data_controller.instrument_manager.all_instruments:
#     if 'IC' in instrument_id:
#         instrument = qi_data_controller.instrument_manager.all_instruments[instrument_id]
#         lst_ic.append([instrument_id, instrument.expire_date])
# lst_ic.sort(key=lambda x: x[0])
# for data in lst_ic:
#     instrument_id = data[0]
#     if '99' not in instrument_id:
#         year = int(instrument_id[2:4]) + 2000
#         month = int(instrument_id[4:6])
#         month_first_day = datetime.datetime(year, month, 1)
#         week_day = month_first_day.weekday()
#         if week_day <= 4:
#             expire_date = month_first_day + datetime.timedelta(days=2 * 7 + 4 - week_day)
#         else:
#             expire_date = month_first_day + datetime.timedelta(days=2 * 7 + 6 - week_day + 5)
#         expire_date = TradingDayHelper.get_first_trading_day(expire_date)
#         equanl = data[1] == expire_date
#         print('{0}:{1},{2},{3}'.format(instrument_id, data[1].strftime('%Y%m%d'), expire_date.strftime('%Y%m%d'), equanl))
