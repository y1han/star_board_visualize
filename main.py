import pandas as pd
import matplotlib.pyplot as plt
import configparser
import os


def read_data_flow(code, file_path="", data_type="Order", config_file="data_config.cfg"):
    config = configparser.ConfigParser()
    config.read(config_file)
    reserve_index = [e.strip() for e in config.get('reserve_index', data_type).split(",")]
    print(reserve_index)
    file_path = file_path + str(code) + "/"
    order_files = [item for item in os.listdir(file_path) if data_type in item]
    res = pd.concat((pd.read_csv(file_path + f) for f in order_files), ignore_index=True)
    res["MDTime"] = transform_time(res["MDDate"].astype(str), res["MDTime"].astype(str))
    return res[reserve_index].sort_values(by=["MDTime"]).set_index("MDTime")


def transform_time(date_series, time_series):
    return pd.to_datetime(date_series + " " + time_series, format="%Y%m%d %H%M%S%f")


if __name__ == "__main__":
    df = read_data_flow(code=688017, file_path="/Users/y1han/databases/STAR Board/", data_type="Transaction")
    # print(df)
    plt.plot(df["TradeQty"][df.index.date.astype(str) == "2022-07-04"].cumsum())
    plt.show()
