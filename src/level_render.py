import pygame
import settings
from tile import Grass, CherryTree
from player import Player#, interact_obj
from debug import debug
from os import path

class LevelRender:
    """ This class is incharge of rendering the game level 
        using pygame framework. Normally, it will be updated
        with the FPS frequency.
    """    
    def __init__(self, game_map ):
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
        self.player_references = []        
        self.init_map(game_map)
        self.state = settings.GameStates.PLAYER

    def init_map(self, game_map):
        for row_index, row in enumerate(game_map.obstacles_map):
            for col_index, col in enumerate(row):
                x = col_index*game_map.tile_size
                y = row_index*game_map.tile_size
                Grass((x,y),self.background_tiles)
                if game_map.obstacles_map[row_index][col_index]!=0:
                    CherryTree((x,y),[self.visible_sprites,self.obstacle_sprites])
                if game_map.players_map[row_index][col_index]!=0:
                    #(position, [added to sprite group], passing obstacle_sprites, giving reference)
                    if game_map.players_map[row_index][col_index]==1:
                        self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites,game_map.players_map[row_index][col_index]) 
                        self.player_references.append(self.player)


    def update_game_state(self):
        keys = pygame.key.get_pressed()
        # Debounce check
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]: 
            if not self.k_space_is_press:
                if keys[pygame.K_RETURN]:
                    self.state = settings.GameStates.MOVING
                    self.start_state_ticks=pygame.time.get_ticks()
                    self.player.reset_pos()
                if keys[pygame.K_SPACE]:
                    self.player.reset_pos()
                self.k_space_is_press=True
        else:
            self.k_space_is_press=False

    def update_map(self):
        # TODO: define game stages. 
        # 1. Player preparation
        # 2. Player moving turn
        # 3. AI turn
        # 4. Other stuff in the map
        # Updating all visable sprites, including user
        #self.background_tiles.custom_draw()
        self.update_game_state()
        self.background_tiles.update()
        self.background_tiles.custom_draw(self.player)
        if self.state == settings.GameStates.PLAYER:
            debug(str(f"{self.state}"))
            self.visible_sprites.update()
            self.visible_sprites.custom_draw(self.player)
            
        elif self.state == settings.GameStates.MOVING:
            self.visible_sprites.custom_draw(self.player)
            #self.visible_sprites.update()
            seconds=(pygame.time.get_ticks()-self.start_state_ticks)/1000
            debug(f"{self.state}: {str(int(10-seconds))}")
            if seconds>10:
                self.state = settings.GameStates.PLAYER


          
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

        self.cherry_image = pygame.image.load(path.join("..","tiles","cherry.png")).convert_alpha()
        self.cherry_image = pygame.transform.scale(self.cherry_image,(80,80))
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
        self.user_interface(player)

    def user_interface(self,player):
        top=settings.game_map.map_height*settings.game_map.tile_size


        cherry_rect = self.cherry_image.get_rect(topleft=(10,top+10))


        cherry_number=player.basket_content.count("cherry")
        text_cherry="X "+str(cherry_number)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        text_surf = self.font.render(text_cherry, False, "white")
        text_rect = text_surf.get_rect(topleft=cherry_rect.topright)


        box_width=cherry_rect.width+text_rect.width+20
        interface_rect=(0,top,box_width,cherry_rect.height+20)
        pygame.draw.rect(self.display_surface,"royalblue",interface_rect)
        self.display_surface.blit(self.cherry_image,cherry_rect)
        self.display_surface.blit(text_surf,text_rect)

#    def draw_background(self, game_map):
#        # TODO: Change to a less complex rendering
#        for row_index,row in enumerate(game_map.get_matrix()):
#            for col_index, col in enumerate(row):
#                display_surface = pygame.display.get_surface()
#                x = col_index * game_map.tile_size
#                y = row_index * game_map.tile_size
#                grass = Grass((x,y))
#                display_surface.blit(grass.image, grass.rect.topleft - self.camara_off)



    def input(self):
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
        self.input()

