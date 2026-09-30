import taup
from heatmap import create_gridpoint,EQ,Station,read_stations_adept,read_earthquakes_adept
from StaEvtGrid import PhArrEvt,greatcircle,get_pierce
from PointSegment import ptPierceCheck
import matplotlib.pyplot as plt 
import sys
from datetime import datetime
import jsonpickle

start = datetime.now()
stations = read_stations_adept('station.txt')
evts = read_earthquakes_adept('evt.txt')
#phase = ['SKKS','SKKKS']
phase = ['SKKS','SKKKS','ScS']
numberPoints = 40000
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

count_value=[]
for pt in grid_cmb:
    if pt.count>=1:
        print(f' this is the count {pt.count} for this point loc {pt.loc}')

mydata={"grid_cmb":grid_cmb,
        "phase_list": phase,
        "staEvtPair":staEvtPair
        }
with open('testing.json', "w") as outf:
        outf.write(jsonpickle.encode(mydata))


end=datetime.now()
print(start,end)