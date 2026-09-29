from StaEvtGrid import calcDistPt
from heatmap import latlon_cartesian
class LineSegment:
    "ArrEvt pairs with phase specific resid and differential measurements"
    def __init__(self,pt1,pt2):
        self.pt1 = pt1
        self.pt2 = pt2

def ptPierceCheck(lat1,lon1,depth1,grid):
    cart1=latlon_cartesian(lat1,lon1,depth1)
    closet_point=None
    closest_distance=10000
    for pt in grid:
        point=(pt.loc._cart[0],pt.loc._cart[1],pt.loc._cart[2])
        dist=calcDistPt(cart1,point)
        if dist<closest_distance:
            closet_point=pt
            closest_distance=dist
    return closet_point