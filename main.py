import pygame, sys, asyncio
from settings import *
from level import Level
from overworld import Overworld
from ui import UI

class Game:
    def __init__(self):

        # Game attributes
        self.max_level = 0
        self.max_health = 100
        self.current_health = 100

        # Audio
        self.level_bg_music = pygame.mixer.Sound('audio/music/level_music.ogg')
        self.level_bg_music.set_volume(0.5)

        self.overworld_bg_music = pygame.mixer.Sound('audio/music/overworld_music.ogg')
        self.overworld_bg_music.set_volume(0.5)

        self.lose_sound = pygame.mixer.Sound('audio/effects/lose.ogg')
        self.lose_sound.set_volume(0.3)

        # Overworld creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops = -1)

        # User interface
        self.ui = UI(screen)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_health)
        self.current_health = 100
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops = -1)
        
    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.level_bg_music.stop()
        self.overworld_bg_music.play(loops = -1)

    def change_health(self, amount):
        self.current_health += amount

    def check_game_over(self):
        if self.current_health <= 0:
            self.current_health = 100
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'
            pygame.mixer.stop()
            self.lose_sound.play()
            self.level_bg_music.stop()
            self.overworld_bg_music.play(loops = -1)

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.check_game_over()

# Pygame set up  
pygame.init()
pygame.display.set_caption('Game Jam')
screen = pygame.display.set_mode((screen_width, screen_height))

# Loading the background image
background_img = pygame.image.load('graphics/background/grassy_mountain_scaled.png').convert_alpha()

# Hide the mouse cursor
pygame.mouse.set_visible(False)

# Initialize the clock
clock = pygame.time.Clock()

# Creating Game instance
game = Game()

# Toggle fullscreen using F key
def toggle_fullscreen(event):
    click_sound = pygame.mixer.Sound('audio/effects/click.ogg')
    click_sound.set_volume(0.8)
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_f:
            click_sound.play()
            if screen.get_flags() & pygame.FULLSCREEN:
                pygame.display.set_mode((screen_width, screen_height))
            else:
                pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

async def main():           
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            toggle_fullscreen(event)
        screen.blit(background_img,(0,0))
        game.run()
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())