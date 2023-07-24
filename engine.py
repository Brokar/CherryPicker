import numpy as np
import random as random




class Bot:
    def __init__(self): 
        self.position=[]

    def random_move(self, map):
        map[3,self.position[0],self.position[1]]-=1
        #remove possibilities for edge of map
        possibilities=["right","left","up","down"]
        if self.position[0]==0:
            possibilities.remove("left")
        elif self.position[0]==len(map[3]):
            possibilities.remove("right")
        if self.position[1]==0:
            possibilities.remove("down")
        elif self.position[1]==len(map[3][0]):
            possibilities.remove("up")
            
        direction=random.sample(possibilities,1)
        if direction=="right":
            self.position[0]+=1
        elif direction =="left":
            self.position[0]-=1
        elif direction =="up":
            self.position[1]+=1
        else:
            self.position[1]-=1
        map[3,self.position[0],self.position[1]]+=1



