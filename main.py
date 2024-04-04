import pygame, sys
from settings import *
from level import Level
from overworld import Overworld

class Game:
    def __init__(self):
        self.max_level = 0
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld)
        self.status = 'level'
        
    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()

# Pygame set up  
pygame.init()
pygame.display.set_caption('Game Jam')

# Add ",pygame.FULLSCREEN" for fullscreen mode
screen = pygame.display.set_mode((screen_width,screen_height))

# Loading and scaling the background image
background_img = pygame.image.load('graphics/background/layers/grassy_mountain_combined.png').convert()
scaled_background = pygame.transform.scale(background_img, (screen_width, screen_height))

# Initialize the clock
clock = pygame.time.Clock()

# Creating Game instance
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(scaled_background,(0,0))
    game.run()
    pygame.display.update()
    clock.tick(60)