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
# Prefix in Hexadecimal to identify a Tree
ROCK_HANDLER = (0x524F0000)
TREE_HANDLER = (0x54520000)
HANDLER_MASK = 0xFFFF0000

class GameMap:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = 30
        self.map_height=10
        self.number_of_cherries=15
        self.number_of_rock=9
        self.tile_size = 32 
        self.occupied_tiles = []
        self.random_map()

    def __generate_rocks(self, num):
        rock_concat = 3
        self.occupied_tiles=[]
        for rock_block_idx in range(0,num,rock_concat):
            x=random.randint(0,self.map_width-1)
            y=random.randint(0,self.map_height-2) # Trees occupy two vertical tiles
            pair=[y,x]
            pairbefore=[y,x-1]
            pairafter=[y,x+1]
            if (self.players_map[y,x] == 0 and 
                (pair not in self.occupied_tiles) and 
                (pairbefore not in self.occupied_tiles) and 
                (pairafter not in self.occupied_tiles) 
                and ((x+1) < (self.map_width))):
                self.occupied_tiles.append(pair)
                self.occupied_tiles.append(pairbefore)
                self.occupied_tiles.append(pairafter)
                
                self.obstacles_map[y,x] = rock_block_idx+1  | ROCK_HANDLER
                self.obstacles_map[y,x-1] = rock_block_idx+2 | ROCK_HANDLER
                self.obstacles_map[y,x+1] = rock_block_idx+3 | ROCK_HANDLER
            else: # in case of overlap, we retry in the next iteration
                rock_block_idx-=1

    def __generate_trees(self, num):
        for cherry_idx in range(num):
            x=random.randint(0,self.map_width-1)
            y=random.randint(0,self.map_height-2) # Trees occupy two vertical tiles
            pair=[y,x]
            if self.players_map[y,x] == 0 and pair not in self.occupied_tiles:
                self.occupied_tiles.append(pair)
                self.obstacles_map[y,x] = cherry_idx+1 | TREE_HANDLER
            else: # in case of overlap, we retry in the next iteration
                cherry_idx-=1
                
    def random_map(self):
        #layer0=terrain,layer1=player1,layer2=bot
        self.obstacles_map = np.zeros((self.map_height,self.map_width), dtype=int)
        self.players_map = np.zeros((self.map_height,self.map_width), dtype=int)
        #player and bot are placed in the middle of theon top and bottom of map
        self.place_players(self.players_map,NUM_ADVERSARIES)
        # Generating Rocks in the map
        self.__generate_rocks(self.number_of_rock) 
        # Generating Trees in the map
        self.__generate_trees(self.number_of_cherries)

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
