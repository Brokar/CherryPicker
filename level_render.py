import pygame
from settings import *
from player import *

class LevelRender:
    """ This class is incharge of rendering the game level 
        using pygame framework. Normally, it will be updated
        with the FPS frequency.
    """    
    def __init__(self,screen,map):
        # Get the display surface

        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.grasses = pygame.sprite.Group()
        self.initialise_map_render(screen,map)

    def initialise_map_render(self, screen, map):
        # update and draw the map in the screen
        # Render obstacles

        for row_index, row in enumerate (map[0]):
            for col_index, col in enumerate(row):
                x = col_index*tile_size
                y = row_index*tile_size
                grass_patch = Grass ([x,y])
                self.grasses.add(grass_patch)
                if map[0][row_index][col_index]==1:
                    cherrytree = CherryTree([x,(y+tile_size)])
                    self.visible_sprites.add(cherrytree)
                if map[2][row_index][col_index]==1:
                    player=Player([x,y])
                    self.visible_sprites.add(player)
        self.grasses.update()
        self.grasses.draw(screen)
        self.visible_sprites.update(map)
        self.visible_sprites.draw(screen)
        # Render interact_obj and player
        pass

    def update_map_render (self, screen, map):
        self.grasses.update()
        self.grasses.draw(screen)
        self.visible_sprites.update(map)
        self.visible_sprites.draw(screen)

class Grass (pygame.sprite.Sprite):
    def __init__(self, position):
        # Get the display surface
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Tiles\grass.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (position[0], position[1]))
         

class CherryTree (pygame.sprite.Sprite):
    def __init__(self, position):
        # Get the display surface
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Tiles\\fullbush.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (position[0], position[1]))    

