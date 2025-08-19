import pygame
from typing import Tuple
import sys
import os

# Add game module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from game.constants import *

class ProgressBar:
    def __init__(self, x: int, y: int, width: int, height: int,
                 bg_color: Tuple[int, int, int] = (50, 50, 50),
                 fill_color: Tuple[int, int, int] = (0, 255, 0),
                 border_color: Tuple[int, int, int] = (255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.border_color = border_color
        self.value = 0.0
        self.max_value = 1.0
    
    def set_value(self, value: float, max_value: float = None):
        self.value = value
        if max_value is not None:
            self.max_value = max_value
    
    def render(self, screen: pygame.Surface):
        # Background
        pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # Fill
        if self.max_value > 0:
            fill_width = int((self.value / self.max_value) * self.rect.width)
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(screen, self.fill_color, fill_rect)
        
        # Border
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

class ResourceDisplay:
    def __init__(self, x: int, y: int, label: str, color: Tuple[int, int, int] = WHITE, font_size: int = 24):
        self.x = x
        self.y = y
        self.label = label
        self.color = color
        self.font = pygame.font.Font(None, font_size)
        self.value = 0
        self.last_value = 0
        self.highlight_timer = 0.0
        
        # Pre-render label
        self.label_surface = self.font.render(f"{label}:", True, self.color)
    
    def update_value(self, value: int, dt: float = 0.0):
        if value > self.last_value:
            self.highlight_timer = 1.0  # Highlight for 1 second
        self.last_value = self.value
        self.value = value
        
        if self.highlight_timer > 0:
            self.highlight_timer -= dt
    
    def render(self, screen: pygame.Surface):
        # Label
        screen.blit(self.label_surface, (self.x, self.y))
        
        # Value with highlight effect
        value_color = WHITE
        if self.highlight_timer > 0:
            # Flash effect when value increases
            flash_intensity = int(255 * (self.highlight_timer / 1.0))
            value_color = (255, 255, flash_intensity)
        
        value_text = self.font.render(str(self.value), True, value_color)
        screen.blit(value_text, (self.x + 60, self.y))

class HUD:
    def __init__(self):
        # Resource displays with proper colors
        self.meat_display = ResourceDisplay(10, 10, "Meat", (255, 100, 100))  # Red
        self.eggs_display = ResourceDisplay(10, 40, "Eggs", (255, 255, 100))  # Yellow
        self.dna_display = ResourceDisplay(10, 70, "DNA", (100, 255, 100))    # Green
        self.cells_display = ResourceDisplay(10, 100, "Cells", (100, 200, 255))  # Blue
        
        # Progress bars
        self.cargo_bar = ProgressBar(200, 10, 200, 20, fill_color=(255, 165, 0))
        
        # Labels
        self.font_small = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 36)
        
        # Cargo label
        self.cargo_label = self.font_small.render("Cargo:", True, WHITE)
    
    def update(self, game_world, dt: float = 0.0):
        # Update resource displays with delta time for animations
        self.meat_display.update_value(game_world.resources.meat, dt)
        self.eggs_display.update_value(game_world.resources.eggs, dt)
        self.dna_display.update_value(game_world.resources.dna, dt)
        self.cells_display.update_value(game_world.resources.cells, dt)
        
        # Update progress bars
        self.cargo_bar.set_value(game_world.alien.cargo, game_world.alien.max_cargo)
    
    def render(self, screen: pygame.Surface, game_world):
        # Semi-transparent HUD background
        hud_bg = pygame.Surface((450, 140))
        hud_bg.set_alpha(180)
        hud_bg.fill((0, 0, 0))
        screen.blit(hud_bg, (5, 5))
        
        # Resource displays  
        self.meat_display.render(screen)
        self.eggs_display.render(screen)
        self.dna_display.render(screen)
        self.cells_display.render(screen)
        
        # Cargo section
        screen.blit(self.cargo_label, (200, 35))
        self.cargo_bar.render(screen)
        
        # Cargo text with value
        cargo_text = f"{game_world.alien.cargo}/{game_world.alien.max_cargo}"
        if hasattr(game_world.alien, 'cargo_value') and game_world.alien.cargo_value > 0:
            cargo_text += f" (Value: {game_world.alien.cargo_value})"
        cargo_surface = self.font_small.render(cargo_text, True, WHITE)
        cargo_rect = cargo_surface.get_rect(center=(300, 20))
        screen.blit(cargo_surface, cargo_rect)
        
        # Base proximity hint
        distance_to_base = ((game_world.alien.x - game_world.base_x) ** 2 + 
                           (game_world.alien.y - game_world.base_y) ** 2) ** 0.5
        
        if game_world.alien.cargo > 0 and distance_to_base < game_world.base_size * 2:
            hint_text = self.font_small.render("Near base - cargo will be deposited!", True, (255, 255, 0))
            screen.blit(hint_text, (10, 150))
        
        # Speed/Stats info
        stats_text = f"Speed: {game_world.alien.speed:.0f} | Size: {game_world.alien.size}"
        stats_surface = self.font_small.render(stats_text, True, (200, 200, 200))
        screen.blit(stats_surface, (10, SCREEN_HEIGHT - 50))
        
        # Controls reminder
        controls_text = "WASD: Move | ESC: Menu | U: Upgrades"
        controls_surface = self.font_small.render(controls_text, True, (150, 150, 150))
        screen.blit(controls_surface, (10, SCREEN_HEIGHT - 25))