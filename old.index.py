import pygame
import sys
               #THIS WAS TRIAL WINDOW
pygame.init()
screen=pygame.display.set_mode((1600,900))
pygame.display.set_caption('TRIAL WINDOW')
clock = pygame.time.Clock()
test_font = pygame. font. Font('Font/ARCADECLASSIC.TTF',100) #small font - size:30 ,x=300
                                                                       # large font - size:50 ,x=295
sky_surface = pygame.image.load('Graphics/Battleground3.png').convert()
text_surface = test_font.render('Game Jam',False,"cyan")

hero_one = pygame.image.load('Graphics/Sprites/run5_new.png').convert_alpha() # hero size 50 x70
hero_x_pos =0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface,(0,0))
    screen.blit(text_surface,(595,50))
    hero_x_pos +=4
    if hero_x_pos > 1500: hero_x_pos = -300    #hero runs to end and starts again
    screen.blit(hero_one,(hero_x_pos,280))

    #update everything
    pygame.display.update()
    clock.tick(60)
