############################################################################################################
####################################### Importation de Bibliothèques #######################################
############################################################################################################

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
from DATA.utilities.commands import *
from random import randint
from DATA.utilities.Sound_manager import musicvolume, playsound,soundvolume
import DATA.utilities.Sound_manager

import time

############################################################################################################
############################################## Initialisation ##############################################
############################################################################################################

pygame.init()  # Initialisation de pygame
clock = pygame.time.Clock()  # Horloge

pygame.joystick.init()  # Initialisation des manettes
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

for j in joysticks:
    j.init()

pygame.mixer.init() # Initialisation du module de musique

############################################################################################################
############################################################################################################


def main():
    """"""""""""""""""""""""""""""""""""
    """""""""Progamme Principal"""""""""
    """"""""""""""""""""""""""""""""""""

    # création de la fenêtre
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

        ################################################################################################################

        """ Déclaration des variables """

        # Noms des personnages et des stages
        chars = Chars.chars
        stages = Stages.stages
        # Config des musiques
        musics = Stages.musics
        musicplaying = False

        # Variables de gestion du jeu et du menu
        Menu = "title"
        Play = False
        focusedbutton = 0 # numéro de bouton
        row = 0 # numéro de colonne (menu)
        confirm = False # permet de ne pas détecter la confirmation du menu plusieurs frames à la suite
        commandconfig = None # gestion des configs de commandes
        getting = list() # gestion des inputs multiples pour les commandes

        # Gestion de la fumee de hitstun
        smoke = list()
        smokeframe  = 0

        # gestion de la pause
        pause = False
        hold_pause = False



        # Training
        TrainingHDI = 0
        TrainingVDI = 0
        Tech = 0

        # Gestion de la fin de la partie
        stock = [0,0]
        time_game = 0
        begin_game = 0
        pause_time = 0
        game_running = -1

        # Animation de l'ecran titre
        titleframe = 0
        titleanimation = [pygame.transform.scale(pygame.image.load(f"DATA/Images/Logo/{i}.png"),(512,512)) for i in range(37)]

        ################################################################################################################       

        pygame.mixer.music.load("DATA/Musics/BGM/intro_2.mp3") # musique de l'écran titre
        pygame.mixer.music.play()
        global musicvolume
        global soundvolume


        ################################################################################################################       

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""   INSTRUCTIONS   """""""""""""""""""""
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""


        # Boucle du programme
        while run:
            # actualisation du volum
            pygame.mixer.music.set_volume(musicvolume)
            # gestion de répétition des touches lorsqu'elles sont maintenues (toutes les 10 frames)
            actualize_repeating()

            ##########################################  Ecran titre  ##########################################

            if Menu == "title" :
                window.fill((0x99,0x55,0x99)) # Arrière plan
                pygame.draw.rect(window,(60,60,60),(0,0,width,128))
                pygame.draw.rect(window,(60,60,60),(0,height-128,width,128))
                # Affichage de la version
                Texte("1.0.0 beta",("Arial",15,True,True),(0,0,0),100,64,format_="left").draw(window)
                
                key = "A" if controls[0] == commands["Menu"] else "Espace"
                Texte(f"Appuyez sur {key}",("Arial black",50,True,False),(0,0,0),width/2,height-64).draw(window)
                #window.blit(pygame.transform.scale(pygame.image.load("./DATA/Images/logo.png"),(512,512)),(width/2-256,height/2-256-64))
                window.blit(titleanimation[titleframe//2],(width/2-256,height/2-256-64))
                Texte("OCTOGONE",("Comic",128,True,False),(40,40,40),width/2+5,height/2 + 256+5).draw(window)
                Texte("OCTOGONE",("Comic",128,True,False),(128,0,128),width/2,height/2 + 256).draw(window)
                if convert_inputs(controls[0],joysticks,0)[6] :
                    confirm = True
                    Menu = "main"
                titleframe = min(titleframe+1,72)

            ###################################################################################################

            else :
                window.fill((0x66,0x22,0x66)) # Remplissage de l'arrière-plan

            # Récupération des events
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT: # Bouton croix en haut à droite de l'écran
                    run = False

            if not Play :
        
                # Musique du menu
                if not musicplaying and Menu != "title":
                    if Menu == "credits":
                        pygame.mixer.music.load("DATA/Musics/BGM/intro_.mp3")
                    else:
                        pygame.mixer.music.load("DATA/Musics/BGM/menu.mp3")
                    pygame.mixer.music.play(-1)
                    musicplaying = True
                
                if not convert_inputs(controls[0],joysticks,0)[6]:
                    confirm = False

                ##########################################  Menu Principal  ##########################################

                if Menu == "main":
                    # inputs haut et bas pour se déplacer dans le menu
                    if input_but_no_repeat(3,controls,joysticks,0):
                        focusedbutton += 1
                        
                    if input_but_no_repeat(2,controls,joysticks,0):
                        focusedbutton -= 1
                        
                    focusedbutton = ((focusedbutton+1)%4)-1

                    # Bouton "Combat"
                    Bouton = Button("Combat",("arial",50,True,False),"./DATA/Images/Menu/Button.png",width/2,height/8,250,100)
                    if focusedbutton == 0:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                            Menu = "stage"
                            training = False
                            focusedbutton = 0
                            confirm = True
                    Bouton.draw(window)

                    # Bouton "Pandaball"
                    Bouton = Button("",("arial",45,True,False),"./DATA/Images/Menu/Button.png",width/2,2*height/8,250,100)
                    if focusedbutton == 1:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                            Menu = "stage"
                            training = True
                            focusedbutton = 0
                            confirm = True
                    Bouton.draw(window)
                    Texte("Pandaball",("arial",45,True,False),(0,0,0),width/2,2*height/8-20).draw(window)
                    Texte("(Entraînement)",("arial",30,True,False),(0,0,0),width/2,2*height/8+20).draw(window)

                    # Bouton "Paramètres"
                    Bouton = Button("Paramètres",("arial",50,True,False),"./DATA/Images/Menu/Button.png",width/2,3*height/8,250,100)
                    if focusedbutton == 2:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                            Menu = "settings"
                            focusedbutton = 0
                            confirm = True
                    Bouton.draw(window)

                    # Bouton "Credits"
                    Bouton = Button("Credits",("arial",40,True,False),"./DATA/Images/Menu/Button.png",width/4,7*height/8,120,80)
                    if focusedbutton == -1:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                            Menu = "credits"
                            musicplaying = False
                            confirm = True
                    Bouton.draw(window)

                ######################################################################################################
                ##########################################  Menu paramètres  ##########################################

                if Menu == "settings":
                    # inputs haut et bas pour se déplacer dans le menu
                    if input_but_no_repeat(3,controls,joysticks,0):
                        focusedbutton += 1
                        
                    if input_but_no_repeat(2,controls,joysticks,0):
                        focusedbutton -= 1
                        
                    focusedbutton = focusedbutton%3

                    # Bouton "Paramètres audio"
                    Bouton = Button("Paramètres audio",("arial",50,True,False),"./DATA/Images/Menu/Button.png",width/2,height/3,600,100)
                    if focusedbutton == 0:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                            Menu = "musics"
                            oldmusicvolume = musicvolume
                            oldsoundvolume = soundvolume
                            focusedbutton = 0
                            confirm = True
                    Bouton.draw(window)

                    # Bouton "Controles"
                    Bouton = Button("Configuration des contrôles",("arial",50,True,False),"./DATA/Images/Menu/Button.png",width/2,2*height/3,600,100)
                    if focusedbutton == 1:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                            Menu = "commands"
                            focusedbutton = 0
                            confirm = True
                    Bouton.draw(window)

                    # Retour
                    Bouton = Button("<--",("arial",50,True,False),"./DATA/Images/Menu/Button.png",100,850,100,60)
                    if focusedbutton == 2:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                            Menu = "main"
                            confirm = True
                    Bouton.draw(window)

                ######################################################################################################
                ##########################################  Menu commandes  ##########################################

                if Menu == "musics":
                    # inputs haut et bas pour se déplacer dans le menu
                    if input_but_no_repeat(3,controls,joysticks,0):
                        focusedbutton += 1
                        
                    if input_but_no_repeat(2,controls,joysticks,0):
                        focusedbutton -= 1
                        
                    focusedbutton = focusedbutton%4

                    #### Musique 

                    Texte(f"Volume musique : {round(musicvolume*100)}%",("Arial",20,True,False),(0,0,0),width/2,height/3-25).draw(window)
                    pygame.draw.rect(window,(10,10,10),(width/2-122,height/3,254,4))
                    Bouton = Button(f"",("Arial",20,False,False),"./DATA/Images/Menu/Slider.png",(musicvolume)*250+width/2-125,height/3,12,12)
                    if focusedbutton == 0 :
                        # Compris entre 0.5 et 1
                        Bouton.changeImage("./DATA/Images/Menu/Slider_focused.png")
                        if convert_inputs(controls[0],joysticks,0)[1] :
                            musicvolume += 0.01
                            if musicvolume > 1 :
                                musicvolume = 1
                        if convert_inputs(controls[0],joysticks,0)[0] :
                            musicvolume -= 0.01
                            if musicvolume < 0 :
                                musicvolume = 0
                    Bouton.draw(window)

                    #### Sons 

                    Texte(f"Volume sons : {round(soundvolume*100)}%",("Arial",20,True,False),(0,0,0),width/2,2*height/3-25).draw(window)
                    pygame.draw.rect(window,(10,10,10),(width/2-122,2*height/3,254,4))
                    Bouton = Button(f"",("Arial",20,False,False),"./DATA/Images/Menu/Slider.png",(soundvolume)*250+width/2-125,2*height/3,12,12)
                    if focusedbutton == 1 :
                        # Compris entre 0.5 et 1
                        Bouton.changeImage("./DATA/Images/Menu/Slider_focused.png")
                        if convert_inputs(controls[0],joysticks,0)[1] :
                            soundvolume += 0.01
                            if soundvolume > 1 :
                                soundvolume = 1
                            if round(soundvolume,1) == round(soundvolume,2):
                                playsound("DATA/Musics/SE/hits and slap/8bit hit.mp3")
                        if convert_inputs(controls[0],joysticks,0)[0] :
                            soundvolume -= 0.01
                            if soundvolume < 0 :
                                soundvolume = 0
                            if round(soundvolume,1) == round(soundvolume,2):
                                playsound("DATA/Musics/SE/hits and slap/8bit hit.mp3")
                        # Raffraichissement du volume du module qui exécute les sons
                        DATA.utilities.Sound_manager.soundvolume = soundvolume
                    Bouton.draw(window)

                    # Sauvegarder
                    Bouton = Button("Sauvegarder",("arial",40,True,False),"./DATA/Images/Menu/Button.png",150,750,200,60)
                    if focusedbutton == 2:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                            with open("DATA/utilities/Settings.txt","w") as settings :
                                settings.write(f"Music :\nmusicvolume={round(musicvolume,2)}\nsoundvolume={round(soundvolume,2)}\n")
                            Menu = "settings"
                            confirm = True
                    Bouton.draw(window)

                    # Annuler
                    Bouton = Button("Annuler",("arial",40,True,False),"./DATA/Images/Menu/Button.png",150,850,200,60)
                    if focusedbutton == 3:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                            soundvolume = oldsoundvolume
                            musicvolume = oldmusicvolume
                            DATA.utilities.Sound_manager.soundvolume = soundvolume
                            Menu = "settings"
                            confirm = True
                    Bouton.draw(window)


                ######################################################################################################
                ##########################################  Menu commandes  ##########################################

                if Menu == "commands":

                    #### Aucun profil sélectionné

                    if commandconfig is None:
                        # Haut/Bas pour se déplacer dans le menu
                        if input_but_no_repeat(3,controls,joysticks,0):
                            focusedbutton += 1
                            
                        if input_but_no_repeat(2,controls,joysticks,0):
                            focusedbutton -= 1
                        # bouclage du bouton
                        focusedbutton = (focusedbutton+2)%(len(commands)-1)-2
                        # liste des commandes
                        for i,n in enumerate(commands) :
                            # on ne paramètre pas les configurations par défaut et du menu
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

                        # Ajout d'un profil
                        Bouton = Button("+",("arial",50,True,False),"./DATA/Images/Menu/Button.png",100,800,50,50)
                        if focusedbutton == -2:
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                commandconfig = 0
                                name = "Player"
                                confirm = True
                        Bouton.draw(window)

                        # Retour
                        Bouton = Button("<--",("arial",50,True,False),"./DATA/Images/Menu/Button.png",100,850,100,60)
                        if focusedbutton == -1:
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                Menu = "settings"
                                confirm = True
                        Bouton.draw(window)

                    #### Création d'un nouveau profil

                    elif commandconfig == 0:
                        # entrée texte pour créer le nom
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

                    #### Modification d'un profil

                    else :
                        if inputget <= -1 :
                            # Haut/Bas/Gauche/Droite pour naviguer dans le menu
                            if input_but_no_repeat(3,controls,joysticks,0):
                                focusedbutton += 1
                                
                            if input_but_no_repeat(2,controls,joysticks,0):
                                focusedbutton -= 1
                                
                            if input_but_no_repeat(0,controls,joysticks,0):
                                row -= 1
                                
                            if input_but_no_repeat(1,controls,joysticks,0):
                                row += 1
                        # Bouclage de la sélection selon la colonne (donc le nombre de boutons dans la colonne)
                        if row == 0 :
                            focusedbutton = ((focusedbutton+1)%5)-1
                        if row == 1 :
                            focusedbutton = ((focusedbutton+1)%6)-1
                        if row == 2 :
                            focusedbutton = ((focusedbutton+1)%5)-1
                        if row == 3 :
                            focusedbutton = ((focusedbutton+1)%6)-1
                        row = row%4 # bouclage de la colonne

                        # Paramétrage des inputs
                        if inputget > -1:
                            
                            # attente de l'input
                            if get_controler_input(events,joysticks) and not confirm:
                                add = get_controler_input(events,joysticks)
                                for i in add :
                                    if i not in getting :
                                        getting.append(i)
                            # enregistrement de l'input
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
                        # Sauvegarde
                        Bouton = Button("Sauvegarder",("arial",50,True,False),"./DATA/Images/Menu/Button.png",200,850,250,60)
                        if focusedbutton == -1 and row%2 == 0:
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                with open("./DAT/utilities/commands.py","w") as commandfile :
                                    commandfile.write("commands = {\n")
                                    for k in commands :
                                        commandfile.write(f'\t"{k}":{commands[k]},\n')
                                    commandfile.write("}")

                                commandconfig = None
                                confirm = True
                        Bouton.draw(window)

                        # Suppression
                        Bouton = Button("Supprimer",("arial",50,True,False),"./DATA/Images/Menu/Button.png",1450,850,200,60)
                        if focusedbutton == -1 and row%2 == 1:
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                del commands[commandconfig]
                                with open("./DATA/utilities/commands.py","w") as commandfile :
                                    commandfile.write("commands = {\n")
                                    for k in commands :
                                        commandfile.write(f'\t"{k}":{commands[k]},\n')
                                    commandfile.write("}")

                                commandconfig = None
                                confirm = True
                        Bouton.draw(window)
                            
                ######################################################################################################
                ############################################  Menu stage  ############################################


                if Menu == "stage":
                    # ajout du pandadrome (terrain d'entraînement)
                    if training :
                        actualstages = ["Pandadrome"] + stages
                    else :
                        actualstages = stages
                    # haut/bas/gauche/droite pour naviguer dans le menu
                    if input_but_no_repeat(3,controls,joysticks,0):
                        focusedbutton += 9
                        
                    if input_but_no_repeat(2,controls,joysticks,0):
                        focusedbutton -= 9
                        
                    if input_but_no_repeat(0,controls,joysticks,0):
                        focusedbutton -= 1
                        
                    if input_but_no_repeat(1,controls,joysticks,0):
                        focusedbutton += 1
                        
                    # bouclage de la navigation
                    focusedbutton = ((focusedbutton+1)%(len(actualstages)+1))-1

                    # retour
                    Bouton = Button("<--",("arial",50,True,False),"./DATA/Images/Menu/Button.png",100,850,100,60)
                    if focusedbutton == -1:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                            Menu = "main"
                            confirm = True
                    else :
                        # Affichage du nom du stage sélectionné
                        Texte(actualstages[focusedbutton],("arial",50,True,False),(0,0,0),30,height//2,format_="left").draw(window)
                    Bouton.draw(window)

                    # Boutons de sélection du stage
                    for i in range(len(actualstages)):
                        Bouton = Button("",("arial",50,True,False),"./DATA/Images/Menu/Button.png",((i%9)*150)+250,(i//9*150)+100,100,100)
                        if focusedbutton == i :
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")

                            # setup du mennu personnage
                            if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                Menu = "char"
                                stage = i
                                scroll1 = 0 # permet un scroll continu
                                scroll2 = 0
                                selectchar_1 = 0 # numéro du personnage sélectionné
                                selectchar_2 = 0
                                selected_1 = False # le joueur a-t-il choisi ?
                                selected_2 = False
                                # sens dans lequel le joueur défile les noms (gestion de la compatibilité entre la configuration et la manette)
                                movename1 = -1
                                movename2 = -1
                                names = [0,0] # numéro des configurations
                                namelist = [k for k in commands] # nom des configurations
                                namelist.pop(0)
                                b = 0 # temps de maintien du bouton B pour le retour
                                confirm = True
                        Bouton.draw(window)
                        # image du stage
                        window.blit(pygame.transform.scale(pygame.image.load(f"./DATA/Images/Stages/{actualstages[i]}/{actualstages[i]}.png"),(90,90)),((i%9*150)+205,(i//9*150)+55))
                            
                ######################################################################################################
                #########################################  Menu personnages  #########################################

                if Menu == "char":
                    # retour
                    Bouton = Button("",("arial",30,True,False),"./DATA/Images/Menu/Button.png",width/2,40,100,60)
                    # le retour se fait en maintenant le bouton B
                    if not convert_inputs(controls[0],joysticks,0)[7]: 
                        b = 0
                    else :
                        b += 1
                    if b > 0:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                    if b >= 10:
                        Menu = "stage"
                    Bouton.draw(window)
                    Texte("<--",("arial",30,True,False),(0,0,0),width/2,25).draw(window)
                    Texte("(B)",("arial",30,True,False),(0,0,0),width/2,50).draw(window)


                    ### Interface personnages P1
                    for i in range(len(chars)):
                        # Roulette
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
                        # icones sur la roulette
                        window.blit(icons64[chars[i]],(64,105*(i-scroll1+4)-32))
                        window.blit(icons64[chars[i]],(64,105*(i-scroll1+4-len(chars))-32))
                        window.blit(icons64[chars[i]],(64,105*(i-scroll1+4+len(chars))-32))

                    # Haut/Bas pour choisir un personnage
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
                    # scroll continu
                    if round(scroll1,1) < selectchar_1 :
                        scroll1 += 0.25
                        scroll1 = round(scroll1,3)
                    if round(scroll1,1) > selectchar_1 :
                        scroll1 -= 0.25
                        scroll1 = round(scroll1,3)
                    if round(scroll1,1) == selectchar_1 :
                        scroll1 = selectchar_1

                    # Confirmation / Annulation
                    if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                        selected_1 = True
                    if convert_inputs(controls[0],joysticks,0)[7]:
                        selected_1 = False

                    ### Interface personnages P2
                    if training :
                        # Pandapluche (Peluche Panda des A-L)
                        Bouton = Button("",("arial",50,True,False),standard,width,height/2,384,100)
                        Bouton.draw(window)
                        window.blit(pygame.transform.scale(pygame.image.load("./DATA/Images/Sprites/Misc/Training/Training_icon.png"),(64,64)),(width-128,height/2-32))
                    else :
                        for i in range(len(chars)):
                            # Roulette
                            Bouton = Button("",("arial",50,True,False),standard,width,105*(i-scroll2-len(chars)+4),384,100)
                            Bouton.draw(window)
                            Bouton = Button("",("arial",50,True,False),standard,width,105*(i-scroll2+len(chars)+4),384,100)
                            Bouton.draw(window)
                            Bouton = Button("",("arial",50,True,False),standard,width,105*(i-scroll2+4),384,100)
                            if selectchar_2 == i :
                                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                                Bouton.resize(400,100)
                            Bouton.draw(window)
                        for i in range(len(chars)):
                            # Icones de la roulette
                            window.blit(icons64[chars[i]],(width-128,105*(i-scroll2+4)-32))
                            window.blit(icons64[chars[i]],(width-128,105*(i-scroll2+4-len(chars))-32))
                            window.blit(icons64[chars[i]],(width-128,105*(i-scroll2+4+len(chars))-32))

                        # Haut/Bas pour choisir un personnage
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
                        # scroll continu
                        if round(scroll2,1) < selectchar_2 :
                            scroll2 += 0.25
                            scroll2 = round(scroll2,3)
                        if round(scroll2,1) > selectchar_2 :
                            scroll2 -= 0.25
                            scroll2 = round(scroll2,3)
                        if round(scroll2,1) == selectchar_2 :
                            scroll2 = selectchar_2

                        # Confirmation / Annulation
                        if convert_inputs(controls[1],joysticks,1)[6] and not confirm:
                            selected_2 = True
                        if convert_inputs(controls[1],joysticks,1)[7]:
                            selected_2 = False

                    # Choix du nom
                    if names[0] == 0 :
                        text = "Player 1"
                    else :
                        text = namelist[names[0]]
                    Bouton = Button(text,("arial",24,True,False),"./DATA/Images/Menu/Button.png",3*width/10,height-150,200,32)
                    Bouton.draw(window)
                    # Test de compatibilité entre le nom et la manette
                    try :
                        convert_inputs(commands[namelist[names[0]]],joysticks,0)
                    except :
                        names[0] += movename1
                        if names[0] >= len(namelist):
                            names[0] = 0
                    # Choix du nom avec les gâchettes
                    if input_but_no_repeat(10,controls,joysticks,0):
                        names[0] += 1
                        movename1 = 1
                        if names[0] == 1 : # Configuration du menu
                            names[0] += 1
                        if names[0] >= len(namelist):
                            names[0] = 0
                    if input_but_no_repeat(9,controls,joysticks,0):
                        names[0] -= 1
                        movename1 = -1
                        if names[0] == 1 : # Configuration du menu
                            names[0] -= 1
                        if names[0] < 0:
                            names[0] = len(namelist)-1

                    # Choix du nom
                    if names[1] == 0 :
                        text = "Player 2"
                    else :
                        text = namelist[names[1]]
                    Bouton = Button(text,("arial",24,True,False),"./DATA/Images/Menu/Button.png",7*width/10,height-150,200,32)
                    Bouton.draw(window)
                    # Test de compatibilité entre le nom et la manette
                    try :
                        convert_inputs(commands[namelist[names[1]]],joysticks,1)
                    except :
                        names[1] += movename2
                        if names[1] >= len(namelist):
                            names[1] = 0
                    # Choix du nom avec les gâchettes
                    if input_but_no_repeat(10,controls,joysticks,1):
                        names[1] += 1
                        movename2 = 1
                        if names[1] == 1 : # Configuration du menu
                            names[1] += 1
                        if names[1] >= len(namelist):
                            names[1] = 0
                    if input_but_no_repeat(9,controls,joysticks,1):
                        names[1] -= 1
                        movename2 = -1
                        if names[1] == 1 : # Configuration du menu
                            names[1] -= 1
                        if names[1] < 0:
                            names[1] = len(namelist)-1

                    # Affichage si le joueur est prêt
                    if selected_1 :
                        pygame.draw.rect(window,(230,230,230),(width/8,height-120,width/4,30))
                        Texte("PRET",("arial",24,True,False),(0,0,0),width/4,height-110,format_="center").draw(window)
                    if selected_2 :
                        pygame.draw.rect(window,(230,230,230),(5*width/8,height-120,width/4,30))
                        Texte("PRET",("arial",24,True,False),(0,0,0),3*width/4,height-110,format_="center").draw(window)
                    
                    ## Affichage des noms
                    pygame.draw.rect(window,(200,200,200),(0,height-90,width,90))
                    Texte(str(Chars.charobjects[chars[selectchar_1]](0,0,0)),("arial",64,True,False),(0,0,0),width/2-30,height-50,format_="right").draw(window)
                    if training :
                        Texte("Pandapluche",("arial",64,True,False),(0,0,0),width/2+30,height-50,format_="left").draw(window)
                    else :
                        Texte(str(Chars.charobjects[chars[selectchar_2]](0,0,0)),("arial",64,True,False),(0,0,0),width/2+30,height-50,format_="left").draw(window)
                    Texte("|",("arial",80,True,False),(0,0,0),width/2,height-50,format_="center").draw(window)
                    ##

                    #### Démarrage de la partie
                    if (selected_2 or training) and selected_1 :
                        # Jeu clavier
                        if names[0] == 0 and controls[0] == commands["DefaultKeyboard"]:
                            names[0] = 1
                        if names[1] == 0 and controls[1] == commands["DefaultKeyboard"]:
                            names[1] = 1
                        Play = True
                        Menu = "stage"

                        ### Création des objets parsonnages
                        Char_P1 = Chars.charobjects[chars[selectchar_1]](-350,0,0)

                        if training :
                            Char_P2 = Chars.Training(0,0,1)
                            # gestion des statistiques en entreînement
                            basedamages = 0
                            airspeed=1.25
                            deceleration=0.75
                            fallspeed=0.85
                            fastfallspeed=1.25
                        else :
                            Char_P2 = Chars.charobjects[chars[selectchar_2]](350,0,1)
                        ###

                        # initialisation des vies et du temps
                        stock = [7,7]
                        time_game = 7*60
                        begin_game = time.time()
                        pause_time = 0
                        pausefrom = 0
                        game_running = -1

                        # conversion des contrôles
                        controls = [commands[namelist[names[0]]],commands[namelist[names[1]]]]

                        # importation de l'arrière-plan et de la musique
                        background = pygame.transform.scale(pygame.image.load(f"./DATA/Images/Stages/{actualstages[stage]}/{actualstages[stage]}.png"),(1600,900))
                        for m in musics :
                            if m[1] == actualstages[stage] and (str(Char_P1) == m[2] or str(Char_P2) == m[2] or m[2] == True):
                                currentmusic = m[0]
                        musicplaying = False
                        # création du stage
                        stage = Stages.create_stage(actualstages[stage])

                ##########################################  Credits  ##########################################

                if Menu == "credits":
                    Texte("CREDITS",("Arial",55,True,False),(0,0,0),width/2,50).draw(window)

                    Texte("Game Director :",("Arial",40,True,False),(0,0,0),width/3,height/6,format_="left").draw(window)
                    Texte("Elsa RUFFIN",("Arial",40,False,False),(0xBC,0x79,0xE4),2*width/3,height/6).draw(window)
                    
                    Texte("Graphismes :",("Arial",40,True,False),(0,0,0),width/3,2*height/6,format_="left").draw(window)
                    Texte("Loic JERMAN",("Arial",40,False,False),(0x50,0x50,0xFF),2*width/3,2*height/6-50).draw(window)
                    Texte("Elsa RUFFIN",("Arial",40,False,False),(0xBC,0x79,0xE4),2*width/3,2*height/6).draw(window)
                    Texte("Nicolas VINCENT",("Arial",40,False,False),(0x80,0x80,0x80),2*width/3,2*height/6+50).draw(window)
                    
                    Texte("Musiques & Sons :",("Arial",40,True,False),(0,0,0),width/3,3*height/6,format_="left").draw(window)
                    Texte("Iwan DEROUET",("Arial",40,False,False),(0xF0,0xF0,0x20),2*width/3,3*height/6).draw(window)
                    
                    Texte("Programmation :",("Arial",40,True,False),(0,0,0),width/3,4*height/6,format_="left").draw(window)
                    Texte("Iwan DEROUET",("Arial",40,False,False),(0xF0,0xF0,0x20),2*width/3,4*height/6-25).draw(window)
                    Texte("Nicolas VINCENT",("Arial",40,False,False),(0x80,0x80,0x80),2*width/3,4*height/6+25).draw(window)
                    
                    Texte("Chara-design :",("Arial",40,True,False),(0,0,0),width/3,5*height/6,format_="left").draw(window)
                    Texte("Elsa RUFFIN",("Arial",40,False,False),(0xBC,0x79,0xE4),2*width/3,5*height/6-25).draw(window)
                    Texte("Nicolas VINCENT",("Arial",40,False,False),(0x80,0x80,0x80),2*width/3,5*height/6+25).draw(window)

                    # retour
                    Bouton = Button("<--",("arial",50,True,False),"./DATA/Images/Menu/Button_focused.png",100,850,100,60)
                    if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                        Menu = "main"
                        confirm = True
                        musicplaying = False
                    Bouton.draw(window)

                ######################################################################################################
                ########################################  Ecran de résultats  ########################################

                if Menu == "results":
                    # réinitialisation des contrôles
                    if len(joysticks) > 1 :
                        controls = [commands["Menu"],commands["Menu"]]
                    elif len(joysticks) > 0 :
                        controls = [commands["Menu"],commands["DefaultKeyboard"]]
                    else :
                        controls = [commands["DefaultKeyboard"],commands["DefaultKeyboard"]]
                    Menu = "stage"
        
            ######################################################################################################
            ############################################  En  combat  ############################################

            else :

                # musique
                if not musicplaying :
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(currentmusic)
                    pygame.mixer.music.play(-1)
                    musicplaying = True

                # Réinitialisation de l'écran à chaque frame
                window.fill((255, 255, 255)) 
                window.blit(background,(0,0))

                # Recuperation des touches
                if game_running < 0 and (convert_inputs(controls[0],joysticks,0)[-1] or convert_inputs(controls[1],joysticks,1)[-1]):
                    if not hold_pause:
                        pause = not pause
                        hold_pause  = True
                else :
                    hold_pause = False

                # hors pause, si le jeu continue
                if game_running < 0 and not pause:
                    pausefrom = time.time() # gestion du chrono en pause
                    

                    #### récupération des inputs du joueur 1

                    inputs_1 = convert_inputs(controls[0],joysticks,0)[0:-1]
                    if not (inputs_1[4] or inputs_1[5]): # gestion du saut
                        Char_P1.jumping = False

                    # Transmission des inputs à l'objet Palyer 1
                    Char_P1.act(inputs_1, stage, Char_P2,not(pause or Char_P1.BOUM or Char_P2.BOUM))
                    if Char_P1.die == 30 and not training:
                        stock[0] -= 1


                    ####  récupération des inputs du joueur 2

                    inputs_2 = convert_inputs(controls[1],joysticks,1)[0:-1]
                    if not (inputs_2[4] or inputs_2[5]): # gestion du saut
                        Char_P2.jumping = False

                    if training :
                        ################### Gestion de la DI et de la tech en entraînement ###################
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
                        ######################################################################################
                    else :
                        # Transmission des inputs à l'objet Palyer 2
                        Char_P2.act(inputs_2, stage, Char_P1,not(pause or Char_P1.BOUM or Char_P2.BOUM))
                    if Char_P2.die == 30 and not training:
                        stock[1] -= 1
                    ########

                    # détection des collision
                    Char_P2.collide(Char_P1)
                    Char_P1.collide(Char_P2)

                elif pause :
                    pause_time += time.time() - pausefrom # gestion du chrono en pause
                    pausefrom = time.time()
                    Texte(f"Pause",("Arial",60,False,False),(0,0,0),width//2,height//2,800).draw(window)

                ################### Affichage des éléments ###################

                ### Debug
                for h in Char_P1.active_hitboxes:
                    h.draw(window)
                for h in Char_P2.active_hitboxes:
                    h.draw(window)
                #########

                # Fumée de hitstun
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
                
                # Affichage du stage
                stage.draw(window)

                # Affichage des personnages
                Char_P2.draw(window)
                Char_P1.draw(window)

                # Affichage des degats
                Char_P1.damages = float(Char_P1.damages)
                Texte(f"{str(round(Char_P1.damages,2)).split('.')[0]}  %",("Arial",60,False,False),(255-(Char_P1.damages/5),max(255-Char_P1.damages,0),max(255-Char_P1.damages*2,0)),width//3,height-50,800,format_="left").draw(window)
                Texte(f".{str(round(Char_P1.damages,2)).split('.')[1]}",("Arial",30,False,False),(255-(Char_P1.damages/5),max(255-Char_P1.damages,0),max(255-Char_P1.damages*2,0)),width//3+len(str(round(Char_P1.damages,2)).split('.')[0])*25,height-30,800,format_="left").draw(window)
                
                Char_P2.damages = float(Char_P2.damages)
                Texte(f"{str(round(Char_P2.damages,2)).split('.')[0]}  %",("Arial",60,False,False),(255-(Char_P2.damages/5),max(255-Char_P2.damages,0),max(255-Char_P2.damages*2,0)),2*width//3,height-50,800,format_="left").draw(window)
                Texte(f".{str(round(Char_P2.damages,2)).split('.')[1]}",("Arial",30,False,False),(255-(Char_P2.damages/5),max(255-Char_P2.damages,0),max(255-Char_P2.damages*2,0)),2*width//3+len(str(round(Char_P2.damages,2)).split('.')[0])*25,height-30,800,format_="left").draw(window)
                
                # Affichage des vies
                if not training :
                    for s in range(stock[0]//5+1): # colonnes de 5 icones à côté des dégâts
                        for k in range(min(stock[0]-5*s,5)):
                            window.blit(pygame.transform.scale(icons[Char_P1.name],(16,16)),(width/3-25-20*s,height - 40 - 20*k))

                    for s in range(stock[1]//5+1):
                        for k in range(min(stock[1]-5*s,5)):
                            window.blit(pygame.transform.scale(icons[Char_P2.name],(16,16)),(2*width/3-25-20*s,height - 40 - 20 * k))

                #########################################################

                ###################### Gestion de la fin de la partie ######################
                if not training :
                    s = time_game+(begin_game-time.time()) + pause_time # calcul du temps restant
                    ms = str(round(s*100)/100).split(".")[1]
                    if len(ms) == 1 :
                        ms = ms+"0"
                    s = str(round(s*100)/100).split(".")[0]
                    m = int(s)//60
                    s = int(s) - m*60
                    # affichage du temps restant
                    if m*60+s > 0 and game_running < 0:
                        if m*60+s > 5 :
                            Texte(f"{str(m)}:{str(s)}'{str(ms)}",("Arial",60,True,False),(255,255,255),width/2,75).draw(window)
                        else :
                            Texte(f"{str(s)}",("Arial",180,True,False),(100,0,0),width/2,height/2).draw(window)

                    # fin de la partie
                    if (m*60+s < 1 or min(stock) <= 0) and game_running < 0 :
                        game_running = 180 # attente de 3 secondes
                        pygame.mixer.music.stop()
                    if game_running > 0 :
                        Texte("FIN DU MATCH",("Arial",200,True,False),(150,0,0),width/2,height/2).draw(window)
                        game_running -= 1
                        if game_running < 1 :
                            Play = False
                            musicplaying = False
                            Menu = "results"
                

                ############################################ Interface Entraînement ############################################

                if training :
                    # Combo counter
                    pygame.draw.rect(window,(250,250,250),(width-120,height/2,120,60))
                    Texte(str(Char_P2.combo),("Arial",40,False,False),(0,0,0),width-80,height/2+25).draw(window)
                    pygame.draw.rect(window,(250,250,250),(width-120,height/2+75,120,60))
                    Texte(str(round(Char_P2.combodamages,2))+"%",("Arial",40,False,False),(0,0,0),width-80,height/2+100).draw(window)

                    # Menu
                    if pause :
                        if training :
                            # reset des dégâts
                            Char_P2.damages = basedamages
                            pygame.draw.rect(window,(180,180,180),(0,0,300,height))
                            # gestion de la confirmation
                            if not convert_inputs(controls[0],joysticks,0)[6] :
                                confirm = False
                            # Haut/Bas pour naviguer dans le menu
                            focusedbutton = (focusedbutton+1)%10-1
                            if input_but_no_repeat(2,controls,joysticks,0):
                                focusedbutton -= 1
                                
                            if input_but_no_repeat(3,controls,joysticks,0):
                                focusedbutton += 1
                                
                            # Quitter
                            Bouton = Button(f"Quitter",("Arial",20,False,False),"./DATA/Images/Menu/Button.png",150,height/12,200,60)
                            if focusedbutton == -1 :
                                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                                if convert_inputs(controls[0],joysticks,0)[6] and not confirm :
                                    confirm = True
                                    Menu = "stage"
                                    Play = False
                                    pause = False
                                    focusedbutton = 0
                                    musicplaying = False
                                    stage = 0
                                    # reinitialisation des controles
                                    if len(joysticks) > 1 :
                                        controls = [commands["Menu"],commands["Menu"]]
                                    elif len(joysticks) > 0 :
                                        controls = [commands["Menu"],commands["DefaultKeyboard"]]
                                    else :
                                        controls = [commands["DefaultKeyboard"],commands["DefaultKeyboard"]]
                                    clock.tick(10)
                            Bouton.draw(window)

                            # Bouton réinitialiser
                            Bouton = Button("Réinitialiser",("Arial",40,False,False),"./DATA/Images/Menu/Button.png",150,2.5*height/12,200,60)
                            if focusedbutton == 0 :
                                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                                if convert_inputs(controls[0],joysticks,0)[6] and not confirm:
                                    confirm = True
                                    Char_P2 = Training(0,0,1)
                            Bouton.draw(window)

                            # Bouton de gestion de DI (Horizontale)
                            Bouton = Button(f"DI Horizontale : {['Aucune','Droite','Gauche'][TrainingHDI]}",("Arial",20,False,False),"./DATA/Images/Menu/Button.png",150,3.5*height/12,200,60)
                            if focusedbutton == 1 :
                                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                                if convert_inputs(controls[0],joysticks,0)[6] and not confirm :
                                    confirm = True
                                    TrainingHDI += 1
                                    TrainingHDI = (TrainingHDI+1)%3 - 1
                            Bouton.draw(window)

                            # Bouton de gestion de DI (Verticale)
                            Bouton = Button(f"DI Verticale : {['Aucune','Haut','Bas'][TrainingVDI]}",("Arial",20,False,False),"./DATA/Images/Menu/Button.png",150,4.5*height/12,200,60)
                            if focusedbutton == 2 :
                                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                                if convert_inputs(controls[0],joysticks,0)[6] and not confirm :
                                    confirm = True
                                    TrainingVDI += 1
                                    TrainingVDI = (TrainingVDI+1)%3 - 1
                            Bouton.draw(window)
                            
                            # Bouton de probabilité de tech
                            Bouton = Button(f"Tech : {['Jamais','1/2','Toujours'][Tech]}",("Arial",20,False,False),"./DATA/Images/Menu/Button.png",150,5.5*height/12,200,60)
                            if focusedbutton == 3 :
                                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                                if convert_inputs(controls[0],joysticks,0)[6] and not confirm :
                                    confirm = True
                                    Tech += 1
                                    Tech = (Tech+1)%3 - 1
                            Bouton.draw(window)

                            # Bouton de gestion des dégâts
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

                            ########################### Gestion des statistiques ###########################
                            Texte(f"Caractéristiques :",("Arial black",24,False,False),(0,0,0),150,7.5*height/12-20).draw(window)

                            #### Décélération 

                            Texte(f"Decéleration : {round(deceleration,2)}",("Arial",20,True,False),(0,0,0),150,8*height/12-25).draw(window)
                            pygame.draw.rect(window,(10,10,10),(40,8*height/12+3,254,4))
                            Bouton = Button(f"",("Arial",20,False,False),"./DATA/Images/Menu/Slider.png",(deceleration-0.5)*500+40,8*height/12+5,12,12)
                            if focusedbutton == 5 :
                                # Compris entre 0.5 et 1
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
                            # affichage des équivalents personnages
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

                            #### Vitesse aérienne 

                            Texte(f"Vitesse aérienne : {round(airspeed,1)}",("Arial",20,True,False),(0,0,0),150,9*height/12-25).draw(window)
                            pygame.draw.rect(window,(10,10,10),(40,9*height/12+3,254,4))
                            Bouton = Button(f"",("Arial",20,False,False),"./DATA/Images/Menu/Slider.png",(airspeed-0.5)/1.5*250+40,9*height/12+5,12,12)
                            if focusedbutton == 6 :
                                # Compris entre 0.5 et 2
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
                            # affichage des équivalents personnages
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

                            #### Vitesse de chute 

                            Texte(f"Vitesse de chute : {round(fallspeed,1)}",("Arial",20,True,False),(0,0,0),150,10*height/12-25).draw(window)
                            pygame.draw.rect(window,(10,10,10),(40,10*height/12+3,254,4))
                            Bouton = Button(f"",("Arial",20,False,False),"./DATA/Images/Menu/Slider.png",(fallspeed-0.25)/1.25*250+40,10*height/12+5,12,12)
                            if focusedbutton == 7 :
                                # Compris entre 0.25 et 1.5
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
                            # affichage des équivalents personnages
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

                            #### Vitesse de fastfall 

                            Texte(f"Vitesse de Fastfall : {round(fastfallspeed,1)}",("Arial",20,True,False),(0,0,0),150,11*height/12-25).draw(window)
                            pygame.draw.rect(window,(10,10,10),(40,11*height/12+3,254,4))
                            Bouton = Button(f"",("Arial",20,False,False),"./DATA/Images/Menu/Slider.png",(fastfallspeed-0.5)/1.5*250+40,11*height/12+5,12,12)
                            if focusedbutton == 8 :
                                # Compris entre 0.5 et 2
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
                            # affichage des équivalents personnages
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
                #########################################################

            ######################################################################################################

            pygame.display.flip() # actualisation de l'écran
            clock.tick(60)  # FPS


    except:
        traceback.print_exc()

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
