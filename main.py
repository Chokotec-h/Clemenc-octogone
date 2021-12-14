import pygame
import traceback

from DATA.assets.Chars.Training_Mob import Training
import DATA.assets.CharsLoader as Chars
import DATA.assets.Stages as Stages
from DATA.assets.Misc import *
from DATA.assets.animations import icons, icons64
from DATA.utilities.Interface import *
from DATA.utilities.Gamepad_gestion import *
from DATA.utilities.functions import *
from DATA.utilities.Entry import TextInput
from commands import *
from random import randint

import time

####################################
########## Initialisation ##########
####################################

pygame.init()  # Initialisation de pygame
clock = pygame.time.Clock()  # Horloge

pygame.joystick.init()  # Initialisation des manettes
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

for j in joysticks:
    j.init()


####################################
####################################


def main():
    """"""""""""""""""""""""""""""""""""
    """""""""Progamme Principal"""""""""
    """"""""""""""""""""""""""""""""""""

    # initialisation de la fenêtre
    width = 1600
    height = 900
    window = pygame.display.set_mode((width, height))
    

    # test de music et de bruitages

    try:
        
        # Initialisation des contrôles
        run = True
        if len(joysticks) > 1 :
            controls = [commands["Menu"],commands["Menu"]]
        elif len(joysticks) > 0 :
            controls = [commands["Menu"],commands["DefaultKeyboard"]]
        else :
            controls = [commands["DefaultKeyboard"],commands["DefaultKeyboard"]]
        # Déclaration des variables
        stages = ["K201"] # Add stages here
        chars = ["Balan","Millet","Gregoire","Poissonnier","Renault","Reignaud","Rey","Joueur de air-president","Pyro-Aubin","Kebab"] # Add characters here
        # Ajouter les musiques : (Nom de fichier,durée,stage,musique par defaut?)
        musics = [("DATA/Musics/lets_fight.mp3",136,"K201",True),("DATA/Musics/Panda_Ball.mp3",166,"Pandadrome",True)]

        Menu = "title"

        smoke = list()
        smokeframe  = 0
        pause = False
        hold_pause = False
        Play = False
        musicplaying = False
        focusedbutton = 0
        row = 0
        confirm = False
        musicstartedat = 0
        commandconfig = None
        getting = list()

        # Training
        TrainingHDI = 0
        TrainingVDI = 0
        Tech = 0

        # Ending
        stock = [0,0]
        time_game = 0
        begin_game = 0
        pause_time = 0
        game_running = -1

        ############################
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1)
        

        pygame.mixer.music.load("DATA/Musics/intro_2.mp3")
        pygame.mixer.music.play()
        musicstartedat = time.time()
        while run:  # Boucle du programme
            actualize_repeating()
            if Menu == "title" :
                window.fill((0x99,0x55,0x99)) # Background color
                pygame.draw.rect(window,(60,60,60),(0,0,width,128))
                pygame.draw.rect(window,(60,60,60),(0,height-128,width,128))
                Texte("Beta version",("Arial",15,True,True),(0,0,0),100,64,format_="left").draw(window)

                Texte("Appuyez sur A / Espace",("Arial black",50,True,False),(0,0,0),width/2,height-64).draw(window)
                window.blit(pygame.transform.scale(pygame.image.load("./DATA/Images/logo.png"),(512,512)),(width/2-256,height/2-256-64))
                Texte("OCTOGONE",("Comic",128,True,False),(40,40,40),width/2+5,height/2 + 256+5).draw(window)
                Texte("OCTOGONE",("Comic",128,True,False),(128,0,128),width/2,height/2 + 256).draw(window)
                if convert_inputs(controls[0],joysticks,0)[6] :
                    confirm = True
                    Menu = "main"
                    pygame.mixer.music.load("DATA/Musics/menu.mp3")
                    pygame.mixer.music.play()
            else :
                window.fill((0x66,0x22,0x66)) # Background color

            # Récupération des events
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT: # Bouton croix en haut à droite de l'écran
                    run = False

            if not Play :
        
                if time.time()-musicstartedat > 59 and Menu != "title": # Loop
                    pygame.mixer.music.load("DATA/Musics/menu.mp3")
                    pygame.mixer.music.play()
                    musicstartedat = time.time()
                
                if not convert_inputs(controls[0],joysticks,0)[6]:
                    confirm = False
                if Menu == "main":
                    if input_but_no_repeat(3,controls,joysticks,0):
                        focusedbutton += 1
                        
                    if input_but_no_repeat(2,controls,joysticks,0):
                        focusedbutton -= 1
                        
                    focusedbutton = focusedbutton%3

                    Bouton = Button("Combat",("arial",50,True,False),"./DATA/Images/Menu/Button.png",width/2,height/4,250,100)
                    if focusedbutton == 0:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                            Menu = "stage"
                            training = False
                            focusedbutton = 0
                            confirm = True
                    Bouton.draw(window)
                    Bouton = Button("Paramètres",("arial",50,True,False),"./DATA/Images/Menu/Button.png",width/2,height/2,250,100)
                    if focusedbutton == 1:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                            Menu = "commands"
                            focusedbutton = 0
                            confirm = True
                    Bouton.draw(window)

                    Bouton = Button("",("arial",45,True,False),"./DATA/Images/Menu/Button.png",width/2,3*height/4,250,100)
                    if focusedbutton == 2:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                            Menu = "stage"
                            training = True
                            focusedbutton = 0
                            confirm = True
                    Bouton.draw(window)
                    Texte("Pandaball",("arial",45,True,False),(0,0,0),width/2,3*height/4-20).draw(window)
                    Texte("(Entraînement)",("arial",30,True,False),(0,0,0),width/2,3*height/4+20).draw(window)

                # MENU COMMANDES
                if Menu == "commands":
                    if commandconfig is None:
                        if input_but_no_repeat(3,controls,joysticks,0):
                            focusedbutton += 1
                            
                        if input_but_no_repeat(2,controls,joysticks,0):
                            focusedbutton -= 1
                            
                        focusedbutton = (focusedbutton+2)%(len(commands)-1)-2
                        for i,n in enumerate(commands) :
                            if n not in ["Default","Menu","DefaultKeyboard"]:
                                Bouton = Button(n,("arial",24,False,False),"./DATA/Images/Menu/Button.png",width/2,(i+1)*60-180,120,50)
                                Bouton.resize(Bouton.textobject.width+20,50)
                                if focusedbutton == i-3:
                                    Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                                    if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                        commandconfig = n
                                        inputget = -3
                                        confirm = True
                                Bouton.draw(window)
                        Bouton = Button("+",("arial",50,True,False),"./DATA/Images/Menu/Button.png",100,800,50,50)
                        if focusedbutton == -2:
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                commandconfig = 0
                                name = "Player"
                                confirm = True
                        Bouton.draw(window)
                        Bouton = Button("<--",("arial",50,True,False),"./DATA/Images/Menu/Button.png",100,850,100,60)
                        if focusedbutton == -1:
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                Menu = "main"
                                confirm = True
                        Bouton.draw(window)
                    elif commandconfig == 0:
                        Entry = TextInput(name)
                        enter = Entry.update(events)
                        name = Entry.get_text()
                        Texte("Enter name :  "+Entry.get_text(),("arial",30,False,False),(0,0,0),width/2,height/2).draw(window)
                        Texte("<A/Enter to confirm>",("arial",30,False,False),(0,0,0),width/2,50+height/2).draw(window)
                        if enter :
                            commands[name] = commands["Default"]
                            commandconfig = name
                            inputget = -1
                            confirm = True
                    else :
                        if inputget <= -1 :
                            if input_but_no_repeat(3,controls,joysticks,0):
                                focusedbutton += 1
                                
                            if input_but_no_repeat(2,controls,joysticks,0):
                                focusedbutton -= 1
                                
                            if input_but_no_repeat(0,controls,joysticks,0):
                                row -= 1
                                
                            if input_but_no_repeat(1,controls,joysticks,0):
                                row += 1
                            
                        if row == 0 :
                            focusedbutton = ((focusedbutton+1)%5)-1
                        if row == 1 :
                            focusedbutton = ((focusedbutton+1)%6)-1
                        if row == 2 :
                            focusedbutton = ((focusedbutton+1)%5)-1
                        if row == 3 :
                            focusedbutton = ((focusedbutton+1)%6)-1
                        row = row%4
                        if inputget > -1:
                            
                            if get_controler_input(events,joysticks) and not confirm:
                                add = get_controler_input(events,joysticks)
                                for i in add :
                                    if i not in getting :
                                        getting.append(i)
                            if not get_controler_input(events,joysticks) and getting :
                                commands[commandconfig][inputget] = getting
                                inputget = -1
                                confirm = True
                                getting = list()

                        # Stick
                        for i,k in enumerate(commands[commandconfig][0:4]):
                            draw_input(window,width/6,(i+1)*80,i,k,inputget,i,focusedbutton,row,0)
                            if focusedbutton == i and row == 0:
                                if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                    inputget = i
                                    confirm = True
                        # Jump, Attack, Special, Shield
                        for i,k in enumerate(commands[commandconfig][4:9]):
                            draw_input(window,2*width/6,(i+1)*80,i+4,k,inputget,i,focusedbutton,row,1)
                            if focusedbutton == i and row == 1:
                                if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                    inputget = i+4
                                    confirm = True
                        # C-Stick
                        for i,k in enumerate(commands[commandconfig][9:13]):
                            draw_input(window,4*width/6,(i+1)*80,i+9,k,inputget,i,focusedbutton,row,2)
                            if focusedbutton == i and row == 2:
                                if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                    inputget = i+9
                                    confirm = True
                        # D-Pad + Pause
                        for i,k in enumerate(commands[commandconfig][13:]):
                            draw_input(window,5*width/6,(i+1)*80,i+13,k,inputget,i,focusedbutton,row,3)
                            if focusedbutton == i and row == 3:
                                if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                    inputget = i+13
                                    confirm = True
                        Bouton = Button("Sauvegarder",("arial",50,True,False),"./DATA/Images/Menu/Button.png",200,850,250,60)
                        if focusedbutton == -1 and row%2 == 0:
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                with open("./commands.py","w") as commandfile :
                                    commandfile.write("commands = {\n")
                                    for k in commands :
                                        commandfile.write(f'\t"{k}":{commands[k]},\n')
                                    commandfile.write("}")

                                commandconfig = None
                                confirm = True
                        Bouton.draw(window)

                        Bouton = Button("Supprimer",("arial",50,True,False),"./DATA/Images/Menu/Button.png",1450,850,200,60)
                        if focusedbutton == -1 and row%2 == 1:
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                del commands[commandconfig]
                                with open("./commands.py","w") as commandfile :
                                    commandfile.write("commands = {\n")
                                    for k in commands :
                                        commandfile.write(f'\t"{k}":{commands[k]},\n')
                                    commandfile.write("}")

                                commandconfig = None
                                confirm = True
                        Bouton.draw(window)
                            

                if Menu == "stage":
                    if training :
                        actualstages = ["Pandadrome"] + stages
                    else :
                        actualstages = stages
                    if input_but_no_repeat(3,controls,joysticks,0):
                        focusedbutton += 9
                        
                    if input_but_no_repeat(2,controls,joysticks,0):
                        focusedbutton -= 9
                        
                    if input_but_no_repeat(0,controls,joysticks,0):
                        focusedbutton -= 1
                        
                    if input_but_no_repeat(1,controls,joysticks,0):
                        focusedbutton += 1
                        
                    #row = row%1
                    focusedbutton = ((focusedbutton+1)%(len(actualstages)+1))-1
                    Bouton = Button("<--",("arial",50,True,False),"./DATA/Images/Menu/Button.png",100,850,100,60)
                    if focusedbutton == -1:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                            Menu = "main"
                            confirm = True
                    else :
                        Texte(actualstages[focusedbutton],("arial",50,True,False),(0,0,0),30,height//2,format_="left").draw(window)
                    Bouton.draw(window)
                    for i in range(len(actualstages)):
                        Bouton = Button("",("arial",50,True,False),"./DATA/Images/Menu/Button.png",((i%9)*150)+250,(i//9*150)+100,100,100)
                        if focusedbutton == i :
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                Menu = "char"
                                scroll1 = 0
                                scroll2 = 0
                                selectchar_1 = 0
                                selectchar_2 = 0
                                selected_1 = False
                                selected_2 = False
                                movename1 = -1
                                movename2 = -1
                                stage = i
                                names = [0,0]
                                namelist = [k for k in commands]
                                namelist.pop(0)
                                confirm = True
                                b = 0
                        Bouton.draw(window)
                        window.blit(pygame.transform.scale(pygame.image.load(f"./DATA/Images/Stages/{actualstages[i]}.png"),(90,90)),((i%9*150)+205,(i//9*150)+55))
                if Menu == "char":
                    Bouton = Button("<--",("arial",50,True,False),"./DATA/Images/Menu/Button.png",width/2,40,100,60)
                    if not convert_inputs(controls[0],joysticks,0)[7]:
                        b = 0
                    else :
                        b += 1
                    if b > 0:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                    if b >= 10:
                        Menu = "stage"
                    Bouton.draw(window)
                    ### P1
                    for i in range(len(chars)):
                        Bouton = Button("",("arial",50,True,False),standard,0,105*(i-scroll1-len(chars)+4),384,100)
                        Bouton.draw(window)
                        Bouton = Button("",("arial",50,True,False),standard,0,105*(i-scroll1+len(chars)+4),384,100)
                        Bouton.draw(window)
                        Bouton = Button("",("arial",50,True,False),standard,0,105*(i-scroll1+4),384,100)
                        if selectchar_1 == i :
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            Bouton.resize(400,100)
                        Bouton.draw(window)
                    for i in range(len(chars)):
                        window.blit(icons64[chars[i]],(64,105*(i-scroll1+4)-32))
                        window.blit(icons64[chars[i]],(64,105*(i-scroll1+4-len(chars))-32))
                        window.blit(icons64[chars[i]],(64,105*(i-scroll1+4+len(chars))-32))
                    # Arrows
                    if convert_inputs(controls[0],joysticks,0)[3] and not selected_1 and scroll1 == selectchar_1:
                        selectchar_1 += 1
                        scroll1 += 1
                        scroll1 = scroll1%len(chars)
                        scroll1 -= 1
                        if selectchar_1 >= len(chars) :
                            selectchar_1 = 0
                    if convert_inputs(controls[0],joysticks,0)[2] and not selected_1 and scroll1 == selectchar_1:
                        selectchar_1 -= 1
                        scroll1 -= 1
                        scroll1 = scroll1%len(chars)
                        scroll1 += 1
                        if selectchar_1 < 0 :
                            selectchar_1 = len(chars) - 1
                    if round(scroll1,1) < selectchar_1 :
                        scroll1 += 0.25
                        scroll1 = round(scroll1,3)
                    if round(scroll1,1) > selectchar_1 :
                        scroll1 -= 0.25
                        scroll1 = round(scroll1,3)
                    if round(scroll1,1) == selectchar_1 :
                        scroll1 = selectchar_1

                    # OK Buttons
                    if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                        selected_1 = True
                    if convert_inputs(controls[0],joysticks,0)[7]:
                        selected_1 = False

                    ### P2
                    if training :
                        Bouton = Button("",("arial",50,True,False),standard,width,height/2,384,100)
                        Bouton.draw(window)
                        window.blit(pygame.transform.scale(pygame.image.load("./DATA/Images/Sprites/Misc/Training/Training_icon.png"),(64,64)),(width-128,height/2-32))
                    else :
                        for i in range(len(chars)):
                            # Buttons
                            Bouton = Button("",("arial",50,True,False),standard,width,105*(i-scroll2-len(chars)+4),384,100)
                            Bouton.draw(window)
                            Bouton = Button("",("arial",50,True,False),standard,width,105*(i-scroll2+len(chars)+4),384,100)
                            Bouton.draw(window)
                            Bouton = Button("",("arial",50,True,False),standard,width,105*(i-scroll2+4),384,100)
                            if selectchar_2 == i :
                                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                                Bouton.resize(400,100)
                            Bouton.draw(window)
                        # Sprites
                        for i in range(len(chars)):
                            window.blit(icons64[chars[i]],(width-128,105*(i-scroll2+4)-32))
                            window.blit(icons64[chars[i]],(width-128,105*(i-scroll2+4-len(chars))-32))
                            window.blit(icons64[chars[i]],(width-128,105*(i-scroll2+4+len(chars))-32))
                        # Arrows
                        if convert_inputs(controls[1],joysticks,1)[3] and not selected_2 and scroll2 == selectchar_2:
                            selectchar_2 += 1
                            scroll2 += 1
                            scroll2 = scroll2%len(chars)
                            scroll2 -= 1
                            if selectchar_2 >= len(chars) :
                                selectchar_2 = 0
                        if convert_inputs(controls[1],joysticks,1)[2] and not selected_2 and scroll2 == selectchar_2:
                            selectchar_2 -= 1
                            scroll2 -= 1
                            scroll2 = scroll2%len(chars)
                            scroll2 += 1
                            if selectchar_2 < 0 :
                                selectchar_2 = len(chars) - 1
                        if round(scroll2,1) < selectchar_2 :
                            scroll2 += 0.25
                            scroll2 = round(scroll2,3)
                        if round(scroll2,1) > selectchar_2 :
                            scroll2 -= 0.25
                            scroll2 = round(scroll2,3)
                        if round(scroll2,1) == selectchar_2 :
                            scroll2 = selectchar_2
                        if convert_inputs(controls[1],joysticks,1)[6] and not confirm:
                            selected_2 = True
                        if convert_inputs(controls[1],joysticks,1)[7]:
                            selected_2 = False

                    # Names
                    if names[0] == 0 :
                        text = "Player 1"
                    else :
                        text = namelist[names[0]]
                    Bouton = Button(text,("arial",24,True,False),"./DATA/Images/Menu/Button.png",3*width/10,height-150,200,32)
                    Bouton.draw(window)
                    # Stop crash
                    try :
                        convert_inputs(commands[namelist[names[0]]],joysticks,0)
                    except :
                        names[0] += movename1
                        if names[0] >= len(namelist):
                            names[0] = 0
                    if input_but_no_repeat(10,controls,joysticks,0):
                        names[0] += 1
                        movename1 = 1
                        if names[0] == 1 : # Defaultkeyboard
                            names[0] += 1
                        if names[0] >= len(namelist):
                            names[0] = 0
                    if input_but_no_repeat(9,controls,joysticks,0):
                        names[0] -= 1
                        movename1 = -1
                        if names[0] == 1 : # Defaultkeyboard
                            names[0] -= 1
                        if names[0] < 0:
                            names[0] = len(namelist)-1

                    if names[1] == 0 :
                        text = "Player 2"
                    else :
                        text = namelist[names[1]]
                    Bouton = Button(text,("arial",24,True,False),"./DATA/Images/Menu/Button.png",7*width/10,height-150,200,32)
                    Bouton.draw(window)
                    try :
                        convert_inputs(commands[namelist[names[1]]],joysticks,1)
                    except :
                        names[1] += movename2
                        if names[1] >= len(namelist):
                            names[1] = 0
                    if input_but_no_repeat(10,controls,joysticks,1):
                        names[1] += 1
                        movename2 = 1
                        if names[1] == 1 : # Defaultkeyboard
                            names[1] += 1
                        if names[1] >= len(namelist):
                            names[1] = 0
                    if input_but_no_repeat(9,controls,joysticks,1):
                        names[1] -= 1
                        movename2 = -1
                        if names[1] == 1 : # Defaultkeyboard
                            names[1] -= 1
                        if names[1] < 0:
                            names[1] = len(namelist)-1

                    # Text
                    if selected_1 :
                        pygame.draw.rect(window,(230,230,230),(width/8,height-120,width/4,30))
                        Texte("READY",("arial",24,True,False),(0,0,0),width/4,height-110,format_="center").draw(window)
                    if selected_2 :
                        pygame.draw.rect(window,(230,230,230),(5*width/8,height-120,width/4,30))
                        Texte("READY",("arial",24,True,False),(0,0,0),3*width/4,height-110,format_="center").draw(window)
                    
                    pygame.draw.rect(window,(200,200,200),(0,height-90,width,90))
                    Texte(str(Chars.charobjects[chars[selectchar_1]](0,0,0)),("arial",64,True,False),(0,0,0),width/2-30,height-50,format_="right").draw(window)
                    if training :
                        Texte("Pandapluche",("arial",64,True,False),(0,0,0),width/2+30,height-50,format_="left").draw(window)
                    else :
                        Texte(str(Chars.charobjects[chars[selectchar_2]](0,0,0)),("arial",64,True,False),(0,0,0),width/2+30,height-50,format_="left").draw(window)
                    Texte("|",("arial",80,True,False),(0,0,0),width/2,height-50,format_="center").draw(window)

                    if (selected_2 or training) and selected_1 :
                        if names[0] == 0 and controls[0] == commands["DefaultKeyboard"]:
                            names[0] = 1
                        if names[1] == 0 and controls[1] == commands["DefaultKeyboard"]:
                            names[1] = 1
                        Play = True
                        Menu = "stage"
                        Char_P1 = Chars.charobjects[chars[selectchar_1]](-350,0,0)

                        stock = [5,5]
                        time_game = 0.3*60
                        begin_game = time.time()
                        pause_time = 0
                        pausefrom = 0
                        game_running = -1

                        if training :
                            Char_P2 = Chars.Training(0,0,1)
                            basedamages = 0
                            airspeed=1.25
                            deceleration=0.75
                            fallspeed=0.85
                            fastfallspeed=1.25
                        else :
                            Char_P2 = Chars.charobjects[chars[selectchar_2]](350,0,1)
                        controls = [commands[namelist[names[0]]],commands[namelist[names[1]]]]
                        background = pygame.transform.scale(pygame.image.load(f"./DATA/Images/Stages/{actualstages[stage]}.png"),(1600,900))
                        for m in musics :
                            if m[2] == actualstages[stage] and m[3]:
                                currentmusic = m[0]
                                lenmusic = m[1]
                        musicplaying = False
                        musicstartedat = time.time()
                        stage = Stages.create_stage(actualstages[stage])
                if Menu == "results":
                    Menu = "stage"
        

            else :
                #""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""#
                """""""""""""""""""""  IN  BATTLE  """""""""""""""""""""""""""
                #""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""#
                if not musicplaying :
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(currentmusic)
                    pygame.mixer.music.play()
                    musicplaying = True
                    musicstartedat = time.time()
        
                if time.time()-musicstartedat > lenmusic : # Loop
                    musicplaying = False

                window.fill((255, 255, 255)) # Réinitialisation de l'écran à chaque frame
                window.blit(background,(0,0))

                # Recuperation des touches
                if game_running < 0 and (convert_inputs(controls[0],joysticks,0)[-1] or convert_inputs(controls[1],joysticks,1)[-1]):
                    if not hold_pause:
                        pause = not pause
                        hold_pause  = True
                else :
                    hold_pause = False

                if game_running < 0 and not pause:
                    pausefrom = time.time()
                    
                    # P1
                    inputs_1 = convert_inputs(controls[0],joysticks,0)[0:-1]
                    if not (inputs_1[4] or inputs_1[5]): # Jump
                        Char_P1.jumping = False

                    # Transmission des inputs à l'objet Palyer 1
                    Char_P1.act(inputs_1, stage, Char_P2,not(pause or Char_P1.BOUM or Char_P2.BOUM))
                    if Char_P1.die == 30 and not training:
                        stock[0] -= 1

                    # P2
                    inputs_2 = convert_inputs(controls[1],joysticks,1)[0:-1]
                    if not (inputs_2[4] or inputs_2[5]): # Jump
                        Char_P2.jumping = False

                    #Char_P2.act([False for _ in range(17)], stage, Char_P1,not(pause or Char_P1.BOUM or Char_P2.BOUM))
                    if training :
                        Char_P2.deceleration = deceleration
                        traininginputs = [False for _ in range (17)]
                        if Char_P2.hitstun or Char_P2.tumble :
                            if TrainingHDI > 0 :
                                traininginputs[1] = True
                            if TrainingHDI < 0 :
                                traininginputs[0] = True
                            if TrainingVDI > 0 :
                                traininginputs[2] = True
                            if TrainingVDI < 0 :
                                traininginputs[3] = True
                            if Tech > 0 :
                                if randint(0,1) == 1:
                                    Char_P2.tech = 5
                                else :
                                    Char_P2.tech = 0
                            if Tech < 0 :
                                Char_P2.tech = 5
                        else :
                            Char_P2.tech = 0
                            
                        Char_P2.act(traininginputs, stage, Char_P1,not(pause or Char_P1.BOUM or Char_P2.BOUM))
                    else :
                        Char_P2.act(inputs_2, stage, Char_P1,not(pause or Char_P1.BOUM or Char_P2.BOUM))
                    if Char_P2.die == 30 and not training:
                        stock[1] -= 1
                    ########

                    Char_P2.collide(Char_P1)
                    Char_P1.collide(Char_P2)
                elif pause :
                    pause_time += time.time() - pausefrom
                    pausefrom = time.time()
                    Texte(f"Pause",("Arial",60,False,False),(0,0,0),width//2,height//2,800).draw(window)

                """ Affichage des éléments """

                ### Debug
                for h in Char_P1.active_hitboxes:
                    h.draw(window)
                for h in Char_P2.active_hitboxes:
                    h.draw(window)
                # Smoke
                smokeframe += 1
                smokeframe = smokeframe%4
                if Char_P1.hitstun and smokeframe == 0:
                    smoke.append(Smoke(Char_P1.rect.x+Char_P1.rect.w/2,Char_P1.rect.y+Char_P1.rect.h/2))
                if Char_P2.hitstun and smokeframe == 0:
                    smoke.append(Smoke(Char_P2.rect.x+Char_P2.rect.w/2,Char_P2.rect.y+Char_P2.rect.h/2))
                for i,s in enumerate(smoke):
                    s.draw(window)
                    if s.duration <= 0:
                        del smoke[i]
                # Stage
                stage.draw(window)
                # Chars
                Char_P2.draw(window)
                Char_P1.draw(window)
                # Damages
                Char_P1.damages = float(Char_P1.damages)
                Texte(f"{str(round(Char_P1.damages,2)).split('.')[0]}  %",("Arial",60,False,False),(255-(Char_P1.damages/5),max(255-Char_P1.damages,0),max(255-Char_P1.damages*2,0)),width//3,height-50,800,format_="left").draw(window)
                Texte(f".{str(round(Char_P1.damages,2)).split('.')[1]}",("Arial",30,False,False),(255-(Char_P1.damages/5),max(255-Char_P1.damages,0),max(255-Char_P1.damages*2,0)),width//3+len(str(round(Char_P1.damages,2)).split('.')[0])*25,height-30,800,format_="left").draw(window)
                for s in range(stock[0]):
                    window.blit(pygame.transform.scale(icons[Char_P1.name],(16,16)),(width/3-10+20*s,height - 100))

                Char_P2.damages = float(Char_P2.damages)
                Texte(f"{str(round(Char_P2.damages,2)).split('.')[0]}  %",("Arial",60,False,False),(255-(Char_P2.damages/5),max(255-Char_P2.damages,0),max(255-Char_P2.damages*2,0)),2*width//3,height-50,800,format_="left").draw(window)
                Texte(f".{str(round(Char_P2.damages,2)).split('.')[1]}",("Arial",30,False,False),(255-(Char_P2.damages/5),max(255-Char_P2.damages,0),max(255-Char_P2.damages*2,0)),2*width//3+len(str(round(Char_P2.damages,2)).split('.')[0])*25,height-30,800,format_="left").draw(window)
                for s in range(stock[1]):
                    window.blit(pygame.transform.scale(icons[Char_P2.name],(16,16)),(2*width/3-10+20*s,height - 100))

                if not training :
                    s = time_game+(begin_game-time.time()) + pause_time
                    ms = str(round(s*100)/100).split(".")[1]
                    if len(ms) == 1 :
                        ms = ms+"0"
                    s = str(round(s*100)/100).split(".")[0]
                    m = int(s)//60
                    s = int(s) - m*60
                    if m*60+s > 0 and game_running < 0:
                        if m*60+s > 5 :
                            Texte(f"{str(m)}:{str(s)}'{str(ms)}",("Arial",60,True,False),(255,255,255),width/2,75).draw(window)
                        else :
                            Texte(f"{str(s)}",("Arial",180,True,False),(100,0,0),width/2,height/2).draw(window)

                    if (m*60+s < 1 or min(stock) <= 0) and game_running < 0 :
                        game_running = 180
                    if game_running > 0 :
                        Texte("FIN DU MATCH",("Arial",200,True,False),(150,0,0),width/2,height/2).draw(window)
                        game_running -= 1
                        if game_running < 1 :
                            Play = False
                            Menu = "results"
                

                """"""""""""""""""""""""""""""""""""""""""
                ########  INTERFACE ENTRAINEMENT  ########
                """"""""""""""""""""""""""""""""""""""""""
                if training :
                    pygame.draw.rect(window,(250,250,250),(width-120,height/2,120,60))
                    Texte(str(Char_P2.combo),("Arial",40,False,False),(0,0,0),width-80,height/2+25).draw(window)
                    pygame.draw.rect(window,(250,250,250),(width-120,height/2+75,120,60))
                    Texte(str(round(Char_P2.combodamages,2))+"%",("Arial",40,False,False),(0,0,0),width-80,height/2+100).draw(window)
                    if pause :
                        if training :
                            Char_P2.damages = basedamages
                            pygame.draw.rect(window,(180,180,180),(0,0,300,height))
                            if not convert_inputs(controls[0],joysticks,0)[6] :
                                confirm = False
                            focusedbutton = (focusedbutton+1)%10-1
                            if input_but_no_repeat(2,controls,joysticks,0):
                                focusedbutton -= 1
                                
                            if input_but_no_repeat(3,controls,joysticks,0):
                                focusedbutton += 1
                                

                            Bouton = Button(f"<---",("Arial",20,False,False),"./DATA/Images/Menu/Button.png",150,height/12,200,60)
                            if focusedbutton == -1 :
                                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                                if convert_inputs(controls[0],joysticks,0)[6] and not confirm :
                                    confirm = True
                                    Menu = "stage"
                                    Play = False
                                    pause = False
                                    focusedbutton = 0
                                    musicstartedat = 1000
                                    stage = 0
                                    if len(joysticks) > 1 :
                                        controls = [commands["Menu"],commands["Menu"]]
                                    elif len(joysticks) > 0 :
                                        controls = [commands["Menu"],commands["DefaultKeyboard"]]
                                    else :
                                        controls = [commands["DefaultKeyboard"],commands["DefaultKeyboard"]]
                                    clock.tick(10)
                            Bouton.draw(window)

                            Bouton = Button("Réinitialiser",("Arial",40,False,False),"./DATA/Images/Menu/Button.png",150,2.5*height/12,200,60)
                            if focusedbutton == 0 :
                                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                                if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                    confirm = True
                                    Char_P2 = Training(0,0,1)
                            Bouton.draw(window)

                            Bouton = Button(f"DI Horizontale : {['Aucune','Droite','Gauche'][TrainingHDI]}",("Arial",20,False,False),"./DATA/Images/Menu/Button.png",150,3.5*height/12,200,60)
                            if focusedbutton == 1 :
                                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                                if convert_inputs(controls[0],joysticks,0)[6] and not confirm :
                                    confirm = True
                                    TrainingHDI += 1
                                    TrainingHDI = (TrainingHDI+1)%3 - 1
                            Bouton.draw(window)
                            Bouton = Button(f"DI Verticale : {['Aucune','Haut','Bas'][TrainingVDI]}",("Arial",20,False,False),"./DATA/Images/Menu/Button.png",150,4.5*height/12,200,60)
                            if focusedbutton == 2 :
                                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                                if convert_inputs(controls[0],joysticks,0)[6] and not confirm :
                                    confirm = True
                                    TrainingVDI += 1
                                    TrainingVDI = (TrainingVDI+1)%3 - 1
                            Bouton.draw(window)

                            Bouton = Button(f"Tech : {['Jamais','1/2','Toujours'][Tech]}",("Arial",20,False,False),"./DATA/Images/Menu/Button.png",150,5.5*height/12,200,60)
                            if focusedbutton == 3 :
                                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                                if convert_inputs(controls[0],joysticks,0)[6] and not confirm :
                                    confirm = True
                                    Tech += 1
                                    Tech = (Tech+1)%3 - 1
                            Bouton.draw(window)

                            Texte(f"Dégâts : {round(basedamages)}%",("Arial",20,False,False),(0,0,0),150,6.5*height/12-25).draw(window)
                            pygame.draw.rect(window,(10,10,10),(60,6.5*height/12-2,204,4))
                            Bouton = Button(f"",("Arial",20,False,False),"./DATA/Images/Menu/Slider.png",basedamages/999*200+60,6.5*height/12,12,12)
                            if focusedbutton == 4 :
                                Bouton.changeImage("./DATA/Images/Menu/Slider_focused.png")
                                if convert_inputs(controls[0],joysticks,0)[1] :
                                    basedamages += 1
                                    if basedamages > 999 :
                                        basedamages = 0
                                if convert_inputs(controls[0],joysticks,0)[0] :
                                    basedamages -= 1
                                    if basedamages < 0 :
                                        basedamages = 999
                                Char_P2.damages = basedamages
                            Bouton.draw(window)

                            # Change Statistics
                            Texte(f"Caractéristiques :",("Arial black",24,False,False),(0,0,0),150,7.5*height/12-20).draw(window)

                            Texte(f"Decéleration : {round(deceleration,2)}",("Arial",20,True,False),(0,0,0),150,8*height/12-25).draw(window)
                            pygame.draw.rect(window,(10,10,10),(40,8*height/12+3,254,4))
                            Bouton = Button(f"",("Arial",20,False,False),"./DATA/Images/Menu/Slider.png",(deceleration-0.5)*500+40,8*height/12+5,12,12)
                            if focusedbutton == 5 :
                                Bouton.changeImage("./DATA/Images/Menu/Slider_focused.png")
                                if convert_inputs(controls[0],joysticks,0)[1] :
                                    deceleration += 0.005
                                    if deceleration > 1 :
                                        deceleration = 1
                                if convert_inputs(controls[0],joysticks,0)[0] :
                                    deceleration -= 0.005
                                    if deceleration < 0.5 :
                                        deceleration = 0.5
                            equal = []
                            for p in Chars.decelerations :
                                window.blit(pygame.transform.scale(icons[p],(20,20)),((Chars.decelerations[p]-0.5)*500+30,8*height/12+15))
                                if abs(deceleration - Chars.decelerations[p]) < 0.01 and (not (convert_inputs(controls[0],joysticks,0)[1] or convert_inputs(controls[0],joysticks,0)[0]) or focusedbutton != 5):
                                    deceleration = Chars.decelerations[p]
                                    equal.append(p)
                            if equal :
                                txt = ""
                                for e in equal :
                                    txt += e + "/"
                                Texte(f"({txt[:-1]})",("Arial",15,False,False),(0,0,0),150,8*height/12-10).draw(window)
                            Bouton.draw(window)

                            Texte(f"Vitesse aérienne : {round(airspeed,1)}",("Arial",20,True,False),(0,0,0),150,9*height/12-25).draw(window)
                            pygame.draw.rect(window,(10,10,10),(40,9*height/12+3,254,4))
                            Bouton = Button(f"",("Arial",20,False,False),"./DATA/Images/Menu/Slider.png",(airspeed-0.5)/1.5*250+40,9*height/12+5,12,12)
                            if focusedbutton == 6 :
                                Bouton.changeImage("./DATA/Images/Menu/Slider_focused.png")
                                if convert_inputs(controls[0],joysticks,0)[1] :
                                    airspeed += 0.05
                                    if airspeed > 2 :
                                        airspeed = 2
                                if convert_inputs(controls[0],joysticks,0)[0] :
                                    airspeed -= 0.05
                                    if airspeed < 0.5 :
                                        airspeed = 0.5
                            equal = []
                            for p in Chars.airspeeds :
                                window.blit(pygame.transform.scale(icons[p],(20,20)),((Chars.airspeeds[p]-0.5)/1.5*250+30,9*height/12+15))
                                if abs(airspeed - Chars.airspeeds[p]) < 0.03 and (not (convert_inputs(controls[0],joysticks,0)[1] or convert_inputs(controls[0],joysticks,0)[0]) or focusedbutton != 6):
                                    airspeed = Chars.airspeeds[p]
                                    equal.append(p)
                            if equal :
                                txt = ""
                                for e in equal :
                                    txt += e + "/"
                                Texte(f"({txt[:-1]})",("Arial",15,False,False),(0,0,0),150,9*height/12-10).draw(window)
                            Bouton.draw(window)

                            Texte(f"Vitesse de chute : {round(fallspeed,1)}",("Arial",20,True,False),(0,0,0),150,10*height/12-25).draw(window)
                            pygame.draw.rect(window,(10,10,10),(40,10*height/12+3,254,4))
                            Bouton = Button(f"",("Arial",20,False,False),"./DATA/Images/Menu/Slider.png",(fallspeed-0.25)/1.25*250+40,10*height/12+5,12,12)
                            if focusedbutton == 7 :
                                Bouton.changeImage("./DATA/Images/Menu/Slider_focused.png")
                                if convert_inputs(controls[0],joysticks,0)[1] :
                                    fallspeed += 0.05
                                    if fallspeed > 1.5 :
                                        fallspeed = 1.5
                                if convert_inputs(controls[0],joysticks,0)[0] :
                                    fallspeed -= 0.05
                                    if fallspeed < 0.25 :
                                        fallspeed = 0.25
                            equal = []
                            for p in Chars.fallspeeds :
                                window.blit(pygame.transform.scale(icons[p],(20,20)),((Chars.fallspeeds[p]-0.25)/1.25*250+30,10*height/12+15))
                                if abs(fallspeed - Chars.fallspeeds[p]) < 0.03 and (not (convert_inputs(controls[0],joysticks,0)[1] or convert_inputs(controls[0],joysticks,0)[0]) or focusedbutton != 7):
                                    fallspeed = Chars.fallspeeds[p]
                                    equal.append(p)
                            if equal :
                                txt = ""
                                for e in equal :
                                    txt += e + "/"
                                Texte(f"({txt[:-1]})",("Arial",15,False,False),(0,0,0),150,10*height/12-10).draw(window)
                            Bouton.draw(window)

                            Texte(f"Vitesse de Fastfall : {round(fastfallspeed,1)}",("Arial",20,True,False),(0,0,0),150,11*height/12-25).draw(window)
                            pygame.draw.rect(window,(10,10,10),(40,11*height/12+3,254,4))
                            Bouton = Button(f"",("Arial",20,False,False),"./DATA/Images/Menu/Slider.png",(fastfallspeed-0.5)/1.5*250+40,11*height/12+5,12,12)
                            if focusedbutton == 8 :
                                Bouton.changeImage("./DATA/Images/Menu/Slider_focused.png")
                                if convert_inputs(controls[0],joysticks,0)[1] :
                                    fastfallspeed += 0.05
                                    if fastfallspeed > 2 :
                                        fastfallspeed = 2
                                if convert_inputs(controls[0],joysticks,0)[0] :
                                    fastfallspeed -= 0.05
                                    if fastfallspeed < 0.5 :
                                        fastfallspeed = 0.5
                            equal = []
                            for p in Chars.fastfallspeeds :
                                window.blit(pygame.transform.scale(icons[p],(20,20)),((Chars.fastfallspeeds[p]-0.5)/1.5*250+30,11*height/12+15))
                                if abs(fastfallspeed - Chars.fastfallspeeds[p]) < 0.03 and (not (convert_inputs(controls[0],joysticks,0)[1] or convert_inputs(controls[0],joysticks,0)[0]) or focusedbutton != 8):
                                    fastfallspeed = Chars.fastfallspeeds[p]
                                    equal.append(p)
                            if equal :
                                txt = ""
                                for e in equal :
                                    txt += e + "/"
                                Texte(f"({txt[:-1]})",("Arial",15,False,False),(0,0,0),150,11*height/12-10).draw(window)
                            Bouton.draw(window)

            pygame.display.flip()
            clock.tick(60)  # FPS (à régler sur 60)


    except:
        traceback.print_exc()

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
