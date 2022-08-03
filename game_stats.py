class GameStats:
    """Track statistics for pirate Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start pirate Invasion in inactive state
        self.game_active = False

        # High score - never to be resetted
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ships_limit
        self.score = 0
        self.level = 1