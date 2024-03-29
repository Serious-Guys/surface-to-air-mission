import glob
import os
from datetime import datetime

import sentinel5dl
import datetime as date
from utils import format_datetime, make_dirs

AVAILABLE_PRODUCTS = {
    'Ozone'         : 'L2__O3____',
    'Aerosol'       : 'L2__Aerosol____',
    'CarbonMonoxide': 'L2__CO____',
    'NitrogenDioxide': 'L2__NO2____',
    'SulfurDioxide': 'L2__SO2____',
    'Formaldehyde': 'L2__HCHO____',
    'Glyoxal': 'L2__CHOCHO____',
    'Methane': 'L2__CH4____',
    'Cloud': 'L2__Cloud____',
    'SurfaceAlbedo': 'L2__Surface____',
    'UV': 'L2__UV____',
}


class SentinelWrapper:

    def __init__(self, dots=None, products=None, level=None, begin_datetime=None, end_datetime=None):
        if dots:
            self.set_polygon(dots)
        if level:
            self.set_processing_level(level)
        if begin_datetime:
            self.set_interval(begin_datetime, end_datetime)
        if products:
            self.set_products(products)

    def set_polygon(self, dots: list):
        self.polygon = 'POLYGON(('
        for i, (lon, lat) in enumerate(dots, start=1):
            self.polygon += f'{lon:.5f} {lat:.5f}'
            if i != len(dots):
                self.polygon += ', '
        self.polygon += '))'

    def set_interval(self, begin_datetime: date.datetime, end_datetime: date.datetime = None):
        self.begin_datetime = format_datetime(begin_datetime)

        if not end_datetime:
            end_datetime = date.datetime.fromordinal(begin_datetime.toordinal() + 1)
        else:
            self.end_datetime = end_datetime

        self.end_datetime = format_datetime(end_datetime)

    def set_products(self, products):
        self.products = []
        for product in products:
            if product in AVAILABLE_PRODUCTS.keys():
                self.products.append(AVAILABLE_PRODUCTS[product])

    def set_processing_level(self, level: int = 2):
        self.processing_level = f'L{level}'

    def assert_readiness(self):
        if self.products and self.begin_datetime and self.polygon and self.processing_level and self.end_datetime:
            return True
        print('Wrapper isn\'t ready')
        return False

    def save(self):
        if self.assert_readiness():
            base_save_dir = 'cache/sentinel/'
            rfiles = []
            for product in self.products:
                result = sentinel5dl.search(
                        polygon=self.polygon,
                        begin_ts=self.begin_datetime,
                        end_ts=self.end_datetime,
                        product=product,
                        processing_level=self.processing_level
                    )

                save_dir = base_save_dir + f"{product.strip('_')}_{self.begin_datetime[:10]}_{self.end_datetime[:10]}"

                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                else:
                    for file in glob.glob(save_dir + '/*'):
                        os.remove(file)

                sentinel5dl.download(result.get('products'), output_dir=save_dir)

                rfiles.extend(glob.glob(save_dir + '/*'))

            return rfiles


if __name__ == '__main__':
    # TODO: remove before deployment
    dots = [(11.1, 48.1), (11.1, 48.2), (11.12, 48.2), (11.2, 48.1), (11.1, 48.1)]
    products = ['CarbonMonoxide']

    begin_time_str = '2019-10-01 00:00:00.000'
    begin_df = datetime.strptime(begin_time_str, '%Y-%m-%d %H:%M:%S.%f')

    end_time_str = '2019-10-18 00:00:00.000'
    end_df = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S.%f')

    sentinel_wrapper = SentinelWrapper(dots=dots, products=products, begin_datetime=begin_df, end_datetime=end_df,
                                       level=2)
    sentinel_wrapper.save()
