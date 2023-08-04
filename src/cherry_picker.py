import pygame, sys
import settings  
from level_render import *

class Game:
    def __init__(self): 
        
        pygame.init()
        # Get resolution of the screen
        infoObject = pygame.display.Info()
        settings.init(infoObject.current_w, infoObject.current_h)
        # Initialize setting object
        # Generate a screen
        self.screen = pygame.display.set_mode((settings.game_map.screen_width-5, settings.game_map.screen_height-20))
        self.clock = pygame.time.Clock()
        # Initialize the rendering class
        self.level = LevelRender(settings.game_map)
        pygame.display.set_caption('CherryPicker')
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill('black')
            self.level.update_map()
            pygame.display.update()
            self.clock.tick(settings.FPS)
if __name__ == '__main__':
    game = Game()
    game.run()
