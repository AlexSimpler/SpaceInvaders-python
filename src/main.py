import random
import pygame
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

SIZE = WIDTH, HEIGHT = (600, 600)
FPS = 60
MAIN_FONT = pygame.font.Font("../fonts/clacon.ttf", 24)
SMALL_FONT = pygame.font.Font("../fonts/clacon.ttf", 20)
PLUS = 93
MINUS = 47

fenetre = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

invaders = []
alien_per_level = 2
alien_mult_factor = 1.5
difficulty_levels, diff_factor = (["hard","so-so","easy"], 2) # level difficulty possibilites
press_count = 0

ship = None
dead = False
home = True

projectiles = []

imageAlien = pygame.image.load('../assets/alien.png')
imageHitAlien = pygame.image.load('../assets/touche.png')
imageShip = pygame.image.load("../assets/vaisseau.png")
imageHeart = pygame.image.load("../assets/heart.png")
imageShip = pygame.transform.scale(imageShip, (64, 64))

dot_count = 1
home_text = """
  ____                       ___                     _                \n 
 / ___| _ __   __ _  ___ ___|_ _|_ ____   ____ _  __| | ___ _ __ ___  \n 
 \___ \| '_ \ / _` |/ __/ _ \| || '_ \ \ / / _` |/ _` |/ _ \ '__/ __| \n 
  ___) | |_) | (_| | (_|  __/| || | | \ V / (_| | (_| |  __/ |  \__\\ \n 
 |____/| .__/ \__,_|\___\___|___|_| |_|\_/ \__,_|\__,_|\___|_|  |___/ \n 
       |_|                                                           
"""
score = 0
level = 0
running = True


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
    def __init__(self, pos, speed=[5, 0]):
        rect = pygame.Rect(pos[0], int(pos[1]), imageAlien.get_rect(
        ).size[0], imageAlien.get_rect().size[1])
        super().__init__(rect, speed, 2)

        self.shoot_delay = random.uniform(1.1, 3.5)
        self.shoot_timer = self.shoot_delay

    def update(self):
        global score
        super().update()
        if self.health <= 0:
            invaders.remove(self)
            score += 1

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
        projectiles.append(Projectile((self.rect.x + 10, self.rect.y + 16), True))


class Ship(Entity):
    def __init__(self, pos, speed=[0, 0]):
        rect = pygame.Rect(pos[0], pos[1], imageShip.get_rect(
        ).size[0], imageShip.get_rect().size[1])
        super().__init__(rect, speed, 3)

        self.shoot_delay = 0.20
        self.shoot_timer = 0

    def update(self):
        global dead
        super().update()
        if self.rect.x >= WIDTH-20:
            self.rect.x = 5
        elif self.rect.x <= 5:
            self.rect.x = WIDTH-20

        if self.health <= 0:
            projectiles.clear() # clear projectiles to stop rendering
            invaders.clear() # remove aliens if dead
            dead = True

        self.shoot_timer -= 1/FPS

    def draw(self, fenetre):
        for i in range(0, self.health * 25, 25):
            fenetre.blit(imageHeart, (i, 0))

        if self.health > 0: #byeeee salut  haha hahahah
            fenetre.blit(imageShip, (self.rect.x, self.rect.y))

    def shoot(self):
        if self.shoot_timer <= 0:
            projectiles.append(Projectile((self.rect.x+32, self.rect.y+16), False))
            self.shoot_timer = self.shoot_delay


class Projectile(Entity):
    def __init__(self, pos, alien=True):
        rect = pygame.Rect(pos[0], pos[1], 3, 3)
        self.alien = alien
        if(self.alien):
            speed = self.calc_alien_trajectory(rect)
        else:
            speed = [0, -7] # our ship
        super().__init__(rect, speed, 0)
    
    def update(self):
        super().update()

    def calc_alien_trajectory(self, rect): # updated
        global ship
        sx, sy = ship.rect.x + 33, ship.rect.y + 16
        ax, ay = rect.x + rect.size[0]/2, rect.y - rect.size[1]/2
        diffX = int((sx - ax) * 0.01) # position difference between ship and invader
        diffY = int((sy - ay) * 0.01) # reduce the trajectory velocity of the projectiles
        return [diffX, diffY]


    def draw(self, fenetre):
        color = (0, 255, 0)
        if self.alien:
            color = (255, 0, 0)
        pygame.draw.circle(fenetre, color, (self.rect.x, self.rect.y), 3)

# Fonction utilitaire pour plus facilement afficher du texte
def _afficher_texte(texte, pos, font=MAIN_FONT, color=(255, 255, 255)):
    fenetre.blit(font.render(texte, True, color), pos)


def draw_ui():
    affichage = " point"
    if score > 1:
        affichage += "s"
    _afficher_texte(str(score) + affichage, (280, 0))
    _afficher_texte("Niveau "+str(level), (518, 0))


def init_new_level():
    global alien_per_level, level
    level += 1
    alien_per_level *= alien_mult_factor
    alien_per_level = round(alien_per_level)
    for i in range(alien_per_level):
        inv = Invader((random.randint(20, HEIGHT-20), random.randint(10, 80)*(level/2)), [2, 0])
        invaders.append(inv)


def init():
    global ship, dead
    ship = Ship((280, HEIGHT-60))
    ship.health = diff_factor+1
    init_new_level()


def draw():
    global dead, home, dot_count
    fenetre.fill((0, 0, 0))

    if not dead and not home:
        ship.draw(fenetre)

        for inv in invaders:
            inv.draw(fenetre)

        for p in projectiles:
            p.draw(fenetre)

        
        draw_ui()
    elif dead:
        _afficher_texte("Game Over !", (263, 260))
        if(score == 1337):
            _afficher_texte("Haxor?", (275, 280))
        else:
            _afficher_texte("Score : "+str(score), (269, 280))
        _afficher_texte("Press ENTER to restart...", (210, 340))
        _afficher_texte("Press Q to quit", (240, 360))
        _afficher_texte("Press M to return to the menu", (180, 380))

    elif home:
        for i, line in enumerate(home_text.split("\n")):
            _afficher_texte(line, (30, 10 + 9 * i), font=SMALL_FONT)
        _afficher_texte("Remastered", (260, 110))
        _afficher_texte("A,D or ←,→ to move", (225, 280))
        _afficher_texte("SPACE or ↑ to shoot", (220, 310))
        _afficher_texte("Press ENTER to start...", (215, 340))
        _afficher_texte("+ or - to adjust the difficulty ["+str(difficulty_levels[diff_factor])+"]", (140, 560))
        _afficher_texte("Made by Alexis and Alexandre", (185, 580))
    pygame.display.flip()


def update():
    if not dead and not home:
        ship.update()

        for p in projectiles:
            p.update()
            if(p.rect.y >= HEIGHT or p.rect.y <= 0):
                projectiles.remove(p)
            if(ship.is_hit((p.rect.x, p.rect.y)) and p.alien):
                ship.hit()
                try:
                    projectiles.remove(p)
                except:
                    pass

        for inv in invaders: # updated
            inv.update()
            for p in projectiles:
                if(inv.is_hit((p.rect.x, p.rect.y)) and not p.alien):
                    inv.hit()
                    projectiles.remove(p)

        if len(invaders) == 0:
            init_new_level()


def handle_keyboard():
    global dead, level, score, alien_per_level, first, home, running, diff_factor, press_count, choice

    key = pygame.key.get_pressed()

    if(key[pygame.K_LEFT] or key[pygame.K_a]):
        ship.rect.x -= 5
    elif(key[pygame.K_RIGHT] or key[pygame.K_d]):
        ship.rect.x += 5
    if(key[pygame.K_SPACE] or key[pygame.K_UP]):
        ship.shoot()
    elif(key[pygame.K_RETURN]):
        if dead:
            invaders.clear()
            alien_per_level = 2
            health = 3
            score = 0
            level = 0
            dead = False
            init()
        elif home:
            invaders.clear()
            alien_per_level = 2
            level = 0
            score = 0
            health = 3
            init()
            home = False
            dead = False
    if(dead):
        if(key[pygame.K_q]):
                running = False
        elif (key[pygame.K_m]):
            invaders.clear()
            alien_per_level = 2
            home = True
            dead = False
    if(home):
        if(key[PLUS] or key[MINUS]):
            press_count += 1

        if(key[PLUS]):
            if(not press_count % 5 or not press_count):
                if(diff_factor > 0): # difficulty_levels["hard"]
                    diff_factor -= 1 
                    ship.health = diff_factor+1
        elif(key[MINUS]):
            if(not press_count % 5 or not press_count):
                if(diff_factor < len(difficulty_levels) - 1): # difficulty_levels["hard"]
                    diff_factor += 1
                    ship.health = diff_factor+1
        if(press_count > 9999):
            press_count = 0


init()
while(running):
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    handle_keyboard()
    update()
    draw()

pygame.quit()
