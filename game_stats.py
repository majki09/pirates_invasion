class GameStats:
    """Track statistics for pirate Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start pirate Invasion in inactive state
        self.game_active = False

        # High score - read from game_stats.dat file
        with open("game_stats.dat", 'rb') as stats_file:
            score_bytes = stats_file.read(4)
            self.high_score = int.from_bytes(score_bytes, byteorder='big')

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ships_limit
        self.score = 0
        self.level = 1
