import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Tiles\\player1front.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (position[0], position[1]))
        self.direction = pygame.math.Vector2()
        # self.direction = (0,0,32,32)
        self.speed = 1 
        self.position = position

    def input(self):
        
        keys = pygame.key.get_pressed()
        # Movement Input
        if keys[pygame.K_UP]:
            self.direction = 0,-1
            self.status = "up"
        elif keys[pygame.K_DOWN]:
            self.direction = 0,1
            self.status = "down"
        elif keys[pygame.K_RIGHT]:
            self.direction = 1,0
            self.status = "right"
        elif keys[pygame.K_LEFT]:
            self.direction = -1,0
            self.status = "left"
        else:
            self.direction = (0,0,32,32)
        # Attack Input
        if keys [pygame.K_SPACE]:
            self.pick(pos)

    def input_diagonale(self):
        
        keys = pygame.key.get_pressed()
        # Movement Input
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = "down"
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = "right"
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "left"
        else:
            self.direction.x = 0
            self.direction.y = 0
        # Attack Input
        if keys [pygame.K_SPACE]:
            self.pick(pos)

    def update(self,map):
        self.input_diagonale()
        self.move(map)

    def move(self,map):
        print(type(self.direction))
        self.rect.topleft += self.direction*self.speed
        print(self.rect)
        map[2][int(self.position[0]/tile_size)][int(self.position[1]/tile_size)]-=1
        self.position += self.direction*self.speed
        map[2][int(self.position[0]/tile_size)][int(self.position[1]/tile_size)]+=1


    def pick(position):
        pass
