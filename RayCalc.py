import taup
from heatmap import create_gridpoint,EQ,Station,read_stations_adept,read_earthquakes_adept,latlon_cartesian
from StaEvtGrid import PhArrEvt
import matplotlib.pyplot as plt 


stations = read_stations_adept('station.txt')
evts = read_earthquakes_adept('evt.txt')
phase = 'SKKS'
numberPoints = 1000
#---------------------------
StaEvtPair = []
for evt in evts:
    for sta in stations:
        StaEvtPair.append(PhArrEvt(sta,evt))

for pair in StaEvtPair:
    pair.get_raypath(phase)


grid=create_gridpoint(numberPoints)



fig = plt.figure()
ax = plt.figure().add_subplot(111,projection='3d')
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
            pos_dep=s.depth
            neg_dep=(s.depth*-1)
            carts=latlon_cartesian(s.lat,s.lon)
            cart_x.append(carts.x)
            cart_y.append(carts.y)
            cart_z.append(neg_dep)
#             depth.append(neg_dep)
#         print('-----------------------------')
for pt in grid:
    ax.scatter(pt.loc._cart[0],pt.loc._cart[1],pt.loc._cart[2],s=.5,alpha=.5)
# #ax.plot(lat,lon,depth,label='raypath')
ax.plot(cart_x,cart_y,cart_z)
plt.savefig(f'ray.png', dpi=900, bbox_inches='tight', pad_inches=0.1)