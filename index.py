import pygame
import sys #pygame. font. SysFont()

pygame.init()
screen=pygame.display.set_mode((800,500))
pygame.display.set_caption('VSGP MARIO LITE')
clock = pygame.time.Clock()
test_font = pygame. font. SysFont(None,50)

sky_surface = pygame.image.load('Graphics/gb3.jpg')
text_surface = test_font.render('Lord Gaurav',False,"cyan")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface,(0,0))
    screen.blit(text_surface,(300,50))
    #draw all our elements
    #update every fucking thing
    pygame.display.update()
    clock.tick(60)
