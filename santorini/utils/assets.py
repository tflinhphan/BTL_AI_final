"""
Assets used throughout the project
"""
from multiprocessing.pool import CLOSE
from tkinter.messagebox import CANCEL

import pygame

pygame.init()

# Font to be used
SQUIRK = "assets/Parkinsans-Bold.ttf"
# Initialising font usages
TITLE_FONT = pygame.font.Font(SQUIRK, 48)
BUTTON_FONT = pygame.font.Font(SQUIRK, 23)
MESSAGE_FONT = pygame.font.Font(SQUIRK, 25)
OUTLINE_FONT = pygame.font.Font(SQUIRK, 21)
DESCRIPTION_FONT = pygame.font.Font(SQUIRK, 15)

# Menu Items
CLOUD = pygame.image.load('assets/cloud.png')
LOGO = pygame.transform.smoothscale(pygame.image.load('assets/logo.png'), (500, 150))
MENU_BACKGROUND = pygame.transform.scale(pygame.image.load('assets/menu_background.png'), (600, 600))
GAME_BACKGROUND = pygame.transform.smoothscale(pygame.image.load('assets/game_background_1.png'), (600, 600))

BG_NOTI = pygame.transform.smoothscale(pygame.image.load('assets/bg_noti_1.png'), (360, 260))
BG_NOTI_2 = pygame.transform.smoothscale(pygame.image.load('assets/bg_noti_1.png'), (450, 350))
SUPPORTER = pygame.image.load('assets/woo.png')

# Worker placeholders
RED_WORKER = pygame.transform.scale(pygame.image.load('assets/red.png'), (50, 50))
YELLOW_WORKER = pygame.transform.scale(pygame.image.load('assets/yellow.png'), (50, 50))

# Worker option placeholders
MOVE_ICON = pygame.transform.scale(pygame.image.load('assets/move.png'), (50, 50))
BUILD_ICON = pygame.transform.scale(pygame.image.load('assets/build.png'), (50, 50))

# Button placeholder
## BUTTON_ICON = pygame.image.load("assets/the_button_that_survived.png")
BUTTON_ICON = pygame.image.load("assets/bg_button.png")
EXIT_ICON = pygame.image.load("assets/back_button.png")
SETTING_ICON = pygame.image.load("assets/setting_button.png")
MUSIC_ON_ICON = pygame.transform.scale(pygame.image.load('assets/musicon_button.png'), (70, 70))
MUSIC_OFF_ICON = pygame.transform.scale(pygame.image.load('assets/musicoff_button.png'), (70, 70))
SOUND_ON_ICON = pygame.transform.scale(pygame.image.load('assets/soundon_button.png'), (70, 70))
SOUND_OFF_ICON = pygame.transform.scale(pygame.image.load('assets/soundoff_button.png'), (70, 70))
CLOSE_ICON = pygame.transform.scale(pygame.image.load('assets/close_button.png'), (40, 40))
YES_ICON = pygame.transform.scale(pygame.image.load('assets/agree_button.png'), (70, 70))
NO_ICON = pygame.transform.scale(pygame.image.load('assets/cancel_button.png'), (70, 70))
HOME_ICON = pygame.transform.scale(pygame.image.load('assets/home_button.png'), (70, 70))
REPLAY_ICON = pygame.transform.scale(pygame.image.load('assets/replay_button.png'), (70, 70))

MOVE_SOUND = pygame.mixer.Sound("assets/move_sound.wav")
BUILD_SOUND = pygame.mixer.Sound("assets/build_sound.wav")
CLICK_SOUND = pygame.mixer.Sound("assets/click_sound.wav")
WIN_SOUND = pygame.mixer.Sound("assets/win_sound.wav")

# Building placeholders
L1 = pygame.image.load('assets/l1.png')
L2 = pygame.image.load('assets/l2.png')
L3 = pygame.image.load('assets/l3.png')
L4 = pygame.image.load('assets/l4.png')
