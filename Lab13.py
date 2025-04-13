# Lab 13 #1 / Nicholas Smith / 10 April 2025

import sys
import pygame as pg
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pg.init()
        self.clock = pg.time.Clock()
        self.settings = Settings()

        # Set up screen, fullscreen.
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.settings.screen_width = self.screen.get_width()
        self.settings.screen_height = self.screen.get_height()

        # Set title bar of game window.
        pg.display.set_caption("Alien Invasion")

        # Create instance of Ship class.
        self.ship = Ship(self)
        # Create a group to store bullets in.
        self.bullets = pg.sprite.Group()
        # Create a group of aliens.
        self.aliens = pg.sprite.Group()

        self._create_fleet()

    def _create_fleet(self):
            """Create the fleet of aliens"""
            # Create an alien and keep adding aliens to the fleet until no room left.
            alien = Alien(self)
            self.aliens.add(alien)
            alien_width, alien_height = alien.rect.size

            current_x, current_y = alien_width, alien_height
            while current_y < (self.settings.screen_height - 8 * alien_height):
                while current_x < (self.settings.screen_width - 7 * alien_width):
                    self._create_alien(current_x, current_y)
                    current_x += 2 * alien_width

                current_x = alien_width
                current_y += 2 * alien_height

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            #self.bullets.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """
        Respond to key presses.

        Args:
            event (pygame.event.Event): The event object containing information about the key press.

        """
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pg.K_q:
            sys.exit()
        elif event.key == pg.K_SPACE:
            self._fire_bullet()
   
    def _check_keyup_events(self, event):
        """Respond to key releases.
        
        Args: 
            event (pygame.event.Event): The event object containing information about the key press
        
        """
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions."""
        self._check_fleet_edges()
        self.aliens.update()

    
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        
        # Set background color, redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        pg.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()