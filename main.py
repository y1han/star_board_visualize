import pandas as pd
import matplotlib.pyplot as plt
from transaction import Transaction
from price import Price

if __name__ == "__main__":
    # t = Transaction(688017, "/Users/y1han/databases/STAR Board/")
    # t.avg_cum_trade_quantity.plot()
    # plt.show()

    p = Price(688082, "/Users/y1han/databases/STAR Board/")
    # p.order_quantity("2022-07-04").plot()
    # p.price_series("2022-07-04").plot(secondary_y=True, alpha=0.5, color="grey")
    # p.bid_ask_spread("2022-07-04").plot(secondary_y=True, alpha=0.5, color="grey", marker='.', linestyle='none')
    # p.avg_order_quantity.plot()
    p.avg_bid_ask_spread.plot.line(secondary_y=True, alpha=0.5, color="grey", marker='.', linestyle='none')
    plt.show()
