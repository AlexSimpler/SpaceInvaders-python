# -*- coding: utf-8 -*-

import pygame
from random import *
import time
import cv2


pygame.init()  # INIT

fenetre = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Space Invader")

im = cv2.imread('assets/alien.png')
imgAlienSize = im.shape

imageVaisseau = pygame.image.load("assets/vaisseau.png")
imageVaisseau = pygame.transform.scale(imageVaisseau, (64, 64))
heart = pygame.image.load('assets/heart.png')
hit = pygame.image.load('assets/touche.png')
imageAlien = pygame.image.load('assets/alien.png')

bandeau = pygame.Rect(0, 0, 600, 40)
arial24 = pygame.font.Font("fonts/clacon.ttf", 24)

level = 1
levelTxt = ["level ", str(level)]
levelstring = ''.join(levelTxt)
levelscore = arial24.render(levelstring, True, pygame.Color(255, 255, 255))

score = 0
scorelist = [str(score), " points"]
scorestring = ''.join(scorelist)
surfacescore = arial24.render(scorestring, True, pygame.Color(255, 255, 255))


class list2(list):
    def __init__(self):
        super().__init__()

    def findIndex(self, index):
        for i, j in enumerate(self):
            if j == str(index):
                return i
        return -1

    def unique(self, value):
        count = 0
        for i in range(len(self)):
            if(self[i] == value):
                count += 1
        if(count > 1):
            return False
        else:
            return True

    def last(self):
        return self[len(self)-1]


class dictv2(dict):
    def __init__(self):
        super().__init__()

    def getKey(self, value):
        return list(self.keys())[list(self.values()).index(value)]

    def at(self, index):
        for x in self.keys():
            for y in range(index):
                continue
            return x

    def last(self):
        arr = list()
        for key in self:
            arr.append(x)
        return arr[len(arr)-1] if len(arr) else False

    def everyup(self, check):
        for key in self:
            for i in range(len(self[key])):
                if i > check:
                    return True
        return False

    def everydown(self, check):
        for key in self:
            for i in range(len(self[key])):
                if i < check:
                    return True
        return False

    def every(self, check):
        for key in self:
            for i in range(len(self[key])):
                if i == check:
                    return True
        return False


DEBUG = False
positionVaisseau = (300, 545)
health = 3
positions = dictv2()
projectiles = dictv2()
enemyProjectiles = dictv2()
count = 0
nbAliens = 0
vieAlien = 2
x = 0
difficulty = 1
loop = True
timeout = 0
enemyTimeout = 0
clock = pygame.time.Clock()  # fps
droite = False
sleepI = 0
droite = True
w, h = pygame.display.get_surface().get_size()
nbr = 1
heartPos = [0, 25, 50]
interval = 0
queue = list2()

# UTILITY
# ----------------------------- #


def everytuple(struct, check):
    final = []
    for i in range(len(struct)):
        if(struct[i] == check):
            final.append(struct[i])
    if(struct == final):
        return True
    else:
        return False


def everydict(dict, index, check):
    iterations = 0
    for value in dict.values():
        if(value[index] == check):
            iterations += 1
    if(iterations == len(dict)):
        return True
    else:
        return False


def already(dict, val):
    for value in dict.values():
        if value == val:
            return True
    return False


def cmpPos(pos1, pos2, comparaison: int):
    resultats: [bool] = []
    retour: bool = False

    if len(pos1) != len(pos2):
        raise ValueError(
            'Les deux positions doivent avoir une longueur égale.')
    for i in range(len(pos1)):
        if comparaison == 1:
            if(pos1[i] == pos2[i]):
                resultats.append(True)
            else:
                resultats.append(False)
        if comparaison == 2:
            if(pos1[i] < pos2[i]):
                resultats.append(True)
            else:
                resultats.append(False)
        if comparaison == 3:
            if(pos1[i] > pos2[i]):
                resultats.append(True)
            else:
                resultats.append(False)

    return everytuple(resultats, True)


def between(val, left: int, right: int):
    if(val >= left and val <= right):
        return True
    else:
        return False

# ----------------------------- #


def draw():  # RENDERING
    global imageAlien, imageVaisseau, fenetre, projectile, x, health
    fenetre.fill(pygame.Color(0, 0, 0))

    for i in range(health):
        fenetre.blit(heart, (heartPos[i], 0))
    fenetre.blit(imageVaisseau, positionVaisseau)
    fenetre.blit(levelscore, (530, 0))
    fenetre.blit(surfacescore, (280, 0))
    for i in positions.keys():
        fenetre.blit(positions[i][2], positions[i][0])
    for j in projectiles.keys():
        pygame.draw.circle(fenetre, (255, 255, 255), projectiles[j], 5)
    for k in enemyProjectiles.keys():
        pygame.draw.circle(fenetre, (255, 255, 255), enemyProjectiles[k][0], 5)
    pygame.display.flip()


def updateScore(facteur: int):
    global score, scorelist, scorestring, surfacescore
    score += facteur
    scorelist = [str(score), " points"]
    scorestring = ''.join(scorelist)
    surfacescore = arial24.render(
        scorestring, True, pygame.Color(255, 255, 255))
    fenetre.blit(surfacescore, (280, 0))  # On affiche le score


def updateLevel():
    global level, levelTxt, levelstring, levelscore, difficulty
    difficulty *= 2
    level += 1
    levelTxt = ["level ", str(level)]
    levelstring = ''.join(levelTxt)
    levelscore = arial24.render(levelstring, True, pygame.Color(255, 255, 255))


def cleanAliens(struct):
    global positions
    for i in range(len(struct)):
        positions.pop(struct[i])


def isHit():
    global projectile, positions, hit
    w = imgAlienSize[1]
    h = imgAlienSize[0]
    cleaned = list()

    if(not bool(positions)):
        updateLevel()
        addAlien(difficulty)
    if(len(positions) > 0 and len(projectiles) > 0):
        for alien in positions.keys():
            if(positions[alien][1] > 0):
                for j in projectiles.keys():
                    if(between(projectiles[j][0], positions[alien][0][0], positions[alien][0][0]+w) and
                       between(projectiles[j][1], positions[alien][0][1], positions[alien][0][1]+h)):
                        positions[alien][1] -= 1
                        if(DEBUG):
                            print("touched ", positions.getKey(
                                positions[alien]))
                        positions[alien][2] = hit
                        projectiles[j] = (-100, -100)
            elif(positions[alien][1] <= 0):
                cleaned.append(alien)
                positions[alien][1] = -1
                positions[alien][0] = (-100, -100)
                updateScore(1)
    cleanAliens(cleaned)


def playerHit():
    global enemyProjectiles, positionVaisseau, health
    cleaned = list()
    if(bool(enemyProjectiles)):
        for i in enemyProjectiles.keys():
            if(between(enemyProjectiles[i][0][0], positionVaisseau[0], positionVaisseau[0]+64) and between(enemyProjectiles[i][0][1], positionVaisseau[1], positionVaisseau[1]+64)):
                enemyProjectiles[i][0] = (-100, -100)
                cleaned.append(i)
                health -= 1
        cleanProjectiles(cleaned, True)


def addAlien(facteur: int = 1):
    global positionAlien, fenetre, nbAliens
    for i in range(facteur):
        img = pygame.image.load('assets/alien.png')
        nbAliens += 1
        positions[nbAliens-1] = [(randint(1, 580), randint(50, 150)), 2, img]
        if((positions.get(nbAliens-1)[0] in positions.values())):
            fenetre.blit(img, positions.get(nbAliens-1)[0])


def gererClavierEtSouris():
    global loop, positionVaisseau, count, projectiles, timeout
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

    keyPressed = pygame.key.get_pressed()
    if keyPressed[pygame.K_SPACE] == True:
        if(timeout % 15 == 0 or timeout == 0):
            projectiles[count] = (positionVaisseau[0] +
                                  32, positionVaisseau[1])
            count += 1
        if(timeout > 9999):
            timeout = 0
        timeout += 1
    if keyPressed[pygame.K_RIGHT] or keyPressed[pygame.K_d] == True:
        positionVaisseau = (positionVaisseau[0] + 5, positionVaisseau[1])
    if keyPressed[pygame.K_LEFT] or keyPressed[pygame.K_a] == True:
        positionVaisseau = (positionVaisseau[0] - 5, positionVaisseau[1])


def moveAliens():
    global droite, nbr, w, timeout, enemyProjectiles
    for i in positions.keys():
        if(positions[i][1] != 0):
            if (positions[i][0][0] <= 5):
                positions[i][0] = (5, positions[i][0][1])
                droite = True
            elif(positions[i][0][0] >= w-20):
                positions[i][0] = (580, positions[i][0][1])
                droite = False
            if droite:
                positions[i][0] = (positions[i][0][0] +
                                   nbr, positions[i][0][1])
            else:
                positions[i][0] = (positions[i][0][0] -
                                   nbr, positions[i][0][1])


def cleanProjectiles(my_list, isEnemy=True):
    global enemyProjectiles
    for i in range(len(my_list)):
        if(isEnemy):
            enemyProjectiles.pop(my_list[i])
        else:
            projectiles.pop(my_list[i])


def addAmmo(x):
    global positions, enemyProjectiles, interval, queue
    print(queue)
    for i in positions.keys():
        if(queue.unique(i)):
            enemyProjectiles[i] = [
                (positions[i][0][0] + 16, positions[i][0][1] + 33), enemyTimeout]
            queue.append(i)


def alienShoot():
    global enemyTimeout, enemyProjectiles, interval
    toClean = list()
    if(enemyTimeout % 150 == 0 or enemyTimeout == 0):
        addAmmo(interval)
        interval += 1
    if(len(enemyProjectiles) > 0):
        for i in enemyProjectiles.keys():
            if i < len(queue):
                break
            index = queue[i]
            enemyProjectiles[index][0] = (
                enemyProjectiles[index][0][0], enemyProjectiles[index][0][1] + 5)
        # if(emptyProjectiles.everwyup(600) or enemyProjectiles[enemyProjectiles.last()][0][1] < 0):
            if(enemyProjectiles[index][0][1] > 600 or enemyProjectiles[index][0][1] < 0):
                toClean.append(index)
        cleanProjectiles(toClean, True)
    if(enemyTimeout > 9999):
        enemyTimeout = 0
    enemyTimeout += 1


def checkShipPos():
    global positionVaisseau, w, h
    if(positionVaisseau[0] <= 0):
        positionVaisseau = (580, positionVaisseau[1])
    elif (positionVaisseau[0] >= 580):
        positionVaisseau = (0, positionVaisseau[1])


def shoot():  # POW
    global count, projectiles, timeout
    cleanList = list()
    if(bool(projectiles)):
        for i in projectiles.keys():
            projectiles[i] = (projectiles[i][0], projectiles[i][1] - 5)
            if(projectiles[i][1] > 600 or projectiles[i][1] < 0):
                cleanList.append(i)
        cleanProjectiles(cleanList, False)


def gameover():
    global loop
    # if(health <= 0):# display gameover
    #     loop = False
    return True


def main():  # MAIN LOOP
    global count, projectiles, timeout
    addAlien(1)  # SPAWN ALIENS
    while(loop):
        clock.tick(100)
        draw()
        moveAliens()
        alienShoot()
        gererClavierEtSouris()
        checkShipPos()
        shoot()
        isHit()
        playerHit()
        gameover()  # GAMEOVER?


if __name__ == "__main__":  # GIBBERISH ?
    main()

pygame.quit()  # VOID?
