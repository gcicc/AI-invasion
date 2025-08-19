import pygame
import sys
import os
from typing import Dict, List
from .button import Button

# Add game module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from game.constants import *

class UpgradeMenu:
    def __init__(self, game_world):
        self.game_world = game_world
        self.visible = False
        self.buttons: List[Button] = []
        
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.create_upgrade_buttons()
        
        # Close button
        close_button = Button(SCREEN_WIDTH - 120, 10, 100, 40, "CLOSE", callback=self.close)
        self.buttons.append(close_button)
    
    def create_upgrade_buttons(self):
        self.upgrade_buttons = []
        upgrades = ["speed", "cargo", "size", "efficiency"]
        
        for i, upgrade_name in enumerate(upgrades):
            x = 50 + (i % 2) * 300
            y = 200 + (i // 2) * 150
            
            button = Button(x, y, 250, 100, upgrade_name.upper(),
                          callback=lambda u=upgrade_name: self.purchase_upgrade(u))
            self.upgrade_buttons.append((upgrade_name, button))
            self.buttons.append(button)
    
    def purchase_upgrade(self, upgrade_name: str):
        success = self.game_world.upgrade_system.purchase_upgrade(upgrade_name)
        if success:
            # Create particle effect at alien location
            self.game_world.particles.create_upgrade_effect(
                self.game_world.alien.x, 
                self.game_world.alien.y
            )
            print(f"Purchased {upgrade_name} upgrade!")
        else:
            print(f"Cannot afford {upgrade_name} upgrade")
    
    def close(self):
        self.visible = False
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible:
            return False
            
        for button in self.buttons:
            if button.handle_event(event):
                return True
        return False
    
    def render(self, screen: pygame.Surface):
        if not self.visible:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Title
        title = self.font.render("ALIEN UPGRADES", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title, title_rect)
        
        # Resource display
        resources_text = (f"Meat: {self.game_world.resources.meat} | "
                         f"Eggs: {self.game_world.resources.eggs} | "
                         f"DNA: {self.game_world.resources.dna} | "
                         f"Cells: {self.game_world.resources.cells}")
        resources_surface = self.font_small.render(resources_text, True, (200, 200, 200))
        resources_rect = resources_surface.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(resources_surface, resources_rect)
        
        # Upgrade information
        for upgrade_name, button in self.upgrade_buttons:
            info = self.game_world.upgrade_system.get_upgrade_info(upgrade_name)
            if not info:
                continue
            
            # Update button color based on affordability
            if info["maxed"]:
                button.color = (50, 100, 50)
                button.text_color = (200, 255, 200)
                button.enabled = False
                button.update_text(f"{info['name']} (MAX)")
            elif info["can_afford"]:
                button.color = (0, 150, 0)
                button.text_color = WHITE
                button.enabled = True
                button.update_text(f"{info['name']} Lv.{info['level']}")
            else:
                button.color = (150, 50, 50)
                button.text_color = (200, 200, 200)
                button.enabled = True
                button.update_text(f"{info['name']} Lv.{info['level']}")
            
            # Draw upgrade info below button
            info_y = button.rect.y + button.rect.height + 5
            
            desc_text = self.font_small.render(info["description"], True, WHITE)
            screen.blit(desc_text, (button.rect.x, info_y))
            
            if not info["maxed"]:
                cost_text = f"Cost: {info['cost_meat']} Meat"
                if info['cost_eggs'] > 0:
                    cost_text += f", {info['cost_eggs']} Eggs"
                if info['cost_dna'] > 0:
                    cost_text += f", {info['cost_dna']} DNA"
                if info['cost_cells'] > 0:
                    cost_text += f", {info['cost_cells']} Cells"
                
                cost_color = (0, 255, 0) if info["can_afford"] else (255, 100, 100)
                cost_surface = self.font_small.render(cost_text, True, cost_color)
                screen.blit(cost_surface, (button.rect.x, info_y + 25))
        
        # Render buttons
        for button in self.buttons:
            button.render(screen)