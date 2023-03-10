from matplotlib import pyplot as plt
from pygame import Vector3, Vector2
from math import  *
import numpy as np
import matplotlib
from Utils import *
import multiprocessing as mp
matplotlib.rcParams['animation.ffmpeg_path'] = "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe"



class ABCD:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    def __repr__(self) -> str:
        return f"ABCD({round(self.a,5)}, {round(self.b,5)}, {round(self.c,5)}, {round(self.d,5)})"

class BowlingBall:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    MaxY = 1.064
    MaxX = 18.288
    MinX = -0.01
    MinY = -0.01
    Gravity = 9.8
    Mass = 7
    Radius = 0.1085
    MomentsOfInertia = Vector3(0.031, 0.033, 0.033)
    oil_length = feet2meter(42)
    noOil_k_friction = 0.2
    oil_k_friction = 0.04
    k_friction = noOil_k_friction
    s_friction = 0.2
    r0 = Vector3(0, 0.001, 0)
    TimeStep = 0.0001
    Graph_sample_interval = 100
    isAnimated = False
    # def __init__(self,revangle:int=0,throwangle:int=0, startpos:float=1/2,rev:float=30):
    def __init__(self,**kwargs):
        
        """Initializes BowlingBall class

        Args:
            revangle (float, optional): sets the angle of angular velocity to x degrees left of the y axis. Defaults to 0.
            throwangle (float, optional): angle that the velocity starts at. Defaults to 0.
            startpos (float, optional): percentage of . Defaults to 1/2.
            rev (float, optional): _description_. Defaults to 30.
        """
        self.ax.plot([meter2feet(self.oil_length) for i in range(0,40)],[i for i in range(0,40)],color="black",alpha=0.5)
        self.ax.grid(color="black",alpha=0.5)
        
        self.ax.set_title("Bowling Ball Trajectory")
        self.ax.set_xticks(np.arange(0,60+1,1))
        self.Running = False
        self._Rolling = False
        self.Time = 0
        self.position = Vector2(0, self.MaxY*kwargs.get("startpos",1/2))
        self.velocity = Vector2(8, 0).rotate(kwargs.get("throwangle",0))
        self.acceleration = Vector2(0, 0)
        angle = radians(kwargs.get("revangle",0))
        rev = kwargs.get("rev",30)
        self.angularVelocity = Vector3(-rev*sin(angle), rev*cos(angle), 0)
        # self.angularVelocity = Vector3(0, 30, 0)
        
        self.angularAcceleration = Vector3(0, 0, 0)
        
        # Change orientation of ball
        self.lmnX = Vector3(-0.966, 0.259, 0)
        self.lmnY = Vector3(0.259, 0.966, 0)
        self.lmnZ = Vector3(0, 0, 1)
        
        
        self.theta = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.r = Vector3(0, 0.001, 0)
        
        self.abcd1 = ABCD(0, 0, 0, 0)
        self.abcd2 = ABCD(0, 0, 0, 0)
        self.abcd3 = ABCD(0, 0, 0, 0)
        self.forces = Vector2(0, 0)
        self.N = 0
        self._r_factor = 0
        self._mag = Vector3(0, 0, 0)
        self._Vp = Vector2(0, 0)
        self._VpMag = 0
        self._RollingPositions = [[],[]]
        self._notRollingPositions = [[],[]]
        self._wasRolling = []
        self._maxStaticFrictionMinusActual = 0
        self._breakPointX = 0
        self._lowestY = 100
        self._hookFromBreakPoint = 0
        self._breakPointTime = 0
    


    def run(self):
        self.Running = True
        while self.Running:
            
            if self.position.x > self.oil_length:
                self.k_friction = self.noOil_k_friction
            else:
                self.k_friction = self.oil_k_friction
            if self._lowestY > self.position.y:
                self._lowestY = self.position.y
                self._breakPointX = self.position.x
                self._breakPointTime = (len(self._notRollingPositions[0])//100)
            
            self.update()
            self.Time = round(self.Time + self.TimeStep,4)
        
        



    def update(self):
        if self.Time > 0:
            
            # Update r factor
            self._r_factor = (sqrt((self.r.x+self.TimeStep*(self.angularVelocity.y*self.r.z-self.angularVelocity.z*self.r.y))**2+(self.r.y-self.TimeStep*(self.angularVelocity.x*self.r.z-self.angularVelocity.z*self.r.x))**2+(self.r.z+self.TimeStep*(self.angularVelocity.x*self.r.y-self.angularVelocity.y*self.r.x))**2))/sqrt((self.r0.x)**2+(self.r0.y)**2+(self.r0.z)**2)
            self._mag.x = sqrt((self.lmnX.x+self.TimeStep*(self.angularVelocity.y*self.lmnX.z-self.angularVelocity.z*self.lmnX.y))**2+(self.lmnX.y-self.TimeStep*(self.angularVelocity.x*self.lmnX.z-self.angularVelocity.z*self.lmnX.x))**2+(self.lmnX.z+self.TimeStep*(self.angularVelocity.x*self.lmnX.y-self.angularVelocity.y*self.lmnX.x))**2)
            self._mag.y = sqrt((self.lmnY.x+self.TimeStep*(self.angularVelocity.y*self.lmnY.z-self.angularVelocity.z*self.lmnY.y))**2+(self.lmnY.y-self.TimeStep*(self.angularVelocity.x*self.lmnY.z-self.angularVelocity.z*self.lmnY.x))**2+(self.lmnY.z+self.TimeStep*(self.angularVelocity.x*self.lmnY.y-self.angularVelocity.y*self.lmnY.x))**2)
            self._mag.z = sqrt((self.lmnZ.x+self.TimeStep*(self.angularVelocity.y*self.lmnZ.z-self.angularVelocity.z*self.lmnZ.y))**2+(self.lmnZ.y-self.TimeStep*(self.angularVelocity.x*self.lmnZ.z-self.angularVelocity.z*self.lmnZ.x))**2+(self.lmnZ.z+self.TimeStep*(self.angularVelocity.x*self.lmnZ.y-self.angularVelocity.y*self.lmnZ.x))**2)
            # lmn Updates After initial time step
            self.lmnX.x = (self.lmnX.x+self.TimeStep*(self.angularVelocity.y*self.lmnX.z-self.angularVelocity.z*self.lmnX.y))/self._mag.x
            self.lmnX.y = (self.lmnX.y-self.TimeStep*(self.angularVelocity.x*self.lmnX.z-self.angularVelocity.z*self.lmnX.x))/self._mag.x
            self.lmnX.z = (self.lmnX.z+self.TimeStep*(self.angularVelocity.x*self.lmnX.y-self.angularVelocity.y*self.lmnX.x))/self._mag.x

            self.lmnY.x = (self.lmnY.x+self.TimeStep*(self.angularVelocity.y*self.lmnY.z-self.angularVelocity.z*self.lmnY.y))/self._mag.y
            self.lmnY.y = (self.lmnY.y-self.TimeStep*(self.angularVelocity.x*self.lmnY.z-self.angularVelocity.z*self.lmnY.x))/self._mag.y
            self.lmnY.z = (self.lmnY.z+self.TimeStep*(self.angularVelocity.x*self.lmnY.y-self.angularVelocity.y*self.lmnY.x))/self._mag.y

            self.lmnZ.x = (self.lmnZ.x+self.TimeStep*(self.angularVelocity.y*self.lmnZ.z-self.angularVelocity.z*self.lmnZ.y))/self._mag.z
            self.lmnZ.y = (self.lmnZ.y-self.TimeStep*(self.angularVelocity.x*self.lmnZ.z-self.angularVelocity.z*self.lmnZ.x))/self._mag.z
            self.lmnZ.z = (self.lmnZ.z+self.TimeStep*(self.angularVelocity.x*self.lmnZ.y-self.angularVelocity.y*self.lmnZ.x))/self._mag.z

            # r Update
            self.r.x = (self.r.x+self.TimeStep*(self.angularVelocity.y*self.r.z-self.angularVelocity.z*self.r.y))/self._r_factor
            self.r.y = (self.r.y-self.TimeStep*(self.angularVelocity.x*self.r.z-self.angularVelocity.z*self.r.x))/self._r_factor
            self.r.z = (self.r.z+self.TimeStep*(self.angularVelocity.x*self.r.y-self.angularVelocity.y*self.r.x))/self._r_factor

            # Angular Velocity Update
            self.angularVelocity.x += self.TimeStep*self.angularAcceleration.x
            self.angularVelocity.y += self.TimeStep*self.angularAcceleration.y
            self.angularVelocity.z += self.TimeStep*self.angularAcceleration.z

            # Velocity Update
            self.velocity.x += self.TimeStep*self.acceleration.x
            self.velocity.y += self.TimeStep*self.acceleration.y

            # Position Update
            self.position.x += self.TimeStep*self.velocity.x
            self.position.y += self.TimeStep*self.velocity.y
        feet = lambda x: x*3.28084
        meter = lambda x: x*0.3048
        
        inches = lambda x: x*39.3701
        if self._Rolling:
            self.update_rolling()
            if self.Time*int(pow(self.TimeStep,-1)) % self.Graph_sample_interval == 0:
                self._RollingPositions[0].append(feet(self.position.x))
                self._RollingPositions[1].append(inches(self.position.y))
                
            
        else:
            self.update_sliding()
            if self.Time*int(pow(self.TimeStep,-1)) % self.Graph_sample_interval == 0:
                self._notRollingPositions[0].append(feet(self.position.x))
                self._notRollingPositions[1].append(inches(self.position.y))

        
        if self._Vp.magnitude() < 0.01:
            self._VpMag = self._Vp.magnitude()
            self._Rolling = True
        if self.position.x > meter(60) or self.position.x < -0.1 or self.position.y > self.MaxY or self.position.y < -0.1:
            self.Running = False
            self._hookFromBreakPoint = self.position.y - self._lowestY
            


    def update_rolling(self):

        # Theta Update
        self.theta[0] = -self.angularVelocity.x*(self.angularVelocity.x*self.r.z-self.angularVelocity.z*self.r.x)-self.angularVelocity.y*(self.angularVelocity.y*self.r.z-self.angularVelocity.z*self.r.y)
        self.theta[1] = -self.angularVelocity.x*(self.angularVelocity.x*self.r.y-self.angularVelocity.y*self.r.x)+self.angularVelocity.z*(self.angularVelocity.y*self.r.z-self.angularVelocity.z*self.r.y)
        self.theta[2] =  self.angularVelocity.y*(self.angularVelocity.x*self.r.y-self.angularVelocity.y*self.r.x)+self.angularVelocity.z*(self.angularVelocity.x*self.r.z-self.angularVelocity.z*self.r.x)

        # abcd Updates
        self.abcd1.a = -self.lmnX.x*(self.r.y)**2*self.Mass-(self.r.z+self.Radius)**2*self.Mass*self.lmnX.x+self.lmnX.y*self.Mass*self.r.x*self.r.y+self.lmnX.z*self.r.x*self.Mass*(self.r.z+self.Radius)-self.MomentsOfInertia.x*self.lmnX.x
        self.abcd1.b = self.lmnX.x*self.r.y*self.r.x*self.Mass-self.lmnX.y*(self.r.x)**2*self.Mass-self.lmnX.y*self.Mass*(self.r.z+self.Radius)**2+self.lmnX.z*self.r.y*self.Mass*(self.r.z+self.Radius)-self.MomentsOfInertia.x*self.lmnX.y
        self.abcd1.c = self.lmnX.x*(self.r.z+self.Radius)*self.Mass*self.r.x+self.lmnX.y*self.Mass*(self.r.z+self.Radius)*self.r.y-self.lmnX.z*self.Mass*(self.r.x)**2-self.lmnX.z*self.Mass*(self.r.y)**2-self.MomentsOfInertia.x*self.lmnX.z
        self.abcd1.d = self.lmnX.x*self.r.y*self.Mass*(self.Gravity+self.theta[0])-self.lmnX.x*self.Mass*(self.r.z+self.Radius)*self.theta[1]-self.lmnX.y*self.Mass*self.r.x*(self.Gravity+self.theta[0])+self.lmnX.y*self.Mass*(self.r.z+self.Radius)*self.theta[2]+self.lmnX.z*self.r.x*self.Mass*self.theta[1]-self.lmnX.z*self.r.y*self.Mass*self.theta[2]-(self.MomentsOfInertia.y-self.MomentsOfInertia.z)*(self.angularVelocity.x*self.lmnY.x+self.angularVelocity.y*self.lmnY.y+self.angularVelocity.z*self.lmnY.z)*(self.angularVelocity.x*self.lmnZ.x+self.angularVelocity.y*self.lmnZ.y+self.angularVelocity.z*self.lmnZ.z)
        
        self.abcd2.a = -self.lmnY.x*(self.r.y)**2*self.Mass-(self.r.z+self.Radius)**2*self.Mass*self.lmnY.x+self.lmnY.y*self.Mass*self.r.x*self.r.y+self.lmnY.z*self.r.x*self.Mass*(self.r.z+self.Radius)-self.MomentsOfInertia.y*self.lmnY.x
        self.abcd2.b = self.lmnY.x*self.r.y*self.r.x*self.Mass-self.lmnY.y*(self.r.x)**2*self.Mass-self.lmnY.y*self.Mass*(self.r.z+self.Radius)**2+self.lmnY.z*self.r.y*self.Mass*(self.r.z+self.Radius)-self.MomentsOfInertia.y*self.lmnY.y
        self.abcd2.c = self.lmnY.x*(self.r.z+self.Radius)*self.Mass*self.r.x+self.lmnY.y*self.Mass*(self.r.z+self.Radius)*self.r.y-self.lmnY.z*self.Mass*(self.r.x)**2-self.lmnY.z*self.Mass*(self.r.y)**2-self.MomentsOfInertia.y*self.lmnY.z
        self.abcd2.d = self.lmnY.x*self.r.y*self.Mass*(self.Gravity+self.theta[0])-self.lmnY.x*self.Mass*(self.r.z+self.Radius)*self.theta[1]-self.lmnY.y*self.Mass*self.r.x*(self.Gravity+self.theta[0])+self.lmnY.y*self.Mass*(self.r.z+self.Radius)*self.theta[2]+self.lmnY.z*self.r.x*self.Mass*self.theta[1]-self.lmnY.z*self.r.y*self.Mass*self.theta[2]-(self.MomentsOfInertia.z-self.MomentsOfInertia.x)*(self.angularVelocity.x*self.lmnZ.x+self.angularVelocity.y*self.lmnZ.y+self.angularVelocity.z*self.lmnZ.z)*(self.angularVelocity.x*self.lmnX.x+self.angularVelocity.y*self.lmnX.y+self.angularVelocity.z*self.lmnX.z)

        self.abcd3.a = -self.lmnZ.x*(self.r.y)**2*self.Mass-(self.r.z+self.Radius)**2*self.Mass*self.lmnZ.x+self.lmnZ.y*self.Mass*self.r.x*self.r.y+self.lmnZ.z*self.r.x*self.Mass*(self.r.z+self.Radius)-self.MomentsOfInertia.z*self.lmnZ.x
        self.abcd3.b = self.lmnZ.x*self.r.y*self.r.x*self.Mass-self.lmnZ.y*(self.r.x)**2*self.Mass-self.lmnZ.y*self.Mass*(self.r.z+self.Radius)**2+self.lmnZ.z*self.r.y*self.Mass*(self.r.z+self.Radius)-self.MomentsOfInertia.z*self.lmnZ.y
        self.abcd3.c = self.lmnZ.x*(self.r.z+self.Radius)*self.Mass*self.r.x+self.lmnZ.y*self.Mass*(self.r.z+self.Radius)*self.r.y-self.lmnZ.z*self.Mass*(self.r.x)**2-self.lmnZ.z*self.Mass*(self.r.y)**2-self.MomentsOfInertia.z*self.lmnZ.z
        self.abcd3.d = self.lmnZ.x*self.r.y*self.Mass*(self.Gravity+self.theta[0])-self.lmnZ.x*self.Mass*(self.r.z+self.Radius)*self.theta[1]-self.lmnZ.y*self.Mass*self.r.x*(self.Gravity+self.theta[0])+self.lmnZ.y*self.Mass*(self.r.z+self.Radius)*self.theta[2]+self.lmnZ.z*self.r.x*self.Mass*self.theta[1]-self.lmnZ.z*self.r.y*self.Mass*self.theta[2]-(self.MomentsOfInertia.x-self.MomentsOfInertia.y)*(self.angularVelocity.x*self.lmnX.x+self.angularVelocity.y*self.lmnX.y+self.angularVelocity.z*self.lmnX.z)*(self.angularVelocity.x*self.lmnY.x+self.angularVelocity.y*self.lmnY.y+self.angularVelocity.z*self.lmnY.z)

        # angular acceleration update
        self.angularAcceleration.z = ((self.abcd3.a*self.abcd2.b-self.abcd2.a*self.abcd3.b)*(self.abcd2.a*self.abcd1.d-self.abcd1.a*self.abcd2.d)-(self.abcd2.a*self.abcd1.b-self.abcd1.a*self.abcd2.b)*(self.abcd3.a*self.abcd2.d-self.abcd2.a*self.abcd3.d))/((self.abcd3.a*self.abcd2.b-self.abcd2.a*self.abcd3.b)*(self.abcd2.a*self.abcd1.c-self.abcd1.a*self.abcd2.c)-(self.abcd2.a*self.abcd1.b-self.abcd1.a*self.abcd2.b)*(self.abcd3.a*self.abcd2.c-self.abcd2.a*self.abcd3.c))
        self.angularAcceleration.y = ((self.abcd2.a*self.abcd1.c-self.abcd1.a*self.abcd2.c)*(self.abcd3.a*self.abcd2.d-self.abcd2.a*self.abcd3.d)-(self.abcd3.a*self.abcd2.c-self.abcd2.a*self.abcd3.c)*(self.abcd2.a*self.abcd1.d-self.abcd1.a*self.abcd2.d))/((self.abcd3.a*self.abcd2.b-self.abcd2.a*self.abcd3.b)*(self.abcd2.a*self.abcd1.c-self.abcd1.a*self.abcd2.c)-(self.abcd2.a*self.abcd1.b-self.abcd1.a*self.abcd2.b)*(self.abcd3.a*self.abcd2.c-self.abcd2.a*self.abcd3.c))
        self.angularAcceleration.x = (self.abcd1.d-self.abcd1.b*self.angularAcceleration.y-self.abcd1.c*self.angularAcceleration.z)/self.abcd1.a

        # acceleration update
        self.acceleration.x = self.Radius*self.angularAcceleration.y
        self.acceleration.y = self.Radius*self.angularAcceleration.x

        # Forces on Contact Point Update
        self.forces.x = self.Mass*(self.acceleration.x+self.angularAcceleration.y*self.r.z-self.angularAcceleration.z*self.r.y+self.theta[2])
        self.forces.y = self.Mass*(self.acceleration.y-self.angularAcceleration.x*self.r.z+self.angularAcceleration.z*self.r.x+self.theta[1])
        self.N = self.Mass*(self.angularAcceleration.x*self.r.y-self.angularAcceleration.y*self.r.x+self.theta[0]+self.Gravity)

        self._maxStaticFrictionMinusActual = self.N*self.s_friction-sqrt((self.forces.x)**2+(self.forces.y)**2)
        if self._maxStaticFrictionMinusActual < 0:
            self._Rolling = False
        
    def update_sliding(self):

        # Theta Update
        self.theta[0] = -self.angularVelocity.x*(self.angularVelocity.x*self.r.z-self.angularVelocity.z*self.r.x)-self.angularVelocity.y*(self.angularVelocity.y*self.r.z-self.angularVelocity.z*self.r.y)
        self.theta[1] = -self.angularVelocity.x*(self.angularVelocity.x*self.r.y-self.angularVelocity.y*self.r.x)+self.angularVelocity.z*(self.angularVelocity.y*self.r.z-self.angularVelocity.z*self.r.y)
        self.theta[2] =  self.angularVelocity.y*(self.angularVelocity.x*self.r.y-self.angularVelocity.y*self.r.x)+self.angularVelocity.z*(self.angularVelocity.x*self.r.z-self.angularVelocity.z*self.r.x)
        self.theta[3] = -self.r.y+(self.r.z+self.Radius)*(-self.k_friction)*(self.velocity.y+self.Radius*self.angularVelocity.x)/sqrt((self.velocity.x-self.Radius*self.angularVelocity.y)**2+(self.velocity.y+self.Radius*self.angularVelocity.x)**2)
        self.theta[4] =  self.r.x + (((self.r.z+self.Radius) * (-self.k_friction) * (self.velocity.x - self.Radius * self.angularVelocity.y )) / (sqrt((self.velocity.x - self.Radius * self.angularVelocity.y )**2 + (self.velocity.y + self.Radius*self.angularVelocity.x)**2)))
        self.theta[5] = -self.r.x*(-self.k_friction)*(self.velocity.y+self.Radius*self.angularVelocity.x)/sqrt((self.velocity.x-self.Radius*self.angularVelocity.y)**2+(self.velocity.y+self.Radius*self.angularVelocity.x)**2)+self.r.y*(-self.k_friction)*(self.velocity.x-self.Radius*self.angularVelocity.y)/sqrt((self.velocity.x-self.Radius*self.angularVelocity.y)**2+(self.velocity.y+self.Radius*self.angularVelocity.x)**2)


        # ABCD 1-3 Update
        self.abcd1.a = self.lmnX.x*self.Mass*self.r.y*self.theta[3]-self.lmnX.y*self.Mass*self.r.y*self.theta[4]+self.lmnX.z*self.Mass*self.r.y*self.theta[5]-self.MomentsOfInertia.x*self.lmnX.x
        self.abcd1.b = -self.lmnX.x*self.Mass*self.r.x*self.theta[3]+self.lmnX.y*self.Mass*self.r.x*self.theta[4]-self.lmnX.z*self.Mass*self.r.x*self.theta[5]-self.MomentsOfInertia.x*self.lmnX.y
        self.abcd1.c = -self.MomentsOfInertia.x*self.lmnX.z
        dp1 = -self.lmnX.x * self.Mass * (self.Gravity + self.theta[0]) * self.theta[3]
        dp2 = self.lmnX.y * self.Mass * (self.Gravity + self.theta[0]) * self.theta[4]
        dp3 = -self.lmnX.z * self.Mass * (self.Gravity + self.theta[0]) * self.theta[5]
        dp4 = - (self.MomentsOfInertia.y-self.MomentsOfInertia.z)
        dp5 = (self.angularVelocity.x * self.lmnY.x + self.angularVelocity.y * self.lmnY.y + self.angularVelocity.z * self.lmnY.z)
        dp6 = (self.angularVelocity.x * self.lmnZ.x + self.angularVelocity.y * self.lmnZ.y+self.angularVelocity.z * self.lmnZ.z)
        self.abcd1.d = dp1 + dp2 + dp3 + dp4 * dp5 * dp6

        self.abcd2.a = self.lmnY.x*self.Mass*self.r.y*self.theta[3]-self.lmnY.y*self.Mass*self.r.y*self.theta[4]+self.lmnY.z*self.Mass*self.r.y*self.theta[5]-self.MomentsOfInertia.y*self.lmnY.x
        self.abcd2.b = -self.lmnY.x*self.Mass*self.r.x*self.theta[3]+self.lmnY.y*self.Mass*self.r.x*self.theta[4]-self.lmnY.z*self.Mass*self.r.x*self.theta[5]-self.MomentsOfInertia.y*self.lmnY.y
        self.abcd2.c = -self.MomentsOfInertia.y*self.lmnY.z
        dp1 = -self.lmnY.x*self.Mass*(self.Gravity+self.theta[0])*self.theta[3]
        dp2 = self.lmnY.y*self.Mass*(self.Gravity+self.theta[0])*self.theta[4]
        dp3 = -self.lmnY.z*self.Mass*(self.Gravity+self.theta[0])*self.theta[5]
        dp4 = -(self.MomentsOfInertia.z-self.MomentsOfInertia.x)
        dp5 = (self.angularVelocity.x*self.lmnZ.x+self.angularVelocity.y*self.lmnZ.y+self.angularVelocity.z*self.lmnZ.z)
        dp6 = (self.angularVelocity.x*self.lmnX.x+self.angularVelocity.y*self.lmnX.y+self.angularVelocity.z*self.lmnX.z)
        self.abcd2.d = dp1 + dp2 + dp3 + dp4 * dp5 * dp6

        self.abcd3.a = self.lmnZ.x*self.Mass*self.r.y*self.theta[3]-self.lmnZ.y*self.Mass*self.r.y*self.theta[4]+self.lmnZ.z*self.Mass*self.r.y*self.theta[5]-self.MomentsOfInertia.z*self.lmnZ.x
        self.abcd3.b = -self.lmnZ.x*self.Mass*self.r.x*self.theta[3]+self.lmnZ.y*self.Mass*self.r.x*self.theta[4]-self.lmnZ.z*self.Mass*self.r.x*self.theta[5]-self.MomentsOfInertia.z*self.lmnZ.y
        self.abcd3.c = -self.MomentsOfInertia.z*self.lmnZ.z
        dp1 = -self.lmnZ.x*self.Mass*(self.Gravity+self.theta[0])*self.theta[3]
        dp2 =  self.lmnZ.y*self.Mass*(self.Gravity+self.theta[0])*self.theta[4]
        dp3 = -self.lmnZ.z*self.Mass*(self.Gravity+self.theta[0])*self.theta[5]
        dp4 = -(self.MomentsOfInertia.x-self.MomentsOfInertia.y)
        dp5 = (self.angularVelocity.x*self.lmnX.x+self.angularVelocity.y*self.lmnX.y+self.angularVelocity.z*self.lmnX.z)
        dp6 = (self.angularVelocity.x*self.lmnY.x+self.angularVelocity.y*self.lmnY.y+self.angularVelocity.z*self.lmnY.z)
        self.abcd2.d = dp1 + dp2 + dp3 + dp4 * dp5 * dp6

        # Angular Acceleration
        self.angularAcceleration.z = ((self.abcd3.a*self.abcd2.b-self.abcd2.a*self.abcd3.b)*(self.abcd2.a*self.abcd1.d-self.abcd1.a*self.abcd2.d)-(self.abcd2.a*self.abcd1.b-self.abcd1.a*self.abcd2.b)*(self.abcd3.a*self.abcd2.d-self.abcd2.a*self.abcd3.d))/((self.abcd3.a*self.abcd2.b-self.abcd2.a*self.abcd3.b)*(self.abcd2.a*self.abcd1.c-self.abcd1.a*self.abcd2.c)-(self.abcd2.a*self.abcd1.b-self.abcd1.a*self.abcd2.b)*(self.abcd3.a*self.abcd2.c-self.abcd2.a*self.abcd3.c))
        self.angularAcceleration.y = ((self.abcd2.a*self.abcd1.c-self.abcd1.a*self.abcd2.c)*(self.abcd3.a*self.abcd2.d-self.abcd2.a*self.abcd3.d)-(self.abcd3.a*self.abcd2.c-self.abcd2.a*self.abcd3.c)*(self.abcd2.a*self.abcd1.d-self.abcd1.a*self.abcd2.d))/((self.abcd3.a*self.abcd2.b-self.abcd2.a*self.abcd3.b)*(self.abcd2.a*self.abcd1.c-self.abcd1.a*self.abcd2.c)-(self.abcd2.a*self.abcd1.b-self.abcd1.a*self.abcd2.b)*(self.abcd3.a*self.abcd2.c-self.abcd2.a*self.abcd3.c))
        self.angularAcceleration.x = (self.abcd1.d-self.abcd1.b*self.angularAcceleration.y-self.abcd1.c*self.angularAcceleration.z)/self.abcd1.a

        # Acceleration
        self.acceleration.x = (-self.k_friction*self.Mass*(self.angularAcceleration.x*self.r.y-self.angularAcceleration.y*self.r.x+self.Gravity+self.theta[0])*(self.velocity.x-self.Radius*self.angularVelocity.y)/sqrt((self.velocity.x-self.Radius*self.angularVelocity.y)**2+(self.velocity.y+self.Radius*self.angularVelocity.x)**2))/self.Mass-(self.angularAcceleration.y*self.r.z-self.angularAcceleration.z*self.r.y)-self.theta[2]
        self.acceleration.y = (-self.k_friction*self.Mass*(self.angularAcceleration.x*self.r.y-self.angularAcceleration.y*self.r.x+self.Gravity+self.theta[0])*(self.velocity.y+self.Radius*self.angularVelocity.x)/sqrt((self.velocity.x-self.Radius*self.angularVelocity.y)**2+(self.velocity.y+self.Radius*self.angularVelocity.x)**2))
        
        # Forces on Contact Point
        self.forces.x = -self.k_friction*self.Mass*(self.angularAcceleration.x*self.r.y-self.angularAcceleration.y*self.r.x+self.Gravity+self.theta[0])*(self.velocity.x-self.Radius*self.angularVelocity.y)/sqrt((self.velocity.x-self.Radius*self.angularVelocity.y)**2+(self.velocity.y+self.Radius*self.angularVelocity.x)**2)
        self.forces.y = -self.k_friction*self.Mass*(self.angularAcceleration.x*self.r.y-self.angularAcceleration.y*self.r.x+self.Gravity+self.theta[0])*(self.velocity.y+self.Radius*self.angularVelocity.x)/sqrt((self.velocity.x-self.Radius*self.angularVelocity.y)**2+(self.velocity.y+self.Radius*self.angularVelocity.x)**2)
        self.N = self.Mass*(self.angularAcceleration.x*self.r.y-self.angularAcceleration.y*self.r.x+self.Gravity+self.theta[0])

        self._Vp.x = self.velocity.x-self.Radius*self.angularVelocity.y
        self._Vp.y = self.velocity.y+self.Radius*self.angularVelocity.x
        
    def plot(self):
        
        self._notRollingPositions[0].append(self._RollingPositions[0][0])
        self._notRollingPositions[1].append(self._RollingPositions[1][0])
        line, = self.ax.plot(self._notRollingPositions[0],self._notRollingPositions[1],color="red",label="Sliding",linewidth=2,animated=self.isAnimated)
        line2, = self.ax.plot(self._RollingPositions[0],self._RollingPositions[1],color="green",label="Rolling",linewidth=2,animated=self.isAnimated)
        
        bp, = self.ax.plot(meter2feet(self._breakPointX),meter2inch(self._lowestY),'o',color="orange",label="Break Point",animated=self.isAnimated)
        self.ax.axis([0,60,0,39])
        plot = PlotBowlingBall(line,line2,self._RollingPositions,self._notRollingPositions)
        return plot
        
    def __repr__(self) -> str:
        s = f"{self.__class__.__name__}".center(50,"=")+"\n"
        for i in self.__dict__:
            if i == "theta":
                a = [round(i,4) for i in self.__dict__["theta"]]
                s = "".join([s,f"{i} = {a}\n"])
                continue
            if not i.startswith("_"):
                s = "".join([s,f"{i} = {self.__dict__[i]}\n"])
        s= "".join([s,"=".center(50,"=")])
        return s
    @staticmethod
    def StartSimulation(params,runRangeLen:int,Animate:bool=False,Save:bool=False):
        Simulations = []
        with mp.Pool(min(runRangeLen,mp.cpu_count())) as pool:
            Simulations = pool.map(spawnChildProcess,params)
        BowlingBall.isAnimated = Animate
        plotlist = []
        plotTotalLength = 0
        for sim in Simulations:
            plot = sim.plot()
            plotTotalLength = max(plot.totalLength,plotTotalLength)
            plotlist.append(plot)

        BowlingBall.fig.set_figwidth(15)
        BowlingBall.fig.set_figheight(4)

        BowlingBall.ax.plot([meter2feet(BowlingBall.oil_length) for i in range(0,40)],[i for i in range(0,40)],label="Oil Pattern End",color="black",alpha=0.5)
        BowlingBall.fig.canvas.draw()
        BowlingBall.fig.legend(loc="lower right")

        anim = None
        if Animate:
            anim = animation.FuncAnimation(BowlingBall.fig,PlotBowlingBall.updateouter,frames=plotTotalLength,fargs=(plotlist),interval=1,blit=True,repeat=True,repeat_delay=1000)
            
        if Save:
           PlotBowlingBall.savePlot("BowlingBall",anim)
        return anim
    
def spawnChildProcess(params):
    print(f"Starting Simulation: increment={params.get('id',None)}")

    sim = BowlingBall(**params)
    sim.run()
    return sim