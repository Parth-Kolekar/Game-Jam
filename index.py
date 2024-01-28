import pygame
import sys

pygame.init()
screen=pygame.display.set_mode((800,500))
pygame.display.set_caption('VSGP MARIO LITE')
clock = pygame.time.Clock()
test_font = pygame. font. Font('Font/ARCADECLASSIC.TTF',50) #small font - size:30 ,x=300
                                                                       # large font - size:50 ,x=265
sky_surface = pygame.image.load('Graphics/Battleground3Resize.jpg').convert()
text_surface = test_font.render('Game Jam',False,"cyan")

hero_one = pygame.image.load('Graphics/Sprites/run5.png').convert_alpha() # hero size 50 x70
hero_x_pos =0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface,(0,0))
    screen.blit(text_surface,(265,50))
    hero_x_pos +=4
    if hero_x_pos > 900: hero_x_pos = 0
    screen.blit(hero_one,(hero_x_pos,300))


    #draw all our elements
    #update every fucking thing
    pygame.display.update()
    clock.tick(60)
