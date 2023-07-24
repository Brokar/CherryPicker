import pygame
from settings import *
#import tiles, player, interact_obj

class LevelRender:
    """ This class is incharge of rendering the game level 
        using pygame framework. Normally, it will be updated
        with the FPS frequency.
    """    
    def __init__(self):
        # Get the display surface

        self.display_surface = pygame.display.get_surface()


    def render_map(self, screen, map):
        # update and draw the map in the screen
        # Render obstacles
        grasses = pygame.sprite.Group()
        cherry_trees = pygame.sprite.Group()
        for row_index, row in enumerate (map[0]):
            for col_index, col in enumerate(row):
                x = col_index*tile_size
                y = row_index*tile_size
                grass_patch = Grass ([x,y])
                grasses.add(grass_patch)
                if map[0][row_index][col_index]==1:
                    lowcherrytree = LowCherryTree([x,y])
                    upcherrytree = UpCherryTree([x,(y+1)])
                    cherry_trees.add(lowcherrytree)
                    cherry_trees.add(upcherrytree)
        print (grasses)
        grasses.update()
        grasses.draw(screen)
        cherry_trees.update()
        cherry_trees.draw(screen)
                

        
      
        # Render interact_obj and player
        pass

class Grass (pygame.sprite.Sprite):
    def __init__(self, position):
        # Get the display surface
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Tiles\grass.png')
        self.rect = self.image.get_rect(topleft = (position[0], position[1]))

class LowCherryTree (pygame.sprite.Sprite):
    def __init__(self, position):
        # Get the display surface
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Tiles\lowbush.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (position[0], position[1]))          

class UpCherryTree (pygame.sprite.Sprite):
    def __init__(self, position):
        # Get the display surface
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Tiles\grass.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (position[0], position[1]))        
