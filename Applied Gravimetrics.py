import math as m
import random as r
import time

import pygame as p
import pygame.display
from Planet import Planet

planets = []
planetImages=0
gravity = 66.7
scale = 1
visualScale=0.75
paused = False
mode = 0
open = 0
def addPlanet(X, Y, M, DX=0.0, DY=0.0):
    planets.append(Planet(X, Y, M, DX, DY))

def recordPlanets():
    for i in planets:
        print(i)

def passTime(time):
    (xAccels, yAccels) = getAccelerations()
    for i in range(len(planets)):
        planets[i].passTime(time, xAccels[i], yAccels[i])
        planets[i].x = planets[i].x % (600/scale)
        planets[i].y = planets[i].y % (600/scale)
    cleanValues()

def getAccelerations():
    planetD2Xs = [0 for _ in planets]
    planetD2Ys = [0 for _ in planets]
    for i in range(len(planets)):
        for j in range(len(planets)):
            if j != i and j<len(planets) and i<len(planets):
                deltaY = planets[j].y-planets[i].y
                deltaX = planets[j].x-planets[i].x
                theta = m.atan2(deltaY,deltaX)
                radius = m.dist([planets[j].x, planets[j].y], [planets[i].x,planets[i].y])
                if radius<2:
                    mergePlanets(i, j)
                else:
                    magnitude = planets[j].m*gravity/(radius**2)
                    planetD2Xs[i]+=magnitude*m.cos(theta)
                    planetD2Ys[i]+=magnitude*m.sin(theta)
    return planetD2Xs,planetD2Ys

def cleanValues(fidelity = 3):
    global planets
    for i in planets:
        i.x = round(i.x,fidelity)
        i.y = round(i.y,fidelity)
        i.dx = round(i.dx,fidelity)
        i.dy = round(i.dy,fidelity)

def mergePlanets(i, j):
    c = min(i, j)
    d = max(i, j)
    if planets[c].m==0:
        removePlanet(c)
    elif planets[d].m==0:
        removePlanet(d)
    elif not planets[c].m+planets[d].m==0:
        planets[c].dx=(planets[c].dx*planets[c].m+planets[d].dx*planets[d].m)/(planets[c].m*planets[d].m)
        planets[c].dy=(planets[c].dy*planets[c].m+planets[d].dy*planets[d].m)/(planets[c].m*planets[d].m)
        planets[c].m=planets[c].m+planets[d].m
        removePlanet(d)
    else:
        removePlanet(c)
        removePlanet(d-1)

    # print(len(planetYs))
    cleanValues()

def removePlanet(idx):
    planets.pop(idx)

def simulateClick():
    global paused, open, mode
    pos = pygame.mouse.get_pos()
    if bounded(pos, (568, 0), (600, 32)):
        paused = not paused
    elif bounded(pos, (8, 568), (72, 600)):
        open=0
        mode=0
    elif bounded(pos, (80, 568), (144, 600)):
        open=1
        mode=1
    elif bounded(pos, (152, 568), (216, 600)):
        open=2
        mode=2
    elif bounded(pos, (224, 568), (288, 600)):
        open=3
        mode=3
    else:
        if mode == 0:
            addPlanet(pos[0]/scale, pos[1]/scale, 40, 0, 0)
        if mode == 1:
            addPlanet(pos[0]/scale, pos[1]/scale, -40, 0, 0)
        elif mode == 2:
            checkDelete(pos)

def checkDelete(position):
    for i in range(len(planets)):
        if abs(position[0] - (planets[i].x / scale))<8 and abs(position[1] - (planets[i].y / scale))<8:
            removePlanet(i)
            return

def bounded(pos, min, max):
    return (min[0]<=pos[0]<=max[0]) and (min[1]<=pos[1]<=max[1])

def mainLoop():
    global scale, paused
    pygame.init()
    canvas = pygame.display.set_mode([600,600])
    quit=False
    loadAssets()
    while not quit:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit=True
            if event.type==1025:
                simulateClick()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
        if not paused:
            passTime(0.01)
        renderPlanets(canvas, scale)
        time.sleep(0.001)

def loadAssets():
    global planetImages, UI_elements
    planetImages= [pygame.transform.scale_by(pygame.image.load("assets/white_hole.png"), visualScale),
                   pygame.transform.scale_by(pygame.image.load("assets/star_purple.png"), 2*visualScale),
                   pygame.transform.scale_by(pygame.image.load("assets/star_teal.png"), 1.5*visualScale),
                   pygame.transform.scale_by(pygame.image.load("assets/star_green.png"), visualScale),
                   pygame.transform.scale_by(pygame.image.load("assets/moon.png"), 0.5*visualScale),
                   pygame.transform.scale_by(pygame.image.load("assets/planet_cracked.png"), 0.5*visualScale),
                   pygame.transform.scale_by(pygame.image.load("assets/planet_mars.png"), 0.5*visualScale),
                   pygame.transform.scale_by(pygame.image.load("assets/planet_algae.png"), 0.75*visualScale),
                   pygame.transform.scale_by(pygame.image.load("assets/planet_jool.png"), 0.8*visualScale),
                   pygame.transform.scale_by(pygame.image.load("assets/star.png"), 1.5*visualScale),
                   pygame.transform.scale_by(pygame.image.load("assets/star_red.png"), 1.75*visualScale),
                   pygame.transform.scale_by(pygame.image.load("assets/star_blue.png"), 2*visualScale),
                   pygame.transform.scale_by(pygame.image.load("assets/black_hole.png"), visualScale)]
    UI_elements = [
        pygame.image.load("assets/button_play.png"),
        pygame.image.load("assets/button_pause.png"),
        pygame.transform.scale_by(pygame.image.load("assets/button_create.png"), 2),
        pygame.transform.scale_by(pygame.image.load("assets/button_edit.png"), 2),
        pygame.transform.scale_by(pygame.image.load("assets/button_destroy.png"), 2),
        pygame.transform.scale_by(pygame.image.load("assets/button_settings.png"), 2)
    ]
    pygame.display.set_caption("Gravimetrics V0.1")
    pygame.display.set_icon(planetImages[12])

def renderPlanets(canvas, scale=1):
    canvas.fill((0,0,0))
    for i in range(len(planets)):
        if planets[i].m<-1000: # White hole
            canvas.blit(planetImages[0], (planets[i].x * scale - 17 * visualScale, planets[i].y * scale - 17 * visualScale))
        elif planets[i].m<-200: # Purple star
            canvas.blit(planetImages[1], (planets[i].x * scale - 18 * 2 * visualScale, planets[i].y * scale - 18 * 2 * visualScale))
        elif planets[i].m<-80: # Teal star
            canvas.blit(planetImages[2], (planets[i].x * scale - 18 * 1.5 * visualScale, planets[i].y * scale - 18 * 1.5 * visualScale))
        elif planets[i].m<0: # Green star
            canvas.blit(planetImages[3], (planets[i].x * scale - 18 * visualScale, planets[i].y * scale - 18 * visualScale))
        elif planets[i].m<=1: # moon
            canvas.blit(planetImages[4], (planets[i].x * scale - 17 / 2 * visualScale, planets[i].y * scale - 17 / 2 * visualScale))
        elif planets[i].m<3: # cracked
            canvas.blit(planetImages[5], (planets[i].x * scale - 16 / 2 * visualScale, planets[i].y * scale - 16 / 2 * visualScale))
        elif planets[i].m<7: # mars
            canvas.blit(planetImages[6], (planets[i].x * scale - 16 / 2 * visualScale, planets[i].y * scale - 16 / 2 * visualScale))
        elif planets[i].m<12: #algae
            canvas.blit(planetImages[7], (planets[i].x * scale - 16 * 3 / 4 * visualScale, planets[i].y * scale - 16 * 3 / 4 * visualScale))
        elif planets[i].m<250: # gas
            canvas.blit(planetImages[8], (planets[i].x * scale - 16 * 4 / 5 * visualScale, planets[i].y * scale - 16 * 4 / 5 * visualScale))
        elif planets[i].m<500: # hereComesTheSun
            canvas.blit(planetImages[9], (planets[i].x * scale - 18 * 1.5 * visualScale, planets[i].y * scale - 18 * 1.5 * visualScale))
        elif planets[i].m<1000: # red
            canvas.blit(planetImages[10], (planets[i].x * scale - 18 * 1.75 * visualScale, planets[i].y * scale - 18 * 1.75 * visualScale))
        elif planets[i].m<2500: # blue
            canvas.blit(planetImages[11], (planets[i].x * scale - 18 * 2 * visualScale, planets[i].y * scale - 18 * 2 * visualScale))
        else: # black hole
            canvas.blit(planetImages[12], (planets[i].x * scale - 17, planets[i].y * scale - 17))
    renderUI(canvas)
    pygame.display.update()

def renderUI(canvas):
    if not paused:
        canvas.blit(UI_elements[1], (568, 4))
    else:
        canvas.blit(UI_elements[0], (568, 4))
    canvas.blit(UI_elements[2], (8, 568))
    canvas.blit(UI_elements[3], (80, 568))
    canvas.blit(UI_elements[4], (152, 568))
    canvas.blit(UI_elements[5], (224, 568))

mainLoop()