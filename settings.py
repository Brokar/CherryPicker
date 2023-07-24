import numpy as np
import random as random

FPS = 60
map_length=20
map_height=20
tile_size=32


class GameSettings:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.number_of_cherries=6

    def initialise_map (self,width,height):
        #layer1=terrain,layer2=player1,layer3=bot
        map = np.zeros((3,width,height))
        #player and bot are placed in the middle of theon top and bottom of map
        map[1,int(width/2),0] = 1
        map[2,int(width/2),-1] = 1
        x_sample=random.sample(range(width),self.number_of_cherries)
        y_sample=random.sample(range(height),self.number_of_cherries)
        for sample_number in range (self.number_of_cherries):
            map[0,x_sample[sample_number],y_sample[sample_number]] = 1
        return map

