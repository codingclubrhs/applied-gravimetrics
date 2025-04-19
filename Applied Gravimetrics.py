import math
import math as m
import random as r
import time

import pygame
import pygame.display
from Planet import Planet
# Data
planets = []
# Settings
gravity = 66.7
scale = 1
visualScale=0.7
paused = False
timeScale = 1
frameRate=120
# UI rendering
mode = 0
open_screen = 0
font = ''
# UI settings
edit_target = -1
template_planet = [10, 0, 0, False, False]
wrap_method = 0
mStep = 1
vStep = 1
# Assets
UI_elements=[]
text_elements=[]
planetImages=[]


# Simulation and control
def addPlanet(X, Y, M, DX=0.0, DY=0.0, locked=False, vlock=False):
    planets.append(Planet(X, Y, M, DX, DY, locked, vlock))
def recordPlanets():
    for j in planets:
        print(j)
def passTime(t):
    (x_accels, y_accels) = getAccelerations()
    for i in range(len(planets)):
        if i<len(planets):
            planets[i].passTime(t, x_accels[i], y_accels[i])
            if wrap_method==0:
                planets[i].x = planets[i].x % (600/scale)
                planets[i].y = planets[i].y % (600/scale)
            elif wrap_method==1 and not bounded((planets[i].x, planets[i].y), (0,0), (600, 600)):
                removePlanet(i)
                i-=1
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
    global paused, open_screen, mode
    pos = pygame.mouse.get_pos()
    buttonX = 600 if open_screen == 0 else 500
    if bounded(pos, (568, 568), (600, 600)):
        paused = not paused
    elif bounded(pos, (buttonX-32, 8), (buttonX, 72)):
        open_screen=1 if not open_screen == 1 else 0
        mode=1
    elif bounded(pos, (buttonX-32, 80), (buttonX, 144)):
        open_screen=2 if not open_screen == 2 else 0
        mode=2
    elif bounded(pos, (buttonX-32, 152), (buttonX, 216)):
        open_screen=3 if not open_screen == 3 else 0
        mode=3
    elif bounded(pos, (buttonX-32, 224), (buttonX, 288)):
        open_screen=4 if not open_screen==4 else 0
        mode=4
    elif bounded(pos, (500, 0), (600, 600)) and not open_screen == 0:
        UI_click()
    else:
        if mode == 1:
            addPlanet(pos[0]/scale, pos[1]/scale, template_planet[0], template_planet[1], template_planet[2], template_planet[3], template_planet[4])
        elif mode == 2:
            selectPlanet(pos)
        elif mode == 3:
            checkDelete(pos)
def UI_click():
    global open_screen, mode, mStep, vStep, wrap_method, timeScale, scale
    pos = pygame.mouse.get_pos()
    if open_screen==1:
        if bounded(pos, (520, 65), (568, 113)):
            quad = getQuadrant((520, 65), (568, 113), pos)
            if quad == 1:
                template_planet[0]+=mStep
                if template_planet[0] > 10000:
                    template_planet[0] = 10000
            if quad == 3:
                template_planet[0]-=mStep
                if template_planet[0] < -10000:
                    template_planet[0]=-10000
            if quad == 0 and mStep < 1024:
                mStep *= 2
            if quad == 2 and mStep > 1/1024:
                mStep /=2
        if bounded(pos, (520, 170), (568, 218)):
            quad = getQuadrant((520, 170), (568, 218), pos)
            if quad == 1:
                template_planet[1]+=vStep
            if quad == 3:
                template_planet[1]-=vStep
            if quad == 0:
                template_planet[2]-=vStep
            if quad == 2:
                template_planet[2]+=vStep
        if bounded(pos, (500, 170), (526, 218)) and vStep>1/128:
            vStep/=2
        if bounded(pos, (574, 170), (600, 218)) and vStep<128:
            vStep*=2
        if bounded(pos, (570, 257), (586, 273)):
            template_planet[3] = not template_planet[3]
        if bounded(pos, (570, 277), (586, 293)):
            template_planet[4] = not template_planet[4]
    if open_screen==2:
        if bounded(pos, (526, 65), (574, 113)):
            quad = getQuadrant((526, 65), (574, 113), pos)
            if quad == 1:
                planets[edit_target].m+=mStep
                if planets[edit_target].m > 10000:
                    planets[edit_target].m = 10000
            if quad == 3:
                planets[edit_target].m-=mStep
                if planets[edit_target].m < -10000:
                    planets[edit_target].m=-10000
            if quad == 0 and mStep < 1024:
                mStep *= 2
            if quad == 2 and mStep > 1/1024:
                mStep /=2
        if bounded(pos, (526, 170), (574, 218)):
            quad = getQuadrant((526, 170), (574, 218), pos)
            if quad == 1:
                planets[edit_target].dx+=vStep
            if quad == 3:
                planets[edit_target].dx-=vStep
            if quad == 0:
                planets[edit_target].dy-=vStep
            if quad == 2:
                planets[edit_target].dy+=vStep
        if bounded(pos, (500, 170), (526, 218)) and vStep>1/128:
            vStep/=2
        if bounded(pos, (574, 170), (600, 218)) and vStep<128:
            vStep*=2
        if bounded(pos, (570, 257), (586, 273)):
            planets[edit_target].locked = not planets[edit_target].locked
        if bounded(pos, (570, 277), (586, 293)):
            planets[edit_target].vlock = not planets[edit_target].vlock
    if open_screen==4:
        if bounded(pos, (500, 48), (600, 66)):
            wrap_method=(wrap_method+1)%3
        if bounded(pos, (500, 95), (550, 119)) and timeScale>0.25:
            timeScale-=0.25
        if bounded(pos, (550, 95), (600, 119)) and timeScale<10:
            timeScale+=0.25
        if bounded(pos, (500, 113), (600, 131)):
            wrap_method=(wrap_method+1)%3
        if bounded(pos, (500, 160), (550, 184)) and scale>1/64:
            scale/=2
        if bounded(pos, (550, 160), (600, 184)) and scale<64:
            scale*=2
# Control
def checkDelete(position):
    global scale
    for i in range(len(planets)):
        if abs(position[0] - (planets[i].x * scale))<20*visualScale and abs(position[1] - (planets[i].y * scale))<20*visualScale:
            removePlanet(i)
            return
def toggleLocked(position):
    global scale
    for i in range(len(planets)):
        if abs(position[0] - (planets[i].x * scale))<20*visualScale and abs(position[1] - (planets[i].y * scale))<20*visualScale:
            planets[i].locked = not planets[i].locked
            print(planets[i].locked)
            return
def selectPlanet(position):
    global edit_target, scale
    for i in range(len(planets)):
        if abs(position[0] - (planets[i].x * scale))<20*visualScale and abs(position[1] - (planets[i].y * scale))<20*visualScale:
            edit_target = i

# Helper methods
def bounded(pos, top_left, bottom_right):
    return (top_left[0] <= pos[0] <= bottom_right[0]) and (top_left[1] <= pos[1] <= bottom_right[1])
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
        pygame.transform.scale_by(pygame.image.load("assets/UI/velocity_control.png"), 1.5),
        pygame.transform.scale_by(pygame.image.load("assets/UI/checkbox.png"), 1),
        pygame.transform.scale_by(pygame.image.load("assets/UI/checkedbox.png"), 1),
        pygame.transform.scale_by(pygame.image.load("assets/UI/arrow.png"), 2),
        pygame.transform.rotate(pygame.transform.scale_by(pygame.image.load("assets/UI/arrow.png"), 2), 180) #15
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
        font.render("Lock pos", False, (0, 0, 0)),
        font.render("Lock vel", False, (0, 0, 0)),
        font.render("Click on", False, (0,0,0)), # 15
        font.render("a planet", False, (0,0,0)),
        font.render("to edit", False, (0,0,0)),
        font.render("Wrap method", False, (0,0,0)),
        font.render("Wrap", False, (0,0,0)),
        font.render("Destroy", False, (0,0,0)), #20
        font.render("Simulate", False, (0,0,0)),
        font.render("Time passage", False, (0,0,0)),
        font.render("Scale", False, (0,0,0)),
    ]
    pygame.display.set_caption("Gravimetrics V1.0")
    pygame.display.set_icon(planetImages[12])
def renderEverything(canvas):
    global scale
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
    if open_screen==0:
        canvas.blit(UI_elements[2], (568, 8))
        canvas.blit(UI_elements[3], (568, 80))
        canvas.blit(UI_elements[4], (568, 152))
        canvas.blit(UI_elements[5], (568, 224))
    else:
        canvas.blit(UI_elements[2], (468, 8))
        canvas.blit(UI_elements[3], (468, 80))
        canvas.blit(UI_elements[4], (468, 152))
        canvas.blit(UI_elements[5], (468, 224))
        if open_screen==1:
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
            canvas.blit(UI_elements[15], (507, 182))
            canvas.blit(UI_elements[14], (572, 182))
            # MV locking
            canvas.blit(text_elements[13], (510, 260))
            canvas.blit(text_elements[14], (510, 280))
            canvas.blit(UI_elements[13] if template_planet[3] else UI_elements[12], (570, 257))
            canvas.blit(UI_elements[13] if template_planet[4] else UI_elements[12], (570, 277))
        if open_screen==2:
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
                canvas.blit(UI_elements[15], (507, 182))
                canvas.blit(UI_elements[14], (572, 182))
                # MV locking
                canvas.blit(text_elements[13], (510, 260))
                canvas.blit(text_elements[14], (510, 280))
                canvas.blit(UI_elements[13] if planets[edit_target].locked else UI_elements[12], (570, 257))
                canvas.blit(UI_elements[13] if planets[edit_target].vlock else UI_elements[12], (570, 277))
            else:
                canvas.blit(text_elements[15], (510, 30))
                canvas.blit(text_elements[16], (510, 50))
                canvas.blit(text_elements[17], (510, 70))
        if open_screen==3:
            canvas.blit(UI_elements[8], (500, 0))
            canvas.blit(text_elements[4], (510, 10))
            canvas.blit(text_elements[5], (540, 10))
            canvas.blit(text_elements[6], (570, 10))
        if open_screen==4:
            canvas.blit(UI_elements[9], (500, 0))
            canvas.blit(text_elements[3], (510, 10))
            canvas.blit(text_elements[18], (510, 40))
            canvas.blit(text_elements[19+wrap_method], (525, 53))
            canvas.blit(text_elements[22], (510, 75))
            canvas.blit(UI_elements[15], (515, 95))
            canvas.blit(UI_elements[14], (559, 95))
            text_elements[10]=font.render(str(timeScale), False, (0,0,0))
            canvas.blit(text_elements[10], (545, 102))
            canvas.blit(text_elements[23], (510, 140))
            text_elements[10] = font.render(str(scale), False, (0, 0, 0))
            canvas.blit(text_elements[10], (545, 167))
            canvas.blit(UI_elements[15], (515, 160))
            canvas.blit(UI_elements[14], (559, 160))



def mainLoop():
    global scale, paused, frameRate,timeScale
    pygame.init()
    canvas = pygame.display.set_mode([600,600])
    quitting=False
    runTime=0
    loadAssets()
    while not quitting:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quitting=True
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
            passTime(1/frameRate*timeScale)
        runTime+=1
        if runTime>100000:
            exit(682)
        renderEverything(canvas)
        time.sleep(1/frameRate)
mainLoop()