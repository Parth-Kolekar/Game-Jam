import pygame, sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI

class Game:
    def __init__(self):

        # Game attributes
        self.max_level = 0
        self.max_health = 100
        self.current_health = 100

        # Overworld creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'

        # User interface
        self.ui = UI(screen)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_health)
        self.current_health = 100
        self.status = 'level'
        
    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def change_health(self, amount):
        self.current_health += amount

    def check_game_over(self):
        if self.current_health <= 0:
            self.current_health = 100
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.check_game_over()

# Pygame set up  
pygame.init()
pygame.display.set_caption('Game Jam')

# Add "pygame.FULLSCREEN" arguement for fullscreen mode
screen = pygame.display.set_mode((screen_width,screen_height))

# Loading and scaling the background image
background_img = pygame.image.load('graphics/background/layers/grassy_mountain_combined.png').convert_alpha()
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
