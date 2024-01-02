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

		# bar setup 
    def score_counter(self,player):
        top=settings.game_map.map_height*settings.game_map.tile_size

        cherry_rect = self.cherry_image.get_rect(topleft=(UI_CHERRY_POSITION,top+UI_CHERRY_POSITION))

        cherry_number=player.get_cherries()
        text_cherry="X "+str(cherry_number)
        text_surf = self.font.render(text_cherry, False, "white")
        text_rect = text_surf.get_rect(topleft=cherry_rect.topright)

        box_width=cherry_rect.width+text_rect.width + UI_CHERRY_WIDTH 
        interface_rect=(0,top,box_width,cherry_rect.height + UI_CHERRY_HEIGHT)
        pygame.draw.rect(self.display_surface,"royalblue",interface_rect)
        self.display_surface.blit(self.cherry_image,cherry_rect)
        self.display_surface.blit(text_surf,text_rect)
    def show_pause_menu(self):
        top=settings.game_map.map_height*settings.game_map.tile_size

        cherry_rect = self.cherry_image.get_rect(topleft=(UI_CHERRY_POSITION,top+UI_CHERRY_POSITION))
        text_surf = self.font.render("Pause", False, "white")
        text_rect = text_surf.get_rect(topleft=cherry_rect.topright)

        box_width=cherry_rect.width+text_rect.width + UI_CHERRY_WIDTH 
        interface_rect=(0,top,box_width,cherry_rect.height + UI_CHERRY_HEIGHT)
        pygame.draw.rect(self.display_surface,"royalblue",interface_rect)
        self.display_surface.blit(self.cherry_image,cherry_rect)
        self.display_surface.blit(text_surf,text_rect)
    def show_menu(self, game_state):
        if( game_state == settings.GameStates.PAUSED):
            self.show_pause_menu()
    def display(self,player, game_state):
        self.score_counter(player)
        self.show_menu(game_state)
