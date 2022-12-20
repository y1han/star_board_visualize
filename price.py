from utils import read_data_flow
from datetime import time

OPEN_TIME = time(9, 30, 0)
CLOSE_TIME = time(15, 0, 0)
BREAK_TIME = [time(11, 30, 0), time(13, 0, 0)]


class Price:
    def __init__(self, code, file_path):
        self.price_flow = read_data_flow(code=code, file_path=file_path, data_type="Stock")

    def order_quantity(self, date: str = "2022-07-04"):
        return self.price_flow[["TotalBidQty", "TotalOfferQty"]][self.price_flow.index.date.astype(str) == date]

    def price_series(self, date: str = "2022-07-04"):
        return self.price_flow["LastPx"][self.price_flow.index.date.astype(str) == date].between_time(OPEN_TIME,
                                                                                                      CLOSE_TIME)

    def bid_ask_spread(self, date: str = "2022-07-04"):
        resample = self.price_flow[self.price_flow.index.date.astype(str) == date].between_time(OPEN_TIME, CLOSE_TIME)
        return (resample["Sell1Price"] - resample["Buy1Price"]) / resample["Buy1Price"]

    @property
    def avg_bid_ask_spread(self):
        resample = self.price_flow.resample(
            "3s").mean().between_time(OPEN_TIME, CLOSE_TIME).between_time(BREAK_TIME[1],
                                                                          BREAK_TIME[0],
                                                                          include_start=False,
                                                                          include_end=False).copy()
        resample["spread"] = (resample["Sell1Price"] - resample["Buy1Price"]) / resample["Buy1Price"]
        return resample["spread"].groupby([resample.index.time]).mean()

    @property
    def avg_order_quantity(self):
        resample = self.price_flow[["TotalBidQty", "TotalOfferQty"]].resample("3s").sum().between_time(OPEN_TIME,
                                                                                                       CLOSE_TIME)
        return resample.groupby([resample.index.time]).mean()
