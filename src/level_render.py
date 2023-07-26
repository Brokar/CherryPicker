import pygame
import settings
from tile import Grass, Object
from player import Player#, interact_obj

class LevelRender:
    """ This class is incharge of rendering the game level 
        using pygame framework. Normally, it will be updated
        with the FPS frequency.
    """    
    def __init__(self, game_map ):
        # Get the display surface
        self.display_surface = pygame.display.get_surface()
        
        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.init_map(game_map)

    def init_map(self, game_map):
        for row_index,row in enumerate(game_map.get_matrix()):
            for col_index, col in enumerate(row):
                x = col_index * game_map.tile_size
                y = row_index * game_map.tile_size
                if col == 'x':
                    Object((x,y),[self.visible_sprites,self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites ) 
    
    def update_map(self):
        # update and draw the map in the screen
        # Render obstacles
        # Render interact_obj and player
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        pass


          

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup 
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self,player):

        # getting the offset 
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        self.draw_background(settings.game_map)
        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)


    def draw_background(self, game_map):
        # TODO: Change to a less complex rendering
        for row_index,row in enumerate(game_map.get_matrix()):
            for col_index, col in enumerate(row):
                display_surface = pygame.display.get_surface()
                x = col_index * game_map.tile_size
                y = row_index * game_map.tile_size
                grass = Grass((x,y))
                display_surface.blit(grass.image, grass.rect.topleft - self.offset)


