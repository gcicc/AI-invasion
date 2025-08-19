import pygame
import random
from .constants import *

class Human:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.size = HUMAN_SIZE
        self.value = HUMAN_VALUE
        self.alive = True
        
        self.spawn_timer = 0.0
        self.spawn_delay = random.uniform(1.0, 3.0)
    
    def update(self, dt: float):
        if not self.alive:
            self.spawn_timer += dt
            if self.spawn_timer >= self.spawn_delay:
                self.respawn()
    
    def respawn(self):
        self.alive = True
        self.spawn_timer = 0.0
        self.spawn_delay = random.uniform(1.0, 3.0)
    
    def consume(self):
        if self.alive:
            self.alive = False
            return self.value
        return 0
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
    
    def render(self, screen: pygame.Surface):
        if self.alive:
            pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), self.size)
        else:
            alpha = max(0, 255 - int(self.spawn_timer * 127))
            if alpha > 0:
                s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (0, 255, 0, alpha), (self.size, self.size), self.size)
                screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))