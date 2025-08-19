import pygame
import random
import sys
import os
from typing import List
from .alien import Alien
from .human import Human
from .resource_manager import ResourceManager
from .upgrade_system import UpgradeSystem
from .constants import *

# Add ui module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from ui.hud import HUD

class GameWorld:
    def __init__(self):
        self.alien = Alien(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.humans: List[Human] = []
        self.resources = ResourceManager()
        
        self.base_x = 50
        self.base_y = 50
        self.base_size = 40
        
        self.spawn_humans()
        
        # Add frame counter for debugging
        self.frame_count = 0
        
        # Initialize HUD
        self.hud = HUD()
        
        # Initialize upgrade system
        self.upgrade_system = UpgradeSystem(self.alien, self.resources)
    
    def spawn_humans(self):
        num_humans = 20
        for _ in range(num_humans):
            while True:
                x = random.randint(100, SCREEN_WIDTH - 100)
                y = random.randint(100, SCREEN_HEIGHT - 100)
                
                distance_from_alien = ((x - self.alien.x) ** 2 + (y - self.alien.y) ** 2) ** 0.5
                distance_from_base = ((x - self.base_x) ** 2 + (y - self.base_y) ** 2) ** 0.5
                
                if distance_from_alien > 100 and distance_from_base > 80:
                    self.humans.append(Human(x, y))
                    break
    
    def update(self, dt: float):
        self.frame_count += 1
        keys_pressed = pygame.key.get_pressed()
        
        self.alien.update(dt, keys_pressed)
        
        for human in self.humans:
            human.update(dt)
        
        self.check_collisions()
        self.check_base_interaction()
        
        self.resources.update(dt)
        
        # Update HUD
        self.hud.update(self)
    
    def check_collisions(self):
        alien_rect = self.alien.get_rect()
        
        for human in self.humans:
            if human.alive:
                human_rect = human.get_rect()
                if alien_rect.colliderect(human_rect):
                    value = human.consume()  # Get value before consuming
                    if self.alien.consume_human(value):  # Pass value to alien
                        
                        # Add bonus resources for special human types
                        from .human import HumanType
                        if human.type == HumanType.VALUABLE:
                            # Chance for eggs from valuable humans
                            if random.random() < 0.3:  # 30% chance
                                self.resources.add_eggs(1)
                        elif human.type == HumanType.LARGE:
                            # Chance for DNA from large humans
                            if random.random() < 0.2:  # 20% chance
                                self.resources.add_dna(1)
    
    def check_base_interaction(self):
        distance_to_base = ((self.alien.x - self.base_x) ** 2 + (self.alien.y - self.base_y) ** 2) ** 0.5
        
        if distance_to_base < self.base_size and self.alien.cargo > 0:
            # Get cargo info and deposit at base
            cargo_count, cargo_value = self.alien.return_to_base()
            
            # Calculate meat from cargo value with efficiency bonus
            efficiency_bonus = getattr(self.alien, 'efficiency_bonus', 0)
            total_meat = cargo_value + efficiency_bonus
            
            self.resources.add_meat(total_meat)
            
            # Small chance for cells on base return
            if random.random() < 0.1:  # 10% chance
                self.resources.add_cells(1)
    
    def render(self, screen: pygame.Surface):
        # Draw base (blue circle)
        pygame.draw.circle(screen, BLUE, (self.base_x, self.base_y), self.base_size)
        
        # Draw base label
        try:
            font = pygame.font.Font(None, 24)
            base_text = font.render("BASE", True, WHITE)
            base_rect = base_text.get_rect(center=(self.base_x, self.base_y))
            screen.blit(base_text, base_rect)
        except:
            pass  # Skip text if font fails
        
        # Draw humans
        for human in self.humans:
            human.render(screen)
        
        # Draw alien
        self.alien.render(screen)
        
        # Draw enhanced HUD
        self.hud.render(screen, self)
    
    def render_ui(self, screen: pygame.Surface):
        font = pygame.font.Font(None, 36)
        y_offset = 10
        
        meat_text = font.render(f"Meat: {self.resources.meat}", True, WHITE)
        screen.blit(meat_text, (10, y_offset))
        y_offset += 40
        
        cargo_text = font.render(f"Cargo: {self.alien.cargo}/{self.alien.max_cargo}", True, WHITE)
        screen.blit(cargo_text, (10, y_offset))
        y_offset += 40
        
        if self.alien.cargo > 0:
            distance_to_base = ((self.alien.x - self.base_x) ** 2 + (self.alien.y - self.base_y) ** 2) ** 0.5
            if distance_to_base < self.base_size * 1.5:
                hint_text = font.render("At base - cargo will be deposited!", True, (255, 255, 0))
                screen.blit(hint_text, (10, y_offset))