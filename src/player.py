import pygame
from os import path
import settings
from debug import debug
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(path.join("..", "tiles", "player1front.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        # Game position
        self.position = pos 
        # Direction for changing position
        self.direction = pygame.math.Vector2()
        self.speed = 1
        self.k_yet_press = False
        self.obstacle_sprites = obstacle_sprites
        self.status = "down"
        self.import_player_assets()
        self.contact_dict = {"trees":[],"obstacle":[]}
        self.frame_index = 0
        self.animation_speed = 0.001

    def set_pos(self, pos):
        self.position = pos
    
    def get_pos(self):
        return self.position
    
    def reset_pos(self):
        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0
        # Debounce check
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys [pygame.K_SPACE]:
            if not self.k_yet_press:
                if keys[pygame.K_UP] and "up" not in self.contact_dict["trees"] and "up" not in self.contact_dict["obstacle"]:
                    self.direction[:] = 0,-1
                    self.status = "up"
                elif keys[pygame.K_DOWN] and "down" not in self.contact_dict["trees"] and "down" not in self.contact_dict["obstacle"]:
                    self.direction[:] = 0,1
                    self.status = "down"
                elif keys[pygame.K_RIGHT] and "right" not in self.contact_dict["trees"] and "right" not in self.contact_dict["obstacle"]:
                    self.direction[:] = 1,0
                    self.status = "right"
                elif keys[pygame.K_LEFT] and "left" not in self.contact_dict["trees"] and "left" not in self.contact_dict["obstacle"]:
                    self.direction[:] = -1,0
                    self.status = "left"
                elif keys [pygame.K_SPACE] and self.contact_dict["trees"]:
                    self.pick(self.obstacle_sprites)
                self.k_yet_press=True
                
        else:
            self.k_yet_press=False

    def move(self,speed):

        self.rect.topleft += self.direction * speed * settings.game_map.tile_size 
        settings.game_map.game_map[2][int(self.position[1]/settings.game_map.tile_size)][int(self.position[0]/settings.game_map.tile_size)]-=1
        self.position += self.direction * speed * settings.game_map.tile_size
        settings.game_map.game_map[2][int(self.position[1]/settings.game_map.tile_size)][int(self.position[0]/settings.game_map.tile_size)]+=1
        print(self.direction)

    def pick(self,obstacle_sprites):
        inflated=self.rect.inflate(4,4)
        for sprites in obstacle_sprites:
            if inflated.colliderect(sprites.rect):
                if sprites.fruit=="cherry":
#                    self.basket_content.append(sprites.fruit)
                    sprites.empty_tree()

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
    
    def import_player_assets(self):
        #import assets for animation
        character_path = path.join("..","tiles","Player")
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "right_idle": [], "left_idle": [], "up_idle": [], "down_idle":[],
        }       

        for animation in self.animations.keys():
            full_path = path.join(character_path,animation)
            self.animations[animation] = import_folder(full_path)
    def get_status(self):
        # Idle Status
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status:
                self.status = self.status + "_idle"

    def animate(self):
        animation = self.animations[self.status]
        # Loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        pygame.time.wait(50)
        # Set the image
        self.image = animation[int(self.frame_index)]
        #to add intermadiate position for animation
        self.rect = self.image.get_rect(topleft = (self.position[0], self.position[1]))

    def contact(self):
        #x and y order is inverted in the settings.game_map.game_map
        xposition_matrix=int(self.position[0]/settings.game_map.tile_size)
        yposition_matrix=int(self.position[1]/settings.game_map.tile_size)
        self.contact_dict = {"trees":[],"obstacle":[]}
        if yposition_matrix==len(settings.game_map.game_map[0])-1:
            self.contact_dict["obstacle"].append("down")
        elif settings.game_map.game_map[0][(yposition_matrix+1)][xposition_matrix]==1:
            self.contact_dict["trees"].append("down")
        if yposition_matrix==0:
            self.contact_dict["obstacle"].append("up")
        elif settings.game_map.game_map[0][(yposition_matrix-1)][xposition_matrix]==1:
            self.contact_dict["trees"].append("up")
        if xposition_matrix==len(settings.game_map.game_map[0][0])-1:
            self.contact_dict["obstacle"].append("right")
        elif settings.game_map.game_map[0][yposition_matrix][(xposition_matrix+1)]==1:
            self.contact_dict["trees"].append("right")
        if xposition_matrix==0:
            self.contact_dict["obstacle"].append("left")
        elif settings.game_map.game_map[0][yposition_matrix][(xposition_matrix-1)]==1:
            self.contact_dict["trees"].append("left")

    def update(self):
        self.contact()
        self.input()
        self.get_status()
        self.animate()
        self.move(self.speed)
