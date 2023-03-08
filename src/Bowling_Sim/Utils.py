from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib
import os


class PlotBowlingBall:
    def __init__(self,slide:Line2D,roll:Line2D,rollingPositions:list[list],notRollingPositions:list[list]):
        self.slide = slide
        self.roll = roll
        self.rollingPositions:list[list] = rollingPositions
        self.notRollingPositions:list[list] = notRollingPositions
        self.totalLength = len(self.rollingPositions[0])+len(self.notRollingPositions[0])
        self.startOffset = 0
        self.rollingPositions[0].insert(0,self.notRollingPositions[0][-1])
        self.rollingPositions[1].insert(0,self.notRollingPositions[1][-1])
    
    def update(self,i):
        if i > self.startOffset:
            i2 = i-self.startOffset
            # Animate rolling
            if i2 < len(self.notRollingPositions[0]):
                self.slide.set_data(self.notRollingPositions[0][:i2],self.notRollingPositions[1][:i2])
                self.roll.set_data([],[])
            
            # Animate not rolling
            else:
                i3 = i2-len(self.notRollingPositions[0])
                self.slide.set_data(self.notRollingPositions[0][:],self.notRollingPositions[1][:])
                self.roll.set_data(self.rollingPositions[0][:i3],self.rollingPositions[1][:i3])
                
        
            
        else:
            self.slide.set_data([],[])
            self.roll.set_data([],[])
        return self.slide, self.roll,
    @staticmethod
    def savePlot(filename,anim = None):
        plt.savefig(outputIndexer(f"{filename}.png"),dpi=1000)
        if anim is not None:
            writer = animation.FFMpegWriter(fps=200,bitrate=10000)
            anim.save(outputIndexer(f"{filename}.mp4"),writer=writer,dpi=200)

    @staticmethod
    def updateouter(i,*plist):
        lines = []
        
        for object in plist:
            Slide,Roll = object.update(i)
            lines += [Slide,Roll]
        return tuple(lines)

def outputIndexer(filename:str):
    ext = filename.split(".")[-1]
    filename = filename.replace(f".{ext}","")
    if os.path.exists(".\\out") == False:
        os.mkdir(".\\out")
    n = 0
    while True:
        if not os.path.exists(f".\\out\\{filename}{n}.{ext}"):
            return f".\\out\\{filename}{n}.{ext}"
        n+=1


def meter2feet(x):
    return x*3.28084
def feet2meter(x):
    return x/3.28084
def meter2inch(x):
    return x*39.3701

