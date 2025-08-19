import pygame
import sys
import os
from typing import Dict, Any
from enum import Enum
from .constants import *

# Add ui module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from ui.menu import MainMenu, PauseMenu
from ui.upgrade_menu import UpgradeMenu

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing" 
    PAUSED = "paused"
    GAME_OVER = "game_over"

class GameManager:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("AI Invasion RPG")
        self.clock = pygame.time.Clock()
        
        # Set up mouse cursor
        pygame.mouse.set_visible(True)
        
        self.running = True
        self.state = GameState.MENU
        self.dt = 0.0
        
        from .game_world import GameWorld
        
        self.world = GameWorld()
        self.main_menu = MainMenu(self)
        self.pause_menu = PauseMenu(self)
        self.upgrade_menu = UpgradeMenu(self.world)
    
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Handle menu events first
            if self.state == GameState.MENU:
                self.main_menu.handle_event(event)
            elif self.state == GameState.PAUSED:
                self.pause_menu.handle_event(event)
            elif self.upgrade_menu.visible:
                self.upgrade_menu.handle_event(event)
            
            # Handle mouse clicks for gameplay
            elif event.type == pygame.MOUSEBUTTONDOWN and self.state == GameState.PLAYING:
                if not self.upgrade_menu.visible:  # Only if upgrade menu is closed
                    self.world.handle_mouse_click(event.pos, event.button)
                
            # Handle game events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                        self.pause_menu.visible = True
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                        self.pause_menu.visible = False
                elif event.key == pygame.K_u and self.state == GameState.PLAYING:
                    self.upgrade_menu.visible = not self.upgrade_menu.visible
                elif event.key == pygame.K_q and self.state == GameState.PLAYING:
                    # Claim completed quests
                    completed_quests = self.world.quest_system.get_completed_quests()
                    for i in range(len(completed_quests)):
                        self.world.quest_system.claim_quest_reward(0)  # Always claim first completed quest
                elif event.key == pygame.K_r and self.state == GameState.GAME_OVER:
                    self.restart_game()
    
    def update(self):
        if self.state == GameState.PLAYING:
            mouse_pos = pygame.mouse.get_pos()
            self.world.update(self.dt, mouse_pos)
    
    def render(self):
        self.screen.fill(BLACK)
        
        if self.state == GameState.MENU:
            self.main_menu.render(self.screen)
        elif self.state == GameState.PLAYING:
            self.world.render(self.screen)
            if self.upgrade_menu.visible:
                self.upgrade_menu.render(self.screen)
        elif self.state == GameState.PAUSED:
            self.world.render(self.screen)
            self.pause_menu.render(self.screen)
        elif self.state == GameState.GAME_OVER:
            self.render_game_over()
        
        pygame.display.flip()
    
    def render_pause_overlay(self):
        font = pygame.font.Font(None, 72)
        text = font.render("PAUSED", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)
        
        font_small = pygame.font.Font(None, 36)
        text_small = font_small.render("Press ESC to continue", True, WHITE)
        text_small_rect = text_small.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(text_small, text_small_rect)
    
    def render_game_over(self):
        font = pygame.font.Font(None, 72)
        text = font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)
        
        font_small = pygame.font.Font(None, 36)
        text_small = font_small.render("Press R to restart", True, WHITE)
        text_small_rect = text_small.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(text_small, text_small_rect)
    
    def restart_game(self):
        from .game_world import GameWorld
        self.world = GameWorld()
        self.state = GameState.PLAYING
    
    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update()
            self.render()
        
        return