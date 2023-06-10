from copy import deepcopy
from DATA.utilities.Gamepad_gestion import *
from DATA.utilities.Interface import *
from DATA.utilities.build import rootDir
import pygame


def savesettings(musicvolume,soundvolume,width,heigth):
    with open(f"{rootDir()}/utilities/Settings.txt","w") as settings :
        settings.write(f"Music :\n"+ 
        f"musicvolume={musicvolume}\n"+
        f"soundvolume={soundvolume}\n"+
        f"\nGraphics :\n"+
        f"size={width}:{heigth}")

def loadsettings():
    #try :
        with open(f"{rootDir()}/utilities/Settings.txt","r") as settings :
            text = str(settings.read())
            text = text.split("\n")
            musicvolume = text[1].split("=")[1]
            soundvolume = text[2].split("=")[1]
            size = text[5]
            size = size.split("=")[1].split(":")
            size = (int(size[0]),int(size[1]))
        return int(musicvolume),int(soundvolume),size
    #except :
    #    print("EXCEPTION RAISED : COULDN'T LOAD SETTINGS")
    #    savesettings(100,100,800,600)
    #    return 100,100,(800,600)

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
        controls = deepcopy([commands["Menu"],commands["Menu"]])
        try :
            controls[0][-2] = [['Button', 9]]
            controls[0][-1] = [['Button', 10]]
            convert_inputs(controls[0],joysticks,0)
        except :
            controls[0] = commands["Menu"]
        try :
            controls[1][-2] = [['Button', 9]]
            controls[1][-1] = [['Button', 10]]
            convert_inputs(controls[1],joysticks,1)
        except :
            controls[1] = commands["Menu"]
    elif len(joysticks) > 0 :
        controls = deepcopy([commands["Menu"],commands["Keyboard"]])
        try :
            controls[0][-2] = [['Button', 9]]
            controls[0][-1] = [['Button', 10]]
            convert_inputs(controls[0],joysticks,0)
        except :
            controls[0] = commands["Menu"]
    else :
        controls = [commands["Keyboard"],commands["Keyboard"]]
    return controls

musicvolume,soundvolume,size = loadsettings()
width,height = size


bouton = pygame.transform.scale(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/Button.png"),resize_t(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/Button.png").get_size(),width,height))

dpad = {
    (0,1):pygame.transform.scale(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/D_Pad-R.png"),resize_t(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/D_Pad-R.png").get_size(),width,height)),
    (0,-1):pygame.transform.scale(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/D_Pad-L.png"),resize_t(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/D_Pad-L.png").get_size(),width,height)),
    (1,1):pygame.transform.scale(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/D_Pad-U.png"),resize_t(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/D_Pad-U.png").get_size(),width,height)),
    (1,-1):pygame.transform.scale(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/D_Pad-D.png"),resize_t(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/D_Pad-D.png").get_size(),width,height)),
}

joy = {
    (0,1):pygame.transform.scale(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/Joy-Right.png"),resize_t(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/Joy-Right.png").get_size(),width,height)),
    (0,-1):pygame.transform.scale(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/Joy-Left.png"),resize_t(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/Joy-Left.png").get_size(),width,height)),
    (1,-1):pygame.transform.scale(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/Joy-Up.png"),resize_t(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/Joy-Up.png").get_size(),width,height)),
    (1,1):pygame.transform.scale(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/Joy-Down.png"),resize_t(pygame.image.load(f"{rootDir()}/Images/Menu/Controls/Joy-Down.png").get_size(),width,height)),
}
text = ["Gauche","Droite","Haut","Bas","Fullhop","Shorthop","Attaque","Special","Garde","Smash (G)","Smash (D)","Smash (H)","Smash (B)","Taunt (G)","Taunt (D)","Taunt (H)","Taunt (B)","Pause","Fulhop 2","Tilt (G)","Tilt (D)","Tilt (H)","Tilt (B)"]

def specialkeysgestion(t,window,x,y,input_,j,width,height,modif_x):
    size = 55
    if t == "LEFT" :
        t = "<   "
        Texte("__",("arial",resize(0,38,width,height)[1],True,False),(0,0,0),x+j*modif_x,y-15).draw(window)
        size = 38
    if t == "RIGHT" :
        t = "   >"
        Texte("__",("arial",resize(0,38,width,height)[1],True,False),(0,0,0),x+j*modif_x,y-15).draw(window)
        size = 38
    if t == "DOWN" :
        Texte("|",("arial",resize(0,40,width,height)[1],True,False),(0,0,0),x+j*modif_x,y-15).draw(window)
        t = "|"
        Texte("v",("arial",resize(0,40,width,height)[1],True,False),(0,0,0),x+j*modif_x,y+15).draw(window)
        size = 40
    if t == "UP" :
        Texte("^",("arial",resize(0,40,width,height)[1],True,False),(0,0,0),x+j*modif_x,y-10).draw(window)
        t = "|"
        Texte("|",("arial",resize(0,40,width,height)[1],True,False),(0,0,0),x+j*modif_x,y+10).draw(window)
        size = 40
    if t == "SPACE" :
        pygame.draw.rect(window,(200,200,200),(x+j*64-42-(len(input_)-1)*32,y-32,84,64))
        size = 30
    if t == "RETURN" :
        t = "__|"
        Texte("<",("arial",resize(0,35,width,height)[1],True,False),(0,0,0),x+j*modif_x-24,y+15).draw(window)
        size = 35
    if t == "ENTER" :
        t = "[ __|]"
        Texte("<",("arial",resize(0,35,width,height)[1],True,False),(0,0,0),x+j*modif_x-24,y+15).draw(window)
        size = 35
    if t == "BACKSPACE" :
        t = "[<   ]"
        Texte("__",("arial",resize(0,35,width,height)[1],True,False),(0,0,0),x+j*modif_x,y-15).draw(window)
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
        Texte("Caps",("arial",resize(0,30,width,height)[1],True,False),(0,0,0),x+j*modif_x,y-15).draw(window)
        Texte("lock",("arial",resize(0,30,width,height)[1],True,False),(0,0,0),x+j*modif_x,y+15).draw(window)
        t = ""
        size = 0
    if t == "NUMLOCK" :
        Texte("Num",("arial",resize(0,30,width,height)[1],True,False),(0,0,0),x+j*modif_x,y-15).draw(window)
        Texte("lock",("arial",resize(0,30,width,height)[1],True,False),(0,0,0),x+j*modif_x,y+15).draw(window)
        t = ""
        size = 0
    if t == "HOME" :
        t = "Fin"
        size = 36


    return size,t

def draw_input(window,x,y,number,input_,select,line,focusedbutton,row,row_n,width,height,frames=0):
    if row == -1 :
        Texte(text[-5+number],("arial",resize(0,24,width,height)[1],True,False),(0,0,0),x-resize(120,0,width,height)[0],y,format_="right").draw(window)
        if select==-5+number :
            sec = str(round(frames/60))
            Bouton = Button("[input] ("+sec+"s)",("arial",resize(0,24,width,height)[1],True,False),f"{rootDir()}/Images/Menu/Button.png",x,y,resize(200,70,width,height))
            if focusedbutton == line:
                Bouton.changeImage(f"{rootDir()}/Images/Menu/Button_focused.png")

            Bouton.draw(window)
        else :
            Bouton = Button("",("arial",resize(0,24,width,height)[1],True,False),f"{rootDir()}/Images/Menu/Button.png",x,y,resize(200,70,width,height))
            if focusedbutton == line:
                Bouton.changeImage(f"{rootDir()}/Images/Menu/Button_focused.png")
            Bouton.draw(window)
            if input_ :
                for j,i in enumerate(input_) :
                    modif_x = j*resize(64,0,width,height)[0]-(len(input_)-1)*resize(32,0,width,height)[0]
                    withdraw_x = resize(32,0,width,height)[0]
                    withdraw_y = resize(32,0,width,height)[0]
                    if i[0] == "Button" :
                        window.blit(bouton,(x+j*modif_x-withdraw_x,y-withdraw_y))
                        Texte(str(i[1]),("arial",resize(0,55,width,height)[1],True,False),(0,0,0),x+j*modif_x,y).draw(window)
                    if i[0] == "D-Pad" :
                        window.blit(dpad[(i[2],i[3])],(x+modif_x-withdraw_x,y-withdraw_y))
                    if i[0] == "Joy" :
                        window.blit(joy[(i[1]%2,i[2])],(x+modif_x-withdraw_x,y-withdraw_y))
                    if i[0] == "Keyboard" :
                        pygame.draw.rect(window,(200,200,200),(x+modif_x-withdraw_x,
                                        y-withdraw_y,resize(60,64,width,height)[0],resize(60,64,width,height)[1]))
                        t = pygame.key.name(i[1]).upper()
                        size,t = specialkeysgestion(t,window,x,y,input_,j,width,height,modif_x)
                        Texte(t,("arial",resize(0,size,width,height)[1],True,False),(0,0,0),
                            x+modif_x,
                            y).draw(window)
            else :
                modif_x = resize(64,0,width,height)[0]
                Texte("Aucun",("arial",resize(0,32,width,height)[1],True,False),(0,0,0),x,y).draw(window)

    else :
        if row_n%2 == 0 :
            Texte(text[number],("arial",resize(0,24,width,height)[1],True,False),(0,0,0),x-resize(120,0,width,height)[0],y,format_="right").draw(window)
        if row_n%2 == 1 :
            Texte(text[number],("arial",resize(0,24,width,height)[1],True,False),(0,0,0),x+resize(120,0,width,height)[0],y,format_="left").draw(window)
        if select==number :
            Bouton = Button("[input]",("arial",resize(0,24,width,height)[1],True,False),f"{rootDir()}/Images/Menu/Button.png",x,y,resize(200,70,width,height))
            if focusedbutton == line and row == row_n:
                Bouton.changeImage(f"{rootDir()}/Images/Menu/Button_focused.png")

            Bouton.draw(window)
        else :
            Bouton = Button("",("arial",resize(0,24,width,height)[1],True,False),f"{rootDir()}/Images/Menu/Button.png",x,y,resize(200,70,width,height))
            if focusedbutton == line and row == row_n:
                Bouton.changeImage(f"{rootDir()}/Images/Menu/Button_focused.png")

            Bouton.draw(window)
            for j,i in enumerate(input_) :
                modif_x = j*resize(64,0,width,height)[0]-(len(input_)-1)*resize(32,0,width,height)[0]
                withdraw_x = resize(32,0,width,height)[0]
                withdraw_y = resize(32,0,width,height)[0]
                if i[0] == "Button" :
                    window.blit(bouton,(x+j*modif_x-withdraw_x,y-withdraw_y))
                    Texte(str(i[1]),("arial",resize(0,55,width,height)[1],True,False),(0,0,0),x+j*modif_x,y).draw(window)
                if i[0] == "D-Pad" :
                    window.blit(dpad[(i[2],i[3])],(x+modif_x-withdraw_x,y-withdraw_y))
                if i[0] == "Joy" :
                    window.blit(joy[(i[1]%2,i[2])],(x+modif_x-withdraw_x,y-withdraw_y))
                if i[0] == "Keyboard" :
                    pygame.draw.rect(window,(200,200,200),(x+modif_x-withdraw_x,
                                    y-withdraw_y,resize(60,64,width,height)[0],resize(60,64,width,height)[1]))
                    t = pygame.key.name(i[1]).upper()
                    size,t = specialkeysgestion(t,window,x,y,input_,j,width,height,modif_x)
                    Texte(t,("arial",resize(0,size,width,height)[1],True,False),(0,0,0),
                        x+modif_x,
                        y).draw(window)
