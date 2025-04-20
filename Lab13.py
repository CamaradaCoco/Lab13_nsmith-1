# Lab 13 #1 / Nicholas Smith / 10 April 2025

"""
This module defines the AlienInvasion class, which serves as the main entry point
for the Alien Invasion game. It manages the game's initialization, main loop, and
core functionality, including event handling, updating game objects, and rendering
the game screen.

Classes:
    AlienInvasion: The main class to manage game assets and behavior.

Usage:
    To start the game, run this module directly. The game initializes all resources,
    enters the main loop, and handles user input, game updates, and rendering.
"""
import sys
from pathlib import Path
from time import sleep
import pygame as pg
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self) -> None:
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

        # Load laser sound
        self.laser_sound = pg.mixer.Sound(Path.cwd() / "sound" / "laser.mp3")
        self.laser_sound.set_volume(0.05)

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        # Create instance of Ship class.
        self.ship = Ship(self)
        # Create a group to store bullets in.
        self.bullets = pg.sprite.Group()
        # Create a group of aliens.
        self.aliens = pg.sprite.Group()

        self._create_fleet()

        # Start alien invasion in an active state.
        self.game_active = True

    def _create_fleet(self) -> None:
        """Create the fleet of aliens."""
        
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Start the fleet at the left side of the screen.
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 1.5 * alien_height):
            while current_x < (self.settings.screen_width - 10 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 1 * alien_width

            current_x = alien_width
            current_y += 1 * alien_height

    def _check_fleet_edges(self) -> None:
        """Respond appropriately if any aliens have reached an edge."""

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self) -> None:
        """Drop the entire fleet and change the fleet's direction."""

        for alien in self.aliens.sprites():
            alien.rect.x += self.settings.fleet_drop_speed
        

    def _create_alien(self, x_position, y_position) -> None:
        """Create an alien and place it in the fleet."""

        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def run_game(self) -> None:
        """Start the main loop for the game."""

        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self) -> None:
        """Respond to keypresses and mouse events."""

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event) -> None:
        """Respond to key presses."""

        if event.key == pg.K_UP:
            self.ship.moving_up = True
        elif event.key == pg.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pg.K_q:
            sys.exit()
        elif event.key == pg.K_SPACE:
            self._fire_bullet()
   
    def _check_keyup_events(self, event) -> None:
        """Respond to key releases."""

        if event.key == pg.K_UP:
            self.ship.moving_up = False
        elif event.key == pg.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self) -> None:
        """Create a new bullet and add it to the bullets group."""

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

        # Play the laser sound
        self.laser_sound.play()
        self.laser_sound.fadeout(300)

    def _update_bullets(self) -> None:
        """Update position of bullets and get rid of old bullets."""

        # Update bullet positions.
        self.bullets.update()

        self._check_bullet_alien_collisions()

        for bullet in self.bullets.copy():
            if bullet.rect.left <= 0:
                self.bullets.remove(bullet)

    def _check_bullet_alien_collisions(self) -> None:
        """Respond to bullet-alien collisions."""

        # Remove any bullets and aliens that have collided.
        collisions = pg.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self) -> None:
        """Check if the fleet is at an edge, then update the positions."""
        
        self._check_fleet_edges()
        
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_direction * self.settings.alien_speed

        # Move aliens horizontally when fleet hits the bottom
        if alien.rect.bottom >= self.screen.get_rect().bottom:
            alien.rect.x += self.settings.fleet_drop_speed

        # Look for alien-ship collisions.
        if pg.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()


    def _check_aliens_bottom(self) -> None:
        """Check if any aliens have reached the bottom of the screen."""

        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom or alien.rect.top <= 0:
            # Move the fleet to the right and reverse vertical direction
                for alien in self.aliens.sprites():
                    alien.rect.x += self.settings.fleet_drop_speed
                self.settings.fleet_direction *= -1  # Reverse vertical direction
                break

    def _ship_hit(self) -> None:
        """Respond to the ship being hit by an alien."""

        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(1.5)
        else:
            self.game_active = False
    
    def _update_screen(self) -> None:
        """Update images on the screen, and flip to the new screen."""
        
        # Set background color, redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            pg.draw.rect(self.screen, self.settings.bullet_color, bullet.rect)

       # Draw the ship
        self.screen.blit(self.ship.image, self.ship.rect)

        # Draw aliens
        for alien in self.aliens.sprites():
            self.screen.blit(alien.image, alien.rect)

        pg.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()