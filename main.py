import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, screen, IMAGE_PATHS
from player import Player
from enemy import Enemy

# Загрузка и масштабирование фона
try:
    bg_original = pygame.image.load(IMAGE_PATHS['bg'])
    bg = pygame.transform.scale(bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    print("Не удалось загрузить фон")
    bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg.fill((0, 0, 100))

# Загрузка текстуры земли
try:
    ground_tile = pygame.image.load(IMAGE_PATHS['ground'])
    tile_width = ground_tile.get_width()
    tile_height = ground_tile.get_height()
    ground_height = 50

    ground_surface = pygame.Surface((SCREEN_WIDTH, ground_height))
    for x in range(0, SCREEN_WIDTH, tile_width):
        ground_surface.blit(ground_tile, (x, 0))

    ground_rect = ground_surface.get_rect(topleft=(0, SCREEN_HEIGHT - ground_height))
except:
    print("Не удалось загрузить землю")
    ground_surface = pygame.Surface((SCREEN_WIDTH, 50))
    ground_surface.fill((100, 80, 0))
    ground_rect = ground_surface.get_rect(topleft=(0, SCREEN_HEIGHT - 50))

# Инициализация игрока
player = Player(200, ground_rect.y - 70)  # 70 - высота персонажа

bullets = []
enemies = []
enemy_spawn_timer = 0
enemy_spawn_interval = 180  # кадры между спавном врагов

running = True
clock = pygame.time.Clock()  # Для контроля FPS

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not player.is_jumping:
                player.jump()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bullets.append(player.shoot(mouse_x, mouse_y))

    # Обновление игрока
    keys = pygame.key.get_pressed()
    player.update(keys)

    # Спавн врагов
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= enemy_spawn_interval:
        player_center_x = player.x + player.rect.width // 2
        player_center_y = player.y + player.rect.height // 2
        enemies.append(Enemy(player_center_x, player_center_y))
        enemy_spawn_timer = 0
        enemy_spawn_interval = max(30, enemy_spawn_interval - 1)

    # Обновление пуль
    for bullet in bullets[:]:
        bullet.update()
        if bullet.is_off_screen():
            bullets.remove(bullet)
        else:
            # Проверка попадания пули во врагов
            for enemy in enemies[:]:
                if bullet.image and enemy.image:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.hp -= bullet.damage
                        if bullet in bullets:
                            bullets.remove(bullet)
                        if enemy.hp <= 0:
                            enemies.remove(enemy)
                        break
                else:
                    distance = math.sqrt((bullet.x - enemy.x) ** 2 + (bullet.y - enemy.y) ** 2)
                    if distance < 25:
                        enemy.hp -= bullet.damage
                        if bullet in bullets:
                            bullets.remove(bullet)
                        if enemy.hp <= 0:
                            enemies.remove(enemy)
                        break

    # Обновление врагов и проверка столкновений с игроком
    player_center_x = player.x + player.rect.width // 2
    player_center_y = player.y + player.rect.height // 2

    for enemy in enemies[:]:
        enemy.update(player_center_x, player_center_y)
        if enemy.is_off_screen():
            enemies.remove(enemy)
        elif enemy.rect.colliderect(player.rect):
            if player.take_damage(enemy.damage) and player.hp <= 0:
                print("Игра окончена!")
                running = False

    # Отрисовка
    screen.blit(bg, (0, 0))  # Фон
    screen.blit(ground_surface, ground_rect)  # Земля

    # Рисуем игрока (включая его HP)
    player.draw(screen)

    # Рисуем пули
    for bullet in bullets:
        bullet.draw(screen)
    # Рисуем врагов
    for enemy in enemies:
        enemy.draw(screen)

    pygame.display.update()
    clock.tick(60)  # 60 FPS

pygame.quit()