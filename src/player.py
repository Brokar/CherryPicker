import pygame
from os import path
import settings
from debug import debug

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(path.join("..", "tiles", "player1front.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
         
        self.direction = pygame.math.Vector2()
        self.speed = 1
        self.k_yet_press = False
        self.obstacle_sprites = obstacle_sprites
    
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            if not self.k_yet_press:
                if keys[pygame.K_UP]:
                    self.direction.y = -1
                elif keys[pygame.K_DOWN]:
                    self.direction.y = 1 

                if keys[pygame.K_RIGHT]:
                    self.direction.x = 1 
                elif keys[pygame.K_LEFT]:
                    self.direction.x = -1
                self.k_yet_press=True
        else:
            self.k_yet_press=False

    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed * settings.game_map.tile_size 
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed * settings.game_map.tile_size
        self.collision('vertical')

    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: # moving right
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: # moving down
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: # moving up
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.input()
        self.move(self.speed)
