import taup


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




