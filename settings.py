class Settings:
    """A class to store all the settings for pirate Invasion."""

    def __init__(self):
        """Initialize game's static settings."""

        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0, 162, 232)

        # Ship settings
        self.ships_limit = 3

        # Bullet settings
        self.bullet_width = 10
        self.bullet_height = 10
        self.bullet_color = (105, 105, 105)
        self.bullets_allowed = 3

        # pirate settings
        self.fleet_drop_speed = 20
        self.pirate_probability = 8 # probabilty (1-10) of pirate placed in a fleet

        # How fast the game speeds up
        self.speedup_scale = 1.1

        # How fast the scores increase
        self.speedup_score = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 2
        self.bullet_speed = 2
        self.pirate_speed = 0.75

        # Fleet direction: 1 - right, -1 - left
        self.fleet_direction = 1

        # Points for shooting a pirate
        self.pirate_points = 20

    def increase_speed(self):
        """Increase speed settings and scoring."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.pirate_speed *= self.speedup_scale

        self.pirate_points *= self.speedup_score
        self.pirate_points = int(self.pirate_points)