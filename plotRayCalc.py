import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as ticker
from matplotlib import cm
import jsonpickle
from types import SimpleNamespace

plot3D='N'
plot2D='N'
mapplot='Y'
#----------------
infilename = "S2KS_S3KS_ScS.json"
with open(infilename, "r") as inf:
    mydata = jsonpickle.decode(inf.read())
    mydata = SimpleNamespace(mydata)
grid_cmb=mydata.grid_cmb
phase=mydata.phase_list
staEvtPair=mydata.staEvtPair

count_value=[]
for pt in grid_cmb:
    if pt.count>=1:
        count_value.append(pt.count)



if plot3D == 'Y':
    fig = plt.figure()
    ax = plt.figure().add_subplot(111,projection='3d')
    for pt in grid:
        # if pt.loc._cart[0]> min(cart_x) and pt.loc._cart[0]< max(cart_x):
        #     if pt.loc._cart[1]> min(cart_y) and pt.loc._cart[1]< max(cart_y):
                ax.scatter(pt.loc._cart[0],pt.loc._cart[1],pt.loc._cart[2],s=.5,alpha=.5)
    for pt in grid_cmb:
        # if pt.loc._cart[0]> min(cart_x) and pt.loc._cart[0]< max(cart_x):
        #     if pt.loc._cart[1]> min(cart_y) and pt.loc._cart[1]< max(cart_y):
                ax.scatter(pt.loc._cart[0],pt.loc._cart[1],pt.loc._cart[2],s=.5,alpha=.5,c='green')
    # #ax.plot(lat,lon,depth,label='raypath')
    ax.plot(cart_x,cart_y,cart_z)
    ax.invert_yaxis()
    plt.show()
    #plt.savefig(f'ray.png', dpi=900, bbox_inches='tight', pad_inches=0.1)
if plot2D == 'Y':
    fig,ax=plt.subplots()
    ax.plot(lon,depth)
    for pt in grid:
        if pt.loc.lon> min(lon) and pt.loc.lon< max(lon):
            plt.scatter(pt.loc.lon,0,c='blue')
    for pt in grid_cmb:
        if pt.loc.lon> min(lon) and pt.loc.lon< max(lon):
            plt.scatter(pt.loc.lon,2891,c='green')
    ax.set_xlabel("Latitude")
    ax.set_ylabel("Depth (km)")
    ax.invert_yaxis()
    plt.show()
if mapplot == 'Y':
    fig=plt.subplots()
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
    ax.add_feature(cfeature.OCEAN, color='lightblue')
    ax.add_feature(cfeature.LAND, color="oldlace")
    max_value=max(count_value)
    norm=plt.Normalize(0,max_value)
    for pt in grid_cmb:
        if pt.count >= 1: 
            print('this should be plotted') 
            #plt.scatter(pt.loc.lon,pt.loc.lat,marker='o',c='blue',s=10)
            plt.scatter(pt.loc.lon,pt.loc.lat,marker='o', s=30, c=pt.count,cmap=cm.cividis, norm=norm,transform=ccrs.PlateCarree())
    #cbar=fig.colorbar(points)
    # for pair in staEvtPair:
    #     plt.scatter(pair.evt.loc.lon,pair.evt.loc.lat,marker='*',c='yellow',s=10)
    #     plt.scatter(pair.arr.loc.lon,pair.arr.loc.lat,marker='^',c='red',s=10)
    #     for pt in pair.pierce:
    #         plt.scatter(pt.lon,pt.lat,marker='o',color='pink',s=5)
    ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
    plt.savefig('S2KS_S3KS_ScS.png', dpi=900, bbox_inches='tight', pad_inches=0.1)
    plt.show()