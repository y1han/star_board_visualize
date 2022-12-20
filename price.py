from utils import read_data_flow


class Price:
    def __init__(self, code, file_path):
        self.price_flow = read_data_flow(code=code, file_path=file_path, data_type="Stock")
