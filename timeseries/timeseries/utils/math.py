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
# x: 3D xarray of coords [time, level, lat]
# y: 1D xarray of coords [time]
def correlation_3D_1D_time_level_lat(x, y):
    # get lat and level
    lat = x.lat
    level = x.level
    
    # create xarray object with data and return
    data = correlation_3D_1D(x.values, y.values)
    da = xr.DataArray(data, coords=[level,lat], dims=['level', 'lat'])
    return da

# compute the Pearson's r coefficient (and p-value) between x and s along time dimension
# x: 4D xarray of coords [time, level, lat, lon]
# y: 1D xarray of coords [time]
def correlation_4D_1D_time_level_lat_lon(x, s):
    # get level, lat and lon
    level = x.level
    lat = x.lat
    lon = x.lon
    
    x = x.values
    s = s.values
    
    t, l, n, m = x.shape

    # init empty matrix for reg and pvalue
    matrix = np.zeros((l, n, m))
    matrix_pvalue = np.zeros((l, n, m))
    
    # fill matrix using scipy.stats pearsonr
    for i in range(l):
        for j in range(n):
            for k in range(m):
                r,p = stats.pearsonr(s,x[:,i,j,k])
                matrix[i,j,k] = r
                matrix_pvalue[i,j,k] = p
    
    # create xarray object with data and return
    da_correl = xr.DataArray(matrix, coords=[level, lat,lon], dims=['level', 'lat', 'lon'])
    da_pvalue = xr.DataArray(matrix_pvalue, coords=[level,lat,lon], dims=['level', 'lat', 'lon'])
    
    return da_correl, da_pvalue

# compute the regression between x and s along time dimension
# x: 3D xarray of coords [time, lat, lon]
# y: 1D xarray of coords [time]
def regressmap_3D_1D_time_lat_lon(x, s):
    # get lat and lon
    lat = x.lat
    lon = x.lon
    
    x = x.values
    s = s.values
    
    t, n, m = x.shape

    # init empty matrix for reg and pvalue
    matrix = np.zeros((n, m))
    matrix_pvalue = np.zeros((n, m))
    
    # fill matrix using scipy.stats linregress
    for i in range(n):
        for j in range(m):
            model = stats.linregress(s,x[:,i,j])
            matrix[i,j] = model.slope
            matrix_pvalue[i,j] = model.pvalue
    
    # create xarray object with data and return
    da_regres = xr.DataArray(matrix, coords=[lat,lon], dims=['lat', 'lon'])
    da_pvalue = xr.DataArray(matrix_pvalue, coords=[lat,lon], dims=['lat', 'lon'])
    return da_regres, da_pvalue

# compute the regression between x and s along time dimension
# x: 3D xarray of coords [time, level, lat]
# y: 1D xarray of coords [time]
def regress_3D_1D_map_level_lat(x, s):
    # get level and lat
    level = x.level
    lat = x.lat
    
    x = x.values
    s = s.values
    
    t, n, m = x.shape

    # init empty matrix for reg and pvalue
    matrix = np.zeros((n, m))
    matrix_pvalue = np.zeros((n, m))
    
    # fill matrix using scipy.stats linregress
    for i in range(n):
        for j in range(m):
            model = stats.linregress(s,x[:,i,j])
            matrix[i,j] = model.slope
            matrix_pvalue[i,j] = model.pvalue
    
    # create xarray object with data and return
    da_regres = xr.DataArray(matrix, coords=[level,lat], dims=['level', 'lat'])
    da_pvalue = xr.DataArray(matrix_pvalue, coords=[level,lat], dims=['level', 'lat'])
    
    return da_regres, da_pvalue

# compute the regression between x and s along time dimension
# x: 4D xarray of coords [time, level, lat, lon]
# y: 1D xarray of coords [time]
def regressmap_4D_1D_time_level_lat_lon(x, s):
    # get level, lat and lon
    level = x.level
    lat = x.lat
    lon = x.lon
    
    x = x.values
    s = s.values
    
    t, l, n, m = x.shape

    # init empty matrix for reg and pvalue
    matrix = np.zeros((l, n, m))
    matrix_pvalue = np.zeros((l, n, m))
    
    # fill matrix using scipy.stats linregress
    for i in range(l):
        for j in range(n):
            for k in range(m):
                model = stats.linregress(s,x[:,i,j,k])
                matrix[i,j,k] = model.slope
                matrix_pvalue[i,j,k] = model.pvalue
    
    # create xarray object with data and return
    da_regres = xr.DataArray(matrix, coords=[level, lat,lon], dims=['level','lat', 'lon'])
    da_pvalue = xr.DataArray(matrix_pvalue, coords=[level,lat,lon], dims=['level','lat', 'lon'])
    
    return da_regres, da_pvalue



