import pygame

SCREEN_WIDTH = 864
SCREEN_HEIGHT = 486
GROUND_HEIGHT = 50

IMAGE_PATHS = {
    'bg': 'images/bg.png',
    'ground': 'images/grass.png',
    'bullet': 'images/arrow.png',
    'enemy': 'images/enemy.png',
    'armored_enemy': 'images/armored_enemy.png',
    'player': 'images/player.png',
    'icon': 'images/icon.png',
    'run': 'images/run.png',
    'hit_animation': 'images/hurt.png'
}

SOUND_PATHS = {
    'hit_sound': 'sounds/hit.mp3',
    'hit_sound_enemy': 'sounds/hit_enemy.mp3',
    'jump_sound': 'sounds/jump.mp3',
}

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stich")

try:
    icon = pygame.image.load(IMAGE_PATHS['icon'])
    pygame.display.set_icon(icon)
except:
    print("Не удалось загрузить иконку")

try:
    FONT = pygame.font.Font(None, 36)
except:
    print("Не удалось загрузить шрифт, будет использоваться стандартный")
    FONT = pygame.font.SysFont('arial', 36)