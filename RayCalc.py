import taup
from heatmap import create_gridpoint,EQ,Station,read_stations_adept,read_earthquakes_adept,latlon_cartesian
from StaEvtGrid import PhArrEvt,greatcircle,CalcDist
import matplotlib.pyplot as plt 
import sys


stations = read_stations_adept('station.txt')
evts = read_earthquakes_adept('evt.txt')
phase = 'SKKS'
numberPoints = 1000
plot3D='N'
plot2D='N'
#---------------------------
StaEvtPair = []
for evt in evts:
    for sta in stations:
        StaEvtPair.append(PhArrEvt(sta,evt))

for pair in StaEvtPair:
    print(pair.evt)
    print(pair.evt.depth)
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
        print('-----------------------------')
        print(seg.name)
        print(seg.segment[0])
        print(seg.segment[0].lat)
        print(seg.segment[-1])
        for s in seg.segment:
            #print(s.lat)
            #ax.scatter(s.lat,s.lon,(s.depth*-1),label='raypath',s=2)
            lat.append(s.lat)
            lon.append(s.lon)
            depth.append(s.depth)
            carts=latlon_cartesian(s.lat,s.lon)
            cart_x.append(carts.x)
            cart_y.append(carts.y)
            cart_z.append(s.depth)
distances=[]

for i in range(len(cart_x)):
    if cart_z[i] >=2880:
        print(i)
        ptA=(cart_x[i],cart_y[i],cart_z[i])
        ptB=(cart_x[i+1],cart_y[i+1],cart_z[i+1])
        if ptA != ptB:
            for pt in grid_cmb:
                point=(pt.loc._cart[0],pt.loc._cart[1],pt.loc._cart[2])
                dist=CalcDist(point,ptA,ptB)
                pt.dist2Ray=dist
                #print(f'this is the distance between the points {dist}')
                # if dist is float('nan'):
                #      print(pt.loc._cart[0],pt.loc._cart[1],pt.loc._cart[2])
                #      print(ptA,ptB)
                distances.append(dist)
min=5000
for pt in grid_cmb:
    if pt.dist2Ray < min:
        min=pt.dist2Ray
print('--------')
print(min(distances))
print(max(distances))





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

