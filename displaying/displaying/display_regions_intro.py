import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import os
from shapely.geometry.polygon import LinearRing
import xarray as xr
import numpy as np
import glob
import fiona 
import shapely
from shapely.ops import cascaded_union
from cartopy.io.shapereader import Reader

printed = True
outname = '../data/png/display_regions_intro.png'

def get_npi_shapes(basins=False):
    filepath = "../data/shapes/randolph/icefields/randolph_NPI.shp"
    shapes = []
    with fiona.open(filepath) as source:
        for feature in source:
            shp = shapely.geometry.shape(feature['geometry'])
            shapes.append(shp)
    shapes = cascaded_union(shapes) if not basins else shapes
    return shapes

def get_spi_shapes(basins=False):
    filepath = "../data/shapes/randolph/icefields/randolph_SPI.shp"
    shapes = []
    with fiona.open(filepath) as source:
        for feature in source:
            shp = shapely.geometry.shape(feature['geometry'])
            shapes.append(shp)
    shapes = cascaded_union(shapes) if not basins else shapes
    return shapes

def makegrid_from_curvilinear_fromlonlat(lon,lat):
    
    
    n,m = lon.shape
    
    llon = np.zeros((n+1,m+1))
    llat = np.zeros((n+1,m+1))
    
    llon[:n,1:m] = (lon[:,1:]+lon[:,:-1])/2.0
    
    #for i in range(0,n+1):
    #    for j in range(1,m):
    #        llon[i,j] = (lon[i,j-1]+lon[i,j])/2.0
            
    llon[:n,0] = lon[:,0]-(llon[:n,1]-lon[:,0])
    llon[:n,m] = lon[:,m-1]+(llon[:n,m-1]-lon[:,m-2])
    
    llon[n,:] = llon[n-1,:]
    
    llat[1:n,:m] = (lat[1:,:]+lat[:-1,:])/2.0
    
    #for j in range(0,m+1):
    #    for i in range(1,n):
    #        llat[i,j] = (lat[i,j]+lat[i-1,j])/2.0
    
    llat[0,:m] = lat[0,:] - (llat[1,:m]-lat[0,:])
    llat[n,:m] = lat[n-1,:] + (lat[n-1,:]-llat[n-1,:m])    
    
    llat[:,m] = llat[:,m-1]
    
    return llon,llat

fig = plt.figure(figsize=(11,6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_global()
ax.set_ylim([-85, -10])
ax.set_xlim([-135, -44])
# ax.coastlines(linewidth=0.5)
ax.set_xticks([ -130, -115, -100, -85, -70, -55], crs=ccrs.PlateCarree())
ax.set_yticks([ -75, -60, -45, -30, -15], crs=ccrs.PlateCarree())
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)

plt.grid(linewidth=0.3, color='gray', linestyle='--')
ax.outline_patch.set_linewidth(0.4)

resol = '50m'  
land = cfeature.NaturalEarthFeature('physical', 'land',  scale=resol, edgecolor='k', facecolor=cfeature.COLORS['land'])#'lightgrey')#
ocean = cfeature.NaturalEarthFeature('physical', 'ocean', scale=resol, edgecolor='none', facecolor=cfeature.COLORS['water'])#'whitesmoke')#

ax.add_feature(land, linewidth=0.5, alpha=0.5)
ax.add_feature(ocean, alpha = 0.5)

ds = xr.open_dataset('../data/nc/uwnd_700hPa_1980_2014_clim.nc')
u = ds['u'].squeeze()

ax.contourf(u.longitude, u.latitude, u.values, levels=[11, u.values.max()], linewidths=0.5, colors=['blue'], extend='max', alpha=0.3)
ax.contourf(u.longitude, u.latitude, u.values, levels=[12.5, u.values.max()], linewidths=0.5, colors=['blue'], extend='max', alpha=0.3)

ds = xr.open_dataset('../data/nc/mslp_1980_2015_clim.nc')
slp = ds['msl'].squeeze()*0.01

cslp = ax.contourf(slp.longitude, slp.latitude, slp.values, levels=[1020, slp.values.max()], colors=['brown', 'brown'], extend='max', alpha=0.3)

######
minlat=-56.2
maxlat=-39.2
minlon=-77.2
maxlon=-65.0
lons = [minlon, minlon, maxlon, maxlon]
lats = [minlat, maxlat, maxlat, minlat]
ring = LinearRing(list(zip(lons, lats)))
ax.add_geometries([ring], ccrs.PlateCarree(central_longitude=0), facecolor='none',   edgecolor='k', linewidth=0.8)
#######
basedir = '/Users/Tom/tmp/mount/tcarrasc/datasets/climate/RegCM4/alldom_latlongrid/month/pr/*.nc'
filepath = glob.glob(basedir)[0]
datest = xr.open_dataset(filepath)['pr'].mean('time')
datest = datest*0
n,m = datest.values.shape

mat = datest.values

matrix = np.zeros((n,m))*np.nan

for i in range(n):
    found = False
    for j in range(m):
        if np.isnan(mat[i,j]):
            continue
        else:
            matrix[i,j]=1
            matrix[i,j+1]=1
            matrix[i,j+2]=1
            break
        
for j in range(m):
    found = False
    for i in range(n):
        if np.isnan(mat[i,j]):
            continue
        else:
            matrix[i,j]=1
            matrix[i+1,j]=1
            matrix[i+2,j]=1
            break
        
for j in range(m):
    found = False
    for i in reversed(range(n)):
        if np.isnan(mat[i,j]):
            continue
        else:
            matrix[i,j]=1
            matrix[i-1,j]=1
            matrix[i-2,j]=1
            break
        
for i in range(n):
    found = False
    for j in reversed(range(m)):
        if np.isnan(mat[i,j]):
            continue
        else:
            matrix[i,j]=1
            matrix[i,j-1]=1
            matrix[i,j-2]=1
            break
datest[:,:] = matrix

dllon,dllat=np.meshgrid(datest.lon,datest.lat)
llon,llat = makegrid_from_curvilinear_fromlonlat(dllon,dllat)
im0 = ax.pcolormesh(llon,llat,datest.values,transform=ccrs.PlateCarree(),cmap='bwr',alpha=0.8,zorder=100,vmin=0,vmax=1)#, vmin=vmin,vmax=vmax)





########
fglacier_npi  = "../data/shapes/glims/NPI_shape.shp"
fglacier_spi  = "../data/shapes/glims/SPI_shape.shp"
#ax.add_feature(cfeature.ShapelyFeature(Reader(fglacier_npi).geometries(),crs=ccrs.PlateCarree()),linewidth=0.1,edgecolor='k',facecolor='deepskyblue',alpha=1)
#ax.add_feature(cfeature.ShapelyFeature(Reader(fglacier_spi).geometries(),crs=ccrs.PlateCarree()),linewidth=0.1,edgecolor='k',facecolor='deepskyblue',alpha=1)
ax.add_feature(cfeature.ShapelyFeature(get_npi_shapes(),crs=ccrs.PlateCarree()),linewidth=0.1,edgecolor='k',facecolor='deepskyblue',alpha=1)
ax.add_feature(cfeature.ShapelyFeature(get_spi_shapes(),crs=ccrs.PlateCarree()),linewidth=0.1,edgecolor='k',facecolor='deepskyblue',alpha=1)
   

ax.set_ylabel('')
ax.set_xlabel('')
    
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(10) 
    tick.label.set_fontname('Arial')
    tick.label.set_weight('light') 
    
for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(10) 
    tick.label.set_fontname('Arial')
    tick.label.set_weight('light')
plt.tight_layout()

if printed:
    plt.savefig(outname,dpi=300)
    os.system('/usr/local/bin/convert -trim '+outname + ' '+ outname )

else:
    plt.show()