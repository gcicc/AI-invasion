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
        self.cargo_types = []  # Track types of carried humans for base deposit
        self.meat = 0
        self.alive = True
        self.efficiency_bonus = 0
        
        self.vel_x = 0.0
        self.vel_y = 0.0
        
        # Animation properties
        self.animation_timer = 0.0
        self.base_size = self.size
    
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
        
        # Update animation
        self.animation_timer += dt
        
        # Pulse effect when carrying cargo
        if self.cargo > 0:
            pulse = 1.0 + 0.2 * math.sin(self.animation_timer * 4)  # Fast pulse
            self.size = int(self.base_size * pulse)
        else:
            self.size = self.base_size
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
    
    def consume_human(self, human_type: str) -> bool:
        if self.cargo < self.max_cargo:
            self.cargo += 1
            self.cargo_types.append(human_type)
            return True
        return False
    
    def return_to_base(self):
        # Return cargo types for resource processing
        cargo_types = self.cargo_types.copy()
        self.cargo = 0
        self.cargo_types = []
        return cargo_types
    
    def get_evolution_color(self):
        """Get alien color based on upgrade levels"""
        total_upgrades = 0
        if hasattr(self, '_upgrade_system_ref'):
            for upgrade in self._upgrade_system_ref.upgrades.values():
                total_upgrades += upgrade.level
        
        # Evolution colors based on total upgrade levels
        if total_upgrades == 0:
            return PURPLE  # Base alien
        elif total_upgrades < 5:
            return (150, 0, 200)  # Slightly evolved
        elif total_upgrades < 10:
            return (200, 50, 150)  # More evolved
        elif total_upgrades < 15:
            return (255, 100, 100)  # Highly evolved
        else:
            return (255, 200, 0)  # Legendary
    
    def render(self, screen: pygame.Surface):
        if not self.alive:
            return
            
        # Base color with evolution
        color = self.get_evolution_color()
        
        # Cargo effect overlay
        if self.cargo > 0:
            # Pulsing glow when carrying cargo
            glow_intensity = int(50 * (1.0 + math.sin(self.animation_timer * 6)))
            color = (
                min(255, color[0] + glow_intensity),
                min(255, color[1] + glow_intensity // 2),
                min(255, color[2] + glow_intensity)
            )
        
        # Draw alien with current size (includes pulse animation)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        
        # Draw evolution indicators (spikes for higher evolution)
        total_upgrades = 0
        if hasattr(self, '_upgrade_system_ref'):
            for upgrade in self._upgrade_system_ref.upgrades.values():
                total_upgrades += upgrade.level
        
        if total_upgrades >= 5:
            # Draw spikes around the alien
            num_spikes = min(8, total_upgrades // 2)
            for i in range(num_spikes):
                angle = (2 * math.pi * i) / num_spikes
                spike_length = self.size // 3
                start_x = self.x + math.cos(angle) * self.size
                start_y = self.y + math.sin(angle) * self.size
                end_x = self.x + math.cos(angle) * (self.size + spike_length)
                end_y = self.y + math.sin(angle) * (self.size + spike_length)
                pygame.draw.line(screen, color, (int(start_x), int(start_y)), (int(end_x), int(end_y)), 3)
        
        # Draw cargo count
        if self.cargo > 0:
            font = pygame.font.Font(None, 24)
            text = font.render(str(self.cargo), True, WHITE)
            text_rect = text.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(text, text_rect)