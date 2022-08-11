import numpy as np
import pandas as pd
from pandas import DataFrame
from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IStrategy, IntParameter)
import talib.abstract as ta
import pandas_ta as pta
import freqtrade.vendor.qtpylib.indicators as qtpylib

class ha_strat(IStrategy):
    INTERFACE_VERSION = 2
    timeframe = '1m'
    minimal_roi = {
        "60": 0.01
    }
    stoploss = -0.05
    trailing_stop = True
    trailing_only_offset_is_reached = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    process_only_new_candles = False
    use_exit_signal = True
    exit_profit_only = True
    ignore_roi_if_entry_signal = True
    startup_candle_count: int = 1
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe['rsi'] = ta.RSI(dataframe)

        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=15, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_upperband'] = bollinger['upper']

        dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
        dataframe['ema15'] = ta.EMA(dataframe, timeperiod=15)
        dataframe['ema30'] = ta.EMA(dataframe, timeperiod=30)

        heikinashi = qtpylib.heikinashi(dataframe)
        dataframe['ha_open'] = heikinashi['open']
        dataframe['ha_close'] = heikinashi['close']
        dataframe['ha_high'] = heikinashi['high']
        dataframe['ha_low'] = heikinashi['low']

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['ha_high'] > dataframe['ha_close']) & # candle is green
                (dataframe['ha_high'] > dataframe['ha_open']) & # upward wick
                (dataframe['ha_low'] >= dataframe['ha_open']) & # no bottom wick
                (dataframe['ema5'] > dataframe['ema30']) & # momentum
                (dataframe['volume'] > 0) # volume
            ),
            'enter_long'] = 1
        return dataframe

        dataframe.loc[
            (
                    (dataframe['ha_low'] < dataframe['bb_lowerband']) &
                    (dataframe['ema5'] > dataframe['bb_lowerband']) &
                    (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['ha_close'] < dataframe['ha_open']) & # candle is red
                (dataframe['ha_low'] < dataframe['ha_close']) & # downward wick
                (dataframe['ha_high'] >= dataframe['ha_open']) & # no top wick
                (dataframe['ema5'] < dataframe['ema30']) & # momentum
                (dataframe['volume'] > 0) # volume
            ),
            'exit_long'] = 1
        return dataframe


        dataframe.loc[
            (
                (dataframe['ha_high'] > dataframe['bb_upperband']) &
                (dataframe['ema5'] > dataframe['bb_upperband']) &
                (dataframe['volume'] > 0)
            ),
            'exit_long'] = 1
        return dataframe
