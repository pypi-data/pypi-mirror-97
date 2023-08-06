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

# trading_day = datetime.datetime(2019, 10, 13)
tick_path = "\\\\192.168.1.200\\MqData\\futuretick\\Future"
min_path = "\\\\192.168.1.200\\MqData\\futuremin"
day_path = "\\\\192.168.1.200\\MqData\\futureday"

qi_data_directory = QiDataDirectory()
# qi_data_directory.trading_day = trading_day
qi_data_directory.future_tick = tick_path
qi_data_directory.future_tick_cache = tick_path
qi_data_directory.future_min = min_path
qi_data_directory.future_day = day_path

qi_data_controller = QiDataController(qi_data_directory)

instrument_id = 'ag9999'
kline_interval = 30
today_hours_num = 19
back_n = 100
trading_date = datetime.datetime(2020, 5, 7)

hour_kline = qi_data_controller.load_bar_series_by_length(EnumMarket.期货, instrument_id, kline_interval, EnumBarType.minute,
                                                       today_hours_num + back_n + 20,
                                                       trading_date)

print(hour_kline)
print(len(hour_kline))