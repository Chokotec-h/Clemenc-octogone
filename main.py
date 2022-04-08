############################################################################################################
####################################### Importation de Bibliothèques #######################################
############################################################################################################

import pygame
import traceback
from DATA.assets.Chars.Gregoire import Rayon
from DATA.utilities.Menu_Settings import SettingsMenu
from DATA.utilities.Menu_Stages_and_Chars import StagesMenu, CharsMenu
import DATA.utilities.SoundSystem as SoundSystem
import DATA.utilities.SFXEvents as SFXEvents
import time

import DATA.assets.CharsLoader as Chars
import DATA.assets.Stages as Stages
import DATA.utilities.Game as GameObject
from DATA.utilities.Interface import *
from DATA.utilities.Gamepad_gestion import *
from DATA.utilities.functions import *
from DATA.utilities.commands import *

############################################################################################################
############################################## Initialisation ##############################################
############################################################################################################

pygame.init()  # Initialisation de pygame
clock = pygame.time.Clock()  # Horloge

pygame.joystick.init()  # Initialisation des manettes
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

for j in joysticks:
    j.init()

##########################################################################################################

# L'initialisation des sons a lieu dans Base_char.py

UIDicoEvent = SFXEvents.SFXDicoEvent

embient = SoundSystem.instance()
embient.instance = SoundSystem.play_event("event:/BGM/clemenc'octogone")


############################################################################################################

def main():
    """"""""""""""""""""""""""""""""""""
    """""""""Progamme Principal"""""""""
    """"""""""""""""""""""""""""""""""""

    # création de la fenêtre
    width = 1600
    height = 900
    window = pygame.display.set_mode((width, height))
    icon = pygame.image.load("DATA/Images/logo.ico")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("clemenc'octogone", "DATA/Images/logo.ico")

    # test de music et de bruitages

    try:
        controls = reset_commands(joysticks, commands)

        # Initialisation des contrôles
        run = True

        ################################################################################################################

        """ Déclaration des variables """

        # Noms des personnages et des stages
        chars = Chars.chars
        # Config des musiques
        musics = Stages.musics
        musicplaying = False

        # Variables de gestion du jeu et du menu
        Menu = "title"
        Play = False
        focusedbutton = 0  # numéro de bouton
        confirm = False  # permet de ne pas détecter la confirmation du menu plusieurs frames à la suite

        Menu_Settings = SettingsMenu(UIDicoEvent)
        Menu_Stages = StagesMenu(False, UIDicoEvent)
        Menu_Chars = CharsMenu(False, UIDicoEvent)

        # Animation de l'ecran titre
        titleframe = 0
        titleanimation = [pygame.transform.scale(pygame.image.load(f"DATA/Images/Logo/{i}.png"), (512, 512)) for i in
                          range(37)]

        ################################################################################################################       

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""   INSTRUCTIONS   """""""""""""""""""""
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        # Boucle du programme
        while run:
            # gestion de répétition des touches lorsqu'elles sont maintenues (toutes les 10 frames)
            actualize_repeating()

            ##########################################  Ecran titre  ##########################################

            if Menu == "title":
                window.fill((0x99, 0x55, 0x99))  # Arrière plan
                pygame.draw.rect(window, (60, 60, 60), (0, 0, width, 128))
                pygame.draw.rect(window, (60, 60, 60), (0, height - 128, width, 128))
                # Affichage de la version
                Texte("1.0.0 beta", ("Arial", 15, True, True), (0, 0, 0), 100, 64, format_="left").draw(window)

                key = "A" if len(joysticks) > 0 else "Espace"
                if titleframe % 60 < 30:  # Clignotement toutes les demi-secondes
                    Texte(f"Appuyez sur {key}", ("Arial black", 50, True, False), (0, 0, 0), width / 2,
                          height - 64).draw(window)

                window.blit(titleanimation[round(min(titleframe, 54) / 1.5)], (width / 2 - 256, height / 2 - 256 - 64))
                Texte("OCTOGONE", ("Comic", 128, True, False), (40, 40, 40), width / 2 + 5, height / 2 + 256 + 5).draw(
                    window)
                Texte("OCTOGONE", ("Comic", 128, True, False), (128, 0, 128), width / 2, height / 2 + 256).draw(window)
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
                if not musicplaying and Menu != "title":
                    if Menu == "credits":
                        SoundSystem.stop_inst(embient.instance)
                        embient.instance = SoundSystem.play_event("event:/BGM/intro")
                    elif Menu != "game":
                        SoundSystem.stop_inst(embient.instance)
                        embient.instance = SoundSystem.play_event("event:/BGM/menu")

                    musicplaying = True

                if not convert_inputs(controls[0], joysticks, 0)[6]:
                    confirm = False

                ##########################################  Menu Principal  ##########################################

                if Menu == "main":
                    # inputs haut et bas pour se déplacer dans le menu
                    if input_but_no_repeat(3, controls, joysticks, 0):
                        focusedbutton += 1
                        UIDicoEvent["UI1 selection"].play()

                    if input_but_no_repeat(2, controls, joysticks, 0):
                        focusedbutton -= 1
                        UIDicoEvent["UI1 selection"].play()

                    focusedbutton = ((focusedbutton + 2) % 5) - 2

                    # Bouton "Combat"
                    Bouton = Button("Combat", ("arial", 50, True, False), "./DATA/Images/Menu/Button.png", width / 2,
                                    height / 8, 250, 100)
                    if focusedbutton == 0:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not confirm:
                            UIDicoEvent["UI1 validation"].play()
                            Menu = "to char"
                            Menu_Stages.training = False
                            Menu_Chars.training = False
                            training = False
                            confirm = True
                    Bouton.draw(window)

                    # Bouton "Pandaball"
                    Bouton = Button("", ("arial", 45, True, False), "./DATA/Images/Menu/Button.png", width / 2,
                                    2 * height / 8, 250, 100)
                    if focusedbutton == 1:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not confirm:
                            UIDicoEvent["UI1 forward"].play()
                            Menu = "to char"
                            Menu_Stages.training = True
                            Menu_Chars.training = True
                            training = True
                            confirm = True
                    Bouton.draw(window)
                    Texte("Pandaball", ("arial", 45, True, False), (0, 0, 0), width / 2, 2 * height / 8 - 20).draw(
                        window)
                    Texte("(Entraînement)", ("arial", 30, True, False), (0, 0, 0), width / 2, 2 * height / 8 + 20).draw(
                        window)

                    # Bouton "Paramètres"
                    Bouton = Button("Paramètres", ("arial", 50, True, False), "./DATA/Images/Menu/Button.png",
                                    width / 2, 3 * height / 8, 250, 100)
                    if focusedbutton == 2:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not confirm:
                            UIDicoEvent["UI1 forward"].play()
                            Menu = "settings"
                            Menu_Settings = SettingsMenu(UIDicoEvent)
                            confirm = True
                    Bouton.draw(window)

                    # Bouton "Credits"
                    Bouton = Button("Credits", ("arial", 40, True, False), "./DATA/Images/Menu/Button.png", width / 4,
                                    7 * height / 8, 120, 80)
                    if focusedbutton == -2:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not confirm:
                            # UIDicoEvent["UI1 forward"].play()   rien c est bien pour les crédit
                            Menu = "credits"
                            musicplaying = False
                            confirm = True
                    Bouton.draw(window)

                    # Bouton "Title"
                    Bouton = Button("Ecran titre", ("arial", 30, True, False), "./DATA/Images/Menu/Button.png",
                                    3 * width / 4, 7 * height / 8, 120, 80)
                    if focusedbutton == -1:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not confirm:
                            Menu = "title"
                            titleframe = 0
                            musicplaying = False
                            SoundSystem.stop_inst(embient.instance)
                            embient.instance = SoundSystem.play_event("event:/BGM/clemenc'octogone")
                            confirm = True
                            focusedbutton = 0
                    Bouton.draw(window)

                #####################################################################################################
                #############################################  Credits  #############################################

                if Menu == "credits":
                    Texte("CREDITS", ("arial", 45, True, False), (0, 0, 0), width / 2, 40).draw(window)

                    Texte("Game director", ("arial", 28, True, False), (0, 0, 0), width / 3, height / 8).draw(window)
                    Texte("Elsa", ("arial", 28, False, False), (0xBC, 0x79, 0xE4), 2 * width / 3, height / 8).draw(
                        window)

                    Texte("Graphics", ("arial", 28, True, False), (0, 0, 0), width / 3, 2 * height / 8).draw(window)
                    Texte("Loïc", ("arial", 28, False, False), (0x20, 0x50, 0xF0), 2 * width / 3,
                          2 * height / 8 - 15).draw(window)
                    Texte("Elsa", ("arial", 28, False, False), (0xBC, 0x79, 0xE4), 2 * width / 3,
                          2 * height / 8 + 15).draw(window)
                    Texte("Nicolas", ("arial", 28, False, False), (120, 120, 120), 3 * width / 4,
                          2 * height / 8 - 15).draw(window)
                    Texte("Aubin", ("arial", 28, False, False), (0x55, 0x77, 0xBB), 3 * width / 4,
                          2 * height / 8 + 15).draw(window)

                    Texte("Musics & Sounds", ("arial", 28, True, False), (0, 0, 0), width / 3, 3 * height / 8).draw(
                        window)
                    Texte("Iwan", ("arial", 28, False, False), (0xBC, 0xBC, 0x10), 2 * width / 3, 3 * height / 8).draw(
                        window)

                    Texte("Programation", ("arial", 28, True, False), (0, 0, 0), width / 3, 4 * height / 8).draw(window)
                    Texte("Nicolas", ("arial", 28, False, False), (120, 120, 120), 2 * width / 3,
                          4 * height / 8 - 20).draw(window)
                    Texte("Iwan", ("arial", 28, False, False), (0xBC, 0xBC, 0x10), 2 * width / 3,
                          4 * height / 8 + 20).draw(window)

                    # retour
                    Bouton = Button("<--", ("arial", 50, True, False), "./DATA/Images/Menu/Button.png", 100, 850, 100,
                                    60)
                    Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                    if convert_inputs(controls[0], joysticks, 0)[6] and not confirm:
                        UIDicoEvent["UI1 back"].play()
                        Menu = "main"
                        musicplaying = False
                        confirm = True
                    Bouton.draw(window)

                #######################################################################################################
                ##########################################  Menu paramètres  ##########################################

                if Menu == "settings":
                    Menu = Menu_Settings.update(window, width, height, events, controls, joysticks, 0, 0)
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
                    if not gamecreated :
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
                        del names

                        Game = GameObject.Game(training, chars, Menu_Chars.selectchar_1, Menu_Chars.selectchar_2,
                                               Menu_Chars.alt, UIDicoEvent)

                        # importation de l'arrière-plan et de la musique
                        background = pygame.transform.scale(pygame.image.load(
                            f"./DATA/Images/Stages/{Menu_Stages.actualstages[stage]}/{Menu_Stages.actualstages[stage]}.png"),
                            (1600, 900))
                        for m in musics:
                            if m[1] == Menu_Stages.actualstages[stage] and (
                                    str(Game.Char_P1) == m[2] or str(Game.Char_P2) == m[2] or m[2] == True):
                                currentmusic = m[0]

                        # création du stage
                        stage, [(Game.Char_P1.x, Game.Char_P1.rect.y),
                                (Game.Char_P2.x, Game.Char_P2.rect.y)] = Stages.create_stage(
                            Menu_Stages.actualstages[stage])

                        gamecreated = True


                    window.fill((255, 255, 255))
                    window.blit(background, (0, 0))

                    # Affichage du stage
                    stage.draw(window)

                    # Affichage des personnages
                    Game.Char_P2.draw(window)
                    Game.Char_P1.draw(window)

                    if 3 - round(time.time() - Game.begin_game - 0.2) < 1 and round(
                            time.time() - Game.begin_game) < 5 and not training:
                        if beep < 4:
                            UIDicoEvent["UI1 ready"].play()
                            beep += 1

                        Texte(f"PARTEZ !", ("Arial", 180, True, False), (120, 0, 120), width / 2, height / 2).draw(
                            window)

                    elif 4 > time.time() - Game.begin_game > 0.2 and not training:
                        if beep < round(time.time() - Game.begin_game + 0.2):
                            UIDicoEvent["UI1 selection 2"].play()
                            beep += 1
                        Texte(f"{str(3 - round(time.time() - Game.begin_game - 0.2))}", ("Arial", 180, True, False),
                              (0, 0, 100), width / 2, height / 2).draw(window)

                    elif time.time() - Game.begin_game > 5 or training:
                        musicplaying = False
                        Game.begin_game = time.time()
                        Play = True

                ######################################################################################################
                ########################################  Ecran de résultats  ########################################

                if Menu == "results":
                    # réinitialisation des contrôles
                    controls = reset_commands(joysticks, commands)
                    Menu = "char"

            ######################################################################################################
            ############################################  En  combat  ############################################

            else:

                # musique
                if not musicplaying:
                    embient.instance = SoundSystem.play_event(currentmusic)
                    musicplaying = True

                # Réinitialisation de l'écran à chaque frame
                window.fill((255, 255, 255))
                window.blit(background, (0, 0))

                Play, musicplaying, Menu, controls = Game.play(controls, joysticks, stage, width, height, window, clock)
                confirm = Game.confirm
                
                SoundSystem.changeGlobalParameter("pause", int(Game.pause))

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

            ######################################################################################################

            pygame.display.flip()  # actualisation de l'écran
            SoundSystem.tick_update()
            clock.tick(60)  # FPS

    except Exception:
        traceback.print_exc()

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
