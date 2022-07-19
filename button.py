import pygame.font

class Button:
    def __init__(self, ai_game, msg):
        """Initialize button atributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimmenensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (72, 69, 42)
        self.text_color = (220,207,115)
        self.font = pygame.font.SysFont(None,48)

        # Build button's rect object and center it
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Pop-up the message only once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn message into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button, then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)