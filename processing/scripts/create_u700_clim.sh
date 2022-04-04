#!/bin/sh

input="/Users/Tom/tmp/mount/tcarrasc/datasets/climate/ERA_INTERIM/month/level/uwnd_1979_2014.nc"
output_level="../../displaying/data/nc/uwnd_700hPa_1979_2014.nc"
output_mon="../../displaying/data/nc/uwnd_700hPa_1980_2014.nc"
output_clim="../../displaying/data/nc/uwnd_700hPa_1980_2014_clim.nc"

cdo sellevel,700 $input $output_level
cdo seldate,1980-01-01T00:00:00,2014-12-31T23:59:59 $output_level $output_mon
cdo timmean $output_mon $output_clim