import pygame
class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        self.rect = self.image.get_rect(topleft = pos)
        self.image = pygame.Surface((size,))
        self.image.fill('green')