from utils import read_data_flow


class Order:
    def __init__(self, code, file_path):
        self.order_flow = read_data_flow(code=code, file_path=file_path, data_type="Order")
