#!/usr/bin/env python3

import pygame
import sys
from game.game_manager import GameManager

def main():
    pygame.init()
    pygame.font.init()
    
    game = GameManager()
    game.run()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()