from os import path
import pygame 
import settings
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_id):
        super().__init__(groups)
        self.pos = pos
        self.obs_id = obstacle_id
        self.fruit = "obstacle"
    def get_type(self):
        handler = self.obs_id & settings.HANDLER_MASK 
        if handler ==  settings.TREE_HANDLER:
            return settings.TREE_HANDLER if self.fruit == "cherry" else settings.TREE_EMPTY
        elif handler == settings.ROCK_HANDLER:
            return settings.ROCK_HANDLER
        else:
            return 0

class CherryTree(Obstacle):
    def __init__(self,pos,groups, tree_id):
        super().__init__(pos,groups, tree_id)
        self.image = pygame.image.load(path.join("..", "tiles","fullbush.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        # Get the display surface
        self.fruit = "cherry"  
    def empty_tree(self):
        self.fruit = "empty"
        self.image = pygame.image.load(path.join("..","tiles","emptybush.png")).convert_alpha()

class Rock(Obstacle):
    def __init__(self,pos,groups, rock_id):
        super().__init__(pos,groups,rock_id)
        self.image = pygame.image.load(path.join("..", "tiles","rock.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        # Get the display surface
        self.fruit = "obstacle"      


class Grass(pygame.sprite.Sprite):
    def __init__(self,pos, groups):
        super().__init__(groups)
        image = pygame.image.load(path.join("..", "tiles", "grass.png")).convert_alpha()
        tile_size = settings.game_map.tile_size
        self.image = pygame.transform.scale(image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft = pos)

