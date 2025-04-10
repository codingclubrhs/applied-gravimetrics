import math
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
font = ''
mStep = 1
vStep = 1
edit_target = -1
template_planet = [10, 0, 0, False, False]

# Simulation and control
def addPlanet(X, Y, M, DX=0.0, DY=0.0, locked=False, vlock=False):
    planets.append(Planet(X, Y, M, DX, DY, locked, vlock))
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
def mergePlanets(i, j):
    c = min(i, j)
    d = max(i, j)
    if planets[c].locked or planets[d].locked:
        planets[c].locked=True
    elif planets[c].vlock or planets[d].vlock:
        planets[c].vlock = True
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
    global edit_target
    planets.pop(idx)
    if edit_target==idx:
        edit_target=-1
    elif edit_target>idx:
        edit_target-=1

# Mouse input
def simulateClick():
    global paused, open, mode
    pos = pygame.mouse.get_pos()
    buttonX = 600 if open == 0 else 500
    if bounded(pos, (568, 568), (600, 600)):
        paused = not paused
    elif bounded(pos, (buttonX-32, 8), (buttonX, 72)):
        open=1 if not open==1 else 0
        mode=1
    elif bounded(pos, (buttonX-32, 80), (buttonX, 144)):
        open=2 if not open==2 else 0
        mode=2
    elif bounded(pos, (buttonX-32, 152), (buttonX, 216)):
        open=3 if not open==3 else 0
        mode=3
    elif bounded(pos, (buttonX-32, 224), (buttonX, 288)):
        # open=4 if not open==4 else 0
        mode=4
    elif bounded(pos, (500, 0), (600, 600)) and not open == 0:
        UI_click()
    else:
        if mode == 1:
            addPlanet(pos[0]/scale, pos[1]/scale, template_planet[0], template_planet[1], template_planet[2], template_planet[3], template_planet[4])
        elif mode == 2:
            selectPlanet(pos)
        elif mode == 3:
            checkDelete(pos)
        elif mode == 4:
            toggleLocked(pos)
def UI_click():
    global open, mode, mStep, vStep
    pos = pygame.mouse.get_pos()
    if open==1:
        if bounded(pos, (520, 65), (568, 113)):
            q = getQuadrant((520, 65), (568, 113), pos)
            if q == 1:
                template_planet[0]+=mStep
                if template_planet[0] > 10000:
                    template_planet[0] = 10000
            if q == 3:
                template_planet[0]-=mStep
                if template_planet[0] < -10000:
                    template_planet[0]=-10000
            if q == 0 and mStep < 1024:
                mStep *= 2
            if q == 2 and mStep > 1/1024:
                mStep /=2
        if bounded(pos, (520, 170), (568, 218)):
            q = getQuadrant((520, 170), (568, 218), pos)
            if q == 1:
                template_planet[1]+=vStep
            if q == 3:
                template_planet[1]-=vStep
            if q == 0:
                template_planet[2]-=vStep
            if q == 2:
                template_planet[2]+=vStep
        if bounded(pos, (500, 170), (526, 218)) and vStep>1/128:
            vStep/=2
        if bounded(pos, (574, 170), (600, 218)) and vStep<128:
            vStep*=2
    if open==2:
        if bounded(pos, (526, 65), (574, 113)):
            q = getQuadrant((526, 65), (574, 113), pos)
            if q == 1:
                planets[edit_target].m+=mStep
                if planets[edit_target].m > 10000:
                    planets[edit_target].m = 10000
            if q == 3:
                planets[edit_target].m-=mStep
                if planets[edit_target].m < -10000:
                    planets[edit_target].m=-10000
            if q == 0 and mStep < 1024:
                mStep *= 2
            if q == 2 and mStep > 1/1024:
                mStep /=2
        if bounded(pos, (526, 170), (574, 218)):
            q = getQuadrant((526, 170), (574, 218), pos)
            if q == 1:
                planets[edit_target].dx+=vStep
            if q == 3:
                planets[edit_target].dx-=vStep
            if q == 0:
                planets[edit_target].dy-=vStep
            if q == 2:
                planets[edit_target].dy+=vStep
        if bounded(pos, (500, 170), (526, 218)) and vStep>1/128:
            vStep/=2
        if bounded(pos, (574, 170), (600, 218)) and vStep<128:
            vStep*=2

# Control
def checkDelete(position):
    for i in range(len(planets)):
        if abs(position[0] - (planets[i].x / scale))<8 and abs(position[1] - (planets[i].y / scale))<8:
            removePlanet(i)
            return
def toggleLocked(position):
    for i in range(len(planets)):
        if abs(position[0] - (planets[i].x / scale))<8 and abs(position[1] - (planets[i].y / scale))<8:
            planets[i].locked = not planets[i].locked
            print(planets[i].locked)
            return
def selectPlanet(position):
    global edit_target
    for i in range(len(planets)):
        if abs(position[0] - (planets[i].x / scale))<8 and abs(position[1] - (planets[i].y / scale))<8:
            edit_target = i

# Helper methods
def bounded(pos, min, max):
    return (min[0]<=pos[0]<=max[0]) and (min[1]<=pos[1]<=max[1])
def getQuadrant(topRight, bottomLeft, pos):
    # 0 -> top, 1-> right, 2 -> bottom, 3 -> left
    relativePos = (pos[0]-topRight[0], pos[1]-topRight[1])
    half0 = relativePos[1] >= relativePos[0]
    half1 = relativePos[1] >= bottomLeft[0]-topRight[0]-relativePos[0]
    return (2 if half1 else 3) if half0 else (1 if half1 else 0)
def cleanValues(fidelity = 3):
    global planets
    for i in planets:
        i.x = round(i.x,fidelity)
        i.y = round(i.y,fidelity)
        i.dx = round(i.dx,fidelity)
        i.dy = round(i.dy,fidelity)

# UI and rendering
def loadAssets():
    global planetImages, UI_elements, text_elements, font
    pygame.font.init()
    font = pygame.font.SysFont("courier_new", 12)
    title_font = pygame.font.SysFont("courier_new", 16, True)
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
        pygame.image.load("assets/UI/button_play.png"), #0
        pygame.image.load("assets/UI/button_pause.png"),
        pygame.transform.scale_by(pygame.image.load("assets/UI/button_create.png"), 2),
        pygame.transform.scale_by(pygame.image.load("assets/UI/button_edit.png"), 2),
        pygame.transform.scale_by(pygame.image.load("assets/UI/button_destroy.png"), 2),
        pygame.transform.scale_by(pygame.image.load("assets/UI/button_settings.png"), 2), #5
        pygame.transform.scale_by(pygame.image.load("assets/UI/UI_bar_create.png"), 5),
        pygame.transform.scale_by(pygame.image.load("assets/UI/UI_bar_edit.png"), 5),
        pygame.transform.scale_by(pygame.image.load("assets/UI/UI_bar_destroy.png"), 5),
        pygame.transform.scale_by(pygame.image.load("assets/UI/UI_bar_settings.png"), 5),
        pygame.transform.scale_by(pygame.image.load("assets/UI/mass_control.png"), 1.5), #10
        pygame.transform.scale_by(pygame.image.load("assets/UI/velocity_control.png"), 1.5)
    ]
    text_elements = [
        title_font.render("Create", False, (0, 0, 0)), # 0
        title_font.render("Edit", False, (0, 0, 0)),
        title_font.render("Destroy", False, (0, 0, 0)),
        title_font.render("Settings", False, (0, 0, 0)),
        pygame.transform.rotate(font.render("Click on planets to destroy them", False, (0, 0, 0)), 90),
        pygame.transform.rotate(font.render("This really shouldn't be hard", False, (0, 0, 0)), 90), # 5
        pygame.transform.rotate(font.render("IDK why you need instructions", False, (0, 0, 0)), 90),
        font.render("Set mass", False, (0,0,0)),
        font.render("-", False, (0,0,0)),
        font.render("Set velocity", False, (0,0,0)),
        font.render("_", False, (0,0,0)), # 10
        font.render("Edit mass", False, (0, 0, 0)),
        font.render("Edit velocity", False, (0, 0, 0)),
        font.render("Lock position", False, (0, 0, 0)),
        font.render("Lock velocity", False, (0, 0, 0)),
        font.render("Click on", False, (0,0,0)), # 15
        font.render("a planet", False, (0,0,0)),
        font.render("to edit", False, (0,0,0))
    ]
    pygame.display.set_caption("Gravimetrics V0.2")
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
    global font
    if not paused:
        canvas.blit(UI_elements[1], (568, 568))
    else:
        canvas.blit(UI_elements[0], (568, 568))
    if open==0:
        canvas.blit(UI_elements[2], (568, 8))
        canvas.blit(UI_elements[3], (568, 80))
        canvas.blit(UI_elements[4], (568, 152))
        # canvas.blit(UI_elements[5], (568, 224))
    else:
        canvas.blit(UI_elements[2], (468, 8))
        canvas.blit(UI_elements[3], (468, 80))
        canvas.blit(UI_elements[4], (468, 152))
        # canvas.blit(UI_elements[5], (468, 224))
        if open==1:
            canvas.blit(UI_elements[6], (500, 0))
            canvas.blit(text_elements[0], (520, 5))
            # Mass control
            canvas.blit(text_elements[7], (520, 45))
            canvas.blit(UI_elements[10], (526, 65))
            text_elements[8]=font.render("Mass: " + str(template_planet[0]), False, (0,0,0))
            canvas.blit(text_elements[8], (510, 120))
            text_elements[8]=font.render("Step: " + str(mStep), False, (0, 0, 0))
            canvas.blit(text_elements[8], (510, 130))
            # Velocity control
            canvas.blit(text_elements[9], (505, 150))
            canvas.blit(UI_elements[11], (526, 170))
            text_elements[10] = font.render("("+str(template_planet[1])+", " + str(template_planet[2]) + ")", False, (0, 0, 0))
            canvas.blit(text_elements[10], (505, 225))
            text_elements[10] = font.render("Step: " + str(vStep), False, (0, 0, 0))
            canvas.blit(text_elements[10], (510, 235))
        if open==2:
            canvas.blit(UI_elements[7], (500, 0))
            canvas.blit(text_elements[1], (525, 5))
            if not edit_target == -1:
                # Mass control
                canvas.blit(text_elements[11], (510, 45))
                canvas.blit(UI_elements[10], (526, 65))
                text_elements[8] = font.render("Mass: " + str(planets[edit_target].m), False, (0, 0, 0))
                canvas.blit(text_elements[8], (510, 120))
                text_elements[8]=font.render("Step: " + str(mStep), False, (0, 0, 0))
                canvas.blit(text_elements[8], (510, 130))
                # Velocity control
                canvas.blit(text_elements[12], (504, 150))
                canvas.blit(UI_elements[11], (526, 170))
                text_elements[10] = font.render("(" + str(round(planets[edit_target].dx, 1)) + ", " + str(round(planets[edit_target].dy, 1)) + ")", False,(0, 0, 0))
                canvas.blit(text_elements[10], (505, 225))
                text_elements[10]=font.render("Step: " + str(vStep), False, (0, 0, 0))
                canvas.blit(text_elements[10], (510, 235))
            else:
                canvas.blit(text_elements[15], (510, 30))
                canvas.blit(text_elements[16], (510, 50))
                canvas.blit(text_elements[17], (510, 70))
        if open==3:
            canvas.blit(UI_elements[8], (500, 0))
            canvas.blit(text_elements[4], (510, 10))
            canvas.blit(text_elements[5], (540, 10))
            canvas.blit(text_elements[6], (570, 10))
        if open==4:
            canvas.blit(UI_elements[9], (500, 0))
            canvas.blit(text_elements[3], (510, 10))

def mainLoop():
    global scale, paused
    pygame.init()
    canvas = pygame.display.set_mode([600,600])
    quit=False
    runTime=0
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
                if event.key == pygame.K_1:
                    for p in planets:
                        p.locked=False
                if event.key == pygame.K_2:
                    for p in planets:
                        p.locked=True
                if event.key == pygame.K_3:
                    for p in planets:
                        p.vlock=False
                if event.key == pygame.K_4:
                    for p in planets:
                        p.vlock=True
        if not paused:
            passTime(0.01)
        runTime+=1
        if runTime>100000:
            exit(682)
        renderPlanets(canvas, scale)
        time.sleep(0.001)


for i in range(32):
    addPlanet(300+100*m.cos(2*m.pi/32*i), 300+100*m.sin(2*m.pi/32*i), 100, 30*m.cos(2*m.pi/32*i), 30*m.sin(2*m.pi/32*i))
    addPlanet(300+150*m.cos(2*m.pi/32*i), 300+150*m.sin(2*m.pi/32*i), 100, 30*m.cos(2*m.pi/32*i+m.pi/3), 30*m.sin(2*m.pi/32*i+m.pi/3))
mainLoop()