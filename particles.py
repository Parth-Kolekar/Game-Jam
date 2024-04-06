import pygame
from support import import_folder

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type, enemy_speed):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.18
        if type == 'enemy_death':
            self.frames = import_folder('graphics/entities/Rogue/Death')
            if enemy_speed < 0:
                for i in range(len(self.frames)):
                    self.frames[i] = pygame.transform.flip(self.frames[i], True, False)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
    
    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift