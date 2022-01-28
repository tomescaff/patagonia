import sys
import pandas as pd

# append the path of the parent directory
sys.path.append("..")

from processing import extseries, piseries

time = piseries.load_piseries_monthly()['mb'].time

mon_data = dict()
mon_data['u850_pat'] = extseries.u850_pat()
mon_data['t850_pat'] = extseries.t850_pat()
mon_data['v850_pat'] = extseries.v850_pat()
mon_data['q850_pat'] = extseries.q850_pat()

mon_data['evap_pat'] = extseries.evap_pat()
mon_data['huss_pat'] = extseries.huss_pat()
mon_data['sensible_pat'] = extseries.sensible_pat()
mon_data['rsnl_pat'] = extseries.rsnl_pat()
mon_data['sst_pat'] = extseries.sst_pat()

mon_data['z300_drake'] = extseries.z300_drake()
mon_data['z500_drake'] = extseries.z500_drake()
mon_data['z700_drake'] = extseries.z700_drake()
mon_data['sst_drake'] = extseries.sst_drake()
mon_data['t700_drake'] = extseries.t700_drake()
mon_data['t850_drake'] = extseries.t700_drake()

mon_data['asl_mean'] = extseries.asl_mean()
mon_data['sst_pacsub'] = extseries.sst_pacsub()
mon_data['sst_australia'] = extseries.sst_australia()

for varname in mon_data:
    mon_data[varname] = mon_data[varname].sel(time=slice('1980-04-01', '2015-03-31'))

mon_df = pd.DataFrame()

mon_df['time'] = time

for varname in mon_data:
    mon_df[varname] = mon_data[varname]

mon_df.to_csv('../data/month_extseries.txt', sep=';', index=False, encoding='utf-8')