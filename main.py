import pygame
import math
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, screen, IMAGE_PATHS, FONT, SOUND_PATHS
from player import Player
from enemy import Enemy, Enemy_armor

try:
    bg_original = pygame.image.load(IMAGE_PATHS['bg'])
    bg = pygame.transform.scale(bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    print("Не удалось загрузить фон")
    bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg.fill((0, 0, 100))

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

player = Player(200, ground_rect.y - 70)

bullets = []
enemies = []
enemy_spawn_timer = 0
enemy_spawn_interval = 80

k = 20

running = True
clock = pygame.time.Clock()

pygame.mixer.music.load('sounds/background.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not player.is_jumping:
                player.jump()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bullets.append(player.shoot(mouse_x, mouse_y))

    hit_sound_enemy = pygame.mixer.Sound(SOUND_PATHS['hit_sound_enemy'])
    hit_sound_enemy.set_volume(0.1)

    if k <= 0:
        running = False

    keys = pygame.key.get_pressed()
    player.update(keys)

    enemy_spawn_timer += 1
    if enemy_spawn_timer >= enemy_spawn_interval:
        player_center_x = player.x + player.rect.width // 2
        player_center_y = player.y + player.rect.height // 2
        if random.randint(0, 2) == 0:
            enemies.append(Enemy(player_center_x, player_center_y))
        elif random.randint(0, 2) == 1:
            enemies.append(Enemy_armor(player_center_x, player_center_y))
        enemy_spawn_timer = 0
        enemy_spawn_interval = max(30, enemy_spawn_interval - 1)

    for bullet in bullets[:]:
        bullet.update()
        if bullet.is_off_screen():
            bullets.remove(bullet)
        else:
            for enemy in enemies[:]:
                if bullet.image and enemy.image:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.hp -= bullet.damage
                        if bullet in bullets:
                            bullets.remove(bullet)
                            hit_sound_enemy.play()
                        if enemy.hp <= 0:
                            enemies.remove(enemy)
                            k -= 1
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

    player_center_x = player.x + player.rect.width // 2
    player_center_y = player.y + player.rect.height // 2

    for enemy in enemies[:]:
        enemy.update(player_center_x, player_center_y)
        if enemy.is_off_screen():
            enemies.remove(enemy)

        elif enemy.rect.colliderect(player.rect):
            if player.take_damage(enemy.damage) and player.hp <= 0:
                running = False


    screen.blit(bg, (0, 0))
    screen.blit(ground_surface, ground_rect)

    player.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    hp_text = f"Цель: убить {k} врагов"
    text_surface = FONT.render(hp_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 40))

    pygame.display.update()
    clock.tick(60)  # 60 FPS

pygame.quit()