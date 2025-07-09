import pygame
from settings import SCREEN_WIDTH, GROUND_HEIGHT, FONT, IMAGE_PATHS, SCREEN_HEIGHT
from bullet import Bullet

class Player:
    def __init__(self, x, y):
        # Загрузка изображений
        player_original = pygame.image.load(IMAGE_PATHS['player'])
        new_width, new_height = 70, 70
        self.player_right = pygame.transform.scale(player_original, (new_width, new_height))
        self.player_left = pygame.transform.flip(self.player_right, True, False)
        self.current_image = self.player_right
        self.rect = self.player_right.get_rect()

        # Позиция и движение
        self.x = x
        self.y = y
        self.speed = 5
        self.is_jumping = False
        self.gravity = 0.5
        self.jump_power = 12
        self.initial_jump_power = 12
        self.y_velocity = 0  # Добавляем вертикальную скорость

        # Характеристики
        self.hp = 10
        self.max_hp = 10
        self.invincibility_timer = 0

    def update(self, keys):
        # Обработка движения
        if keys[pygame.K_a]:
            self.x -= self.speed
            self.current_image = self.player_left
        if keys[pygame.K_d]:
            self.x += self.speed
            self.current_image = self.player_right

        # Границы экрана по горизонтали
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.rect.width))

        # Механика прыжка и гравитации
        if self.is_jumping:
            self.y_velocity -= self.jump_power
            self.is_jumping = False  # Сбрасываем флаг прыжка после применения силы

        # Применяем гравитацию
        self.y_velocity += self.gravity
        self.y += self.y_velocity

        # Проверка приземления
        ground_level = SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height
        if self.y >= ground_level:
            self.y = ground_level
            self.y_velocity = 0  # Сбрасываем вертикальную скорость при приземлении

        # Обновление таймера неуязвимости
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

        # Обновление rect для коллизий
        self.rect.topleft = (self.x, self.y)

    def jump(self):
        # Проверяем, что персонаж стоит на земле (не в прыжке)
        ground_level = SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height
        if self.y >= ground_level - 1:  # Небольшой допуск для плавающей точки
            self.is_jumping = True

    def shoot(self, target_x, target_y):
        player_center_x = self.x + self.rect.width // 2
        player_center_y = self.y + self.rect.height // 2
        return Bullet(player_center_x, player_center_y, target_x, target_y)

    def take_damage(self, damage):
        if self.invincibility_timer <= 0:
            self.hp -= damage
            self.invincibility_timer = 60  # 1 секунда неуязвимости
            return True
        return False

    def draw(self, screen):
        # Рисуем игрока
        screen.blit(self.current_image, (self.x, self.y))

        # Рисуем здоровье
        hp_text = f"HP: {self.hp}/{self.max_hp}"
        text_surface = FONT.render(hp_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))