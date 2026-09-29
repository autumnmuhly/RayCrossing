import taup
from pyproj import Geod
from heatmap import Location
import numpy as np
import math


class PhArrEvt:
    "Phase Array Event pairs"
    def __init__(self,arr,evt):
        self.arr = arr
        self.evt = evt
    def get_pierce(self,phase):
        evtlatlon=([[self.evt.loc.lat,self.evt.loc.lon]])
        staLatLons=(self.arr.loc.lat,self.arr.loc.lon)
        pierce=[]
        with taup.TauPServer(verbose=True) as taupserver:
            params = taup.PierceQuery()
            params.phase([phase])
            params.model('prem')
            params.geodetic(True)
            params.event( *evtlatlon[0] )
            params.sourcedepth(self.evt.depth)
            params.station(staLatLons[0],staLatLons[1])
            pierceResult = params.calc(taupserver)
            print('--------')
            print(pierceResult)
            #print(pathResult.arrivals)
            for a in pierceResult.arrivals:
                for td in a.pierce:
                    if td.depth == 2891:
                        pierce.append(td)
            self.pierce=pierce
                # if a.puristdist >=180 and a.puristdist<=360:
                #     print('this is major arc')
        return

def greatcircle(pt1,pt2):
    points=[]
    "return lat and lon for greatcircle path between two points"
    g=Geod(ellps='clrk66')
    (az12, az21, dist) = g.inv(pt1.loc.lon,pt1.loc.lat,pt2.loc.lon,pt2.loc.lat)
    npts=int(dist/1000)
    lonlats=g.npts(pt1.loc.lon,pt1.loc.lat,pt2.loc.lon,pt2.loc.lat, 1 + int(dist / 1000))
    lonlats=[(pt1.loc.lon,pt1.loc.lat),*lonlats,(pt2.loc.lon,pt2.loc.lat)]
    for pair in lonlats:
        points.append(Location(pair[1],pair[0]))
    return points



def calcDistSeg(p,a,b):
    "calc distance between point and line segment"
    #https://stackoverflow.com/questions/56463412/distance-from-a-point-to-a-line-segment-in-3d-python
    # print(p)
    # print(a)
    # print(b)
    p=np.array(p)
    a=np.array(a)
    b=np.array(b)
    d = np.divide(b - a, np.linalg.norm(b - a))
    #print(f'this is the value of d {d}')
    s = np.dot(a - p, d)
    t = np.dot(p - b, d)
    h = np.maximum.reduce([s, t, 0])
    c = np.cross(p - a, d)
    return np.hypot(h, np.linalg.norm(c))

def calcDistPt(p1,p2):
    dx=(p2[0]-p1.x)**2
    dy=(p2[1]-p1.y)**2
    dz=(p2[2]-p1.z)**2
    d=math.sqrt(dx+dy+dz)
    return d