import pygame
import random
from enum import Enum
from .constants import *

class HumanType(Enum):
    NORMAL = "normal"
    FAST = "fast"
    VALUABLE = "valuable"
    LARGE = "large"

class Human:
    def __init__(self, x: float, y: float, human_type: HumanType = None):
        self.x = x
        self.y = y
        self.alive = True
        
        # Determine human type
        if human_type is None:
            # Random type with weighted probability
            rand = random.random()
            if rand < 0.6:  # 60% normal
                self.type = HumanType.NORMAL
            elif rand < 0.8:  # 20% fast
                self.type = HumanType.FAST
            elif rand < 0.95:  # 15% valuable
                self.type = HumanType.VALUABLE
            else:  # 5% large
                self.type = HumanType.LARGE
        else:
            self.type = human_type
        
        # Set attributes based on type
        self.setup_attributes()
        
        self.spawn_timer = 0.0
        self.spawn_delay = random.uniform(1.0, 3.0)
    
    def setup_attributes(self):
        if self.type == HumanType.NORMAL:
            self.size = HUMAN_SIZE
            self.value = 1
            self.color = (0, 255, 0)  # Green
            self.move_speed = 0
        elif self.type == HumanType.FAST:
            self.size = HUMAN_SIZE - 2
            self.value = 1
            self.color = (0, 255, 255)  # Cyan
            self.move_speed = 30  # Moves around
        elif self.type == HumanType.VALUABLE:
            self.size = HUMAN_SIZE + 2
            self.value = 3
            self.color = (255, 215, 0)  # Gold
            self.move_speed = 0
        elif self.type == HumanType.LARGE:
            self.size = HUMAN_SIZE + 5
            self.value = 5
            self.color = (255, 0, 255)  # Magenta
            self.move_speed = 0
        
        # Movement for fast humans
        if self.move_speed > 0:
            self.move_direction = random.uniform(0, 2 * 3.14159)
            self.move_timer = 0.0
    
    def update(self, dt: float):
        if not self.alive:
            self.spawn_timer += dt
            if self.spawn_timer >= self.spawn_delay:
                self.respawn()
        elif self.move_speed > 0:  # Fast humans move around
            import math
            self.move_timer += dt
            
            # Change direction periodically
            if self.move_timer > 2.0:
                self.move_direction = random.uniform(0, 2 * math.pi)
                self.move_timer = 0.0
            
            # Move
            self.x += math.cos(self.move_direction) * self.move_speed * dt
            self.y += math.sin(self.move_direction) * self.move_speed * dt
            
            # Bounce off boundaries
            if self.x < self.size or self.x > SCREEN_WIDTH - self.size:
                self.move_direction = math.pi - self.move_direction
                self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
            if self.y < self.size or self.y > SCREEN_HEIGHT - self.size:
                self.move_direction = -self.move_direction
                self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))
    
    def respawn(self):
        self.alive = True
        self.spawn_timer = 0.0
        self.spawn_delay = random.uniform(1.0, 3.0)
        
        # Reset movement attributes for fast humans
        if self.move_speed > 0:
            self.move_direction = random.uniform(0, 2 * 3.14159)
            self.move_timer = 0.0
    
    def consume(self):
        if self.alive:
            self.alive = False
            return self.value
        return 0
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
    
    def render(self, screen: pygame.Surface):
        if self.alive:
            # Draw main circle with type-specific color
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
            
            # Add visual indicators for special types
            if self.type == HumanType.VALUABLE or self.type == HumanType.LARGE:
                # Draw outline for valuable/large humans
                pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size, 2)
            
            if self.type == HumanType.FAST and hasattr(self, 'move_timer'):
                # Add motion trails for fast humans
                trail_alpha = int(100 * (1 - (self.move_timer % 0.5) / 0.5))
                if trail_alpha > 0:
                    s = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
                    pygame.draw.circle(s, (*self.color, trail_alpha), (self.size * 2, self.size * 2), self.size + 2)
                    screen.blit(s, (int(self.x - self.size * 2), int(self.y - self.size * 2)))
        else:
            # Fading respawn indicator
            alpha = max(0, 255 - int(self.spawn_timer * 127))
            if alpha > 0:
                s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*self.color, alpha), (self.size, self.size), self.size)
                screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))