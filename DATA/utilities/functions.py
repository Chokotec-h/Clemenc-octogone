from DATA.utilities.Gamepad_gestion import *
from DATA.utilities.Interface import *
import pygame

keyrepeat = [[],[]]
repeat = [[],[]]

def addkeyrepeat(key,p):
    keyrepeat[p].append(key)
    repeat[p].append(10)

def input_but_no_repeat(key,controls,joysticks,player):
    if convert_inputs(controls[player],joysticks,player)[key] and key not in keyrepeat[player]:
        addkeyrepeat(key,player)
        return True
    else :
        return False

def actualize_repeating():
    for p in range(2):
        for k in range(len(keyrepeat[p])):
            try :
                repeat[p][k] = repeat[p][k]-1
                if repeat[p][k] < 0 :
                    keyrepeat[p].pop(k)
                    repeat[p].pop(k)
            except :
                pass


def get_controler_input(events,joysticks):
    controls = []
    for joystick in joysticks:
        inputs = get_inputs(joystick)
        for i in inputs :
            if len(i) > 3 :
                if i[0] == "D-Pad":
                    controls.append(i)
                else :
                    if abs(i[-1]) > 0.3 and abs(i[-1]) != 1:
                        move = list(i[0:3])+[signe(i[-1])]
                        controls.append(move)
            else :
                controls.append(i)
    for e in events:
        # Récupération des inputs claviers
        if e.type == pygame.KEYDOWN:
            controls.append(["Keyboard","",e.key])
    if controls :
        joy = False
        pop = []
        for i in range(len(controls)):
            controls[i].pop(1)
            if joy and controls[0] == "Joystick":
                pop.append(i)
        popped = 0
        for i in pop :
            controls.pop(pop-popped)
            popped += 1
        return controls


bouton = pygame.image.load("./DATA/Images/Menu/Controls/Button.png")
dpad = {
    (0,1):pygame.image.load("./DATA/Images/Menu/Controls/D_Pad-R.png"),
    (0,-1):pygame.image.load("./DATA/Images/Menu/Controls/D_Pad-L.png"),
    (1,1):pygame.image.load("./DATA/Images/Menu/Controls/D_Pad-U.png"),
    (1,-1):pygame.image.load("./DATA/Images/Menu/Controls/D_Pad-D.png"),
}
joy = {
    (0,1):pygame.image.load("./DATA/Images/Menu/Controls/Joy-Right.png"),
    (0,-1):pygame.image.load("./DATA/Images/Menu/Controls/Joy-Left.png"),
    (1,1):pygame.image.load("./DATA/Images/Menu/Controls/Joy-Up.png"),
    (1,-1):pygame.image.load("./DATA/Images/Menu/Controls/Joy-Down.png"),
}
text = ["Left","Right","Down","Up","Fullhop","Shorthop","Attack","Special","Shield","Smash (G)","Smash (D)","Smash (B)","Smash (H)","Taunt (G)","Taunt (D)","Taunt (B)","Taunt (H)","Pause"]
def draw_input(window,x,y,number,input_,select,line,focusedbutton,row,row_n):
    if row_n%2 == 0 :
        Texte(text[number],("arial",24,True,False),(0,0,0),x-120,y,format_="right").draw(window)
    if row_n%2 == 1 :
        Texte(text[number],("arial",24,True,False),(0,0,0),x+120,y,format_="left").draw(window)
    if select==number :
        Bouton = Button("[input]",("arial",24,True,False),"./DATA/Images/Menu/Button.png",x,y,200,70)
        if focusedbutton == line and row == row_n:
            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")

        Bouton.draw(window)
    else :
        Bouton = Button("",("arial",24,True,False),"./DATA/Images/Menu/Button.png",x,y,200,70)
        if focusedbutton == line and row == row_n:
            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")

        Bouton.draw(window)
        for j,i in enumerate(input_) :
            if i[0] == "Button" :
                window.blit(bouton,(x+j*64-32-(len(input_)-1)*32,y-32))
                Texte(str(i[1]),("arial",55,True,False),(0,0,0),x+j*64-(len(input_)-1)*32,y).draw(window)
            if i[0] == "D-Pad" :
                window.blit(dpad[(i[1],i[2])],(x+j*64-32-(len(input_)-1)*32,y-32))
            if i[0] == "Joy" :
                window.blit(joy[(i[1]%2,i[2])],(x+j*64-32-(len(input_)-1)*32,y-32))
