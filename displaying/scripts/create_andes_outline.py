import xarray as xr

# path of terrain elevation data 
filepath = '/Users/Tom/tmp/mount/tcarrasc/datasets/climate/RegCM4/alldom_latlongrid/border_conds/CTR_10_DOMAIN000_setgrid_lonlat.nc'

# open as xarray dataset
ds = xr.open_dataset(filepath)

# select southern Andes
topo = ds['topo'].sel(lat=slice(-80,-13)).sel(lon=slice(-90,-60))

# compute max topography
maxtopo = topo.max(dim='lon')
maxtopo = maxtopo.where(maxtopo>0, drop=True)

# filter with 6 point window
maxtopo = maxtopo.rolling(lat=6,center=True).mean()

# save as netcdf
outds = xr.Dataset({'topo': maxtopo})
outds.to_netcdf('../data/nc/andes_outline.nc')