import sys
import numpy as np
import pandas as pd
import xarray as xr
from scipy import stats
# append the path of the parent directory
sys.path.append("..")

from processing import piseries

mon_data = piseries.load_piseries_monthly()

sys.path.append("../../indices/")

from readers import enso, sam

enso_data = enso.ep_nino_index()
sam_data = sam.aaoi_index()

mon_data = mon_data.sel(time=slice('1980-04', '2015-03'))
enso_data = enso_data.sel(time=slice('1980-04', '2015-03'))
sam_data = sam_data.sel(time=slice('1980-04', '2015-03'))

mb_data = mon_data.mb.groupby("time.month") - mon_data.mb.groupby("time.month").mean("time")
enso_data = enso_data.groupby("time.month") - enso_data.groupby("time.month").mean("time")
sam_data = sam_data.groupby("time.month") - sam_data.groupby("time.month").mean("time")

enso_data['time'] = mb_data.time

# months = [10,11,12,1,2,3]#[4,5,6,7,8,9]#
# mb_data = mb_data.sel(time=mb_data.time.dt.month.isin(months)).rolling(time=len(months), center=True).mean().dropna("time")[::len(months)]
# enso_data = enso_data.sel(time=enso_data.time.dt.month.isin(months)).rolling(time=len(months), center=True).mean().dropna("time")[::len(months)]
# sam_data = sam_data.sel(time=sam_data.time.dt.month.isin(months)).rolling(time=len(months), center=True).mean().dropna("time")[::len(months)]

# print('enso-sam', stats.pearsonr(enso_data, sam_data))
# print('enso-mb', stats.pearsonr(enso_data, mb_data))
# print('mb-sam', stats.pearsonr(mb_data, sam_data))
# for time in range(3,12*35):
#     mb = mb_data.rolling(time=time, center=True).mean().dropna("time")
#     enso = enso_data.rolling(time=time, center=True).mean().dropna("time")
#     r = stats.pearsonr(mb, enso)
#     print(r)

# for init in range(1,12):
#     mb = mb_data.rolling(time=12, center=True).sum().dropna("time")[init::12]
#     enso = enso_data.rolling(time=12, center=True).mean().dropna("time")[:-init:12]
#     r = stats.pearsonr(mb, enso)
#     print(init, r)

# lag=1
# mb = mb_data.rolling(time=11, center=True).mean().dropna("time")[lag:]
# enso = enso_data.rolling(time=11, center=True).mean().dropna("time")[:-lag]
# r = stats.pearsonr(mb, enso)
# print(r)

# months = [12,1,2]#[4,5,6,7,8,9]#
# lag=2
# mb_data = mb_data[11:-1].sel(time=mb_data[11:-1].time.dt.month.isin([(x+lag)%12+1 for x in months]))#.rolling(time=len(months), center=True).mean().dropna("time")[::len(months)]
# enso_data = enso_data[:-11].sel(time=enso_data[:-11].time.dt.month.isin(months))#.rolling(time=len(months), center=True).mean().dropna("time")[::len(months)]
# sam_data = sam_data[:-11].sel(time=sam_data[:-11].time.dt.month.isin(months))#.rolling(time=len(months), center=True).mean().dropna("time")[::len(months)]



# print('enso-sam', stats.pearsonr(enso_data, sam_data))
# print('enso-mb', stats.pearsonr(enso_data, mb_data))
# print('mb-sam', stats.pearsonr(mb_data, sam_data))

# 1.1 ENSO-MB corr intermensual filtrando por mes
# -6 -5 -4 -3 -2 -1 0 +1 +2 +3 +4 +5 +6 
# J
# F
# M
# A
# M
# J
# J
# A
# S
# O
# N
# D
# 1.2 SAM-MB corr intermensual filtrando por mes
# 1.3 ENSO-SAM corr intermensual filtrando por mes

# 2.1 ENSO-MB corr intermensual filtrando por estacion
# -6 -5 -4 -3 -2 -1 0 +1 +2 +3 +4 +5 +6
# DJF
# MAM
# JJA
# SON
# A-S
# O-M
# 2.2 SAM-MB corr intermensual filtrando por mes
# 2.3 ENSO-SAM corr intermensual filtrando por mes


# 3.1 ENSO-MB corr interestacional seleccionando por estacion
# -6 -5 -4 -3 -2 -1 0 +1 +2 +3 +4 +5 +6
# DJF
# MAM
# JJA
# SON
# A-S
# O-M
# 3.2 SAM-MB corr interestacional seleccionando por estacion
# 3.3 ENSO-SAM corr interestacional seleccionando por estacion

# 4.1 ENSO-MB corr interanual 
# -6 -5 -4 -3 -2 -1 0 +1 +2 +3 +4 +5 +6
# J-D
# F-J
# M-F 
# A-M
# M-A
# J-M
# J-J
# A-J
# S-A
# O-S
# N-O
# D-N
# 4.2 SAM-MB corr interestacional seleccionando por estacion
# 4.3 ENSO-SAM corr interestacional seleccionando por estacion

x = enso_data
y = mb_data
month=4
lag = -2
mon_end = (month+lag-1)%12+1
yea_off = (month+lag-1)//12
if month >= 4:
    init_year = 1980
    end_year = 2014
else:
    init_year = 1981
    end_year = 2015
dr_a = pd.date_range(f'{init_year}-{month}-01',f'{end_year}-{month}-01', freq='12MS')
dr_b = pd.date_range(f'{init_year+yea_off}-{mon_end}-01',f'{end_year+yea_off}-{mon_end}-01', freq='12MS')
#validar

dummy = np.zeros((35,))
time_a = xr.DataArray(dummy, coords=[dr_a], dims=['time'])
time_b = xr.DataArray(dummy, coords=[dr_b], dims=['time'])

if lag >= 0:
    time_b = time_b.sel(time=slice('1980-04-01', '2015-03-31')) 
    time_a = time_a[:time_b.size:]
else:
    time_b = time_b.sel(time=slice('1980-04-01', '2015-03-31'))
    time_a = time_a[-time_b.size::]
    
x = x.sel(time = time_a.time)
y = y.sel(time = time_b.time)
    
    
