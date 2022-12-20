from utils import read_data_flow
from datetime import time

OPEN_TIME = time(9, 30, 0)
CLOSE_TIME = time(15, 0, 0)


class Price:
    def __init__(self, code, file_path):
        self.price_flow = read_data_flow(code=code, file_path=file_path, data_type="Stock")

    def order_quantity(self, date: str = "2022-07-04"):
        return self.price_flow[["TotalBidQty", "TotalOfferQty"]][self.price_flow.index.date.astype(str) == date]

    def price_series(self, date: str = "2022-07-04"):
        return self.price_flow["LastPx"][self.price_flow.index.date.astype(str) == date].between_time(OPEN_TIME,
                                                                                                       CLOSE_TIME)

    @property
    def avg_order_quantity(self):
        resample = self.price_flow[["TotalBidQty", "TotalOfferQty"]].resample("3s").sum().between_time(OPEN_TIME,
                                                                                                       CLOSE_TIME)
        return resample.groupby([resample.index.time]).mean()
