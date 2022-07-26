class Settings:
    """A class to store all the settings for Alien Invasion."""

    def __init__(self):
        """Initialize game's static settings."""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (221, 183, 123)

        # Ship settings
        self.ships_limit = 0

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 30

        # How fast the game speeds up
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 2
        self.bullet_speed = 2
        self.alien_speed = 0.75

        # Fleet direction: 1 - right, -1 - left
        self.fleet_direction = 1

        # Points for shooting an alien
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale