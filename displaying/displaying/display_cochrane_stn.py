import matplotlib.pyplot as plt
import xarray as xr

stn_name = 'Lord Cochrane Ad.'
ds = xr.open_dataset('../data/nc/CR2ARMADA_REGCM_monthly_allvars_bajo38S.nc')
ds = ds.where(ds['nombre']==stn_name,drop=True).squeeze()
obs_pr = ds.pr.sel(time=slice('1980-01-01','2015-12-31'))
mod_pr = ds.pr_regcm.sel(time=slice('1980-01-01','2015-12-31'))

obs_pr_ann = obs_pr.resample(time='1YS').sum('time')
mod_pr_ann = mod_pr.resample(time='1YS').sum('time')

x_anom = obs_pr_ann - obs_pr_ann.mean('time')
y_anom = mod_pr_ann - mod_pr_ann.mean('time')

plt.figure()
plt.plot(x_anom.time, x_anom.values)
plt.plot(y_anom.time, y_anom.values)
plt.show()
