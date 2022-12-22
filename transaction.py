import talib
from datetime import time
from utils import read_data_flow

OPEN_TIME = time(9, 30, 0)
CLOSE_TIME = time(15, 0, 0)
BREAK_TIME = [time(11, 30, 0), time(13, 0, 0)]


class Transaction:
    def __init__(self, code, file_path):
        self.transaction_flow = read_data_flow(code=code, file_path=file_path, data_type="T")
        self.buffer = {
            "intraday_price_series": {},
            "price_series": {}
        }

    def day_cum_trade_quantity(self, date: str = "2022-07-04"):
        return self.transaction_flow["TradeQty"][self.transaction_flow.index.date.astype(str) == date].cumsum()

    @property
    def avg_cum_trade_quantity(self):
        resample = self.transaction_flow["TradeQty"].resample("3s").sum().between_time(OPEN_TIME, CLOSE_TIME)
        return resample.groupby([resample.index.time]).mean().cumsum()

    def intraday_price_series(self, date: str = "2022-07-04"):
        buffer = self.buffer["intraday_price_series"].get(date, 0)
        if isinstance(buffer, int):
            buffer = self.transaction_flow["TradePrice"][self.transaction_flow.index.date.astype(str) == date].resample(
                "3s").last().ffill().between_time(OPEN_TIME, CLOSE_TIME).between_time(BREAK_TIME[1],
                                                                                      BREAK_TIME[0],
                                                                                      include_start=False,
                                                                                      include_end=False)
            self.buffer["intraday_price_series"][date] = buffer
        return buffer

    def price_series(self, resample_period="1D"):
        buffer = self.buffer["price_series"].get(resample_period, 0)
        if isinstance(buffer, int):
            buffer = self.transaction_flow["TradePrice"].resample(resample_period).last().dropna().between_time(
                OPEN_TIME, CLOSE_TIME)
            self.buffer["price_series"][resample_period] = buffer
        return buffer

    def macd(self, date: str = "2022-07-04"):
        return talib.MACD(self.intraday_price_series(date), fastperiod=12, slowperiod=26, signalperiod=9)

    def ma(self, date: str = "2022-07-04"):
        return talib.MA(self.intraday_price_series(date), timeperiod=30, matype=0)
