import pygame

SIZE = WIDTH, HEIGHT = (600, 600)
FPS = 60
MAIN_FONT = pygame.font.Font("../fonts/clacon.ttf", 24)


invaders = []
alien_projectiles = []
alien_per_level = 2
alien_mult_factor = 1.5

ship = None
dead = False
ship_projectiles = []

imageAlien = pygame.image.load('../assets/alien.png')
imageHitAlien = pygame.image.load('../assets/touche.png')
imageShip = pygame.image.load("../assets/vaisseau.png")
imageHeart = pygame.image.load("../assets/heart.png")
imageShip = pygame.transform.scale(imageShip, (64, 64))

score = 0
level = 0
