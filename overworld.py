import pygame
from game_data import levels
import sys

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, node_graphics):
        super().__init__()
        self.image = pygame.image.load(node_graphics).convert_alpha()
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        if not self.status == 'available':
            tint_surf = self.image.copy()
            tint_surf.fill('black', None, pygame.BLEND_RGB_MULT)
            self.image.blit(tint_surf, (0,0))

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('graphics/overworld/cursor.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)

class Overworld:
    def __init__(self, start_level, max_level, surface, create_level):

        # Setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level
        self.moving = False

        # Sprites
        self.setup_nodes()
        self.setup_icon()
    
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite  = Node(node_data['node_pos'], 'available', node_data['node_graphics'])
            else:
                node_sprite  = Node(node_data['node_pos'], 'locked', node_data['node_graphics'])
            self.nodes.add(node_sprite)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        current_node_rect = self.nodes.sprites()[self.current_level].rect
        icon_sprite = Icon(current_node_rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
            if not self.moving:
                self.current_level += 1
                self.moving = True
        elif keys[pygame.K_LEFT] and self.current_level > 0:
            if not self.moving:
                self.current_level -= 1
                self.moving = True
        else:
            self.moving = False

        if keys[pygame.K_RETURN]:
            self.create_level(self.current_level)

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        
    def update_icon_pos(self):
        self.icon.sprite.rect.center = self.nodes.sprites()[self.current_level].rect.center
        
    def run(self):
        self.input()
        self.update_icon_pos()
        self.nodes.update()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)