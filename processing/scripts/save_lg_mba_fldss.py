import sys
import xarray as xr

# append the path of the parent directory
sys.path.append("..")

from processing import lgstats
from processing.utils import resampling
from prepare_series import prepare_series
from functools import partial

# get series of monthly anomalies
data = prepare_series(detrend=False)

# create series for stats
series = resampling.to_yearly_acc_values(data['mb'])

# resampling functions
res_mean = resampling.to_summer_mean_values
res_acc_acc = partial(resampling.to_summer_acc_values, from_monthly_acc=True)

output_filename = 'lg_mba_fldss.nc'

# ****************************************************
# dictionary with results
stats = dict()

# geopotential height
stats.update( lgstats.get_z_stats( series, res_mean) )

# air temperature 
stats.update( lgstats.get_t_stats( series, res_mean) )

# zonal wind
stats.update( lgstats.get_u_stats( series, res_mean) )

# meridional wind
stats.update( lgstats.get_v_stats( series, res_mean) )

# relative humidity
stats.update( lgstats.get_r_stats( series, res_mean) )

# specific humidity
stats.update( lgstats.get_q_stats( series, res_mean) )

# sea surface temperature
stats.update( lgstats.get_sst_stats( series, res_mean) )

# sea level pressure
stats.update( lgstats.get_mslp_stats( series, res_mean) )

# surface air temperature
stats.update( lgstats.get_sat_stats( series, res_mean) )

# precipitation
stats.update( lgstats.get_precip_stats( series, res_acc_acc) )

# precipitable water
stats.update( lgstats.get_pw_stats( series, res_mean) )

# olr
stats.update( lgstats.get_olr_stats( series, res_mean) )

# code snippet for sst/sat

for suf in ['corr', 'pvalue', 'regress']:
    stats['sstsat__' + suf] = xr.where( stats['sst__' + suf].notnull(), 
                                        stats['sst__' + suf],
                                        stats['t2m__' + suf])

outds = xr.Dataset(stats)
outds.to_netcdf('../data/' + output_filename)