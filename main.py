import pandas as pd
import matplotlib.pyplot as plt
from transaction import Transaction

if __name__ == "__main__":
    t = Transaction(688017, "/Users/y1han/databases/STAR Board/")
    t.avg_cum_trade_quantity.plot()
    plt.show()
