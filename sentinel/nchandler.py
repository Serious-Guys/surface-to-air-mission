import numpy as np
import netCDF4 as nc4

DEFAULT_KEYS = {'scanline', 'ground_pixel', 'time', 'corner', 'latitude', 'longitude', 'delta_time', 'time_utc',
                'qa_value', 'layer', 'level'}


class NC4Handler:

    def __init__(self, filename):
        fh = nc4.Dataset(filename, mode='r')
        keys = set(fh.groups['PRODUCT'].variables.keys())
        new_keys = list(keys - DEFAULT_KEYS)

        key_val, key_pres = '', ''
        for new_key in new_keys:
            if 'precision' in new_key.split('_'):
                key_pres = new_key
                break

        for new_key in new_keys:
            if len(new_key) != len(key_pres) and new_key == key_pres[:len(new_key)]:
                key_val = new_key
                break

        self._lons = np.array(fh.groups['PRODUCT'].variables['longitude'][:][0, :, :])
        self._lats = np.array(fh.groups['PRODUCT'].variables['latitude'][:][0, :, :])

        self._vals = np.array(fh.groups['PRODUCT'].variables[key_val][:][0, :, :])
        self._vals_pres = np.array(fh.groups['PRODUCT'].variables[key_pres][:][0, :, :])

        self._vals_units = fh.groups['PRODUCT'].variables[key_val].units
        self._vals_pres_units = fh.groups['PRODUCT'].variables[key_pres].units

    @property
    def lons(self) -> np.ndarray:
        return self._lons

    @property
    def lats(self) -> np.ndarray:
        return self.lats

    @property
    def vals(self) -> np.ndarray:
        return self._vals

    @property
    def vals_pres(self) -> np.ndarray:
        return self._vals_pres

    @staticmethod
    def load_files(filenames):
        return [NC4Handler(filename) for filename in filenames]

    @staticmethod
    def load_file(filename):
        return NC4Handler(filename)


if __name__ == '__main__':
    # TODO: remove before deployment
    handler = NC4Handler('./cache/sentinel/L2__CO_2019-10-01_2019-10-18/'
                         'S5P_NRTI_L2__CO_____20191017T105303_20191017T105803_10414_01_010302_20191017T125829.nc')
