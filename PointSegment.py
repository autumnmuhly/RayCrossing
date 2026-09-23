from StaEvtGrid import CalcDist
class LineSegment:
    "ArrEvt pairs with phase specific resid and differential measurements"
    def __init__(self,pt1,pt2):
        self.pt1 = pt1
        self.pt2 = pt2

def PtSegCheck(cart_x,cart_y,cart_z,grid):
    segments=[]
    for i in range(len(cart_z)):
        distances=[]
        if cart_z[i] >=2880:
            ptA=(cart_x[i],cart_y[i],cart_z[i])
            ptB=(cart_x[i+1],cart_y[i+1],cart_z[i+1])
            segments.append(LineSegment(ptA,ptB))
    for seg in segments:
        seg.points_list=[]
        if seg.pt1 != seg.pt2:
            closet_point=None
            closest_distance=10000
            for pt in grid:
                point=(pt.loc._cart[0],pt.loc._cart[1],pt.loc._cart[2])
                dist=CalcDist(point,seg.pt1,seg.pt2)
                if dist<closest_distance:
                    closet_point=pt
                    closest_distance=dist
            seg.points_list.append(closet_point)
    return segments