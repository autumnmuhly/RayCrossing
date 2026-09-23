import taup
from heatmap import create_gridpoint,EQ,Station,read_stations_adept,read_earthquakes_adept,latlon_cartesian
from StaEvtGrid import PhArrEvt,greatcircle,CalcDist
from PointSegment import PtSegCheck
import matplotlib.pyplot as plt 
import sys


stations = read_stations_adept('station.txt')
evts = read_earthquakes_adept('evt.txt')
phase = 'SKKS'
numberPoints = 40000
plot3D='N'
plot2D='N'
#---------------------------
StaEvtPair = []
for evt in evts:
    for sta in stations:
        StaEvtPair.append(PhArrEvt(sta,evt))

for pair in StaEvtPair:
    pair.get_raypath(phase)


grid=create_gridpoint(numberPoints)
grid_cmb=create_gridpoint(numberPoints,2891)

for evt in evts:
    for sta in stations:
        gcPoints=greatcircle(evt,sta)


lat=[]
lon=[]
depth=[]
cart_x=[]
cart_y=[]
cart_z=[]
for pair in StaEvtPair:
    for seg in pair.path:
        for s in seg.segment:
            lat.append(s.lat)
            lon.append(s.lon)
            depth.append(s.depth)
            carts=latlon_cartesian(s.lat,s.lon)
            cart_x.append(carts.x)
            cart_y.append(carts.y)
            cart_z.append(s.depth)


segments=PtSegCheck(cart_x,cart_y,cart_z,grid_cmb)


for pt in grid_cmb:
    pt.count=0

for seg in segments:
     for pt in grid_cmb:
        for pt_seg in seg.points_list:
            if pt_seg == pt:
                #print(f'adding one {pt}')
                pt.count=1
print('-----------')
for pt in grid_cmb:
    if pt.count == 1:
        print(pt)




if plot3D is 'Y':
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
if plot2D is 'Y':
    fix,ax=plt.subplots()
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

