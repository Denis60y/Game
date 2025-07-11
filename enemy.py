import pygame
import random
import math
from settings import IMAGE_PATHS, SCREEN_WIDTH, SCREEN_HEIGHT

class Enemy:
    def __init__(self, player_x, player_y):
        # Спавн строго за пределами экрана
        spawn_side = random.randint(0, 2)

        if spawn_side == 0:  # Сверху (за экраном)
            self.x = random.randint(-50, SCREEN_WIDTH + 50)
            self.y = -50
        elif spawn_side == 1:  # Справа (за экраном)
            self.x = SCREEN_WIDTH + 50
            self.y = random.randint(-50, SCREEN_HEIGHT)
        elif spawn_side == 2:  # Слева (за экраном)
            self.x = -50
            self.y = random.randint(-50, SCREEN_HEIGHT)

        self.speed = random.uniform(4.0, 6.0)
        self.hp = 5
        self.max_hp = 5
        self.width = 50
        self.height = 50
        self.damage = 1

        try:
            self.image = pygame.image.load(IMAGE_PATHS['enemy']).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect(center=(self.x, self.y))
        except:
            self.image = None
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Направление к игроку
        self.calculate_direction(player_x, player_y)

    def calculate_direction(self, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        distance = max(1, math.sqrt(dx * dx + dy * dy))
        self.vx = self.speed * dx / distance
        self.vy = self.speed * dy / distance

    def update(self, player_x, player_y):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x, self.y)

        # Обновляем направление (чтобы враги преследовали игрока)
        self.calculate_direction(player_x, player_y)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)

        # Рисуем здоровье
        hp_bar_width = 40
        hp_bar_height = 5
        hp_bar_x = self.x - hp_bar_width // 2
        hp_bar_y = self.y - 30

        # Фон полоски HP
        pygame.draw.rect(screen, (255, 0, 0),
                         (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))
        # Текущее HP
        current_hp_width = (self.hp / self.max_hp) * hp_bar_width
        pygame.draw.rect(screen, (0, 255, 0),
                         (hp_bar_x, hp_bar_y, current_hp_width, hp_bar_height))

    def is_off_screen(self):
        return (self.x < -100 or self.x > SCREEN_WIDTH + 100 or
                self.y < -100 or self.y > SCREEN_HEIGHT + 100)


class Enemy_armor:
    def __init__(self, player_x, player_y):
        # Спавн строго за пределами экрана
        spawn_side = random.randint(0, 2)

        if spawn_side == 0:  # Сверху (за экраном)
            self.x = random.randint(-50, SCREEN_WIDTH + 50)
            self.y = -50
        elif spawn_side == 1:  # Справа (за экраном)
            self.x = SCREEN_WIDTH + 50
            self.y = random.randint(-50, SCREEN_HEIGHT)
        elif spawn_side == 2:  # Слева (за экраном)
            self.x = -50
            self.y = random.randint(-50, SCREEN_HEIGHT)

        self.speed = random.uniform(2.0, 4.0)
        self.hp = 8
        self.max_hp = 8
        self.width = 50
        self.height = 50
        self.damage = 1

        try:
            self.image = pygame.image.load(IMAGE_PATHS['armored_enemy']).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect(center=(self.x, self.y))
        except:
            self.image = None
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Направление к игроку
        self.calculate_direction(player_x, player_y)

    def calculate_direction(self, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        distance = max(1, math.sqrt(dx * dx + dy * dy))
        self.vx = self.speed * dx / distance
        self.vy = self.speed * dy / distance

    def update(self, player_x, player_y):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x, self.y)

        # Обновляем направление (чтобы враги преследовали игрока)
        self.calculate_direction(player_x, player_y)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)

        # Рисуем здоровье
        hp_bar_width = 40
        hp_bar_height = 5
        hp_bar_x = self.x - hp_bar_width // 2
        hp_bar_y = self.y - 30

        # Фон полоски HP
        pygame.draw.rect(screen, (255, 0, 0),
                         (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))
        # Текущее HP
        current_hp_width = (self.hp / self.max_hp) * hp_bar_width
        pygame.draw.rect(screen, (0, 255, 0),
                         (hp_bar_x, hp_bar_y, current_hp_width, hp_bar_height))

    def is_off_screen(self):
        return (self.x < -100 or self.x > SCREEN_WIDTH + 100 or
                self.y < -100 or self.y > SCREEN_HEIGHT + 100)