from enum import Enum
from typing import Type
import numpy as np
import random as random

class GameStates():
    PLAYER = "player"
    MOVING = 1
    AI = 2

class TypePlayer():
    PLAYER = 1
    BOT_1 = 2
    BOT_2 = 3
    BOT_3 = 4

NUM_ADVERSARIES=1
DEFAULT_STAMINA=1
FPS = 60



class GameMap:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = 30
        self.map_height=10
        self.number_of_cherries=15
        self.number_of_rock=9
        self.tile_size = 32 

        [self.obstacles_map,self.players_map] = self.random_map()

    
    def random_map(self):
        #layer0=terrain,layer1=player1,layer2=bot
        obstacles_map = np.zeros((self.map_height,self.map_width))
        players_map = np.zeros((self.map_height,self.map_width))
        self.place_players(players_map,NUM_ADVERSARIES) 
        #player and bot are placed in the middle of theon top and bottom of map
        cherry_position=[]
        for rock_idx in range(0,self.number_of_rock,3):
            x=random.randint(0,self.map_width-1)
            y=random.randint(0,self.map_height-2) # Trees occupy two vertical tiles
            pair=[y,x]
            pairbefore=[y,x-1]
            pairafter=[y,x+1]
            if players_map[y,x] == 0 and pair not in cherry_position and pairbefore not in cherry_position and pairafter not in cherry_position:
                cherry_position.append(pair)
                cherry_position.append(pairbefore)
                cherry_position.append(pairafter)
                obstacles_map[y,x] = rock_idx+101
                obstacles_map[y,x-1] = rock_idx+102
                obstacles_map[y,x+1] = rock_idx+103
            else: # in case of overlap, we retry in the next iteration
                rock_idx-=1

        for cherry_idx in range(self.number_of_cherries):
            x=random.randint(0,self.map_width-1)
            y=random.randint(0,self.map_height-2) # Trees occupy two vertical tiles
            pair=[y,x]
            if players_map[y,x] == 0 and pair not in cherry_position:
                cherry_position.append(pair)
                obstacles_map[y,x] = cherry_idx+1
            else: # in case of overlap, we retry in the next iteration
                cherry_idx-=1
        return [obstacles_map,players_map]

    def place_players(self, players_map, num_adv):
        middle_width = int(self.map_width/2)
        middle_height = int(self.map_height/2)
        players_map[0,middle_width] = TypePlayer.PLAYER
        players_map[-1,middle_width] = TypePlayer.BOT_1
        if(num_adv == 2):
            players_map[middle_height, 0] = TypePlayer.BOT_2
        if(num_adv == 3):
            players_map[middle_height, -1] = TypePlayer.BOT_3
        


def init(width, height):
    global game_map
    game_map = GameMap(width, height) 
