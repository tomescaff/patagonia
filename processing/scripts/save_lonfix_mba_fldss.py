import sys
import xarray as xr

# append the path of the parent directory
sys.path.append("..")

from processing import lonfixstats
from processing.utils import resampling
from prepare_series import prepare_series

# get series of monthly anomalies
data = prepare_series(detrend=False)

# create series for stats
series = resampling.to_yearly_acc_values(data['mb'])
series = (series-series.mean('time'))/series.std('time')

# define longitude for transect
sel_lon = -80.0

# resampling functions
res_mean = resampling.to_summer_mean_values

output_filename = 'lonfix_80w_mba_fldss.nc'

# ****************************************************
# dictionary with results
stats = dict()

# geopotential height
stats.update( lonfixstats.get_z_stats( series, res_mean, sel_lon) )

# air temperature 
stats.update( lonfixstats.get_t_stats( series, res_mean, sel_lon) )

# zonal wind
stats.update( lonfixstats.get_u_stats( series, res_mean, sel_lon) )

# meridional wind
stats.update( lonfixstats.get_v_stats( series, res_mean, sel_lon) )

# vertical wind
stats.update( lonfixstats.get_w_stats( series, res_mean, sel_lon) )

# relative humidity
stats.update( lonfixstats.get_r_stats( series, res_mean, sel_lon) )

# specific humidity
stats.update( lonfixstats.get_q_stats( series, res_mean, sel_lon) )

outds = xr.Dataset(stats)
outds.to_netcdf('../data/nc/' + output_filename)