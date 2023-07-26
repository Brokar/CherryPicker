from os import times_result
import pygame 
import settings

class Object(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.image = pygame.image.load('../tiles/empybush.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)

class Bot(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.image = pygame.image.load('../tiles/lowbush.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)

class Grass(pygame.sprite.Sprite):
	def __init__(self,pos):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load('../tiles/grass.png').convert_alpha()
		tile_size = settings.game_map.tile_size
		self.image = pygame.transform.scale(image, (tile_size, tile_size))
		self.rect = self.image.get_rect(topleft = pos)
