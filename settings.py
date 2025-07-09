import pygame

# Настройки экрана
SCREEN_WIDTH = 864
SCREEN_HEIGHT = 486
GROUND_HEIGHT = 50

# Пути к изображениям
IMAGE_PATHS = {
    'bg': 'images/bg.png',
    'ground': 'images/grass.png',
    'bullet': 'images/arrow.png',
    'enemy': 'images/enemy.png',
    'player': 'images/player.png',
    'icon': 'images/icon.png'
}

# Инициализация pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stich")

# Загрузка иконки
try:
    icon = pygame.image.load(IMAGE_PATHS['icon'])
    pygame.display.set_icon(icon)
except:
    print("Не удалось загрузить иконку")

# Загрузка шрифта
try:
    FONT = pygame.font.Font(None, 36)
except:
    print("Не удалось загрузить шрифт, будет использоваться стандартный")
    FONT = pygame.font.SysFont('arial', 36)