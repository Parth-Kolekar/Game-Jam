import pygame
import sys

pygame.init()
screen=pygame.display.set_mode((800,500))
pygame.display.set_caption('VSGP MARIO LITE')
clock = pygame.time.Clock()
test_font = pygame. font. Font('Font/ARCADECLASSIC.TTF',50) #small font - size:30 ,x=300
                                                                       # large font - size:50 ,x=265
sky_surface = pygame.image.load('Graphics/gb3.jpg')
text_surface = test_font.render('Lord Gaurav',False,"cyan")

hero_one = pygame.image.load('Graphics/Sprites/he2.jpg') # hero size 50 x70

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface,(0,0))
    screen.blit(text_surface,(265,50))
    screen.blit(hero_one,(0,300))


    #draw all our elements
    #update every fucking thing
    pygame.display.update()
    clock.tick(60)
