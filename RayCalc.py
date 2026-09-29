import taup
from heatmap import create_gridpoint,EQ,Station,read_stations_adept,read_earthquakes_adept
from StaEvtGrid import PhArrEvt,greatcircle,get_pierce
from PointSegment import ptPierceCheck
import matplotlib.pyplot as plt 
import sys


stations = read_stations_adept('station.txt')
evts = read_earthquakes_adept('evt.txt')
phase = ['SKKS','SKKKS']
numberPoints = 40000
plot3D='N'
plot2D='N'
#---------------------------
staEvtPair = []
for evt in evts:
    for sta in stations:
        staEvtPair.append(PhArrEvt(sta,evt))
calc_staEvtPair=[]
for ph in phase:
    pair=get_pierce(staEvtPair,ph)
    for p in pair:
        calc_staEvtPair.append(p)
staEvtPair=calc_staEvtPair
print('constructing grid')
grid=create_gridpoint(numberPoints)
grid_cmb=create_gridpoint(numberPoints,2891)
points_list=[]

for pt in grid_cmb:
     pt.count=0
print(staEvtPair)
for pair in staEvtPair:
    print(pair.phase,pair.arr.loc, pair.pierce)
    for p in pair.pierce:
        closest_point=ptPierceCheck(p.lat,p.lon,p.depth,grid_cmb)
        for pt in grid_cmb:
             if closest_point==pt:
                print('-------')
                print(pair.arr.loc)
                print(pair.evt.time)
                print(pt.loc)
                pt.count+=1


for pt in grid_cmb:
    if pt.count>=1:
        print(f' this is the count {pt.count} for this point loc {pt.loc}')






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

