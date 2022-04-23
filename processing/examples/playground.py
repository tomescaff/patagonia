import sys
import numpy as np
import pandas as pd
import xarray as xr
from scipy import stats
# append the path of the parent directory
sys.path.append("..")

from processing import piseries
from processing.utils import resampling

mon_data = piseries.load_piseries_monthly()

sys.path.append("../../indices/")

from readers import enso, sam

enso_data = enso.ep_nino_index()
sam_data = sam.aaoi_index()

mon_data = mon_data.sel(time=slice('1980-04', '2015-03'))
enso_data = enso_data.sel(time=slice('1980-04', '2015-03'))
sam_data = sam_data.sel(time=slice('1980-04', '2015-03'))

mb_data = mon_data['mb']
pr_data = mon_data['pr']

# mb_summer = resampling.to_summer_acc_values(mb_data)
# pr_summer = resampling.to_summer_acc_values(pr_data)

# print(stats.pearsonr(mb_summer, pr_summer))

# mb_winter = resampling.to_winter_acc_values(mb_data)
# pr_winter = resampling.to_winter_acc_values(pr_data)

# print(stats.pearsonr(mb_winter, pr_winter))

mb_annual = resampling.to_yearly_acc_values(mon_data['mb'], from_monthly_acc=True)
pr_annual = resampling.to_yearly_acc_values(mon_data['pr'], from_monthly_acc=True)
acc_annual = resampling.to_yearly_acc_values(mon_data['acc'], from_monthly_acc=True)
abl_annual = resampling.to_yearly_acc_values(mon_data['abl'], from_monthly_acc=True)
tas_annual = resampling.to_yearly_mean_values(mon_data['tas'])
rsds_annual = resampling.to_yearly_mean_values(mon_data['rsds'])

mb_winter = resampling.to_winter_acc_values(mon_data['mb'], from_monthly_acc=True)
pr_winter = resampling.to_winter_acc_values(mon_data['pr'], from_monthly_acc=True)
acc_winter = resampling.to_winter_acc_values(mon_data['acc'], from_monthly_acc=True)
abl_winter = resampling.to_winter_acc_values(mon_data['abl'], from_monthly_acc=True)
tas_winter = resampling.to_winter_mean_values(mon_data['tas'])
rsds_winter = resampling.to_winter_mean_values(mon_data['rsds'])

mb_summer = resampling.to_summer_acc_values(mon_data['mb'], from_monthly_acc=True)
pr_summer = resampling.to_summer_acc_values(mon_data['pr'], from_monthly_acc=True)
acc_summer = resampling.to_summer_acc_values(mon_data['acc'], from_monthly_acc=True)
abl_summer = resampling.to_summer_acc_values(mon_data['abl'], from_monthly_acc=True)
tas_summer = resampling.to_summer_mean_values(mon_data['tas'])
rsds_summer = resampling.to_summer_mean_values(mon_data['rsds'])
    
    
f=lambda x: (x.mean(), x.std())