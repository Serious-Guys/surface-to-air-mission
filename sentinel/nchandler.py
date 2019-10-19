import netCDF4 as nc4

DEFFAULT_KEYS = {'scanline', 'ground_pixel', 'time', 'corner', 'latitude', 'longitude', 'delta_time', 'time_utc', 'qa_value', 'layer', 'level'}


class NC4Handler:

    def __init__(self, filename):
        fh = nc4.Dataset(filename, mode='r')
        keys = set(fh.groups['PRODUCT'].variables.keys())
        new_keys = list(keys - DEFFAULT_KEYS)

        key_val, key_pres = '', ''
        for new_key in new_keys:
            if 'precision' in new_key.split('_'):
                key_pres = new_key
                break

        for new_key in new_keys:
            if len(new_key) != len(key_pres) and new_key == key_pres[:len(new_key)]:
                key_val = new_key
                break

        self.lons = fh.groups['PRODUCT'].variables['longitude'][:][0, :, :]
        self.lats = fh.groups['PRODUCT'].variables['latitude'][:][0, :, :]

        self.vals = fh.groups['PRODUCT'].variables[key_val][:][0, :, :]
        self.vals_pres = fh.groups['PRODUCT'].variables[key_pres][:][0, :, :]

        self.vals_units = fh.groups['PRODUCT'].variables[key_val].units
        self.vals_pres_units = fh.groups['PRODUCT'].variables[key_pres].units

    @staticmethod
    def load_files(filenames):
        return [NC4Handler(filename) for filename in filenames]

    @staticmethod
    def load_file(filename):
        return NC4Handler(filename)
