import sys
import pandas as pd

# append the path of the parent directory
sys.path.append("..")

from processing import piseries

varnames = ['mb', 'pr', 'acc', 'abl', 'tas', 'rsds']

mon_data = {varname:piseries.monthly_series(varname, 'spi') for varname in varnames}
yea_data = {varname:piseries.yearly_series( varname, 'spi') for varname in varnames}

mon_df = pd.DataFrame()
yea_df = pd.DataFrame()

mon_df['time'] = mon_data['mb'].time
yea_df['time'] = yea_data['mb'].time

for varname in varnames:
    mon_df[varname] = mon_data[varname]
    yea_df[varname] = yea_data[varname]


mon_df.to_csv('../data/month_piseries_spi.txt', sep=';', index=False, encoding='utf-8')
yea_df.to_csv('../data/year_piseries_spi.txt', sep=';', index=False, encoding='utf-8')