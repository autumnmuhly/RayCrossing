import taup
from pyproj import Geod
from heatmap import Location
import numpy as np

class PhArrEvt:
    "ArrEvt pairs with phase specific resid and differential measurements"
    def __init__(self,arr,evt):
        self.arr = arr
        self.evt = evt
    def get_raypath(self,phase):
        evtlatlon=([[self.evt.loc.lat,self.evt.loc.lon]])
        staLatLons=(self.arr.loc.lat,self.arr.loc.lon)
        with taup.TauPServer(verbose=True) as taupserver:
            params = taup.PathQuery()
            params.phase([phase])
            params.model('prem')
            params.geodetic(True)
            params.event( *evtlatlon[0] )
            params.sourcedepth(self.evt.depth)
            params.station(staLatLons[0],staLatLons[1])
            pathResult = params.calc(taupserver)
            for a in pathResult.arrivals:
                #print(f"{a.phase}   {a.sourcedepth} {a.distdeg} {a.time}  {a.desc if a.desc is not None else ''}")
                #print(a.pathSegments)
                self.path = a.pathSegments
                # if a.pathlength is not None:
                #     print(f"  Path length: {a.pathlength} km")
                # else:
                #     print("  No Path")
                for pathseg in a.pathSegments:
                    firstPoint = pathseg.segment[0]
                    lastPoint = pathseg.segment[-1]
                    #print(f"    {pathseg.name} as {pathseg.wavetype} from {firstPoint.depth} km at {firstPoint.distdeg} deg to {lastPoint.depth} km at {lastPoint.distdeg} deg takes {lastPoint.time-firstPoint.time} sec")
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



def CalcDist(p,a,b):
    "calc distance between point and line segment"
    #https://stackoverflow.com/questions/56463412/distance-from-a-point-to-a-line-segment-in-3d-python
    # print(p)
    # print(a)
    # print(b)
    p=np.array(p)
    a=np.array(a)
    b=np.array(b)
    d = np.divide(b - a, np.linalg.norm(b - a))
    print(f'this is the value of d {d}')
    s = np.dot(a - p, d)
    t = np.dot(p - b, d)
    h = np.maximum.reduce([s, t, 0])
    c = np.cross(p - a, d)
    return np.hypot(h, np.linalg.norm(c))

