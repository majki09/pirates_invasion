# Pirates Invasion
by Janek SQ9NIL, www.operator-paranedyk.pl

## Introduction

<i> Pirates Invasion</i> is a simple <i>Space Invaders</i> clone based on tutorial in Eric Matthes _Python Crash Course: A Hands-On, Project-Based Introduction to Programming_ (2nd Edition by No Starch Press, Inc.). I followed his instructions when I started to learn Python and then made some changes:

- changed topic from alien invasion to sea battle with pirates (my son loves them!) by adding graphics by myself,
- added random distribution of pirates in the fleet,
- improve graphics by flipping ships when reaching the boarder of the screen.

## Gameplay

You are the captain of a ship fighting the pirates fleet that wants to enter the port. Your task is to shoot all pirates ships before they cross your position.

To start the game, press __Click to play__ button.

Use __arrows keys__ to move your ship left and right, and press __spacebar__ to shoot the cannon. You can shoot three cannonballs at the same time.

You can quit the game by pressing __q__ at any time.

Every time you shoot all the pirates ships, you progress to next level. New pirates fleet, that is faster than the previous one, is generated and you will get more points for every pirates ship shoot down.

if pirates ship colides with yours or reaches the bottom of the screen, you will loose one ship. Game ends if you loose three ships.

## Game settings

You can control the game with Settings class, stored in settings.py file.

### Static settings

#### Screen settings
self.screen_width = 1200
self.screen_height = 720
self.bg_color = (0, 162, 232)

#### Ship settings
self.ships_limit = 3

#### Bullet settings
self.bullet_width = 10
self.bullet_height = 10
self.bullet_color = (105, 105, 105)
self.bullets_allowed = 3

#### pirate settings
self.fleet_drop_speed = 20
self.pirate_probability = 8 # probabilty (1-10) of pirate placed in a fleet

#### How fast the game speeds up
self.speedup_scale = 1.1

#### How fast the scores increase
self.speedup_score = 1.5

### Dynamic settings

#### Speeds
self.ship_speed = 2
self.bullet_speed = 2
self.pirate_speed = 0.75

##### Fleet direction: 1 - right, -1 - left
self.fleet_direction = 1

#### Points for shooting a pirate
self.pirate_points = 20
