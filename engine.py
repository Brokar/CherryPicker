import numpy as np
import random as random


def initialise_map (layer,lenght,height,number_of_cherries):
    #layer1=terrain,layer2=player1,layer3=bot
    map = np.zeros((layer,lenght,height))
    #player and bot are placed in the middle of theon top and bottom of map
    map[1,int(lenght/2),0] = 1
    map[2,int(lenght/2),-1] = 1
    x_sample=random.sample(range(lenght),number_of_cherries)
    y_sample=random.sample(range(height),number_of_cherries)
    for sample_number in range (number_of_cherries):
        map[0,x_sample[sample_number],y_sample[sample_number]] = 1
    return map

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



