import pygame as pg
from pygame.sprite import Sprite

class Alien(Sprite):
    """Represents a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute.
        global image
        self.image = pg.image.load('images/small.png').convert_alpha()
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""

        screen_rect = self.screen.get_rect()
        if self.rect.top <= 0 or self.rect.bottom >= screen_rect.bottom:
            return True
        return False

    def update(self):
        """Move the alien to the right."""
        
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x