"""
game_stats.py

This module defines the GameStats class, which is responsible for tracking and managing
statistics for the Alien Invasion game. These statistics include the number of ships
remaining and other game-related metrics.

Classes:
    GameStats: A class to track and manage game statistics.

Usage:
    The GameStats class is instantiated at the start of the game and is used to track
    statistics that can change during gameplay, such as the number of ships left.
"""

class GameStats:
    """Track statistics for the game."""
    
    def __init__(self, ai_game):
        """Initialize statistics."""
        
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""

        self.ships_left = self.settings.ship_limit