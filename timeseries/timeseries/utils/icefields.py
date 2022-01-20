import xarray as xr
import numpy as np
from scipy import stats
from os.path import join
from ..settings import *

# compute lat-lon average on both icefields at the same time
def average_icefields_data(npi_dataarray, spi_dataarray):
    
    # reshape arrays for averaging
    x = npi_dataarray.values
    m2d_npi = np.moveaxis(x,0,-1).reshape((-1,x.shape[0]))
    
    y = spi_dataarray.values
    m2d_spi = np.moveaxis(y,0,-1).reshape((-1,y.shape[0]))
    
    m2d = np.concatenate((m2d_npi,m2d_spi),axis=0)

    # compute average
    data = np.nanmean(m2d,axis=0)

    # create and return xarray with timeseries
    time = npi_dataarray.time
    return xr.DataArray(data, coords=[time], dims=['time'])

# return monthly series of varname from icefield (npi, spi or both)
# units are: [tas: C], [rsds: Wm2], [mb, pr, acc, abl: mm/day]
# monthly values correspond to monthly mean values of data with 3H resolution
def monthly_series(filename_npi, filename_spi, varname, icefield):
    
    basedir=dict()
    basedir['npi'] = join(NPI_MODEL_RESULTS_ROOT, filename_npi)
    basedir['spi'] = join(SPI_MODEL_RESULTS_ROOT, filename_spi)
    
    # declare topography dictionaries
    # topo_real_full={}
    # topo_model={}
    topo_real={}
    
    # npi topography data
    # topo_real_full['npi'] = xr.open_dataset(NPI_TOPO_ROOT+'npi_dem_from_pat5x5ave_full.nc')['z'].values
    # topo_model['npi'] = xr.open_dataset(NPI_TOPO_ROOT+'topo.nc')['topo_model'].values
    topo_real['npi'] = xr.open_dataset(join(NPI_TOPO_ROOT, 'topo.nc'))['topo_real'].values
    
    # spi topography data
    # topo_real_full['spi'] = xr.open_dataset(SPI_TOPO_ROOT+'spi_dem_from_pat5x5ave_full.nc')['z'].values
    # topo_model['spi'] = xr.open_dataset(SPI_TOPO_ROOT+'topo.nc')['topo_model'].values
    topo_real['spi'] = xr.open_dataset(join(SPI_TOPO_ROOT, 'topo.nc'))['topo_real'].values
    
    # declare data dictionaries
    icefield_var={}
    icefield_var_masked={}

    # load data from both icefields
    for icefield_name in ['npi','spi']:
        # load full data from icefield
        icefield_var[icefield_name] = xr.open_dataset(basedir[icefield_name])[varname]

        # transform units
        if varname == 'tas':
            icefield_var[icefield_name] = icefield_var[icefield_name] - 273.15
        if varname in ['pr','mb','abl','acc']:
            icefield_var[icefield_name] = icefield_var[icefield_name] * 8.0

        # mask with topography
        icefield_var_masked[icefield_name] = icefield_var[icefield_name]+topo_real[icefield_name]*0
    
    # if only one icefield is needed, return lat-lon average
    if icefield in ['npi','spi']:
        ans = icefield_var_masked[icefield].mean(['lat','lon'])
    # if both icefields are needed, join data
    else:
        ans = average_icefields_data(icefield_var_masked['npi'],icefield_var_masked['spi'])
    return ans