from Bowling import BowlingBall
from matplotlib import pyplot as plt


def main():

    BowlingBall.Graph_sample_interval = 100
    runRange = range(-1,2,1)
    args = (
        {
        "revangle":15,
        "throwangle":-7+increment/2,
        "rev":30,
        "startpos":6/7,
        "id":increment
        } for increment in runRange)
    
    
    
    _ = BowlingBall.StartSimulation(args,len(list(runRange)),Animate=True,Save=True) # Behöver att sparas i en variabel annars startar inte animationen
    
    plt.show()


    
if __name__ == "__main__":
    main()
    
    
    
    