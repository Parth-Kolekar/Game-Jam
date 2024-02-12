import pygame, sys
from settings import *
from tiles import Tile
from level import Level

#pygame set up
pygame.init()
pygame.display.set_caption('Game Jam') #added on my own

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
level = Level(level_map,screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('sky blue')
    level.run()

    pygame.display.update()
    clock.tick(60)