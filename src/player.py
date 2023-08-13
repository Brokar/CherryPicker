import pygame
from os import path
import settings
from debug import debug
from support import import_folder
import random

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups, obstacle_sprite_table):
        super().__init__(groups)
        self.image = pygame.image.load(path.join("..", "tiles","player", 
                                                 "down_idle","down_idle.png")).convert_alpha()
        self.character_path = path.join("..","tiles", "player")
        self.rect = self.image.get_rect(topleft = pos)
        # Game position
        self.position = pos 
        # Direction for changing position
        self.direction = pygame.math.Vector2()
        self.speed = 1
        self.k_yet_press = False
        self.obstacle_sprite_table = obstacle_sprite_table
        self.status = "down"
        self.stamina = settings.DEFAULT_STAMINA 
        self.contact_dict = {"up":"","down":"", "left":"", "right":""}
        self.frame_index = 0
        self.animation_speed = 0.001     
        self.basket_content = []
        self.player_id=settings.TypePlayer.PLAYER
        self.import_player_assets()
        
    def restore_stamina(self):
        self.stamina = settings.DEFAULT_STAMINA

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
        if (keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_RIGHT] 
                            or keys[pygame.K_LEFT] or keys [pygame.K_SPACE]):
            if not self.k_yet_press:
                print(self.contact_dict)
                
                if keys[pygame.K_UP] and not self.contact_dict["up"]:
                    self.direction[:] = 0,-1
                    self.status = "up"
                elif keys[pygame.K_DOWN] and not self.contact_dict["down"]:
                    self.direction[:] = 0,1
                    self.status = "down"
                elif keys[pygame.K_RIGHT] and not self.contact_dict["right"]:
                    self.direction[:] = 1,0
                    self.status = "right"
                elif keys[pygame.K_LEFT] and not self.contact_dict["left"]:
                    self.direction[:] = -1,0
                    self.status = "left"
                elif keys [pygame.K_SPACE] and "cherry" in self.contact_dict.values():
                    self.pick()
                self.k_yet_press=True
                
                
        else:
            self.k_yet_press=False



    def move(self):
        self.rect.topleft += self.direction * self.speed * settings.game_map.tile_size 
        settings.game_map.players_map[int(self.position[1]/settings.game_map.tile_size)][int(self.position[0]/settings.game_map.tile_size)]-=self.player_id
        self.position += self.direction * self.speed * settings.game_map.tile_size
        settings.game_map.players_map[int(self.position[1]/settings.game_map.tile_size)][int(self.position[0]/settings.game_map.tile_size)]+=self.player_id
        if(self.direction != (0,0)):
            self.stamina=self.stamina-1
        


    def pick(self):
        inflated=self.rect.inflate(4,4)
        for  _,sprites in self.obstacle_sprite_table.items():
            if inflated.colliderect(sprites.rect):
                if sprites.fruit=="cherry":
                    self.basket_content.append(sprites.fruit)
                    sprites.empty_tree()

    
    def import_player_assets(self):
        #import assets for animation
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "right_idle": [], "left_idle": [], "up_idle": [], "down_idle":[],
        }       
        for animation in self.animations.keys():
            full_path = path.join(self.character_path,animation)
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
        pygame.time.wait(30)
        # Set the image
        self.image = animation[int(self.frame_index)]
        #to add intermadiate position for animation
        self.rect = self.image.get_rect(topleft = (self.position[0], self.position[1]))

    def contact(self):
        #x and y order is inverted in the settings.game_map.game_map
        xposition_matrix=int(self.position[0]/settings.game_map.tile_size)
        yposition_matrix=int(self.position[1]/settings.game_map.tile_size)
        self.contact_dict = {"up":"","down":"", "left":"", "right":""}
        if yposition_matrix==settings.game_map.map_height-1:
            self.contact_dict["down"]="obstacle"
        elif settings.game_map.obstacles_map[(yposition_matrix+1)][xposition_matrix]!=0:
            self.contact_dict["down"]=self.get_obstacle((yposition_matrix+1),xposition_matrix).fruit
        if yposition_matrix==0:
            self.contact_dict["up"]="obstacle"
        elif settings.game_map.obstacles_map[(yposition_matrix-1)][xposition_matrix]!=0:
            self.contact_dict["up"]=self.get_obstacle((yposition_matrix-1),xposition_matrix).fruit
        if xposition_matrix==settings.game_map.map_width-1:
            self.contact_dict["right"]="obstacle"
        elif settings.game_map.obstacles_map[yposition_matrix][(xposition_matrix+1)]!=0:
            self.contact_dict["right"]=self.get_obstacle((yposition_matrix),xposition_matrix+1).fruit
        if xposition_matrix==0:
            self.contact_dict["left"]="obstacle"
        elif settings.game_map.obstacles_map[yposition_matrix][(xposition_matrix-1)]!=0:
            self.contact_dict["left"]=self.get_obstacle((yposition_matrix),xposition_matrix-1).fruit
    
    def get_obstacle(self,xposition,yposition):
        reference=int(settings.game_map.obstacles_map[xposition][yposition])
        return self.obstacle_sprite_table[reference]


    def update(self):
        """ It is only allowed to update 
            the player when he has stamina
        """
        if self.stamina > 0:
            self.contact()
            self.input()
            self.get_status()
            self.animate()
            self.move()

class Bot(Player):
    """ Bot is a type of player wich doesn't have its input controlled my 
        the keyboard
    """
    def __init__(self,pos,groups, obstacle_sprite_table, reference_id):
        super().__init__(pos,groups, obstacle_sprite_table)
        print(self.image)
        self.player_id = reference_id 
        # Bot uses override attributes as image or stamina
        self.image = pygame.image.load(path.join("..", "tiles","bot","down_idle","down_idle.png")).convert_alpha()
        self.character_path = path.join("..","tiles", "bot")
        self.rect = self.image.get_rect(topleft = pos)
        self.import_player_assets()
        self.stamina = 0
    def input(self):
        """ input method is overriden 
        """

        self.direction.x = 0
        self.direction.y = 0
        # Enter options
        possibilities=[]
        if "cherry" in self.contact_dict.values():
            self.pick()
        else:
            if not self.contact_dict["up"]:
                possibilities.append("up")
            if not self.contact_dict["down"]:
                possibilities.append("down")
            if not self.contact_dict["right"]:
                possibilities.append("right")
            if  not self.contact_dict["left"]:
                possibilities.append("left")
            random_direction = random.sample(possibilities,1)
            if random_direction[0]=="up":
                self.direction[:] = 0,-1
                self.status = "up"
            if random_direction[0]=="down":
                self.direction[:] = 0,1
                self.status = "down"
            if random_direction[0]=="right":
                self.direction[:] = 1,0
                self.status = "right"
            if random_direction[0]=="left":
                self.direction[:] = -1,0
                self.status = "left"
