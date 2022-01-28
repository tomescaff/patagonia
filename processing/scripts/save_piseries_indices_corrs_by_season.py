import pandas as pd
from scipy import stats
from prepare_series import prepare_series

# input section
# this section defines the seasons (for x and y) and the init and end year to be considered
input = {}

# DJF section
input['djf'] = {}
input['djf']['season_x'] = [12, 1, 2]
input['djf']['season_y_list'] = [[12, 1, 2], [1, 2 ,3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7], [6, 7, 8]]
input['djf']['ini_year_list'] = ['1980-12', '1980-12', '1980-12', '1980-12', '1980-12', '1980-12', '1980-12'] 
input['djf']['end_year_list'] = ['2015-03', '2015-03', '2014-11', '2014-11', '2014-11', '2014-11', '2014-11']

# MAM section
input['mam'] = {}
input['mam']['season_x'] = [3, 4, 5]
input['mam']['season_y_list'] = [[3, 4, 5], [4, 5 ,6], [5, 6, 7], [6, 7, 8], [7, 8, 9], [8, 9, 10], [9, 10, 11]]
input['mam']['ini_year_list'] = ['1981-03', '1981-03', '1981-03', '1981-03', '1981-03', '1981-03', '1981-03'] 
input['mam']['end_year_list'] = ['2015-02', '2015-02', '2015-02', '2015-02', '2015-02', '2015-02', '2015-02']

# JJA section
input['jja'] = {}
input['jja']['season_x'] = [6, 7, 8]
input['jja']['season_y_list'] = [[6, 7, 8], [7, 8 ,9], [8, 9, 10], [9, 10, 11], [10, 11, 12], [11, 12, 1], [12, 1, 2]]
input['jja']['ini_year_list'] = ['1980-06', '1980-06', '1980-06', '1980-06', '1980-06', '1980-06', '1980-06'] 
input['jja']['end_year_list'] = ['2015-03', '2015-03', '2015-03', '2015-03', '2015-03', '2015-03', '2015-03']

# SON section
input['son'] = {}
input['son']['season_x'] = [9, 10, 11]
input['son']['season_y_list'] = [[9, 10, 11], [10, 11 , 12], [11, 12, 1], [12, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5]]
input['son']['ini_year_list'] = ['1980-09', '1980-09', '1980-09', '1980-09', '1980-09', '1980-09', '1980-09'] 
input['son']['end_year_list'] = ['2015-03', '2015-03', '2015-03', '2015-03', '2015-03', '2014-08', '2014-08']

# A-S section
input['a-s'] = {}
input['a-s']['season_x'] = [4, 5, 6, 7, 8, 9]
input['a-s']['season_y_list'] = [[4, 5, 6, 7, 8, 9], [5, 6, 7, 8, 9, 10], [6, 7, 8, 9, 10, 11], [7, 8, 9, 10, 11, 12], [8, 9, 10, 11, 12, 1], [9, 10, 11, 12, 1, 2], [10, 11, 12, 1, 2, 3]]
input['a-s']['ini_year_list'] = ['1980-04', '1980-04', '1980-04', '1980-04', '1980-04', '1980-04', '1980-04'] 
input['a-s']['end_year_list'] = ['2015-03', '2015-03', '2015-03', '2015-03', '2015-03', '2015-03', '2015-03']

# O-M section
input['o-m'] = {}
input['o-m']['season_x'] = [10, 11, 12, 1, 2, 3]
input['o-m']['season_y_list'] = [[10, 11, 12, 1, 2, 3], [11, 12, 1, 2, 3, 4], [12, 1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6], [2, 3, 4, 5, 6, 7], [3, 4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 9]]
input['o-m']['ini_year_list'] = ['1980-10', '1980-10', '1980-10', '1980-10', '1980-10', '1980-10', '1980-10'] 
input['o-m']['end_year_list'] = ['2015-03', '2014-09', '2014-09', '2014-09', '2014-09', '2014-09', '2014-09']

# year section
input['yea'] = {}
input['yea']['season_x'] = [(x-1)%12 +1 for x in range(4, 4+12)]
input['yea']['season_y_list'] = [[(x-1)%12 +1 for x in range(4+y, 4+y+12)] for y in range(0,7)]
input['yea']['ini_year_list'] = ['1980-04', '1980-04', '1980-04', '1980-04', '1980-04', '1980-04', '1980-04'] 
input['yea']['end_year_list'] = ['2015-03', '2014-04', '2014-05', '2014-06', '2014-07', '2014-08', '2014-09']

# compute the lagged-correlation between x_data (at season_x) and y_data (ar seasons in season_y_list)
# resolution can be 'month' to stay in monthly resolution or 'season', if you want to resample to series of seasonly averages.
def correlation_by_season(x_data, y_data, season_x, season_y_list, ini_year_list, end_year_list, resolution='month', remove_serie=None):
    
    # define list for storing lagged corr
    r_list = []
    p_list = []
    for season_y, ini_year, end_year in zip(season_y_list, ini_year_list, end_year_list):

        # compute x and y time series from init and end year and seasons
        x_period = x_data.sel(time=slice(ini_year, end_year))
        y_period = y_data.sel(time=slice(ini_year, end_year))
        x = x_period.sel(time=x_period.time.dt.month.isin(season_x))
        y = y_period.sel(time=y_period.time.dt.month.isin(season_y))

        # to seasonly data values
        if resolution == 'season':
            x = x.resample(time = f'{len(season_x)}MS').mean('time').dropna('time')
            y = y.resample(time = f'{len(season_x)}MS').mean('time').dropna('time')

        # for removing one series from x data values (e.g. removing sam from enso)
        if remove_serie is not None:
            z_period = remove_serie.sel(time=slice(ini_year, end_year))
            z = z_period.sel(time=z_period.time.dt.month.isin(season_x))
            if resolution == 'season':
                z = z.resample(time = f'{len(season_x)}MS').mean('time').dropna('time')
            res = stats.linregress(z, x)
            x = x - (res.slope*z + res.intercept)

        # compute r statistics and store in list
        r, p = stats.pearsonr(x.values, y.values)
        r_list.append(r)
        p_list.append(p)
    return r_list, p_list

# create table of lagged-correlation filtered by season at season resolution from
# series of monthly anomalies
def create_dataframes(x_data, y_data, input):

    # define tables as empty dataframes
    seas_r_df = pd.DataFrame()
    seas_p_df = pd.DataFrame()

    # lag ranges from 0 to 6
    seas_r_df['lag'] = list(range(0,7))
    seas_p_df['lag'] = list(range(0,7))

    for seas in input:

        # compute lagged-correlations (a column of a table)
        rs, ps = correlation_by_season( x_data, 
                                        y_data, 
                                        input[seas]['season_x'], 
                                        input[seas]['season_y_list'], 
                                        input[seas]['ini_year_list'], 
                                        input[seas]['end_year_list'],
                                        'season',
                                        None)
        seas_r_df[seas] = rs
        seas_p_df[seas] = ps
    return seas_r_df, seas_p_df

# create and save seasonal correlation tables between serie of monthly anomalies (x and y)
# filtered by season. Print tables to files in markdown format. 
def save_correlation_table(x, y, filepath_r, filepath_p):

    # create and compute lagged-corr tables as dataframes
    seas_r_df, seas_p_df = create_dataframes(x, y, input)

    # fill table with 2 decimal precision
    for key in input:
        seas_r_df[key] = seas_r_df[key].apply(lambda x: round(x, 2))
        seas_p_df[key] = seas_p_df[key].apply(lambda x: round(x, 2))

    # start markdown conversion

    # colour significative correlations. 
    # if p < 0.05: r is red 
    # if 0.05 <= p < 0.1: r is blue.
    n, m = seas_r_df.shape
    for i in range(n):
        for j in range(1,m):
            if seas_p_df.iloc[i,j] < 0.05:
                seas_r_df.iloc[i,j] = '<span style="color: red">'+str(seas_r_df.iloc[i,j])+'</span>'
            if 0.05 <= seas_p_df.iloc[i,j] < 0.1:
                seas_r_df.iloc[i,j] = '<span style="color: blue">'+str(seas_r_df.iloc[i,j])+'</span>'

    # save r table
    with open(filepath_r, 'w') as f:
        print(seas_r_df.to_markdown(), file=f)
    # save p table
    with open(filepath_p, 'w') as f:
        print(seas_p_df.to_markdown(), file=f)

if __name__=='__main__':
    # define runs for creating and saving corr tables
    runs = [
        ['enso-ep', 'mb', 'corr_seas_ensoep_mb'],
        ['enso-ep', 'tas', 'corr_seas_ensoep_tas'],
        ['enso-ep', 'pr', 'corr_seas_ensoep_pr'],

        ['enso-cp', 'mb', 'corr_seas_ensocp_mb'],
        ['enso-cp', 'tas', 'corr_seas_ensocp_tas'],
        ['enso-cp', 'pr', 'corr_seas_ensocp_pr'],

        ['enso-nino12', 'mb', 'corr_seas_enso12_mb'],
        ['enso-nino12', 'tas', 'corr_seas_enso12_tas'],
        ['enso-nino12', 'pr', 'corr_seas_enso12_pr'],

        ['sam', 'mb', 'corr_seas_sam_mb'],
        ['sam', 'tas', 'corr_seas_sam_tas'],
        ['sam', 'pr', 'corr_seas_sam_pr'],

        ['pdo', 'mb', 'corr_seas_pdo_mb'],
        ['pdo', 'tas', 'corr_seas_pdo_tas'],
        ['pdo', 'pr', 'corr_seas_pdo_pr'],

        ['enso-ep', 'sam', 'corr_seas_ensoep_sam'],
        ['enso-cp', 'sam', 'corr_seas_ensocp_sam'],

        ['enso-ep', 'enso-ep', 'corr_seas_ensoep_ensoep'],
        ['sam', 'sam', 'corr_seas_sam_sam'],

        ['enso-ep', 'abl', 'corr_seas_ensoep_abl'],
        ['enso-ep', 'acc', 'corr_seas_ensoep_acc'],
    ]

    # get series of monthly anomalies
    data = prepare_series(detrend=False)

    # create and save tables
    for run in runs:
        save_correlation_table(data[run[0]], data[run[1]], '../data/corr_seas/'+run[2]+'_rval.md', '../data/corr_seas/'+run[2]+'_pval.md')
        