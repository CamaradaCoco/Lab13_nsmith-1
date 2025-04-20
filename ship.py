"""
ship.py

This module defines the Ship class, which is responsible for managing the player's ship
in the Alien Invasion game. The Ship class handles the ship's initialization, movement,
and rendering on the screen.

Classes:
    Ship: A class to manage the player's ship.

Usage:
    The Ship class is instantiated by passing the main game instance (ai_game) as an argument.
    It provides methods to update the ship's position based on user input, draw the ship
    on the screen, and center the ship when needed.
"""

import pygame as pg
from pathlib import Path

class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect.
        image_path = Path.cwd() / "images" / "spaceship.png"
        self.image = pg.image.load(str(image_path)).convert_alpha()
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midright = self.screen_rect.midright

        # Store a floating value for the ship's exact horizontal position.
        self. y= float(self.rect.y)

        # Movement flags
        self.moving_up = False
        self.moving_down = False

    def blitme(self):
        """Draw the ship at its current location."""

        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship's position based on the movement flags."""

        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        
        # Update rect object from self.x.
        self.rect.y = self.y

    def center_ship(self):
        """Center the ship on the screen."""
        
        self.rect.midright = self.screen_rect.midright
        self.x = float(self.rect.x)
