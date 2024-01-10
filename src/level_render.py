import numpy as np
import pygame
from settings import GameStates, TypePlayer, HANDLER_MASK, ROCK_HANDLER, TREE_HANDLER, LOGS_DIR
import settings
from tile import Grass, CherryTree, Obstacle, Rock
from player import Player, Bot#, interact_obj
from debug import debug
from ui import UI
import json
import os
import time

class LevelRender:
    """ This class is incharge of rendering the game level 
        using pygame framework. Normally, it will be updated
        with the FPS frequency.
    """ 
    def __init__(self, game_map, vervose =0 ):
        # Get the display surface
        self.display_surface = pygame.display.get_surface()
        # Button control
        self.k_space_is_press = False
        # State control
        self.start_state_ticks = 0
        # sprite group setup
        self.background_tiles = YSortCameraGroup()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.adversaries = []
        self.pause_request = False
        self.state = GameStates.PLAYING     
        self.obstacle_sprite_table = dict()
        self.init_map(game_map)
        self.logging = False
        self.map_snapshots = []
        self.player_cherries = []
        self.set_vervose(vervose)
        # user interface 
        self.ui = UI()
    def set_vervose(self, vervose):
        if(vervose == 1):
            self.logging = True
            if not os.path.exists(LOGS_DIR):
                os.makedirs(LOGS_DIR)

    def init_map(self, game_map):
        for row_index, row in enumerate(game_map.obstacles_map):
            for col_index, _ in enumerate(row): # _ is used for not accessed variables
                x = col_index*game_map.tile_size
                y = row_index*game_map.tile_size
                Grass((x,y),self.background_tiles)
                obstacle_id =  game_map.obstacles_map[row_index][col_index]
                if obstacle_id!=0:
                    if (obstacle_id & HANDLER_MASK) == TREE_HANDLER :
                        self.obstacle_sprite_table[int(obstacle_id)] = CherryTree((x,y),[self.visible_sprites,self.obstacle_sprites], obstacle_id)
                    elif (obstacle_id & HANDLER_MASK) == ROCK_HANDLER:
                        self.obstacle_sprite_table[int(obstacle_id)] = Rock((x,y),[self.visible_sprites,self.obstacle_sprites], obstacle_id)
                if game_map.players_map[row_index][col_index]!=0:
                    #(position, [added to sprite group], passing obstacle_sprites, obstacle id reference)
                    if game_map.players_map[row_index][col_index]==TypePlayer.PLAYER:
                        self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprite_table) 
                    if game_map.players_map[row_index][col_index]==TypePlayer.BOT_1:
                        self.adversaries.append(Bot((x,y), [self.visible_sprites], self.obstacle_sprite_table, TypePlayer.BOT_1))
                    if game_map.players_map[row_index][col_index]==TypePlayer.BOT_2:
                        self.adversaries.append(Bot((x,y), [self.visible_sprites], self.obstacle_sprite_table, TypePlayer.BOT_2))
                    if game_map.players_map[row_index][col_index]==TypePlayer.BOT_3:
                        self.adversaries.append(Bot((x,y), [self.visible_sprites], self.obstacle_sprite_table, TypePlayer.BOT_3))
        print(self.obstacle_sprite_table)


    def input(self):
        keys = pygame.key.get_pressed()
        # Debounce check
        if keys[pygame.K_ESCAPE] or keys[pygame.K_RETURN]: 
            if not self.k_space_is_press:
                if keys[pygame.K_ESCAPE]:
                    self.pause_request = True
                if keys[pygame.K_RETURN]:
                    self.state = settings.GameStates.PLAYING
                self.k_space_is_press=True
        else:
            self.k_space_is_press=False
    def is_winner(self):
        """
        Calculate if there is a winner.
        Winning condition:
            - Having more charries than anyone
            - Left cherries less than second with most
        """
        total_picked_cherries = self.player.picked_cherries
        current_podium = [self.player]
        for adversary in self.adversaries:
            total_picked_cherries += adversary.picked_cherries
            current_podium.append(adversary)
        current_podium.sort(key=lambda x: x.picked_cherries, reverse=True)
        left_cherries = settings.game_map.number_of_cherries - total_picked_cherries
        if(current_podium[0].picked_cherries > 
           (current_podium[1].picked_cherries + left_cherries) ):
            print("Player {} won wiht {} cherries".format(current_podium[0].player_id, current_podium[0].picked_cherries))
            return True 

        return False

    def current_map(self):
        map = np.zeros((settings.game_map.map_height, settings.game_map.map_width), dtype=Obstacle)
        # add players
        x=int(self.player.position[1]/settings.game_map.tile_size)
        y=int(self.player.position[0]/settings.game_map.tile_size)
        map[x,y]=self.player.player_id
        for adversary in self.adversaries:
            x=int(adversary.position[1]/settings.game_map.tile_size)
            y=int(adversary.position[0]/settings.game_map.tile_size)
            map[x,y]=adversary.player_id

        # add obstacle
        for obstacle in self.obstacle_sprite_table.values():
            x= int(obstacle.pos[1]/settings.game_map.tile_size)
            y= int(obstacle.pos[0]/settings.game_map.tile_size)
            map[x,y]=obstacle.get_type()
        return map
    def capture_log(self):
        """
        Generate logs of every state of the map
        """
        if(self.logging):
            cur_map = self.current_map()
            if(len(self.map_snapshots) == 0 
               or (cur_map!=self.map_snapshots[-1]).any()):
                self.map_snapshots.append(self.current_map())
                self.player_cherries.append(self.player.picked_cherries)
    def save_log(self):
        """
        Generate logs of every state of the map
        """
        if(self.logging):
            timestr = time.strftime("%Y%m%d-%H%M%S")
            np.save(os.path.join(LOGS_DIR,"game_{}.npy".format(timestr)),
                    self.map_snapshots)
            last = 0
            picked = []
            for v in self.player_cherries:
                if(last is not v):
                    picked.append(1)
                else:
                    picked.append(0)
                last = v

            np.save(os.path.join(LOGS_DIR,"picked_{}.npy".format(timestr)),
                    np.array(picked))
            self.logging = False    
           # with open(os.path.join(LOGS_DIR,"cherry_game_{}.data".format(timestr) ), "w+") as fp:
           #      json.dump(self.map_snapshots, fp)

    def update_state(self):
        """
        States of the game are updated here0
        """
        if(self.state == settings.GameStates.GAME_OVER):
            pass
        elif(self.is_winner()):
            self.state = settings.GameStates.GAME_OVER
        elif(self.pause_request):
            if self.state == settings.GameStates.PLAYING:
                self.state = settings.GameStates.PAUSED 
            else:
                self.state = settings.GameStates.PLAYING
            self.pause_request = False


    def update_map(self):
        """
        Level render game cylce update 
        """
        # TODO: define game stages. 
        # 1. Player preparation

        # 2. Player moving turn
        # 3. AI turn
        # 4. Other stuff in the map
        # Updating all visable sprites, including user and background
        if (not (self.state is settings.GameStates.PAUSED or
            self.state is settings.GameStates.GAME_OVER)):
            self.capture_log()
            self.background_tiles.update()
            self.visible_sprites.update()
            self.input()
            self.background_tiles.custom_draw(self.player)
            self.visible_sprites.custom_draw(self.player)
            # Refresh stamina
            if self.player.stamina == 0:
                self.adversaries[0].restore_stamina()
                self.player.restore_stamina()
        else:
            self.input()
        if(self.state is settings.GameStates.GAME_OVER):
            self.save_log()
        # Update main manu and counter
        self.update_state()
        self.ui.display(self.player, self.state)


          
# TODO: free camara. Allow following other sprites
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup 
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.camara_off = pygame.math.Vector2()
        self.input_camera = pygame.math.Vector2()
        self.free_camera = False

    def custom_draw(self,player):


        CAMERA_SPEED = 10
        # Camara follows the player 
        if not self.free_camera:
            self.camara_off.x = player.rect.centerx - self.half_width
            self.camara_off.y = player.rect.centery - self.half_height
        else: 
            self.camara_off.x += self.input_camera.x * CAMERA_SPEED 
            self.camara_off.y += self.input_camera.y * CAMERA_SPEED
        #self.draw_background(settings.game_map)
        # for all sprites in the group, draw with camara_off
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.camara_off
            self.display_surface.blit(sprite.image, offset_pos)




    def menu_input(self):
        """
        Menu inputs
        """
        keys = pygame.key.get_pressed()
        self.input_camera.x = 0
        self.input_camera.y = 0
        # Debounce check
        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_p]:
            self.free_camera=True
            if keys[pygame.K_w]:
                self.input_camera.y = -1
            elif keys[pygame.K_s]:
                self.input_camera.y = 1 
            if keys[pygame.K_d]:
                self.input_camera.x = 1 
            elif keys[pygame.K_a]:
                self.input_camera.x = -1
            if keys[pygame.K_p]:
                self.free_camera=False

    def update(self):
        super().update()
        self.menu_input()



