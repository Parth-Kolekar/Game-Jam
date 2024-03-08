import pygame, sys
from settings import *
from level import Level
from game_data import level_0

#pygame set up
pygame.init()
pygame.display.set_caption('Game Jam')

#add ",pygame.FULLSCREEN" for fullscreen mode
screen = pygame.display.set_mode((screen_width,screen_height), pygame.FULLSCREEN)

background_img = pygame.image.load('graphics/background/layers/grassy_mountain_combined.png').convert()
scaled_background = pygame.transform.scale(background_img, (screen_width, screen_height))

#### Unused code for scrolling parallax backgorund #########################
bg_images = []
for i in range (1,6):
    bg_image = pygame.image.load(f"graphics/background/glacial_mountain/bg_layer_{i}.png").convert_alpha()
    scaled_bg = pygame.transform.scale(bg_image, (screen_width, screen_height))
    bg_images.append(scaled_bg)

bg_width = bg_images[0].get_width()

def draw_bg(bg_scroll):
    for x in range(5):
        speed = 1
        for i in bg_images:
            screen.blit(i, ((x * bg_width) - bg_scroll * speed ,0))
            speed += 0.5
############################################################################
            
clock = pygame.time.Clock()
level = Level(level_0, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(scaled_background,(0,0))
    #bg_scroll = level.world_shift   #unused for scrolling background
    #draw_bg(bg_scroll)              #unused for scrolling background
    level.run()

    pygame.display.update()
    clock.tick(60)