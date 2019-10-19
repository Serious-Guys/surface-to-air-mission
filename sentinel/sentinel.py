# from sentinel5dl import search, download
# import netCDF4 as ncd
#
# # Search for Sentinel-5 products
result = search(
        polygon='POLYGON((7.8 49.3,13.4 49.3,13.4 52.8,7.8 52.8,7.8 49.3))',
        begin_ts='2019-09-01T00:00:00.000Z',
        end_ts='2019-09-17T23:59:59.999Z',
        product='L2__CO____',
        processing_level='L2')
#
# # Download found products to the local folder
# download(result.get('products'))

import netCDF4 as nc4
filename = '/home/fux/projects/surface-to-air-mission/cache/sentinel/L2__O3_2019-09-15_2019-09-16/S5P_OFFL_L2__O3_____20190915T095314_20190915T113443_09960_01_010107_20190921T122755.nc'
fh = nc4.Dataset(filename, mode='r')
keys = fh.groups['PRODUCT'].variables.keys()
print(keys)
lons = fh.groups['PRODUCT'].variables['longitude'][:][0,:,:]
lats = fh.groups['PRODUCT'].variables['latitude'][:][0,:,:]
no2 = fh.groups['PRODUCT'].variables['ozone_total_vertical_column_precision'][0,:,:]
print (lons.shape)
print (lats.shape)
print (no2.shape)


no2_units = fh.groups['PRODUCT'].variables['ozone_total_vertical_column_precision'].units


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
from mpl_toolkits.basemap import Basemap
lon_0 = lons.mean()
lat_0 = lats.mean()
m = Basemap(width=5000000,height=3500000,
            resolution='l',projection='stere',\
            lat_ts=40,lat_0=lat_0,lon_0=lon_0)

xi, yi = m(lons, lats)

# Plot Data
cs = m.pcolor(xi,yi,np.squeeze(no2),norm=LogNorm(), cmap='jet')

# Add Grid Lines
m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

# Add Coastlines, States, and Country Boundaries
m.drawcoastlines()
m.drawstates()
m.drawcountries()

# Add Colorbar
cbar = m.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(no2_units)

# Add Title
plt.title('NO2 in atmosphere')
plt.show()
pass