from typing import List
from datetime import time
from utils import read_data_flow

OPEN_TIME = time(9, 30, 0)
CLOSE_TIME = time(15, 0, 0)


class Transaction:
    def __init__(self, code, file_path):
        self.transaction_flow = read_data_flow(code=code, file_path=file_path, data_type="Transaction")

    def day_cum_trade_quantity(self, date: str = "2022-07-04"):
        return self.transaction_flow["TradeQty"][self.transaction_flow.index.date.astype(str) == date].cumsum()

    def avg_cum_trade_quantity(self):
        resample = self.transaction_flow["TradeQty"].resample("3s").sum().between_time(OPEN_TIME, CLOSE_TIME)
        return resample.groupby([resample.index.time]).mean().cumsum()
