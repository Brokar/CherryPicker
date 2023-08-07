from enum import Enum
import numpy as np
import random as random

class GameStates():
    PLAYER = "player"
    MOVING = 1
    AI = 2


class GameMap:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = 30
        self.map_height=10
        self.number_of_cherries=15
        self.tile_size = 32 

        [self.obstacles_map,self.players_map] = self.random_map()

    
    def random_map(self):
        #layer0=terrain,layer1=player1,layer2=bot
        obstacles_map = np.zeros((self.map_height,self.map_width))
        players_map = np.zeros((self.map_height,self.map_width))
        
        #player and bot are placed in the middle of theon top and bottom of map
        players_map[0,int(self.map_width/2)] = 1
        players_map[-1,int(self.map_width/2)] = 2
        cherry_position=[]
        i=0        
        while i < self.number_of_cherries:
            x=random.randint(0,self.map_width)
            y=random.randint(0,(self.map_height-2))
            pair=[y,x]
            if pair!=[0,int(self.map_width/2)] and pair!=[-1,int(self.map_width/2)] and pair not in cherry_position:
                cherry_position.append(pair)
                i+=1
        sample_number=0
        for row_index in range(0,self.map_height):
            for col_index in range(0,self.map_width):
                for pair in cherry_position:
                    if row_index==pair[0] and col_index==pair[1]:
                        sample_number+=1
                        obstacles_map[row_index,col_index]=sample_number
        return [obstacles_map,players_map]





FPS = 60



def init(width, height):
    global game_map
    game_map = GameMap(width, height) 
