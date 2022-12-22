import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from transaction import Transaction
from price import Price

sns.set_style("darkgrid")

if __name__ == "__main__":
    t = Transaction(688363, "/Users/y1han/databases/STAR Board/")
    # t.avg_cum_trade_quantity.plot()
    t.intraday_price_series().plot()
    # t.ma().plot()

    # p = Price(688017, "/Users/y1han/databases/STAR Board/")
    # p.order_quantity("2022-07-04").plot()
    # p.intraday_price_series("2022-07-04").plot(secondary_y=True, alpha=0.5, color="grey")
    # p.bid_ask_spread("2022-07-04").plot(secondary_y=True, alpha=0.5, color="grey", marker='.', linestyle='none')
    # p.avg_order_quantity.plot()
    # p.avg_bid_ask_spread.plot.line(secondary_y=True, alpha=0.5, color="grey", marker='.', linestyle='none')
    # p.signature_plot_series(resample_period="1H").plot.scatter(x='lag', y='var')
    # p.price_series(resample_period="1H").plot()
    plt.show()
