import pygame
import random
import math
from typing import List, Tuple

class Particle:
    def __init__(self, x: float, y: float, velocity_x: float, velocity_y: float, 
                 color: Tuple[int, int, int], size: float = 3.0, lifetime: float = 1.0):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.color = color
        self.size = size
        self.max_lifetime = lifetime
        self.lifetime = lifetime
        self.alive = True
    
    def update(self, dt: float):
        if not self.alive:
            return
        
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Apply gravity/drag
        self.velocity_y += 100 * dt  # Gravity
        self.velocity_x *= 0.98  # Drag
        self.velocity_y *= 0.98
        
        # Update lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False
    
    def render(self, screen: pygame.Surface):
        if not self.alive:
            return
        
        # Fade alpha based on remaining lifetime
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        current_size = int(self.size * (self.lifetime / self.max_lifetime))
        
        if alpha > 0 and current_size > 0:
            # Create surface with alpha
            particle_surface = pygame.Surface((current_size * 2, current_size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha)
            pygame.draw.circle(particle_surface, color_with_alpha, (current_size, current_size), current_size)
            screen.blit(particle_surface, (int(self.x - current_size), int(self.y - current_size)))

class ParticleSystem:
    def __init__(self):
        self.particles: List[Particle] = []
    
    def add_particle(self, x: float, y: float, velocity_x: float, velocity_y: float,
                    color: Tuple[int, int, int], size: float = 3.0, lifetime: float = 1.0):
        particle = Particle(x, y, velocity_x, velocity_y, color, size, lifetime)
        self.particles.append(particle)
    
    def create_collection_burst(self, x: float, y: float, color: Tuple[int, int, int]):
        """Create particles when alien collects a human"""
        num_particles = 8
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            self.add_particle(
                x + random.uniform(-5, 5),
                y + random.uniform(-5, 5),
                vel_x, vel_y, color,
                size=random.uniform(2, 5),
                lifetime=random.uniform(0.5, 1.0)
            )
    
    def create_base_deposit_effect(self, x: float, y: float, cargo_types: List[str]):
        """Create particles when depositing cargo at base"""
        color_map = {
            "meat": (255, 100, 100),
            "eggs": (255, 255, 100), 
            "dna": (100, 255, 100),
            "cells": (100, 200, 255)
        }
        
        for resource_type in cargo_types:
            color = color_map.get(resource_type, (255, 255, 255))
            
            # Create upward floating particles
            for _ in range(3):
                vel_x = random.uniform(-30, 30)
                vel_y = random.uniform(-100, -50)  # Upward movement
                
                self.add_particle(
                    x + random.uniform(-20, 20),
                    y + random.uniform(-10, 10),
                    vel_x, vel_y, color,
                    size=random.uniform(3, 6),
                    lifetime=random.uniform(1.0, 1.5)
                )
    
    def create_upgrade_effect(self, x: float, y: float):
        """Create particles when purchasing an upgrade"""
        color = (255, 215, 0)  # Gold
        num_particles = 15
        
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 200)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            self.add_particle(
                x, y, vel_x, vel_y, color,
                size=random.uniform(4, 8),
                lifetime=random.uniform(0.8, 1.5)
            )
    
    def update(self, dt: float):
        # Update all particles
        for particle in self.particles:
            particle.update(dt)
        
        # Remove dead particles
        self.particles = [p for p in self.particles if p.alive]
    
    def render(self, screen: pygame.Surface):
        for particle in self.particles:
            particle.render(screen)
    
    def clear(self):
        """Remove all particles"""
        self.particles.clear()