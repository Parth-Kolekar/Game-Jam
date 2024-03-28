import pygame
from tiles import Tile, StaticTile
from settings import tile_size, screen_width
from player import Player
from support import import_csv_layout, import_cut_graphics
from enemy import Enemy

class Level:
    def __init__(self,level_data,surface):
        #level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = None

        #player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        #terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        #decorations setup
        decorations_layout = import_csv_layout(level_data['decorations'])
        self.decoration_sprites = self.create_tile_group(decorations_layout, 'decorations')

        #enemy setup
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        #constraints setup
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraints_layout, 'constraints')

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()    

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('graphics/tiles/ground_tilesheet.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        #sprite_group.add(sprite)

                    if type == 'decorations':
                        decorations_tile_list = import_cut_graphics('graphics/tiles/decorations_tilesheet.png')
                        tile_surface = decorations_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        #sprite_group.add(sprite)

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)
                    
                    sprite_group.add(sprite)
        
        return sprite_group
    
    def player_setup(self, layout):
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if val == '1':
                        sprite = Player((x, y), self.display_surface)
                        self.player.add(sprite) 
                    if val == '0':
                        hat_surface = pygame.image.load('graphics/entities/Rogue/Death/death7.png').convert_alpha()
                        sprite = StaticTile(tile_size, x, y, hat_surface)
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
                    player_sprite = Player((x, y))  # Adjust y + value to make player spawn on tile
                    self.player.add(player_sprite)

    def horizontal_mov_col(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_mov_col(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

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

    def run(self):
        #decorations
        self.decoration_sprites.update(self.world_shift)
        self.decoration_sprites.draw(self.display_surface)

        #terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        #enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        
        #player sprites
        self.player.draw(self.display_surface)
        self.player.update()
        self.horizontal_mov_col()
        self.vertical_mov_col()
        self.scroll_x()
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)