import pygame
from tiles import AnimatedTile
from random import randint
from support import import_folder

class Enemy(AnimatedTile):
    def __init__(self, size, x, y,):
        super().__init__(size, x, y, 'graphics/entities/Rogue/Run')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(3,5)
        self.attacking = False
        self.attack_frames = import_folder('graphics/entities/Rogue/Attack')

    def play_attack_animation(self):
        self.attacking = True
        self.frame_index = 0

    def animate_attack(self):
        self.frame_index += 0.15
        if int(self.frame_index) >= len(self.attack_frames):
            self.frame_index = 0
            self.attacking = False
        self.image = self.attack_frames[int(self.frame_index)]

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        if self.attacking:
            self.animate_attack()
        else:
            self.animate()
        self.move()
        self.reverse_image()