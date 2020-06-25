# TEMP FILE - IGNORE #

import pygame
import random
from game_variables import *

class Entity(object):
    def __init__(self, rect, speed, health):
        self.rect = rect
        self.speed = speed
        self.health = health

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

    def draw(self, fenetre):
        pass

    def hit(self):
        self.health -= 1

    def is_hit(self, pos):
        return self.rect.collidepoint(pos)

class Invader(Entity):
    def __init__(self, pos, speed=[5,0]):
        rect = pygame.Rect(pos[0], int(pos[1]), imageAlien.get_rect().size[0], imageAlien.get_rect().size[1])
        super().__init__(rect, speed, 2)

        self.shoot_delay = random.uniform(1.0, 3.5)
        self.shoot_timer = self.shoot_delay

    def update(self):
        global score
        super().update()
        if self.health <= 0:
            invaders.remove(self)
            inc_score()


        if self.rect[0] >= WIDTH-20 or self.rect[0] <= 5:
            self.speed[0] = -self.speed[0]

        self.shoot_timer -= 1/FPS

        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = self.shoot_delay

    def draw(self, fenetre):
        if self.health > 1:
            fenetre.blit(imageAlien, (self.rect.x, self.rect.y))
        else:
            fenetre.blit(imageHitAlien, (self.rect.x, self.rect.y))

    def shoot(self):
        alien_projectiles.append([self.rect.x, self.rect.y, 5])  # x, y, speed


class Ship(Entity):
    def __init__(self, pos, speed=[0, 0]):
        rect = pygame.Rect(pos[0], pos[1], imageShip.get_rect().size[0], imageShip.get_rect().size[1])
        super().__init__(rect, speed, 10)

        self.shoot_delay = 0.22
        self.shoot_timer = 0

    def update(self):
        global dead
        super().update()
        if self.rect.x >= WIDTH-20:
            self.rect.x = 5
        elif self.rect.x <= 5:
            self.rect.x = WIDTH-20

        if self.health <= 0:
            dead = True
            alien_projectiles.clear()
            ship_projectiles.clear()

        self.shoot_timer -= 1/FPS

    def draw(self, fenetre):
        for i in range(0, self.health*25, 25):
            fenetre.blit(imageHeart, (i, 0))

        if self.health > 0:
            fenetre.blit(imageShip, (self.rect.x, self.rect.y))

    def shoot(self):
        if self.shoot_timer <= 0:
            ship_projectiles.append(
                [self.rect.x+32, self.rect.y+16, (5,0)])  # x, y, speed
            self.shoot_timer = self.shoot_delay
