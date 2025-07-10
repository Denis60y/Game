import pygame
import math
from settings import IMAGE_PATHS, SCREEN_WIDTH, SCREEN_HEIGHT

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.radius = 5
        self.color = (255, 0, 0)
        self.speed = 10
        self.damage = 1

        dx = target_x - x
        dy = target_y - y
        distance = max(1, math.sqrt(dx * dx + dy * dy))
        self.vx = self.speed * dx / distance
        self.vy = self.speed * dy / distance

        # Угол поворота пули в направлении движения
        self.angle = math.degrees(math.atan2(dy, dx))
        try:
            bullet_img = pygame.image.load(IMAGE_PATHS['bullet']).convert_alpha()
            bullet_img = pygame.transform.scale(bullet_img, (40, 10))
            # Поворачиваем изображение пули
            self.image = pygame.transform.rotate(bullet_img, -self.angle)
            self.rect = self.image.get_rect(center=(x, y))
        except:
            self.image = None

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.image:
            self.rect.center = (self.x, self.y)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_off_screen(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or
                self.y < 0 or self.y > SCREEN_HEIGHT)