import sys

# append the path of the parent directory
sys.path.append("..")
sys.path.append("../../indices/")

import xarray as xr
from processing import piseries
from readers import enso, sam, pdo
from scipy import signal

# remove linear trend from xarray time serie using scipy signal
# x: 1D xarray of coords [time]
def detrend(x):
    np_series = signal.detrend(x)
    return xr.DataArray(np_series, coords=[x.time], dims=['time'] )

# prepare series for computing correlations and saving
# return dict with monthly anomalies of selected series (possibly detrended)
def prepare_series(detrend = False):

    # load piseries
    data = {}
    data['mb'] = piseries.load_piseries_monthly()['mb']
    data['tas'] = piseries.load_piseries_monthly()['tas']
    data['pr'] = piseries.load_piseries_monthly()['pr']
    data['abl'] = piseries.load_piseries_monthly()['abl']
    data['acc'] = piseries.load_piseries_monthly()['acc']

    # load indices
    data['enso-ep'] = enso.ep_nino_index()
    data['enso-cp'] = enso.cp_nino_index()
    data['enso-nino12'] = enso.nino12_index()
    data['sam'] = sam.aaoi_index()
    data['pdo'] = pdo.pdo_index()

    # compute monthly anomalies between sel dates
    for key in data:
        data[key] = data[key].sel(time=slice('1980-04', '2015-03'))
        data[key] = data[key].groupby("time.month") - data[key].groupby("time.month").mean("time")
        data[key]['time'] = data['mb'].time
        if detrend:
            data[key] = detrend(data[key])
    
    return data

