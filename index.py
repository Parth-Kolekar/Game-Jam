import pygame
from sys import exit

pygame.init()
screen=pygame.display.set_mode((800,500))
pygame.display.set_caption('VSGP MARIO LITE')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #draw all our elements
    #update every fucking thing
    pygame.display.update()
