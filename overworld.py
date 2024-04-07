import pygame
from game_data import levels
import sys
from settings import screen_width, screen_height


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, node_graphics):
        super().__init__()
        self.image = pygame.image.load(node_graphics).convert_alpha()
        self.lock_image = pygame.image.load('graphics/overworld/lock.png').convert_alpha()
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

            horizontal_offset = (self.image.get_width() - self.lock_image.get_width()) // 2
            vertical_offset = (self.image.get_height() - self.lock_image.get_height()) // 2 + 30
            lock_offset = (horizontal_offset, vertical_offset)
            self.image.blit(self.lock_image, lock_offset)

class Cursor(pygame.sprite.Sprite):
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

        #Font
        font = pygame.font.Font('graphics/overworld/EquipmentPro.ttf', 40)
        self.loading_text = font.render('LOADING...', True, (255, 255, 255))


        # Audio
        self.click_sound = pygame.mixer.Sound('audio/effects/click.wav')
        self.click_sound.set_volume(0.8)

        self.level_select_sound = pygame.mixer.Sound('audio/effects/level_select.mp3')
        self.level_select_sound.set_volume(0.8)

        # Nodes and Cursor Sprites
        self.setup_nodes()
        self.setup_cursor()

        # Controls Sprite
        self.space_key_image = pygame.image.load('graphics/overworld/space_key.png').convert_alpha()
        self.arrow_keys_image = pygame.image.load('graphics/overworld/arrow_keys.png').convert_alpha()
        self.enter_key_image = pygame.image.load('graphics/overworld/enter_key.png').convert_alpha()
        self.esc_key_image = pygame.image.load('graphics/overworld/esc_key.png').convert_alpha()

        # Time
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_length = 300
    
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite  = Node(node_data['node_pos'], 'available', node_data['node_graphics'])
            else:
                node_sprite  = Node(node_data['node_pos'], 'locked', node_data['node_graphics'])
            self.nodes.add(node_sprite)

    def setup_cursor(self):
        self.icon = pygame.sprite.GroupSingle()
        current_node_rect = self.nodes.sprites()[self.current_level].rect
        icon_sprite = Cursor(current_node_rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()

        if self.allow_input:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                if not self.moving:
                    self.click_sound.play()
                    self.current_level += 1
                    self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                if not self.moving:
                    self.click_sound.play()
                    self.current_level -= 1
                    self.moving = True
            else:
                self.moving = False

        if keys[pygame.K_RETURN]:
            self.level_select_sound.play()
            self.display_loading()
            self.create_level(self.current_level)

        if keys[pygame.K_ESCAPE]:
            self.click_sound.play()
            pygame.time.delay(int(self.click_sound.get_length() * 1000 + 175))
            pygame.quit()
            sys.exit()
        
    def update_cursor_pos(self):
        self.icon.sprite.rect.center = self.nodes.sprites()[self.current_level].rect.center

    def input_timer(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_length:
                self.allow_input = True
    
    def display_controls(self):
            # Font
            font = pygame.font.Font('graphics/overworld/EquipmentPro.ttf', 40)

            # Space Key
            space_key_w, space_key_h = self.space_key_image.get_size()
            space_key_bot = 630
            space_key_left = 236
            space_key_top = space_key_bot - space_key_h

            self.display_surface.blit(self.space_key_image, (space_key_left, space_key_top))

            esc_text_surface = font.render("Player jump", False, (22, 23, 26))
            esc_text_rect = esc_text_surface.get_rect()
            esc_text_rect.topleft = (space_key_left + space_key_w + 20, space_key_bot - space_key_h + 10)
            self.display_surface.blit(esc_text_surface, esc_text_rect)

            # Arrow Keys
            arrow_keys_w, arrow_keys_h = self.arrow_keys_image.get_size()
            arrow_keys_top = space_key_top - 30 - arrow_keys_h
            arrow_keys_left = space_key_left

            self.display_surface.blit(self.arrow_keys_image, (arrow_keys_left, arrow_keys_top))

            arrow_keys_text_surface = font.render("Move player & switch level", False, (22, 23, 26))
            arrow_keys_text_rect = arrow_keys_text_surface.get_rect()
            arrow_keys_text_rect.topleft = (arrow_keys_left + arrow_keys_w + 20, arrow_keys_top + 10)
            self.display_surface.blit(arrow_keys_text_surface, arrow_keys_text_rect)

            # Enter Key
            enter_key_w, enter_key_h = self.enter_key_image.get_size()
            enter_key_left = arrow_keys_text_rect.right + 30
            enter_key_top = arrow_keys_top + (arrow_keys_h - enter_key_h) // 2

            self.display_surface.blit(self.enter_key_image, (enter_key_left, enter_key_top))

            enter_text_surface = font.render("Play level", False, (22, 23, 26))
            enter_text_rect = enter_text_surface.get_rect()
            enter_text_rect.topleft = (enter_key_left + enter_key_w + 20, enter_key_top + (enter_key_h - enter_text_surface.get_height()) // 2)
            self.display_surface.blit(enter_text_surface, enter_text_rect)

            # Esc Key
            esc_key_w, esc_key_h = self.esc_key_image.get_size()
            esc_key_left = enter_key_left
            esc_key_top = enter_key_top + enter_key_h + 20

            self.display_surface.blit(self.esc_key_image, (esc_key_left, esc_key_top))

            esc_text_surface = font.render("Exit game", False, (22, 23, 26))
            esc_text_rect = esc_text_surface.get_rect()
            esc_text_rect.topleft = (esc_key_left + esc_key_w + 20, esc_key_top + (esc_key_h - esc_text_surface.get_height()) // 2)
            self.display_surface.blit(esc_text_surface, esc_text_rect)

            '''arrow_keys_text_length = arrow_keys_text_surface.get_width()
            enter_text_length = enter_text_surface.get_width()

            print("Arrow Keys Text Length:", arrow_keys_text_length)
            print("Enter Key Text Length:", enter_text_length)'''

    def display_loading(self):
        font = pygame.font.Font('graphics/overworld/EquipmentPro.ttf', 80)
        loading_text = font.render('LOADING...', True, (255, 255, 255))

        text_rect = loading_text.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2))
        text_rect.top -= loading_text.get_height() // 2  # y margin
        self.display_surface.blit(loading_text, text_rect)
        pygame.display.update()

    def run(self):
        self.input_timer()
        self.input()
        self.update_cursor_pos()
        self.nodes.update()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
        self.display_controls()