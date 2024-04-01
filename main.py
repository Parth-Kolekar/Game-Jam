import pygame, sys
from settings import *
from level import Level
from game_data import level_0

#pygame set up
pygame.init()
pygame.display.set_caption('Game Jam')

#add ",pygame.FULLSCREEN" for fullscreen mode
screen = pygame.display.set_mode((screen_width,screen_height))

background_img = pygame.image.load('graphics/background/layers/grassy_mountain_combined.png').convert()
scaled_background = pygame.transform.scale(background_img, (screen_width, screen_height))

clock = pygame.time.Clock()
level = Level(level_0, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(scaled_background,(0,0))
    level.run()
    pygame.display.update()
    clock.tick(60)