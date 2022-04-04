#!/bin/sh

input="/Users/Tom/tmp/mount/tcarrasc/datasets/climate/ERA_INTERIM/month/surface/mslp_1979_2017.nc"

output_mon="../../displaying/data/nc/mslp_1980_2015.nc"
output_clim="../../displaying/data/nc/mslp_1980_2015_clim.nc"

cdo seldate,1980-01-01T00:00:00,2015-12-31T23:59:59 $input $output_mon
cdo timmean $output_mon $output_clim