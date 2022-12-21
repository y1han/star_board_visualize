from typing import Optional
import pandas as pd
from utils import read_data_flow
from datetime import time
from statsmodels.tsa.stattools import acf

OPEN_TIME = time(9, 30, 0)
CLOSE_TIME = time(15, 0, 0)
BREAK_TIME = [time(11, 30, 0), time(13, 0, 0)]


class Price:
    def __init__(self, code, file_path):
        self.price_flow = read_data_flow(code=code, file_path=file_path, data_type="Stock")

    def order_quantity(self, date: str = "2022-07-04"):
        return self.price_flow[["TotalBidQty", "TotalOfferQty"]][self.price_flow.index.date.astype(str) == date]

    def intraday_price_series(self, date: str = "2022-07-04"):
        return self.price_flow["LastPx"][self.price_flow.index.date.astype(str) == date].between_time(OPEN_TIME,
                                                                                                      CLOSE_TIME)

    def price_series(self, resample_period="1D"):
        return self.price_flow["LastPx"].resample(resample_period).last().dropna().between_time(OPEN_TIME, CLOSE_TIME)

    def signature_plot_series(self, date: Optional[str] = None, resample_period="1D"):
        price_series = self.price_series(resample_period) if date is None else self.intraday_price_series(date)
        var_r = (price_series.diff()/price_series).var()
        acf_series = acf(price_series, nlags=500)
        res = pd.DataFrame([], columns=["lag", "var"])
        for tau in range(0, min(200, len(acf_series))):
            var = var_r * (1 + 2 * sum([(1 - u / tau) * acf_series[u] for u in range(1, tau)]))
            res.loc[len(res)] = [tau, var]
        return res

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
