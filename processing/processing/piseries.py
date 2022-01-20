from .settings import *
from .utils import icefields, resampling
from os.path import join

# return monthly timeseries of modeled variables over icefield (npi, spi, or both)
def monthly_series(varname, icefield='both'):
    # check valid varnames
    assert varname in ['mb', 'acc', 'abl', 'tas', 'pr', 'rsds']
    # define filepath to model results
    npi = join(NPI_MODEL_RESULTS_ROOT, NPI_MODEL_RESULT_FILE)
    spi = join(SPI_MODEL_RESULTS_ROOT, SPI_MODEL_RESULT_FILE)
    # get monthly series and resample if necessary
    series = icefields.monthly_series(npi, spi, varname, icefield)
    if varname in ['mb', 'acc', 'abl', 'pr']:
        series = resampling.to_monthly_acc_values(series)
    return series

# return yearly timeseries of modeled variables over icefield (npi, spi, or both)
def yearly_series(varname, icefield='both'):
    # check valid varnames
    assert varname in ['mb', 'acc', 'abl', 'tas', 'pr', 'rsds']
    # define filepath to model results
    npi = join(NPI_MODEL_RESULTS_ROOT, NPI_MODEL_RESULT_FILE)
    spi = join(SPI_MODEL_RESULTS_ROOT, SPI_MODEL_RESULT_FILE)
    # get yearly series and resample if necessary
    series = icefields.monthly_series(npi, spi, varname, icefield)
    if varname in ['mb', 'acc', 'abl', 'pr']:
        series = resampling.to_yearly_acc_values(series)
    else:
        series = resampling.to_yearly_mean_values(series)
    return series


