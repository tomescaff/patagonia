import sys

# append the path of the parent directory
sys.path.append("..")

from processing import extseries

ext = extseries.load_extseries_monthly()