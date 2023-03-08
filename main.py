import os
import sys
from math import  * 
import pygame
from pygame import Vector3, Vector2
from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib
import numpy as np
import multiprocessing as mp
from Bowling import BowlingBall





            


def startSimulation(dict):
    print(f"Starting Simulation: increment={dict.get('id',None)}")
    
    Bowling = BowlingBall(**dict)
    Bowling.start()
    return Bowling

def updateouter(i,*plist):
    lines = []
    p = plist[0]
    for object in plist:
        Slide,Roll = object.update(i)
        lines += [Slide,Roll]
    return tuple(lines)
def test(params,fig,runRange):
    Simulations = []
    with mp.Pool(min(len(list(runRange)),mp.cpu_count())) as pool:
        Simulations = pool.map(startSimulation,params)
    
    plotlist = []
    plotTotalLength = 0
    for sim in Simulations:
        plot = sim.plot()
        plotTotalLength = max(plot.totalLength,plotTotalLength)
        plotlist.append(plot)

    BowlingBall.fig.set_figwidth(15)
    BowlingBall.fig.set_figheight(4)
    BowlingBall.fig.canvas.draw()
    anim = animation.FuncAnimation(BowlingBall.fig,updateouter,frames=plotTotalLength,fargs=(plotlist),interval=1,blit=True,repeat=True,repeat_delay=1000)
    return anim
    
    
    
    
        
   
   
    

def main():

    BowlingBall.Graph_sample_interval = 100
    print("cpu count:",mp.cpu_count())
    runRange = range(-1,2,1)
    increment = 0
    args = (
        {
        "revangle":15,
        "throwangle":-7+increment/2,
        "rev":30,
        "startpos":6/7,
        "id":increment
        } for increment in runRange)
    
    
    
    matplotlib.rcParams['animation.ffmpeg_path'] = "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe"
    anim = test(args,BowlingBall.fig,runRange)
        
    
    plt.show()


    
if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
     
    
    
