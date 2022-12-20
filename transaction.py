from typing import List
from utils import read_data_flow


class Transaction:
    def __init__(self, code, file_path):
        self.transaction_flow = read_data_flow(code=code, file_path=file_path, data_type="Transaction")

    def day_cum_trade_quantity(self, date: str = "2022-07-04"):
        return self.transaction_flow["TradeQty"][self.transaction_flow.index.date.astype(str) == date].cumsum()

    @property
    def avg_cum_trade_quantity(self):
        return self.transaction_flow["TradeQty"].groupby([self.transaction_flow.index.time]).mean().cumsum()
