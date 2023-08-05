from enum import Enum
import numpy as np
import random as random

class GameStates(Enum):
    PLAYER = 0
    MOVING = 1
    AI = 2


class GameMap:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = 20
        self.map_height=20
        self.number_of_cherries=5
        self.tile_size = 32 
        [self.obstacles_map,self.players_map] = self.random_map()
    
    def random_map(self):
        #layer0=terrain,layer1=player1,layer2=bot
        obstacles_map = np.zeros((self.map_width,self.map_height))
        players_map = np.zeros((self.map_width,self.map_height))
        #player and bot are placed in the middle of theon top and bottom of map
        players_map[int(self.map_width/2),0] = 1
        players_map[int(self.map_width/2),-1] = 2
        x_sample=random.sample(range(self.map_width),self.number_of_cherries)
        y_sample=random.sample(range(self.map_height-1),self.number_of_cherries)
        for sample_number in range (self.number_of_cherries):
            obstacles_map[y_sample[sample_number],x_sample[sample_number]] = sample_number+1
        return [obstacles_map,players_map]




FPS = 60



def init(width, height):
    global game_map
    game_map = GameMap(width, height) 
