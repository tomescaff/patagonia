import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import os
from shapely.geometry.polygon import LinearRing

def eraint_indices(list_of_dicts, outname='../data/png/display_regions.png', printed=False):

    fig = plt.figure(figsize=(11,6))
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=280))
    ax.set_global()
    ax.set_ylim([-90, 30])
    ax.coastlines(linewidth=0.5)
    ax.set_xticks([0, 60, 120, 180, 240, 300, 360], crs=ccrs.PlateCarree())
    ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    
    plt.grid(linewidth=0.3, color='gray', linestyle='--')
    ax.outline_patch.set_linewidth(0.4)

    for d in list_of_dicts:
        minlat=d['coords']['latmin']
        maxlat=d['coords']['latmax']
        minlon=d['coords']['lonmin']
        maxlon=d['coords']['lonmax']
        lons = [minlon, minlon, maxlon, maxlon]
        lats = [minlat, maxlat, maxlat, minlat]
        ring = LinearRing(list(zip(lons, lats)))
        ax.add_geometries([ring], ccrs.PlateCarree(central_longitude=0), **d['args'])
     
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
    ax.set_ylim([-90, 30])
    plt.tight_layout()
    if printed:
        plt.savefig(outname,dpi=300)
        os.system('/usr/local/bin/convert -trim '+outname + ' '+ outname )

if __name__=='__main__':   

    AAOI   = dict(zip(['latmin','latmax','lonmin','lonmax'], [-90,-20,-260,99.9]))
    NINO4  = dict(zip(['latmin','latmax','lonmin','lonmax'], [-5,5,-200,-150]))
    NINO3  = dict(zip(['latmin','latmax','lonmin','lonmax'], [-5,5,-150,-90]))
    NINO34 = dict(zip(['latmin','latmax','lonmin','lonmax'], [-5,5,-170,-120]))
    NINO12 = dict(zip(['latmin','latmax','lonmin','lonmax'], [-10,-0,-90,-80]))
    DRAKE  = dict(zip(['latmin','latmax','lonmin','lonmax'], [-68,-53,-100,-60]))
    AMUND  = dict(zip(['latmin','latmax','lonmin','lonmax'], [-75,-60,-150,-100]))
    PACPAT = dict(zip(['latmin','latmax','lonmin','lonmax'], [-52,-46,-80,-76]))
    FJIORD = dict(zip(['latmin','latmax','lonmin','lonmax'], [-52,-46,-75.5,-74.5]))
    
    eraint_indices([
        dict(coords=NINO3,  args=dict(facecolor='green',  edgecolor='green',alpha=0.2)),
        dict(coords=NINO4,  args=dict(facecolor='purple', edgecolor='purple',alpha=0.2)),
        dict(coords=NINO34, args=dict(facecolor='none',   edgecolor='black',lw=0.5)),
        dict(coords=NINO12, args=dict(facecolor='r',   edgecolor='r', alpha=0.2)),
        dict(coords=FJIORD, args=dict(facecolor='none',   edgecolor='r')),
        dict(coords=PACPAT, args=dict(facecolor='none',   edgecolor='blue')),
        dict(coords=AMUND,  args=dict(facecolor='b',   edgecolor='b',alpha=0.2)),
        dict(coords=DRAKE,  args=dict(facecolor='lightgrey', edgecolor='black', alpha=0.4)),
        dict(coords=AAOI,   args=dict(facecolor='none',   edgecolor='black', ls='--', lw=0.5))
        ], printed=True)