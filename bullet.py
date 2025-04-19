"""
bullet.py

This module defines the Bullet class, which is responsible for managing bullets
fired from the ship in the Alien Invasion game. The Bullet class handles the
creation, movement, and rendering of bullets on the screen.

Classes:
    Bullet: A class to manage bullets fired from the ship.

Usage:
    The Bullet class is instantiated whenever the player fires a bullet. It provides
    methods to update the bullet's position and draw it on the screen.
"""

import pygame as pg
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pg.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midright = ai_game.ship.rect.midleft
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet up the screen."""

        # Update the decimal position of the bullet.
        self.x -= self.settings.bullet_speed
        # Update the rect position.
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        
        pg.draw.rect(self.screen, self.color, self.rect)