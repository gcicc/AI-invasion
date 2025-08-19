import pygame
from typing import Dict, Any
from enum import Enum
from .constants import *

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
        
        self.running = True
        self.state = GameState.PLAYING
        self.dt = 0.0
        
        from .game_world import GameWorld
        self.world = GameWorld()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                elif event.key == pygame.K_r and self.state == GameState.GAME_OVER:
                    self.restart_game()
    
    def update(self):
        if self.state == GameState.PLAYING:
            self.world.update(self.dt)
    
    def render(self):
        self.screen.fill(BLACK)
        
        if self.state == GameState.PLAYING:
            self.world.render(self.screen)
        elif self.state == GameState.PAUSED:
            self.world.render(self.screen)
            self.render_pause_overlay()
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