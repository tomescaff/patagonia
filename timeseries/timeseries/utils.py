import xarray as xr
import numpy as np
from scipy import stats

# compute the Pearson's r coefficient between x and y along time dimension
# valid for 1D xarrays of same shape
# TODO: check it for ND xarrays
def correlation_1D_1D_time(x, y):
    
    anom_xy = (x-x.mean(dim='time'))*(y-y.mean(dim='time'))
    anom_xx = (x-x.mean(dim='time'))**2
    anom_yy = (y-y.mean(dim='time'))**2
    
    corr = anom_xy.sum('time')/np.sqrt(anom_xx.sum('time',skipna=False)*anom_yy.sum('time',skipna=False))
    return corr

# compute the Pearson's r coefficient between x and y along first dimension
# x: 3D numpy array of shape [t, n, m] 
# y: 1D numpy array of shape [t]
def correlation_3D_1D(x, y):
    t, n, m = x.shape

    # init empty matrix 
    matrix = np.zeros((n, m))
    
    # fill matrix with correlations
    for i in range(n):
        for j in range(m):
            # handle case with nans
            if np.isnan(x[:,i,j]).all() or np.isnan(y[:,i,j]).all():
                matrix[i,j] = np.nan
            # handle case with singular value
            elif (x[:,i,j]==x[0,i,j]).all() or (y[:,i,j]==y[0,i,j]).all():
                matrix[i,j] = np.nan
            # get correlation using numpy
            else:
                matrix[i,j] = np.corrcoef(x[:,i,j],y[:,i,j])[0,1]
    
    return matrix

# compute the Pearson's r coefficient between x and y along time dimension
# x: 3D xarray of coords [time, lat, lon]
# y: 1D xarray of coords [time]
def correlation_3D_1D_time_lat_lon(x, y):
    # get lat and lon
    lat = x.lat
    lon = x.lon
    
    # create xarray object with data and return
    data = correlation_3D_1D(x.values, y.values)
    da = xr.DataArray(data, coords=[lat,lon], dims=['lat', 'lon'])
    return da

# compute the Pearson's r coefficient between x and y along time dimension
# x: 3D xarray of coords [time, lat, lon]
# y: 1D xarray of coords [time]
def correlation_3D_1D_time_lat_lon(x, y):
    # get lat and lon
    lat = x.lat
    level = x.level
    
    # create xarray object with data and return
    data = correlation_3D_1D(x.values, y.values)
    da = xr.DataArray(data, coords=[level,lat], dims=['level', 'lat'])
    return da
