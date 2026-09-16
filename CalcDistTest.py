from StaEvtGrid import CalcDist
import matplotlib.pyplot as plt 

point=(1,0,0)
point2=(0,2,1)
linex=(0,0)
liney=(0,0)
linez=(0,2)
fig = plt.figure()
ax = plt.figure().add_subplot(111,projection='3d')
ax.scatter(point[0],point[1],point[2])
ax.scatter(point2[0],point2[1],point2[2])
ax.plot(linex,liney,linez)
plt.show()
points=(point,point2)

lineSeg=list(zip(linex,liney,linez))

dist=[]
for pt in points:
    dist.append(CalcDist(pt,lineSeg[0],lineSeg[1]))

print(dist)