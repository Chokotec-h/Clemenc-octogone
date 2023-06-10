############################################################################################################
####################################### Importation de Bibliothèques #######################################
############################################################################################################

import pygame
import traceback
import time
import tkinter as tk
from tkinter import messagebox
import sys

from DATA.assets.Chars.Gregoire import Rayon
from DATA.utilities.Menu_Settings import SettingsMenu
from DATA.utilities.Menu_Stages_and_Chars import StagesMenu, CharsMenu
from DATA.utilities.Results import *
import DATA.utilities.SoundSystem as SoundSystem
import DATA.utilities.SoundEventsLibs as SFXEvents
import DATA.assets.CharsLoader as Chars
import DATA.assets.Stages as Stages
import DATA.utilities.Game as GameObject
from DATA.utilities.Interface import *
from DATA.utilities.Entry import TextInput
from DATA.utilities.Gamepad_gestion import *
import DATA.utilities.functions as functions
from DATA.utilities.commands import *
from DATA.utilities.Voicename import *
from DATA.utilities.network import Network
from DATA.utilities.Menu_Stages_and_Chars_Online import *
from DATA.utilities.build import rootDir


############################################################################################################
############################################## Initialisation ##############################################
############################################################################################################

skip_intro = False

pygame.init()  # Initialisation de pygame
clock = pygame.time.Clock()  # Horloge

pygame.joystick.init()  # Initialisation des manettes
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

for j in joysticks:
    j.init()
    print(f"Initializing Joystick {j}")

##########################################################################################################

# L'initialisation des sons a lieu dans Base_char.py

UIDicoEvent = SFXEvents.SFXDicoEvent

embient = SoundSystem.instance()

# print(UIDicoEvent["Voix"])

# 1/0
############################################################################################################

def main():
    """"""""""""""""""""""""""""""""""""
    """""""""Progamme Principal"""""""""
    """"""""""""""""""""""""""""""""""""
    width = functions.width
    height = functions.height
    # création de la fenêtre
    window = pygame.display.set_mode((width, height))
    icon = pygame.image.load(f"{rootDir()}/Images/logo.ico")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("clemenc'octogone", f"{rootDir()}/Images/logo.ico")

    # test de music et de bruitages

    try:
        controls = functions.reset_commands(joysticks, commands)

        # Initialisation des contrôles
        run = True

        ################################################################################################################

        """ Déclaration des variables """

        get = ""

        # Noms des personnages et des stages
        chars = Chars.chars
        # Config des musiques
        musics = Stages.musics
        musicplaying = False

        # Variables de gestion du jeu et du menu
        Menu = "title"
        ip = ""
        Play = False
        focusedbutton = 0  # numéro de bouton
        confirm = False  # permet de ne pas détecter la confirmation du menu plusieurs frames à la suite

        Menu_Settings = SettingsMenu(UIDicoEvent, width, height)
        Menu_Stages = StagesMenu(False, UIDicoEvent)
        Menu_Chars = CharsMenu(False, UIDicoEvent)
        
        online = False

        MenucharsOnline = CharsMenuOnline(False,UIDicoEvent)
        MenustagesOnline = StagesMenuOnline(False,UIDicoEvent)

        # Animation de l'ecran titre
        titleframe = 0
        titleanimation = [
            pygame.transform.scale(pygame.image.load(f"{rootDir()}/Images/Logo/{i}.png"), resize(512, 512, width, height)) for
            i in
            range(37)]

        temp_image = pygame.transform.scale(pygame.image.load(f"{rootDir()}/Images/Menu/Intro.png"), (width, height))
        temp_frames = 0

        ################################################################################################################       

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""   INSTRUCTIONS   """""""""""""""""""""
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        if not skip_intro:
            # Test voix au lancement parce que rigolo
            # UIDicoEvent["Voix"]["Bonus"]["ratage"].play()

            # Intro  #4fun
            while temp_frames < 300:
                events = pygame.event.get()
                for e in events:
                    if e.type == pygame.QUIT:  # Bouton croix en haut à droite de l'écran
                        return
                window.fill((0, 0, 0))
                temp_frames += 2
                if temp_frames < 100:
                    temp_image.set_alpha(temp_frames * 255 / 100)

                if temp_frames > 200:
                    temp_image.set_alpha((300 - temp_frames) * 255 / 100)
                window.blit(temp_image, (0, 0))
                pygame.display.flip()
                SoundSystem.tick_update()
                clock.tick(60)  # FPS
        del temp_frames
        del temp_image

        embient.instance = SoundSystem.play_event("event:/BGM/clemenc'octogone")
        # Boucle du programme
        while run:
            # gestion de répétition des touches lorsqu'elles sont maintenues (toutes les 10 frames)
            functions.actualize_repeating()

            ##########################################  Ecran titre  ##########################################

            if Menu == "title":
                window.fill((0x99, 0x55, 0x99))  # Arrière plan
                pygame.draw.rect(window, (60, 60, 60), (0, 0, width, resize(0, 128, width, height)[1]))
                pygame.draw.rect(window, (60, 60, 60), (
                0, height - resize(0, 128, width, height)[1], width, resize(0, 128, width, height)[1]))
                # Affichage de la version

                Texte("1.4.0 Online", ("Arial", resize(0,32,width,height)[1], True, True), (0, 0, 0), resize(100,0,width,height)[0], resize(0,64,width,height)[1], format_="left").draw(window)

                key = "A" if len(joysticks) > 0 else "Espace"
                if titleframe % 60 < 30:  # Clignotement toutes les demi-secondes
                    Texte(f"Appuyez sur {key}", ("Arial black", resize(0, 50, width, height)[1], True, False),
                          (0, 0, 0), width / 2,
                          height - resize(0, 64, width, height)[1]).draw(window)

                window.blit(titleanimation[round(min(titleframe, 54) / 1.5)], (
                width / 2 - resize(512, 512, width, height)[0] / 2,
                height / 2 - resize(512, 512, width, height)[1] / 2 - resize(64, 64, width, height)[1]))
                Texte("OCTOGONE", ("Comic", resize(0, 128, width, height)[1], True, False), (40, 40, 40), width / 2 + 5,
                      height / 2 + resize(512, 512, width, height)[1] / 2 + 5).draw(window)
                Texte("OCTOGONE", ("Comic", resize(0, 128, width, height)[1], True, False), (128, 0, 128), width / 2,
                      height / 2 +
                      resize(512, 512, width, height)[1] / 2).draw(window)
                if convert_inputs(controls[0], joysticks, 0)[6] and not confirm:
                    UIDicoEvent["UI1 ready"].play()
                    confirm = True
                    Menu = "main"
                titleframe += 1

            ###################################################################################################

            else:
                window.fill((0x66, 0x22, 0x66))  # Remplissage de l'arrière-plan

            # Récupération des events
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:  # Bouton croix en haut à droite de l'écran
                    run = False

            if not Play:

                # Musique du menu
                if not musicplaying and Menu not in ("title", "results"):
                    if Menu == "credits":
                        SoundSystem.stop_inst(embient.instance)
                        embient.instance = SoundSystem.play_event("event:/BGM/intro")
                    elif Menu != "game" and Menu != "gameonline":
                        SoundSystem.stop_inst(embient.instance)
                        embient.instance = SoundSystem.play_event("event:/BGM/menu")

                    musicplaying = True

                if not convert_inputs(controls[0], joysticks, 0)[6]:
                    confirm = False

                ##########################################  Menu Principal  ##########################################

                if Menu == "main":
                    online = False
                    # inputs haut et bas pour se déplacer dans le menu
                    if functions.input_but_no_repeat(3, controls, joysticks, 0):
                        focusedbutton += 1
                        UIDicoEvent["UI1 selection"].play()

                    if functions.input_but_no_repeat(2, controls, joysticks, 0):
                        focusedbutton -= 1
                        UIDicoEvent["UI1 selection"].play()

                    # inputs haut et bas pour se déplacer dans le menu
                    if functions.input_but_no_repeat(1, controls, joysticks, 0):
                        focusedbutton += 1
                        UIDicoEvent["UI1 selection"].play()

                    if functions.input_but_no_repeat(0, controls, joysticks, 0):
                        focusedbutton -= 1
                        UIDicoEvent["UI1 selection"].play()

                    focusedbutton = ((focusedbutton + 3) % 7) - 3

                    # Bouton "Combat"
                    Bouton = Button("Octogone", ("arial", resize(0, 50, width, height)[1], True, False),
                                    f"{rootDir()}/Images/Menu/Button.png", width / 2,
                                    height / 8, resize(250, 100, width, height))
                    if focusedbutton == 0:
                        Bouton.changeImage(f"{rootDir()}/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not confirm:
                            UIDicoEvent["UI1 validation"].play()
                            UIDicoEvent["Voix"]["Autre"]["Choix"].play()
                            Menu = "to char"
                            Menu_Stages.training = False
                            Menu_Chars.training = False
                            training = False
                            confirm = True
                    Bouton.draw(window)

                    # Bouton "Pandaball"
                    Bouton = Button("", ("arial", resize(0, 45, width, height)[1], True, False),
                                    f"{rootDir()}/Images/Menu/Button.png", width / 2,
                                    2 * height / 8, resize(250, 100, width, height))
                    if focusedbutton == 1:
                        Bouton.changeImage(f"{rootDir()}/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not confirm:
                            UIDicoEvent["UI1 forward"].play()
                            Menu = "to char"
                            Menu_Stages.training = True
                            Menu_Chars.training = True
                            training = True
                            confirm = True
                    Bouton.draw(window)
                    Texte("Pandaball", ("arial", resize(0, 45, width, height)[1], True, False), (0, 0, 0), width / 2,
                          2 * height / 8 - resize(0, 20, width, height)[1]).draw(
                        window)
                    Texte("(Entraînement)", ("arial", resize(0, 30, width, height)[1], True, False), (0, 0, 0),
                          width / 2, 2 * height / 8 + resize(0, 20, width, height)[1]).draw(
                        window)

                    # Bouton "En ligne Local"
                    Bouton = Button("", ("arial", resize(0, 45, width, height)[1], True, False),
                                    f"{rootDir()}/Images/Menu/Button.png", width / 2,
                                    3 * height / 8, resize(250, 100, width, height))
                    if focusedbutton == 2:
                        Bouton.changeImage(f"{rootDir()}/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not confirm:
                            UIDicoEvent["UI1 validation"].play()
                            Menu = "ipaddress"
                            ip = ""
                            online = True
                            confirm = True
                    Bouton.draw(window)
                    Texte("En ligne", ("arial", resize(0, 45, width, height)[1], True, False), (0, 0, 0), width / 2,
                          3 * height / 8 - resize(0, 20, width, height)[1]).draw(
                        window)
                    Texte("Local", ("arial", resize(0, 45, width, height)[1], True, False), (0, 0, 0),
                          width / 2, 3 * height / 8 + resize(0, 20, width, height)[1]).draw(
                        window)

                    # Bouton "Paramètres"
                    Bouton = Button("Paramètres", ("arial", resize(0, 50, width, height)[1], True, False),
                                    f"{rootDir()}/Images/Menu/Button.png",
                                    width / 2, 4 * height / 8, resize(250, 100, width, height))
                    if focusedbutton == 3:
                        Bouton.changeImage(f"{rootDir()}/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not confirm:
                            UIDicoEvent["UI1 forward"].play()
                            Menu = "settings"
                            Menu_Settings = SettingsMenu(UIDicoEvent, width, height)
                            confirm = True
                    Bouton.draw(window)

                    # Bouton "Credits"
                    Bouton = Button("Credits", ("arial", resize(0, 40, width, height)[1], True, False),
                                    f"{rootDir()}/Images/Menu/Button.png", width / 2,
                                    7 * height / 8, resize(120, 80, width, height))
                    if focusedbutton == -2:
                        Bouton.changeImage(f"{rootDir()}/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not confirm:
                            # UIDicoEvent["UI1 forward"].play()   rien c est bien pour les crédit
                            Menu = "credits"
                            musicplaying = False
                            confirm = True
                    Bouton.draw(window)

                    # Bouton "Title"
                    Bouton = Button("Ecran titre", ("arial", resize(0, 30, width, height)[1], True, False),
                                    f"{rootDir()}/Images/Menu/Button.png",
                                    3 * width / 4, 7 * height / 8, resize(120, 80, width, height))
                    if focusedbutton == -1:
                        Bouton.changeImage(f"{rootDir()}/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not confirm:
                            UIDicoEvent["UI1 back"].play()
                            Menu = "title"
                            titleframe = 0
                            musicplaying = False
                            SoundSystem.stop_inst(embient.instance)
                            embient.instance = SoundSystem.play_event("event:/BGM/clemenc'octogone")
                            confirm = True
                            focusedbutton = 0
                    Bouton.draw(window)

                    # Bouton "Quitter"
                    Bouton = Button("Quitter", ("arial", resize(0, 40, width, height)[1], True, False),
                                    f"{rootDir()}/Images/Menu/Button.png", width / 4,
                                    7 * height / 8, resize(120, 80, width, height))
                    if focusedbutton == -3:
                        Bouton.changeImage(f"{rootDir()}/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not confirm:
                            run = False
                    Bouton.draw(window)

                #####################################################################################################
                #############################################  Credits  #############################################

                if Menu == "credits":
                    Texte("CREDITS", ("arial", resize(0, 45, width, height)[1], True, False), (0, 0, 0), width / 2,
                          40).draw(window)

                    Texte("Game director", ("arial", resize(0, 25, width, height)[1], True, False), (0, 0, 0),
                          width / 3, height / 8).draw(window)
                    Texte("Elsa", ("arial", resize(0, 28, width, height)[1], False, False), (0xBC, 0x79, 0xE4),
                          2 * width / 3, height / 8).draw(
                        window)

                    Texte("Graphics", ("arial", resize(0, 28, width, height)[1], True, False), (0, 0, 0), width / 3,
                          2 * height / 8).draw(window)
                    Texte("Loïc", ("arial", resize(0, 28, width, height)[1], False, False), (0x20, 0x50, 0xF0),
                          2 * width / 3,
                          2 * height / 8 - 15).draw(window)
                    Texte("Elsa", ("arial", resize(0, 28, width, height)[1], False, False), (0xBC, 0x79, 0xE4),
                          2 * width / 3,
                          2 * height / 8 + 15).draw(window)
                    Texte("Nicolas", ("arial", resize(0, 28, width, height)[1], False, False), (120, 120, 120),
                          3 * width / 4,
                          2 * height / 8 - 15).draw(window)
                    Texte("Aubin", ("arial", resize(0, 28, width, height)[1], False, False), (0x55, 0x77, 0xBB),
                          3 * width / 4,
                          2 * height / 8 + 15).draw(window)

                    Texte("Musics & Sounds", ("arial", resize(0, 28, width, height)[1], True, False), (0, 0, 0),
                          width / 3, 3 * height / 8).draw(
                        window)
                    Texte("Iwan", ("arial", resize(0, 28, width, height)[1], False, False), (0xBC, 0xBC, 0x10),
                          2 * width / 3, 3 * height / 8).draw(
                        window)

                    Texte("Programation", ("arial", resize(0, 28, width, height)[1], True, False), (0, 0, 0), width / 3,
                          4 * height / 8).draw(window)
                    Texte("Nicolas", ("arial", resize(0, 28, width, height)[1], False, False), (120, 120, 120),
                          2 * width / 3,
                          4 * height / 8 - 20).draw(window)
                    Texte("Iwan", ("arial", resize(0, 28, width, height)[1], False, False), (0xBC, 0xBC, 0x10),
                          2 * width / 3,
                          4 * height / 8 + 20).draw(window)

                    # retour
                    Bouton = Button("<--", ("arial", resize(0, 50, width, height)[1], True, False),
                                    f"{rootDir()}/Images/Menu/Button.png", 100, height - resize(0, 50, width, height)[1],
                                    resize(100, 60, width, height))
                    Bouton.changeImage(f"{rootDir()}/Images/Menu/Button_focused.png")
                    if convert_inputs(controls[0], joysticks, 0)[6] and not confirm:
                        UIDicoEvent["UI1 back"].play()
                        Menu = "main"
                        musicplaying = False
                        confirm = True
                    Bouton.draw(window)

                #######################################################################################################
                ##########################################  Menu paramètres  ##########################################

                if Menu == "settings":
                    Menu, changescreen = Menu_Settings.update(window, width, height, events, controls, joysticks, 0, 0)
                    if changescreen:
                        root = tk.Tk()
                        root.withdraw()
                        messagebox.showerror('Avertissement',
                                             "Certaines modifications ne prendront effet qu'au redémarrrage")
                    confirm = Menu_Settings.confirm

                ######################################################################################################
                ############################################  Transition  ############################################

                if Menu == "to char":
                    Menu = "char"
                    Menu_Chars.confirm = True

                if Menu == "to stage":
                    Menu = "stage"
                    Menu_Stages.confirm = True
                    gamecreated = False

                ######################################################################################################
                #########################################  Menu personnages  #########################################

                if Menu == "char":
                    Menu = Menu_Chars.update(window, width, height, controls, joysticks)
                    confirm = Menu_Chars.confirm

                ######################################################################################################
                ############################################  Menu stage  ############################################

                if Menu == "stage":
                    Menu = Menu_Stages.update(window, controls, joysticks, width, height)
                    confirm = Menu_Stages.confirm

                ######################################################################################################
                ######################################  Démarrage de la partie  ######################################

                if Menu == "game":
                    if not gamecreated:
                        SoundSystem.stop_inst(embient.instance)
                        beep = 0
                        stage = Menu_Stages.stage

                        names = Menu_Chars.names

                        Menu_Chars.selected_1 = False
                        Menu_Chars.selected_2 = False
                        # Jeu clavier
                        if names[0] == 0 and controls[0] == commands["Keyboard"]:
                            names[0] = 1
                        if names[1] == 0 and controls[1] == commands["Keyboard"]:
                            names[1] = 1

                        # conversion des contrôles
                        controls = [commands[Menu_Chars.namelist[names[0]]], commands[Menu_Chars.namelist[names[1]]]]
                        # Création des objets game et result
                        Game = GameObject.Game(training, chars, Menu_Chars.selectchar_1, Menu_Chars.selectchar_2,
                                               Menu_Chars.alt, UIDicoEvent)
                        results = Results(Game, width, height, Menu_Chars.namelist[names[0]],
                                          Menu_Chars.namelist[names[1]])
                        del names

                        # importation de l'arrière-plan et de la musique
                        background = pygame.transform.scale(pygame.image.load(
                            f"{rootDir()}/Images/Stages/{Menu_Stages.actualstages[stage]}/{Menu_Stages.actualstages[stage]}.png"),
                            (width, height))
                        for m in musics:
                            if m[1] == Menu_Stages.actualstages[stage] and (
                                    str(Game.Char_P1) == m[2] or str(Game.Char_P2) == m[2] or m[2] == True):
                                currentmusic = m[0]

                        # création du stage
                        stage, [(Game.Char_P1.x, Game.Char_P1.rect[1]),
                                (Game.Char_P2.x, Game.Char_P2.rect[1])] = Stages.create_stage(
                            Menu_Stages.actualstages[stage])

                        gamecreated = True

                    window.fill((255, 255, 255))
                    window.blit(background, (0, 0))

                    # Affichage du stage
                    stage.draw(window)

                    # Affichage des personnages
                    Game.Char_P2.draw(window)
                    Game.Char_P1.draw(window)

                    # Compte à rebours
                    if 3 - round(time.time() - Game.begin_game - 0.2) < 1 and round(
                            time.time() - Game.begin_game) < 5 and not training:
                        if beep < 4:
                            UIDicoEvent["UI1 ready"].play()
                            beep += 1

                        Texte(f"PARTEZ !", ("Arial", resize(0, 180, width, height)[1], True, False), (120, 0, 120),
                              width / 2, height / 2).draw(
                            window)

                    elif 4 > time.time() - Game.begin_game > 0.2 and not training:
                        if beep < round(time.time() - Game.begin_game + 0.2):
                            UIDicoEvent["UI1 selection 2"].play()
                            beep += 1
                        Texte(f"{str(3 - round(time.time() - Game.begin_game - 0.2))}",
                              ("Arial", resize(0, 180, width, height)[1], True, False),
                              (0, 0, 100), width / 2, height / 2).draw(window)

                    elif time.time() - Game.begin_game > 5 or training:
                        musicplaying = False
                        Game.begin_game = time.time()
                        Game.pausefrom = time.time()
                        Play = True

                ######################################################################################################
                ########################################  Ecran de résultats  ########################################

                if Menu == "results":
                    if results.frame == 1:
                        if results.winner == -1:
                            UIDicoEvent["Voix"]["Autre"]["Terminer"].play()  # Egalite
                        else:
                            UIDicoEvent["Voix"]["Autre"]["23 Fin du match"].play() # Le gagnant est
                        if results.winner == 0:
                            embient.instance = SoundSystem.play_event(
                                f"event:/VT/{Victorythemes[str(results.game.Char_P1)]}")
                        if results.winner == 1:
                            embient.instance = SoundSystem.play_event(
                                f"event:/VT/{Victorythemes[str(results.game.Char_P2)]}")
                        if results.winner == -1:
                            embient.instance = SoundSystem.play_event(f"event:/VT/{Victorythemes[-1]}")
                    if results.frame == 80:

                        if results.winner == 0:
                            UIDicoEvent["Voix"]["Personnages"][voicename[str(results.game.Char_P1)]].play()

                        if results.winner == 1:
                            UIDicoEvent["Voix"]["Personnages"][voicename[str(results.game.Char_P2)]].play()
                    window.fill((200, 120, 200))
                    results.draw(window, width, height)

                    if results.frame > 300 and convert_inputs(controls[0], joysticks, 0)[6]:
                        # retour au menu
                        SoundSystem.stop_inst(embient.instance)
                        UIDicoEvent["UI1 forward"].play()
                        # réinitialisation des contrôles
                        controls = functions.reset_commands(joysticks, commands)
                        if online :
                            Menu = "online"
                        else :
                            Menu = "char"
                            Menu_Chars.confirm = True
                            confirm = True

            ######################################################################################################
            ############################################  En  combat  ############################################

            else:
                results.check_winner()

                # musique
                if not musicplaying:
                    embient.instance = SoundSystem.play_event(currentmusic)
                    musicplaying = True


                # Réinitialisation de l'écran à chaque frame
                window.fill((255, 255, 255))
                window.blit(background, (0, 0))
                if online :
                    try :
                        if Game.Char_P2.hasbeenhit :
                            sending = Game.Char_P2
                        else :
                            sending = False
                        Game.online = True
                        if myplayer :
                            Play, musicplaying, Menu, controls = Game.play(controls,joysticks,stage,width,height,window,clock,get,False)
                            get = network.send(["Game",Game.Char_P1,sending])[not myplayer]
                        else :
                            Play, musicplaying, Menu, controls = Game.play(controls,joysticks,stage,width,height,window,clock,get,True)
                            get = network.send(["Game",Game.Char_P1, sending, Game.time_game + (Game.begin_game - time.time()) + Game.pause_time])[not myplayer]
                    except :
                        musicplaying = False
                        traceback.print_exc()
                        print("[NETWORK] Lost connection")
                        Menu = "main"
                        Play = False
                        messagebox.showerror('Erreur Réseau',"Connection perdue avec le serveur")
                else :
                    Game.online = False
                    Play, musicplaying, Menu, controls = Game.play(controls, joysticks, stage, width, height, window, clock)
                    confirm = Game.confirm

                SoundSystem.changeGlobalParameter("pause", int(Game.pause))  # gestion du son de la pause


                if stage.name == "Salle de TP":
                    tremolo = 0
                    if Game.Char_P1.name == "Gregoire":
                        for p in Game.Char_P1.projectiles:
                            if isinstance(p, Rayon):
                                tremolo = 1
                    if Game.Char_P2.name == "Gregoire":
                        for p in Game.Char_P2.projectiles:
                            if isinstance(p, Rayon):
                                tremolo = 1
                    embient.changeParameter("tremolo", tremolo)
                if Game.game_running > 0:
                    SoundSystem.stop_inst(embient.instance)

            ######################################################################################################
            ##############################################  Online  ##############################################
            
            try :
                if not Play :
                    if  Menu == "ipaddress":
                        online = True
                        Texte("Entrez l'adresse IP du serveur :",("arial", resize(0,25,width,height)[1], True, False),(0,0,0),width/2,height/2-resize(0,100,width,height)[1]).draw(window)
                        if not ip :
                            ipentry=TextInput(password=True,font_family="arial")
                            ip = " "
                        else :
                            ip = ipentry.get_text()
                            if not ip :
                                ip = " "
                            ipentry.update(events)
                            surface = ipentry.get_surface()
                            window.blit(surface,(width/2-surface.get_width()/2,height/2))
                        if convert_inputs(controls[0], joysticks, 0)[6] and not confirm:
                            Menu = "connect"
                            confirm = True
                        

                    if Menu == "connect" :
                            network = Network(ip)
                            Menu = "online"
                            globalplayer = network.getP()
                            if globalplayer is None :
                                messagebox.showerror('Connection échouée',f"La connection au serveur {ip} a échoué")
                                ip = ""
                                Menu = "main"
                            else :
                                myplayer = (globalplayer-1)%2
                                print("[NETWORK] Connected as player",globalplayer)
                                print("[NETWORK] Local player :",myplayer+1)
                    #print(Menu)
                    if Menu == "online":
                        get = network.send("Waiting")
                        ready = get[not myplayer]
                        if ready :
                            Menu = "charonline"
                            UIDicoEvent["Voix"]["Autre"]["Choix"].play()
                            MenucharsOnline = CharsMenuOnline(False,UIDicoEvent)
                            MenucharsOnline.confirm = True
                            for _ in range(3):
                                get = network.send("Waiting")
                                clock.tick(20)
                        else :
                            Texte("En attente d'un adversaire...",("arial", resize(0,90,width,height)[1], False, False),(0,0,0),width/2,height/2).draw(window)
                        if convert_inputs(controls[0], joysticks, 0)[7]:
                            online = False
                            Menu = "main"
                            try :
                                network.send(False)
                            except :
                                pass
                            UIDicoEvent["UI1 back"].play()
                    #print(Menu)
                    if Menu == "charonline":
                        get = network.send(["Chars",MenucharsOnline.selected_1,MenucharsOnline.selectchar_1,MenucharsOnline.namelist[MenucharsOnline.names[0]],MenucharsOnline.alt])
                        get = get[not myplayer]
                        if isinstance(get,list) and get[0] and MenucharsOnline.selected_1 :
                            Menu = "stageonline"
                            MenustagesOnline = StagesMenuOnline(False,UIDicoEvent)
                            MenustagesOnline.confirm = True
                            MenustagesOnline.stage = -1
                            for _ in range(3):
                                get = network.send(["Chars",MenucharsOnline.selected_1,MenucharsOnline.selectchar_1,MenucharsOnline.namelist[MenucharsOnline.names[0]],MenucharsOnline.alt])
                                clock.tick(20)
                        else :
                            try :
                                MenucharsOnline.update(window,width,height,controls,joysticks,get)
                            except :
                                traceback.print_exc()
                    
                    if Menu == "stageonline":
                        get = network.send(["Stage",MenustagesOnline.stage])
                        stage = get[0]
                        if isinstance(stage,int) and stage > -1 :
                            Menu = "gameonline"
                            gamecreated = False
                            for _ in range(3):
                                get = network.send(["Stage",MenustagesOnline.stage])
                                clock.tick(20)
                        else :
                            if myplayer == 0 :
                                MenustagesOnline.update(window,controls,joysticks,width,height)
                            else :
                                MenustagesOnline.stage = stage
                                Texte("L'hôte sélectionne le stage",("arial", resize(0,90,width,height)[1], False, False),(0,0,0),width/2,height/2).draw(window)

                    if Menu == "gameonline":
                        if not gamecreated:
                            get = network.send(["Countdown",-10])
                            SoundSystem.stop_inst(embient.instance)
                            beep = 0

                            names = MenucharsOnline.names

                            MenucharsOnline.selected_1 = False
                            # Jeu clavier
                            if names[0] == 0 and controls[0] == commands["Keyboard"]:
                                names[0] = 1

                            # conversion des contrôles
                            controls = [commands[MenucharsOnline.namelist[names[0]]], []]
                            # Création des objets game et result
                            Game = GameObject.Game(False, chars, MenucharsOnline.selectchar_1, MenucharsOnline.selectchar_2,
                                                (MenucharsOnline.alt,MenucharsOnline.otheralt), UIDicoEvent)
                            results = Results(Game, width, height, MenucharsOnline.namelist[names[0]], names[1])
                            del names

                            # importation de l'arrière-plan et de la musique
                            background = pygame.transform.scale(pygame.image.load(
                                f"{rootDir()}/Images/Stages/{MenustagesOnline.actualstages[stage]}/{MenustagesOnline.actualstages[stage]}.png"),
                                (width, height))
                            for m in musics:
                                if m[1] == MenustagesOnline.actualstages[stage] and (
                                        str(Game.Char_P1) == m[2] or str(Game.Char_P2) == m[2] or m[2] == True):
                                    currentmusic = m[0]

                            # création du stage
                            if myplayer :
                                stage, [(Game.Char_P2.x, Game.Char_P2.rect[1]),
                                        (Game.Char_P1.x, Game.Char_P1.rect[1])] = Stages.create_stage(
                                    MenustagesOnline.actualstages[stage])
                                Game.Char_P1.look_right, Game.Char_P2.look_right = Game.Char_P2.look_right, Game.Char_P1.look_right
                            else :
                                stage, [(Game.Char_P1.x, Game.Char_P1.rect[1]),
                                        (Game.Char_P2.x, Game.Char_P2.rect[1])] = Stages.create_stage(
                                    MenustagesOnline.actualstages[stage])
                                

                            gamecreated = True

                        if myplayer == 0 :
                            countdown = "Countdown",time.time() - Game.begin_game
                            countdown = network.send(["Countdown",time.time() - Game.begin_game])[1]
                        else :
                            countdown = network.send(["Countdown",-10])[1]
                        if not isinstance(countdown,float):
                            countdown = -10

                        window.fill((255, 255, 255))
                        window.blit(background, (0, 0))

                        # Affichage du stage
                        stage.draw(window)

                        # Affichage des personnages
                        Game.Char_P2.draw(window)
                        Game.Char_P1.draw(window)

                        # Compte à rebours
                        if 3 - round(countdown - 0.2) < 1 and round(
                                countdown) < 5 :
                            if beep < 4:
                                UIDicoEvent["UI1 ready"].play()
                                beep += 1

                            Texte(f"PARTEZ !", ("Arial", resize(0, 180, width, height)[1], True, False), (120, 0, 120),
                                width / 2, height / 2).draw(
                                window)

                        elif 4 > countdown > 0.2 :
                            if beep < round(countdown + 0.2):
                                UIDicoEvent["UI1 selection 2"].play()
                                beep += 1
                            Texte(f"{str(3 - round(countdown - 0.2))}",
                                ("Arial", resize(0, 180, width, height)[1], True, False),
                                (0, 0, 100), width / 2, height / 2).draw(window)

                        elif countdown > 5 :
                            musicplaying = False
                            Game.begin_game = time.time()
                            Game.pausefrom = time.time()
                            Play = True
                            for _ in range(10):
                                if myplayer :
                                    get = network.send(["Game",Game.Char_P1,False])[not myplayer]
                                else :
                                    get = network.send(["Game",Game.Char_P1,False, Game.time_game + (Game.begin_game - time.time()) + Game.pause_time])[not myplayer]
                                
                                
                                clock.tick(60)

            except :
                musicplaying = False
                traceback.print_exc()
                online = False
                print("[NETWORK] Lost connection")
                Menu = "main"
                Play = False
                messagebox.showerror('Erreur Réseau',"Connection perdue avec le serveur")


            ######################################################################################################

            pygame.display.flip()  # actualisation de l'écran
            SoundSystem.tick_update()
            clock.tick(60)  # FPS

    except Exception:
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb = traceback.TracebackException(exc_type, exc_value, exc_tb)

        traceback.print_exc()
        messagebox.showerror('Erreur Critique',
                             f"""Une erreur critique est survenue :

{tb.stack}

{''.join(tb.format_exception_only())}

merci de contacter l'equipe de développement.
Pour plus de details veuillez consulter : 
https://github.com/Chokotec-h/Clemenc-octogone""")

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
