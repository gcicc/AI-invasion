import pygame
import sys
import os
from typing import List, Optional
from .button import Button

# Add game module to path  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from game.constants import *

class Menu:
    def __init__(self):
        self.buttons: List[Button] = []
        self.visible = True
    
    def add_button(self, button: Button):
        self.buttons.append(button)
    
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
            
        for button in self.buttons:
            button.render(screen)

class MainMenu(Menu):
    def __init__(self, game_manager):
        super().__init__()
        self.game_manager = game_manager
        
        # Title
        self.title_font = pygame.font.Font(None, 72)
        self.title_text = self.title_font.render("AI INVASION RPG", True, WHITE)
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        
        # Subtitle
        self.subtitle_font = pygame.font.Font(None, 36)
        self.subtitle_text = self.subtitle_font.render("Phase 2: Enhanced UI & Game Feel", True, (200, 200, 200))
        self.subtitle_rect = self.subtitle_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        
        # Buttons
        button_width, button_height = 200, 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        
        start_button = Button(button_x, 300, button_width, button_height, 
                             "START GAME", callback=self.start_game)
        settings_button = Button(button_x, 370, button_width, button_height, 
                                "SETTINGS", callback=self.open_settings)
        quit_button = Button(button_x, 440, button_width, button_height, 
                            "QUIT", callback=self.quit_game)
        
        self.add_button(start_button)
        self.add_button(settings_button) 
        self.add_button(quit_button)
    
    def start_game(self):
        from game.game_manager import GameState
        self.game_manager.state = GameState.PLAYING
        self.visible = False
    
    def open_settings(self):
        print("Settings menu not implemented yet")
    
    def quit_game(self):
        self.game_manager.running = False
    
    def render(self, screen: pygame.Surface):
        if not self.visible:
            return
            
        # Dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Title and subtitle
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.subtitle_text, self.subtitle_rect)
        
        # Buttons
        super().render(screen)

class PauseMenu(Menu):
    def __init__(self, game_manager):
        super().__init__()
        self.game_manager = game_manager
        
        # Title
        self.title_font = pygame.font.Font(None, 72)
        self.title_text = self.title_font.render("PAUSED", True, WHITE)
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        
        # Buttons
        button_width, button_height = 200, 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        
        resume_button = Button(button_x, 300, button_width, button_height,
                              "RESUME", callback=self.resume_game)
        main_menu_button = Button(button_x, 370, button_width, button_height,
                                 "MAIN MENU", callback=self.to_main_menu)
        quit_button = Button(button_x, 440, button_width, button_height,
                            "QUIT", callback=self.quit_game)
        
        self.add_button(resume_button)
        self.add_button(main_menu_button)
        self.add_button(quit_button)
    
    def resume_game(self):
        from game.game_manager import GameState
        self.game_manager.state = GameState.PLAYING
        self.visible = False
    
    def to_main_menu(self):
        from game.game_manager import GameState
        self.game_manager.state = GameState.MENU
        self.visible = False
    
    def quit_game(self):
        self.game_manager.running = False
    
    def render(self, screen: pygame.Surface):
        if not self.visible:
            return
            
        # Dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Title
        screen.blit(self.title_text, self.title_rect)
        
        # Buttons
        super().render(screen)