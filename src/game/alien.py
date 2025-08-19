import pygame
import math
from typing import Tuple
from .constants import *

class Alien:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.size = ALIEN_SIZE
        self.speed = ALIEN_SPEED
        self.max_cargo = ALIEN_MAX_CARGO
        self.cargo = 0
        self.cargo_value = 0  # Track total value of carried humans
        self.meat = 0
        self.alive = True
        self.efficiency_bonus = 0
        
        self.vel_x = 0.0
        self.vel_y = 0.0
    
    def update(self, dt: float, keys_pressed):
        if not self.alive:
            return
            
        self.vel_x = 0.0
        self.vel_y = 0.0
        
        if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            self.vel_y = -1.0
        if keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            self.vel_y = 1.0
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.vel_x = -1.0
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.vel_x = 1.0
        
        if self.vel_x != 0 and self.vel_y != 0:
            self.vel_x *= 0.707
            self.vel_y *= 0.707
        
        self.x += self.vel_x * self.speed * dt
        self.y += self.vel_y * self.speed * dt
        
        self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
        self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
    
    def consume_human(self, human_value: int = 1) -> bool:
        if self.cargo < self.max_cargo:
            self.cargo += 1
            self.cargo_value += human_value
            return True
        return False
    
    def return_to_base(self):
        # Return both cargo count and total value
        cargo_count = self.cargo
        cargo_value = self.cargo_value
        self.cargo = 0
        self.cargo_value = 0
        return cargo_count, cargo_value
    
    def render(self, screen: pygame.Surface):
        if not self.alive:
            return
            
        color = PURPLE
        if self.cargo > 0:
            color = (min(255, 128 + self.cargo * 25), 0, min(255, 128 + self.cargo * 25))
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        
        if self.cargo > 0:
            font = pygame.font.Font(None, 24)
            text = font.render(str(self.cargo), True, WHITE)
            text_rect = text.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(text, text_rect)