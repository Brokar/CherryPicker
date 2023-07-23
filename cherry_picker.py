import pygame, sys
from settings import *
from level_render import *
from engine import *

class Game:
    def __init__(self): 
        
        pygame.init()
        # Get resolution of the screen
        infoObject = pygame.display.Info()
        # Initialize setting object
        self.settings = GameSettings(infoObject.current_w, infoObject.current_h) 
        # Generate a screen
        self.screen = pygame.display.set_mode(((self.settings.width-30), (self.settings.height-30)))
        self.clock = pygame.time.Clock()
        # Initialize the rendering class
        self.level = LevelRender()
        pygame.display.set_caption('Cherry picker')

    def run(self):
        map = initialise_map (3,map_length,map_height,5)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill('black')
            self.level.render_map()
            pygame.display.update()
            self.clock.tick(FPS)
if __name__ == '__main__':
    game = Game()
    game.run()