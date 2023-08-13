from os import path
import pygame 
import settings

class CherryTree(pygame.sprite.Sprite):
    def __init__(self,pos,groups, tree_id):
        super().__init__(groups)
        self.image = pygame.image.load(path.join("..", "tiles","fullbush.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        # Get the display surface
        self.tree_id = tree_id
        self.fruit = "cherry"  
    def empty_tree(self):
        self.fruit = "empty"
        self.image = pygame.image.load(path.join("..","tiles","emptybush.png")).convert_alpha()



class Grass(pygame.sprite.Sprite):
    def __init__(self,pos, groups):
        super().__init__(groups)
        image = pygame.image.load(path.join("..", "tiles", "grass.png")).convert_alpha()
        tile_size = settings.game_map.tile_size
        self.image = pygame.transform.scale(image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft = pos)

