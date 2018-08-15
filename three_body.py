# -*- coding:UTF-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D 
from matplotlib import animation
from random import *

pos1x=[]
pos1y=[]
pos1z=[]
pos2x=[]
pos2y=[]
pos2z=[]
pos3x=[]
pos3y=[]
pos3z=[]
t=0.1

class star:
   
    def __init__(self,mass=10,x=0,y=0,z=0,vx=0,vy=0,vz=0,ax=0,ay=0,az=0):
        self.mass=mass
        self.x=x
        self.y=y
        self.z=z
        self.vx=vx
        self.vy=vy
        self.vz=vz
        self.ax=ax
        self.ay=ay
        self.az=az

    def trace(self):
        self.x+=t*self.vx
        self.y+=t*self.vy
        self.z+=t*self.vz
        return self.x, self.y, self.z

    def speed(self):
        self.vx-=t*self.ax
        self.vy-=t*self.ay
        self.vz-=t*self.az
        return self.vx, self.vy, self.vz

    def force(self,m1,x1,y1,z1,m2,x2,y2,z2):
        s1=(self.x-x1)**2+(self.y-y1)**2+(self.z-z1)**2
        s2=(self.x-x2)**2+(self.y-y2)**2+(self.z-z2)**2
        af1=100*float(m1)/s1
        af2=100*float(m2)/s2
        self.ax=af1*(self.x-x1)/np.sqrt(s1)+af2*(self.x-x2)/np.sqrt(s2)
        self.ay=af1*(self.y-y1)/np.sqrt(s1)+af2*(self.y-y2)/np.sqrt(s2)
        self.az=af1*(self.z-z1)/np.sqrt(s1)+af2*(self.z-z2)/np.sqrt(s2)
        return self.ax, self.ay, self.az

star1=star()
star2=star()
star3=star()

def initial():
    global star1
    global star2
    global star3

    t=np.random.randint(5,100,3)
    star1.mass=t[0]
    star2.mass=t[1]
    star3.mass=t[2]

    t=np.random.randint(-50,50,9)
    while True:
        if(t[0]==t[3]):
           t[0]+=1
        elif(t[0]==t[6]):
           t[0]+=1
        elif(t[3]==t[6]):
           t[3]+=1
        if((t[0]!=t[3])and(t[3]!=t[6])and(t[0]!=t[6])):
           break

    star1.x,star1.y,star1.z=t[0:3]
    star2.x,star2.y,star2.z=t[3:6]
    star3.x,star3.y,star3.z=t[6:9]

    t=np.random.uniform(-4,4,6)
    star1.vx,star1.vy,star1.vz=t[0:3]
    star2.vx,star2.vy,star2.vz=t[3:6]
    star3.vx=-(star1.mass*star1.vx+star2.mass*star2.vx)/star3.mass
    star3.vy=-(star1.mass*star1.vy+star2.mass*star2.vy)/star3.mass
    star3.vz=-(star1.mass*star1.vz+star2.mass*star2.vz)/star3.mass

    star1.ax,star1.ay,star1.az = star1.force(star2.mass,star2.x,star2.y,star2.z,star3.mass,star3.x,star3.y,star3.z)
    star2.ax,star2.ay,star2.az = star2.force(star1.mass,star1.x,star1.y,star1.z,star3.mass,star3.x,star3.y,star3.z)
    star3.ax,star3.ay,star3.az = star3.force(star2.mass,star2.x,star2.y,star2.z,star1.mass,star1.x,star1.y,star1.z)

initial()
#print star1.mass,star1.x,star1.vx,star1.ax,star1.ay,star1.az
#print pos1,pos2,pos3

def crush():
    if((abs(star1.x-star2.x)<0.1)and(abs(star1.y-star2.y)<0.1)and(abs(star1.z-star2.z)<0.2)):
        return 1
    if((abs(star1.x-star3.x)<0.1)and(abs(star1.y-star3.y)<0.1)and(abs(star1.z-star3.z)<0.2)):
        return 2
    if((abs(star3.x-star2.x)<0.1)and(abs(star3.y-star2.y)<0.1)and(abs(star3.z-star2.z)<0.2)):
        return 3
    return 0

fig = plt.figure()
ax=Axes3D(fig)

t1=ax.scatter(pos1x,pos1y,pos1z)
t2=ax.scatter(pos2x,pos2y,pos2z)
t3=ax.scatter(pos3x,pos3y,pos3z)
t0=[t1,t2,t3]


def run():

    global star1
    global star2
    global star3

    c=crush()
    if(c==0):

        pos1x.append(star1.x)
        pos1y.append(star1.y)
        pos1z.append(star1.z)
        pos2x.append(star2.x)
        pos2y.append(star2.y)
        pos2z.append(star2.z)
        pos3x.append(star3.x)
        pos3y.append(star3.y)
        pos3z.append(star3.z)

        star1.ax,star1.ay,star1.az = star1.force(star2.mass,star2.x,star2.y,star2.z,star3.mass,star3.x,star3.y,star3.z)
        star2.ax,star2.ay,star2.az = star2.force(star1.mass,star1.x,star1.y,star1.z,star3.mass,star3.x,star3.y,star3.z)
        star3.ax,star3.ay,star3.az = star3.force(star2.mass,star2.x,star2.y,star2.z,star1.mass,star1.x,star1.y,star1.z)

        star1.vx,star1.vy,star1.vz = star1.speed()
        star2.vx,star2.vy,star2.vz = star2.speed()
        star3.vx,star3.vy,star3.vz = star3.speed()

        star1.x,star1.y,star1.z = star1.trace()
        star2.x,star2.y,star2.z = star2.trace()
        star3.x,star3.y,star3.z = star3.trace()

    return t0

n=1000
for i in range(n):
    run()

ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)
ax.set_zlim(-100, 100)


def run2(frame):
    t1=ax.plot(pos1x[:frame],pos1y[:frame],pos1z[:frame],c='red')[0]
    t2=ax.plot(pos2x[:frame],pos2y[:frame],pos2z[:frame],c='green')[0]
    t3=ax.plot(pos3x[:frame],pos3y[:frame],pos3z[:frame],c='blue')[0]
    t0=[t1,t2,t3]
    return t0

print (star1.mass,"red")
print (star1.x,star1.y,star1.z)
print (star1.vx,star1.vy,star1.vz)
print (star2.mass,"green")
print (star2.x,star2.y,star2.z)
print (star2.vx,star2.vy,star2.vz)
print (star3.mass,"blue")
print (star3.x,star3.y,star3.z)
print (star3.vx,star3.vy,star3.vz)

anim = animation.FuncAnimation(fig, run2, frames=n, interval=20, blit=True)
plt.show()




