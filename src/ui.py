import pygame
import settings
from settings import  UI_FONT_SIZE, UI_CHERRY_POSITION, UI_CHERRY_WIDTH, UI_CHERRY_HEIGHT 
from os import path
class UI:
    def __init__(self):
		
		# general 
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(pygame.font.get_default_font(),UI_FONT_SIZE)
        self.cherry_image = pygame.image.load(path.join("..","tiles","cherry.png")).convert_alpha()
        self.cherry_image = pygame.transform.scale(self.cherry_image,(80,80))
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
		# bar setup 
    def score_counter(self,player):
        cherry_rect = self.cherry_image.get_rect(topleft=(UI_CHERRY_POSITION,UI_CHERRY_POSITION))

        cherry_number=player.get_cherries()
        text_cherry="X "+str(cherry_number)
        text_surf = self.font.render(text_cherry, False, "white")
        text_rect = text_surf.get_rect(topleft=cherry_rect.topright)

        box_width=cherry_rect.width+text_rect.width + UI_CHERRY_WIDTH 
        interface_rect=(0,0,box_width,cherry_rect.height + UI_CHERRY_HEIGHT)
        pygame.draw.rect(self.display_surface,"royalblue",interface_rect)
        self.display_surface.blit(self.cherry_image,cherry_rect)
        self.display_surface.blit(text_surf,text_rect)
    def show_pause_menu(self):
       # horizontal position
        menu_width = self.display_surface.get_size()[0]*0.7
        left = self.display_surface.get_size()[0]*0.1
        # vertical position 
        menu_height = self.display_surface.get_size()[1] * 0.7
        top = self.display_surface.get_size()[1] * 0.1
        
        menu_rect = pygame.Rect(left,top,menu_width,menu_height)

        text_surf = self.font.render("Paused", False, "white")
        text_rect = (menu_width/2+left,menu_height/2)
        pygame.draw.rect(self.display_surface,"grey",menu_rect)
        self.display_surface.blit(text_surf,text_rect)
    def show_game_over_menu(self):
       # horizontal position
        menu_width = self.display_surface.get_size()[0]*0.7
        left = self.display_surface.get_size()[0]*0.1
        # vertical position 
        menu_height = self.display_surface.get_size()[1] * 0.7
        top = self.display_surface.get_size()[1] * 0.1
        
        menu_rect = pygame.Rect(left,top,menu_width,menu_height)

        text_surf = self.font.render("Game over", False, "white")
        text_rect = (menu_width/2+left,menu_height/2)
        pygame.draw.rect(self.display_surface,"grey",menu_rect)
        self.display_surface.blit(text_surf,text_rect)
    def show_menu(self, game_state):
        if( game_state == settings.GameStates.PAUSED):
            self.show_pause_menu()
        if( game_state == settings.GameStates.GAME_OVER):
            self.show_game_over_menu()
    def display(self,player, game_state):
        self.score_counter(player)
        self.show_menu(game_state)
