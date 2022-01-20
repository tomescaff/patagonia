import sys

# append the path of the parent directory
sys.path.append("..")

from processing import piseries

mb_monthly = piseries.monthly_series('mb')
mb_yearly = piseries.yearly_series('mb')