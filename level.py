import pygame
from tiles import Tile, StaticTile
from settings import tile_size, screen_width, screen_height
from player import Player
from support import import_csv_layout, import_cut_graphics
from enemy import Enemy
from game_data import levels
from particles import ParticleEffect

class Level:
    def __init__(self, current_level, surface, create_overworld, change_health):
        # General setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        # Audio
        self.stomp_sound = pygame.mixer.Sound('audio/effects/stomp.mp3')
        self.stomp_sound.set_volume(0.4)

        self.win_sound = pygame.mixer.Sound('audio/effects/win.wav')
        self.win_sound.set_volume(0.3)

        self.lose_sound = pygame.mixer.Sound('audio/effects/lose.wav')
        self.lose_sound.set_volume(0.3)
        
        # Overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']
        
        # Player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)

        # enemy_death particles
        self.enemy_death_sprites = pygame.sprite.Group()

        # Terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # Decorations setup
        decorations_layout = import_csv_layout(level_data['decorations'])
        self.decoration_sprites = self.create_tile_group(decorations_layout, 'decorations')

        # Enemy setup
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # Constraints setup
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraints_layout, 'constraints')

    def exit_level(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_BACKSPACE]:
            self.create_overworld(self.current_level, 0)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()    

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('graphics/tiles/ground_tilesheet.png')
                        tile_surface = terrain_tile_list[int(val)].convert_alpha()
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'decorations':
                        decorations_tile_list = import_cut_graphics('graphics/tiles/decorations_tilesheet.png')
                        tile_surface = decorations_tile_list[int(val)].convert_alpha()
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)
                    
                    sprite_group.add(sprite)
        
        return sprite_group
    
    def player_setup(self, layout, change_health):
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if val == '1':
                        sprite = Player((x, y), self.display_surface, change_health)
                        self.player.add(sprite) 
                    if val == '0':
                        flag_surface = pygame.image.load('graphics/tiles/end_flag.png').convert_alpha()
                        sprite = StaticTile(tile_size, x, y, flag_surface)
                        self.goal.add(sprite)
                    
    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x,y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

    def horizontal_mov_col(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        '''if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False'''

    def vertical_mov_col(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        '''if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False'''

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < (screen_width/2) and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > (screen_width/2) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def check_void_fall(self):
        if self.player.sprite.rect.top > screen_height:
            pygame.mixer.stop()
            self.lose_sound.play()
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            pygame.mixer.stop()  # Stop all currently playing sounds
            self.win_sound.play()
            self.create_overworld(self.current_level, self.new_max_level)            

    def check_enemy_col(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.stomp_sound.play()
                    self.player.sprite.direction.y = -15
                    enemy_death_sprite = ParticleEffect(enemy.rect.center, 'enemy_death', enemy.speed)
                    self.enemy_death_sprites.add(enemy_death_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def run(self):
        # Decorations
        self.decoration_sprites.update(self.world_shift)
        self.decoration_sprites.draw(self.display_surface)

        # End Flag
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # Terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # Enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.enemy_death_sprites.update(self.world_shift)
        self.enemy_death_sprites.draw(self.display_surface)
        
        # Player sprites
        self.player.draw(self.display_surface)
        self.player.update()
        self.horizontal_mov_col()
        self.vertical_mov_col()
        self.scroll_x()

        # Previously end flag was placed here

        # Win Loss
        self.check_void_fall()
        self.check_win()

        self.check_enemy_col()

        self.exit_level()