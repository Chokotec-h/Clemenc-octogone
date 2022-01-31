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


def reset_commands(joysticks,commands):
    if len(joysticks) > 1 :
        controls = [commands["Menu"],commands["Menu"]]
        try :
            controls[0][-2] = [['Button', 8]]
            controls[0][-1] = [['Button', 9]]
            convert_inputs(controls[0],joysticks,0)
        except :
            controls[0] = commands["Menu"]
        try :
            controls[1][-2] = [['Button', 8]]
            controls[1][-1] = [['Button', 9]]
            convert_inputs(controls[1],joysticks,1)
        except :
            controls[0] = commands["Menu"]
    elif len(joysticks) > 0 :
        controls = [commands["Menu"],commands["DefaultKeyboard"]]
        try :
            controls[0][-2] = [['Button', 8]]
            controls[0][-1] = [['Button', 9]]
            convert_inputs(controls[0],joysticks,0)
        except :
            print("coucou1")
            controls[0] = commands["Menu"]
    else :
        controls = [commands["DefaultKeyboard"],commands["DefaultKeyboard"]]
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
    (1,-1):pygame.image.load("./DATA/Images/Menu/Controls/Joy-Up.png"),
    (1,1):pygame.image.load("./DATA/Images/Menu/Controls/Joy-Down.png"),
}
text = ["Gauche","Droite","Haut","Bas","Fullhop","Shorthop","Attaque","Special","Garde","Smash (G)","Smash (D)","Smash (H)","Smash (B)","Taunt (G)","Taunt (D)","Taunt (H)","Taunt (B)","Pause"]

def specialkeysgestion(t,window,x,y,input_,j):
    size = 55
    if t == "LEFT" :
        t = "<   "
        Texte("__",("arial",38,True,False),(0,0,0),x+j*64-(len(input_)-1)*32,y-15).draw(window)
        size = 38
    if t == "RIGHT" :
        t = "   >"
        Texte("__",("arial",38,True,False),(0,0,0),x+j*64-(len(input_)-1)*32,y-15).draw(window)
        size = 38
    if t == "DOWN" :
        Texte("|",("arial",40,True,False),(0,0,0),x+j*64-(len(input_)-1)*32,y-15).draw(window)
        t = "|"
        Texte("v",("arial",40,True,False),(0,0,0),x+j*64-(len(input_)-1)*32,y+15).draw(window)
        size = 40
    if t == "UP" :
        Texte("^",("arial",40,True,False),(0,0,0),x+j*64-(len(input_)-1)*32,y-10).draw(window)
        t = "|"
        Texte("|",("arial",40,True,False),(0,0,0),x+j*64-(len(input_)-1)*32,y+10).draw(window)
        size = 40
    if t == "SPACE" :
        pygame.draw.rect(window,(200,200,200),(x+j*64-42-(len(input_)-1)*32,y-32,84,64))
        size = 30
    if t == "RETURN" :
        t = "__|"
        Texte("<",("arial",35,True,False),(0,0,0),x+j*64-(len(input_)-1)*32-24,y+15).draw(window)
        size = 35
    if t == "ENTER" :
        t = "[ __|]"
        Texte("<",("arial",35,True,False),(0,0,0),x+j*64-(len(input_)-1)*32-24,y+15).draw(window)
        size = 35
    if t == "BACKSPACE" :
        t = "[<   ]"
        Texte("__",("arial",35,True,False),(0,0,0),x+j*64-(len(input_)-1)*32,y-15).draw(window)
        size = 35
    if t == "LEFT CTRL" :
        t = "L_Ctrl"
        size = 25
    if t == "RIGHT CTRL" :
        t = "R_Ctrl"
        size = 25
    if t == "LEFT ALT" :
        t = "L_Alt"
        size = 25
    if t == "RIGHT ALT" :
        t = "R_Alt"
        size = 25
    if t == "LEFT SHIFT" :
        t = "L_Shift"
        size = 20
    if t == "RIGHT SHIFT" :
        t = "R_Shift"
        size = 20
    if t == "ESCAPE" :
        t = "Esc."
        size = 30
    if t == "TAB" :
        size = 35
    if t == "COMPOSE" :
        t = "Comp."
        size = 25
    if t == "PRINT SCREEN" :
        t = "Impecr."
        size = 30
    if t == "DELETE" :
        t = "Suppr."
        size = 30
    if t == "BREAK" :
        t = "Pause"
        size = 30
    if t == "CAPS LOCK" :
        Texte("Caps",("arial",30,True,False),(0,0,0),x+j*64-(len(input_)-1)*32,y-15).draw(window)
        Texte("lock",("arial",30,True,False),(0,0,0),x+j*64-(len(input_)-1)*32,y+15).draw(window)
        t = ""
        size = 0
    if t == "NUMLOCK" :
        Texte("Num",("arial",30,True,False),(0,0,0),x+j*64-(len(input_)-1)*32,y-15).draw(window)
        Texte("lock",("arial",30,True,False),(0,0,0),x+j*64-(len(input_)-1)*32,y+15).draw(window)
        t = ""
        size = 0
    if t == "HOME" :
        t = "Fin"
        size = 36


    return size,t

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
                window.blit(dpad[(i[2],i[3])],(x+j*64-32-(len(input_)-1)*32,y-32))
            if i[0] == "Joy" :
                window.blit(joy[(i[1]%2,i[2])],(x+j*64-32-(len(input_)-1)*32,y-32))
            if i[0] == "Keyboard" :
                pygame.draw.rect(window,(200,200,200),(x+j*64-30-(len(input_)-1)*32,y-32,60,64))
                t = pygame.key.name(i[1]).upper()
                size,t = specialkeysgestion(t,window,x,y,input_,j)
                Texte(t,("arial",size,True,False),(0,0,0),x+j*64-(len(input_)-1)*32,y).draw(window)
