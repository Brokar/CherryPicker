import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self,position,obstacle_sprites):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Tiles\\player1front.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (position[0], position[1]))
        self.direction = pygame.math.Vector2()
        self.speed = 1
        self.position = position
        self.status = "down"
        self.import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.001
        self.k_yet_press = False
        self.obstacle_sprites = obstacle_sprites
        self.contact_dict = {"trees":[],"obstacle":[]}
        self.number_cherries = 0


    def input(self):
        
        keys = pygame.key.get_pressed()
        # Movement Input
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
                    self.pick()
                self.k_yet_press=True
                
        else:
            self.k_yet_press=False



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



    def move(self):
        global map
        self.rect.topleft += self.direction*self.speed*tile_size
        map[2][int(self.position[1]/tile_size)][int(self.position[0]/tile_size)]-=1
        
        self.position += self.direction*self.speed*tile_size
        map[2][int(self.position[1]/tile_size)][int(self.position[0]/tile_size)]+=1
        



    def pick(self):
        pass

    def import_player_assets(self):
        #import assets for animation
        character_path = "./Tiles/Player/"
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "right_idle": [], "left_idle": [], "up_idle": [], "down_idle":[],
        }       

        for animation in self.animations.keys():
            full_path = character_path + animation
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
        global map
        #x and y order is inverted in the map
        xposition_matrix=int(self.position[0]/tile_size)
        yposition_matrix=int(self.position[1]/tile_size)
        self.contact_dict = {"trees":[],"obstacle":[]}
        if yposition_matrix==len(map[0])-1:
            self.contact_dict["obstacle"].append("down")
        elif map[0][(yposition_matrix+1)][xposition_matrix]==1:
            self.contact_dict["trees"].append("down")
        if yposition_matrix==0:
            self.contact_dict["obstacle"].append("up")
        elif map[0][(yposition_matrix-1)][xposition_matrix]==1:
            self.contact_dict["trees"].append("up")
        if xposition_matrix==len(map[0][0])-1:
            self.contact_dict["obstacle"].append("right")
        elif map[0][yposition_matrix][(xposition_matrix+1)]==1:
            self.contact_dict["trees"].append("right")
        if xposition_matrix==0:
            self.contact_dict["obstacle"].append("left")
        elif map[0][yposition_matrix][(xposition_matrix-1)]==1:
            self.contact_dict["trees"].append("left")
        

    def update(self):
        #self.input_diagonale()
        self.contact()
        self.input()
        self.get_status()
        self.animate()
        self.move()