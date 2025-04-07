import math as m
import random as r
import time

import pygame as p
import pygame.display

planetXs = []
planetYs = []
planetMs = []
planetDXs = []
planetDYs = []
planetD2Xs = []
planetD2Ys = []
planetImages=0
gravity = 66.7
scale = 1
visualScale=0.75
paused = False
def addPlanet(X, Y, M, DX=0.0, DY=0.0):
    planetXs.append(X)
    planetYs.append(Y)
    planetMs.append(M)
    planetDXs.append(DX)
    planetDYs.append(DY)

def recordPlanets():
    for i in range(len(planetXs)):
        print("Planet: [X="+str(planetXs[i])+", Y="+str(planetYs[i])+", M="+str(planetMs[i])+", DX="+str(planetDXs[i])+", DY="+str(planetDYs[i])+"]")

def passTime(time):
    getAccelerations()
    for i in range(len(planetXs)):
        planetDXs[i] += planetD2Xs[i]*time
        planetDYs[i] += planetD2Ys[i]*time
        pass
    for i in range(len(planetXs)):
        planetXs[i] += planetDXs[i]*time
        planetYs[i] += planetDYs[i]*time
        planetXs[i]=planetXs[i] % (600/scale)
        planetYs[i]=planetYs[i] % (600/scale)
    cleanValues()

def getAccelerations():
    global planetD2Xs, planetD2Ys
    planetD2Xs = [0 for _ in planetXs]
    planetD2Ys = [0 for _ in planetYs]
    for i in range(len(planetXs)):
        for j in range(len(planetXs)):
            if j != i and j<len(planetXs) and i<len(planetXs):
                deltaY = planetYs[j]-planetYs[i]
                deltaX = planetXs[j]-planetXs[i]
                theta = m.atan2(deltaY,deltaX)
                radius = m.dist([planetXs[j], planetYs[j]], [planetXs[i],planetYs[i]])
                if radius<2:
                    mergePlanets(i, j)
                else:
                    magnitude = planetMs[j]*gravity/(radius**2)
                    planetD2Xs[i]+=magnitude*m.cos(theta)
                    planetD2Ys[i]+=magnitude*m.sin(theta)

def cleanValues(fidelity = 3):
    global planetXs,planetYs,planetDXs,planetDYs
    planetXs=[round(x,fidelity) for x in planetXs]
    planetYs=[round(x,fidelity) for x in planetYs]
    planetDXs=[round(x,fidelity) for x in planetDXs]
    planetDYs=[round(x,fidelity) for x in planetDYs]

def mergePlanets(i, j):
    c = min(i, j)
    d = max(i, j)
    if planetMs[c]==0:
        removePlanet(c)
        return
    if planetMs[d]==0:
        removePlanet(d)
        return
    if not planetMs[c]+planetMs[d]==0:
        planetDXs[c]=(planetDXs[c]*planetMs[c]+planetDXs[d]*planetMs[d])/(planetMs[c]*planetMs[d])
        planetDYs[c]=(planetDYs[c]*planetMs[c]+planetDYs[d]*planetMs[d])/(planetMs[c]*planetMs[d])
        planetMs[c]=planetMs[c]+planetMs[d]
        removePlanet(d)
    else:
        removePlanet(c)
        removePlanet(d-1)

    # print(len(planetYs))
    cleanValues()

def removePlanet(idx):
    planetXs.pop(idx)
    planetYs.pop(idx)
    planetDXs.pop(idx)
    planetDYs.pop(idx)
    planetMs.pop(idx)

def placePlanets(c):
    pos=pygame.mouse.get_pos()
    if c==0:
        addPlanet(pos[0]/scale, pos[1]/scale, 80)
    if c==1:
        addPlanet(pos[0]/scale, pos[1]/scale, -40)

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
                if pygame.mouse.get_pressed(3)[0]:
                    placePlanets(0)
                if pygame.mouse.get_pressed(3)[2]:
                    placePlanets(1)
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
        pygame.image.load("assets/button_create.png"),
        pygame.image.load("assets/button_edit.png"),
        pygame.image.load("assets/button_destroy.png"),
        pygame.image.load("assets/button_settings.png")
    ]
    pygame.display.set_caption("Gravimetrics V0.1")
    pygame.display.set_icon(planetImages[12])

def renderPlanets(canvas, scale=1):
    canvas.fill((0,0,0))
    for i in range(len(planetXs)):
        if planetMs[i]<-1000: # White hole
            canvas.blit(planetImages[0], (planetXs[i] * scale - 17 * visualScale, planetYs[i] * scale - 17 * visualScale))
        elif planetMs[i]<-200: # Purple star
            canvas.blit(planetImages[1], (planetXs[i] * scale - 18 * 2 * visualScale, planetYs[i] * scale - 18 * 2 * visualScale))
        elif planetMs[i]<-80: # Teal star
            canvas.blit(planetImages[2], (planetXs[i] * scale - 18 * 1.5 * visualScale, planetYs[i] * scale - 18 * 1.5 * visualScale))
        elif planetMs[i]<0: # Green star
            canvas.blit(planetImages[3], (planetXs[i] * scale - 18 * visualScale, planetYs[i] * scale - 18 * visualScale))
        elif planetMs[i]<=1: # moon
            canvas.blit(planetImages[4], (planetXs[i] * scale - 17 / 2 * visualScale, planetYs[i] * scale - 17 / 2 * visualScale))
        elif planetMs[i]<3: # cracked
            canvas.blit(planetImages[5], (planetXs[i] * scale - 16 / 2 * visualScale, planetYs[i] * scale - 16 / 2 * visualScale))
        elif planetMs[i]<7: # mars
            canvas.blit(planetImages[6], (planetXs[i] * scale - 16 / 2 * visualScale, planetYs[i] * scale - 16 / 2 * visualScale))
        elif planetMs[i]<12: #algae
            canvas.blit(planetImages[7], (planetXs[i] * scale - 16 * 3 / 4 * visualScale, planetYs[i] * scale - 16 * 3 / 4 * visualScale))
        elif planetMs[i]<250: # gas
            canvas.blit(planetImages[8], (planetXs[i] * scale - 16 * 4 / 5 * visualScale, planetYs[i] * scale - 16 * 4 / 5 * visualScale))
        elif planetMs[i]<500: # hereComesTheSun
            canvas.blit(planetImages[9], (planetXs[i] * scale - 18 * 1.5 * visualScale, planetYs[i] * scale - 18 * 1.5 * visualScale))
        elif planetMs[i]<1000: # red
            canvas.blit(planetImages[10], (planetXs[i] * scale - 18 * 1.75 * visualScale, planetYs[i] * scale - 18 * 1.75 * visualScale))
        elif planetMs[i]<2500: # blue
            canvas.blit(planetImages[11], (planetXs[i] * scale - 18 * 2 * visualScale, planetYs[i] * scale - 18 * 2 * visualScale))
        else: # black hole
            canvas.blit(planetImages[12], (planetXs[i] * scale - 17, planetYs[i] * scale - 17))
    renderUI(canvas)
    pygame.display.update()

def renderUI(canvas):
    if not paused:
        canvas.blit(UI_elements[1], (568, 4))
    else:
        canvas.blit(UI_elements[0], (568, 4))

# for i in range(0, 32):
    # addPlanet(30+m.cos(i*m.pi/16)*5, 30+m.sin(i*m.pi/16)*5, 1, m.cos(i*m.pi/16+m.pi/4)*2,m.sin(i*m.pi/16+m.pi/4)*2)
    # addPlanet(300+m.cos(i*m.pi/16)*150, 300+m.sin(i*m.pi/16)*150, 10, m.cos(i*m.pi/16-m.pi/4)*59000,m.sin(i*m.pi/16-m.pi/4)*59000)
# for i in range(6):
#     theta = m.pi*i/3
#     addPlanet(30+10*m.cos(theta), 30+10*m.sin(theta), 1, 3 * m.cos(theta+m.pi/3), 3 * m.sin(theta+m.pi/3))
addPlanet(30, 27, 1, 6, 0)
addPlanet(30, 20, 1, 3, 0)
# addPlanet(30, 30, 100)
# addPlanet(30, 40, 1, -6, 0)
for i in range(20):
    addPlanet(r.randint(0, int(600/scale)), r.randint(0, int(600/scale)), 10)
mainLoop()