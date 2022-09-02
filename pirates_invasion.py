import sys
from time import sleep

import pygame
from random import randint

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from pirate import Pirate
from scoreboard import Scoreboard


class PiratesInvasion:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (0, 0),
            pygame.FULLSCREEN
        )
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("pirate Invasion")

        # Create an instance of GameStatistics
        self.stats = GameStats(self)

        # Create a scoreboard
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.pirates = pygame.sprite.Group()

        # Create pirate fleet
        self._create_fleet()

        # Create a start/reset button
        self.play_button = Button(self, "Click to play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse moves
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_pirates()

            self._update_screen()

    def _start_game(self):
        # Reset game pace
        self.settings.initialize_dynamic_settings()

        # Reset game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Delete remaining pirates and bullets.
        self.pirates.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide mouse cursor.
        pygame.mouse.set_visible(False)

    def _check_events(self):
        """Respond to keypresses and mouse moves"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        # TODO: add option to start with space
        """Starts a new game when player clicks a button."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move he ship to the left
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if self.stats.game_active:
                self._fire_bullet()
            elif not self.stats.game_active:
                self._start_game()

    def _check_keyup_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            # Stop movement to the right
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            # Move he ship to the left
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullets position
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Check for collissions between pirates and bullets
        self._check_bullet_pirate_collisions()

    def _check_bullet_pirate_collisions(self):
        """ Check for any bullets that hit pirates.
        If so, get rid of the bullet and the pirate."""
        # Remove any bullets and pirates that collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.pirates, True, True)

        # Update score
        if collisions:
            for pirate in collisions.values():
                self.stats.score += self.settings.pirate_points * len(pirate)
            self.sb.prep_score()
            self.sb.check_high_score()

        # Create new fleet when the last pirate is shoot down.
        if not self.pirates:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Create fleet of pirates."""
        pirate = Pirate(self)
        pirate_width, pirate_height = pirate.rect.size

        # Determine number of pirates in a row
        available_space_x = self.settings.screen_width - 2 * pirate_width
        number_pirates_x = available_space_x // (2 * pirate_width)

        # Determine number of rows
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - ship_height - 3 * pirate_height
        number_rows = available_space_y // (2*pirate_height)

        # Create fleet of pirates
        for row_number in range(number_rows):
            for pirate_number in range(number_pirates_x):
                # Create a pirate and place it into a row with probability of 80%
                if randint(1, 10) <= self.settings.pirate_probability: self._create_pirate(pirate_number, row_number)

        self.settings.fleet_direction = 1

    def _create_pirate(self, pirate_number, row_number):
        """Create a pirate and place it into a row"""
        # Create a pirate
        pirate = Pirate(self)

        # Calculate how many pirates fit into row. Spacing is equal to one pirate.
        pirate_width, pirate_height = pirate.rect.size
        pirate.x = pirate_width + 2 * pirate_width * pirate_number
        pirate.rect.x = pirate.x
        pirate.rect.y = pirate_height + 2 * pirate.rect.height * row_number
        self.pirates.add(pirate)

    def _update_pirates(self):
        """Update the positions of all pirates in the fleet."""
        self._check_fleet_edges()
        self.pirates.update()
        
        # Look for pirate-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.pirates):
            # print('Ship hit!')
            self._ship_hit()

        # Look for pirates hitting the bottom of the screen.
        self._check_pirates_bottom()

    def _change_fleet_direction(self):
        """Drop the entire feet and change its direction."""
        for pirate in self.pirates.sprites():
            pirate.rect.y += self.settings.fleet_drop_speed
            pirate.image = pygame.transform.flip(pirate.image, True, False)
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        """Respond appropriately if any pirates have reached the edge."""
        for pirate in self.pirates.sprites():
            if pirate.check_edges():
                self._change_fleet_direction()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an pirate."""
        if self.stats.ships_left > 0:
            # Update high score to stat file
            with open("game_stats.dat", 'rb') as stats_file:
                score_bytes = stats_file.read(4)
                high_score_from_file = int.from_bytes(score_bytes, byteorder='big')
            if self.stats.high_score > high_score_from_file:
                with open("game_stats.dat", "wb") as stats_file:
                    score_bytes = bytearray(self.stats.score.to_bytes(4, byteorder="big"))
                    stats_file.write(score_bytes)

            # Decrement ships_left and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining pirates and bullets
            self.pirates.empty()
            self.bullets.empty()

            # Create a new ship and a new fleet
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(2)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_pirates_bottom(self):
        """Check if any of the pirates reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()

        for pirate in self.pirates.sprites():
            if pirate.rect.bottom >= screen_rect.bottom:
                # Threat this the same as if the ship got hit
                self._ship_hit()
                break

    def _update_screen(self):
        """Updates the images on the screen, and flip to the new screen."""

        # Redraw the screen
        self.screen.fill(self.settings.bg_color)

        # draw ship
        self.ship.blitme()

        # draw bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # draw pirates
        self.pirates.draw(self.screen)

        # Draw player's score
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance and run a game
    ai = PiratesInvasion()
    ai.run_game()
