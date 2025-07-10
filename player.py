import pygame
from settings import SCREEN_WIDTH, GROUND_HEIGHT, FONT, IMAGE_PATHS, SCREEN_HEIGHT, SOUND_PATHS
from bullet import Bullet


class Player:
    def __init__(self, x, y):
        player_original = pygame.image.load(IMAGE_PATHS['player'])
        new_width, new_height = 70, 70

        self.hit_sound = pygame.mixer.Sound(SOUND_PATHS['hit_sound'])
        self.hit_sound.set_volume(0.3)

        self.jump_sound = pygame.mixer.Sound(SOUND_PATHS['jump_sound'])
        self.jump_sound.set_volume(0.2)

        self.player_right = pygame.transform.scale(player_original, (new_width, new_height))
        self.player_left = pygame.transform.flip(self.player_right, True, False)

        self.hit_animation = self.load_animation(IMAGE_PATHS['hit_animation'], 4, new_width, new_height)
        self.hit_animation_left = [pygame.transform.flip(frame, True, False) for frame in self.hit_animation]

        self.walk_animation_right = self.load_animation(IMAGE_PATHS['run'], 6, new_width, new_height)
        self.walk_animation_left = [pygame.transform.flip(frame, True, False) for frame in self.walk_animation_right]

        self.current_image = self.player_right
        self.rect = self.player_right.get_rect()

        self.x = x
        self.y = y
        self.speed = 5
        self.is_jumping = False
        self.gravity = 0.5
        self.jump_power = 12
        self.initial_jump_power = 12
        self.y_velocity = 0

        self.hp = 10
        self.max_hp = 10
        self.invincibility_timer = 0

        self.is_hit = False
        self.hit_animation_frame = 0
        self.hit_animation_speed = 15
        self.hit_animation_counter = 0

        self.is_walking = False
        self.walk_animation_frame = 0
        self.walk_animation_speed = 5
        self.walk_animation_counter = 0
        self.facing_right = True

    def load_animation(self, image_path, frame_count, width, height):
        """Универсальный метод загрузки анимации"""
        sheet = pygame.image.load(image_path)
        frames = []

        frame_width = sheet.get_width() // frame_count
        frame_height = sheet.get_height()

        for i in range(frame_count):
            frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frames.append(pygame.transform.scale(frame, (width, height)))

        return frames

    def update(self, keys):
        moving_left = keys[pygame.K_a]
        moving_right = keys[pygame.K_d]
        self.is_walking = moving_left or moving_right

        if moving_left:
            self.x -= self.speed
            self.facing_right = False
        if moving_right:
            self.x += self.speed
            self.facing_right = True

        self.x = max(0, min(self.x, SCREEN_WIDTH - self.rect.width))

        if self.is_jumping:
            self.y_velocity -= self.jump_power
            self.is_jumping = False

        self.y_velocity += self.gravity
        self.y += self.y_velocity

        ground_level = SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height
        if self.y >= ground_level:
            self.y = ground_level
            self.y_velocity = 0

        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1
            self.is_hit = True

            self.hit_animation_counter += 1
            if self.hit_animation_counter >= self.hit_animation_speed:
                self.hit_animation_counter = 0
                self.hit_animation_frame = (self.hit_animation_frame + 1) % len(self.hit_animation)
        else:
            self.is_hit = False
            self.hit_animation_frame = 0
            self.hit_animation_counter = 0

        if self.is_walking and not self.is_hit:
            self.walk_animation_counter += 1
            if self.walk_animation_counter >= self.walk_animation_speed:
                self.walk_animation_counter = 0
                self.walk_animation_frame = (self.walk_animation_frame + 1) % len(self.walk_animation_right)

        self.rect.topleft = (self.x, self.y)

    def jump(self):
        ground_level = SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height
        if self.y >= ground_level - 1:
            self.is_jumping = True
            self.jump_sound.play()

    def shoot(self, target_x, target_y):
        player_center_x = self.x + self.rect.width // 2
        player_center_y = self.y + self.rect.height // 2
        return Bullet(player_center_x, player_center_y, target_x, target_y)

    def take_damage(self, damage):
        if self.invincibility_timer <= 0:
            self.hp -= damage
            self.invincibility_timer = 60
            self.is_hit = True
            self.hit_animation_frame = 0
            self.hit_animation_counter = 0

            self.hit_sound.play()

            return True
        return False

    def draw(self, screen):
        if self.is_hit:
            if self.facing_right:
                current_frame = self.hit_animation[self.hit_animation_frame]
            else:
                current_frame = self.hit_animation_left[self.hit_animation_frame]
        elif self.is_walking:
            if self.facing_right:
                current_frame = self.walk_animation_right[self.walk_animation_frame]
            else:
                current_frame = self.walk_animation_left[self.walk_animation_frame]
        else:
            if self.facing_right:
                current_frame = self.player_right
            else:
                current_frame = self.player_left

        screen.blit(current_frame, (self.x, self.y))

        hp_text = f"ОЗ: {self.hp}/{self.max_hp}"
        text_surface = FONT.render(hp_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))