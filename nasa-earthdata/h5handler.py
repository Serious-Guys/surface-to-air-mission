import h5py
import numpy as np


class h5Handler:
    def __init__(self, filename):
        h5file = h5py.File(filename, 'r')
        swaths = h5file['HDFEOS']['SWATHS']
        swaths_keys = list(h5file['HDFEOS']['SWATHS'].keys())
        data_item = swaths[swaths_keys[0]]
        self.data = data_item['Data Fields']
        self.geolocation = data_item['Geolocation Fields']

    def get_data_keys(self) -> list:
        return list(self.data.keys())

    def get_geolocation_keys(self) -> list:
        return list(self.geolocation.keys())

    def get_data_by_key(self, key: str) -> np.ndarray:
        return self.data[key][()]

    def get_geolocation_by_key(self, key: str) -> np.ndarray:
        return self.geolocation[key][()]

    def get_data_all(self) -> dict:
        result = {}
        for key in self.get_data_keys():
            result[key] = self.get_data_by_key(key)
        return result

    def get_geolocation_all(self) -> dict:
        result = {}
        for key in self.get_geolocation_keys():
            result[key] = self.get_geolocation_by_key(key)
        return result


if __name__ == '__main__':
    # TODO: remove before deploying
    hander = h5Handler('cache/nasa-earthdata/CarbonMonoxide/MOP02R-20191004.25-L2V18.2.1.he5')
