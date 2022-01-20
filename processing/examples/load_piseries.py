import sys

# append the path of the parent directory
sys.path.append("..")

from processing import piseries

mon_data = piseries.load_piseries_monthly()
yea_data = piseries.load_piseries_yearly()