from typing import List, Dict

import h5py
import numpy as np


data_cols = {
    'CarbonMonoxide': ['APrioriCOTotalColumn', 'RetrievedCOTotalColumn'],
    'Ozone': ['APrioriLayerO3', 'SO2index', 'ColumnAmountO3', 'SO2index', 'UVAerosolIndex'],
    'AerosolIndex': ['AIRSL3COvalue', 'FinalAerosolAbsOpticalDepth', 'FinalAerosolLayerHeight',
                     'FinalAerosolOpticalDepth', 'FinalAerosolSingleScattAlb', 'UVAerosolIndex']
}

geolocation_data = ['Latitude', 'Longitude', 'Time']


class h5Handler:
    def __init__(self, filename: str, dataset: str):
        h5file = h5py.File(filename, 'r')
        swaths = h5file['HDFEOS']['SWATHS']
        swaths_keys = list(h5file['HDFEOS']['SWATHS'].keys())
        data_item = swaths[swaths_keys[0]]

        self._data_fields = data_item['Data Fields']
        self._geolocation_data = data_item['Geolocation Fields']

        self._data = dict()

        for col in data_cols[dataset]:
            self._data[col] = self._data_fields[col].value

        for col in geolocation_data:
            self._data[col] = self._geolocation_data[col].value

    def get_data_keys(self) -> list:
        return list(self._data.keys())

    def get_geolocation_keys(self) -> list:
        return list(self.geolocation.keys())

    def get_data_by_key(self, key: str) -> np.ndarray:
        return self._data[key][()]

    def get_geolocation_by_key(self, key: str) -> np.ndarray:
        return self.geolocation[key][()]

    @property
    def data(self) -> Dict:
        return self._data

    def get_geolocation_all(self) -> dict:
        result = {}
        for key in self.get_geolocation_keys():
            result[key] = self.get_geolocation_by_key(key)
        return result
