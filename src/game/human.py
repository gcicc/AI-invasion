import pygame
import random
from enum import Enum
from .constants import *

class HumanType(Enum):
    MEAT = "meat"      # Red humans give meat
    EGGS = "eggs"      # Yellow humans give eggs  
    DNA = "dna"        # Green humans give DNA
    CELLS = "cells"    # Blue humans give cells

class Human:
    def __init__(self, x: float, y: float, human_type: HumanType = None):
        self.x = x
        self.y = y
        self.alive = True
        
        # Determine human type
        if human_type is None:
            # Equal distribution of resource types
            rand = random.random()
            if rand < 0.4:  # 40% meat
                self.type = HumanType.MEAT
            elif rand < 0.7:  # 30% eggs
                self.type = HumanType.EGGS
            elif rand < 0.9:  # 20% DNA
                self.type = HumanType.DNA
            else:  # 10% cells
                self.type = HumanType.CELLS
        else:
            self.type = human_type
        
        # Set attributes based on type
        self.setup_attributes()
        
        self.spawn_timer = 0.0
        self.spawn_delay = random.uniform(1.0, 3.0)
    
    def setup_attributes(self):
        if self.type == HumanType.MEAT:
            self.size = HUMAN_SIZE
            self.value = 1
            self.color = (255, 100, 100)  # Red - matches HUD meat color
            self.move_speed = 0
            self.resource_type = "meat"
        elif self.type == HumanType.EGGS:
            self.size = HUMAN_SIZE
            self.value = 1  
            self.color = (255, 255, 100)  # Yellow - matches HUD eggs color
            self.move_speed = 0
            self.resource_type = "eggs"
        elif self.type == HumanType.DNA:
            self.size = HUMAN_SIZE
            self.value = 1
            self.color = (100, 255, 100)  # Green - matches HUD DNA color
            self.move_speed = 0
            self.resource_type = "dna"
        elif self.type == HumanType.CELLS:
            self.size = HUMAN_SIZE
            self.value = 1
            self.color = (100, 200, 255)  # Blue - matches HUD cells color
            self.move_speed = 0
            self.resource_type = "cells"
        
        # No movement - all humans are stationary for clear color identification
        self.move_direction = 0
        self.move_timer = 0.0
    
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
            # Draw main circle with resource-type color
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
            
            # Add white outline for better visibility
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size, 1)
        else:
            # Fading respawn indicator
            alpha = max(0, 255 - int(self.spawn_timer * 127))
            if alpha > 0:
                s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*self.color, alpha), (self.size, self.size), self.size)
                screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))