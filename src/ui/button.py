import pygame
from typing import Callable, Optional, Tuple

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str, font_size: int = 36, 
                 color: Tuple[int, int, int] = (100, 100, 100),
                 hover_color: Tuple[int, int, int] = (150, 150, 150),
                 text_color: Tuple[int, int, int] = (255, 255, 255),
                 callback: Optional[Callable] = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.callback = callback
        self.hovered = False
        self.enabled = True
        
        # Pre-render text
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.enabled:
            return False
            
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:  # Left click
                if self.callback:
                    self.callback()
                return True
        return False
    
    def update_text(self, new_text: str):
        self.text = new_text
        self.text_surface = self.font.render(new_text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def render(self, screen: pygame.Surface):
        if not self.enabled:
            color = (50, 50, 50)
        else:
            color = self.hover_color if self.hovered else self.color
            
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        screen.blit(self.text_surface, self.text_rect)