import pygame
from pygame.sprite import Sprite

class Pirate(Sprite):
    """A class to represent single pirate in a fleet."""

    def __init__(self, ai_game):
        """Initialize the pirate and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the pirate image and set its rect attribute.
        self.image = pygame.image.load('images/ship_pirates.bmp')
        self.rect = self.image.get_rect()

        # Start each new pirate near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Stores pirate's exact horizontal position
        self.x = float(self.rect.x)

    def update(self):
        """Move the fleet right or left."""
        self.x += self.settings.pirate_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """Returns True if pirate is at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            # TODO: turn pirate ship
            return True