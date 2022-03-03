from DATA.utilities.functions import *
from DATA.utilities.Interface import *
from DATA.utilities.commands import commands
import DATA.assets.CharsLoader as Chars
from DATA.assets.animations import icons
from random import randint
from DATA.assets.Misc import *
from DATA.assets.Chars.Training_Mob import Training
import time


class Game():
    def __init__(self, training, chars, selectchar_1, selectchar_2, alt) -> None:

        # Gestion de la fumee de hitstun
        self.smoke = list()
        self.smokeframe = 0

        # gestion de la pause
        self.pause = False
        self.hold_pause = False

        # Training
        self.TrainingHDI = 0
        self.TrainingVDI = 0
        self.Tech = 0

        self.pausefrom = 0
        self.training = training

        ### Création des objets parsonnages
        self.Char_P1 = Chars.charobjects[chars[selectchar_1][alt[0]]](0, 0, 0)

        if training:
            self.Char_P2 = Chars.Training(0, 0, 1)
            # gestion des statistiques en entraînement
            self.basedamages = 0
            self.airspeed = 1.25
            self.deceleration = 0.75
            self.fallspeed = 0.85
            self.fastfallspeed = 1.25
        else:
            self.Char_P2 = Chars.charobjects[chars[selectchar_2][alt[1]]](0, 0, 1)
        ###

        # initialisation des vies et du temps
        self.stock = [7, 7]
        self.time_game = 7 * 60
        self.begin_game = time.time()
        self.pause_time = 0
        self.pausefrom = 0
        self.game_running = -1

        self.focusedbutton = 0
        self.confirm = True

    def play(self, controls, joysticks, stage, width, height, window, clock):

        Play = True
        musicplaying = True
        Menu = "game"

        # Recuperation des touches
        if self.game_running < 0 and (
                convert_inputs(controls[0], joysticks, 0)[-1] or convert_inputs(controls[1], joysticks, 1)[-1]):
            if not self.hold_pause:
                self.pause = not self.pause
                self.hold_pause = True
        else:
            self.hold_pause = False

        # hors pause, si le jeu continue
        if self.game_running < 0 and not self.pause:
            self.pausefrom = time.time()  # gestion du chrono en pause

            #### récupération des inputs du joueur 1

            inputs_1 = convert_inputs(controls[0], joysticks, 0)[0:-1]
            if not (inputs_1[4] or inputs_1[5]):  # gestion du saut
                self.Char_P1.jumping = False

            # Transmission des inputs à l'objet Palyer 1
            self.Char_P1.act(inputs_1, stage, self.Char_P2, not (self.pause or self.Char_P1.BOUM or self.Char_P2.BOUM))
            if self.Char_P1.die == 30 and not self.training:
                self.stock[0] -= 1

            ####  récupération des inputs du joueur 2

            inputs_2 = convert_inputs(controls[1], joysticks, 1)[0:-1]
            if not (inputs_2[4] or inputs_2[5]):  # gestion du saut
                self.Char_P2.jumping = False

            if self.training:
                ################### Gestion de la DI et de la tech en entraînement ###################
                self.Char_P2.deceleration = self.deceleration
                traininginputs = [False for _ in range(17)]
                if self.Char_P2.hitstun or self.Char_P2.tumble:
                    if self.TrainingHDI > 0:
                        traininginputs[1] = True
                    if self.TrainingHDI < 0:
                        traininginputs[0] = True
                    if self.TrainingVDI > 0:
                        traininginputs[2] = True
                    if self.TrainingVDI < 0:
                        traininginputs[3] = True
                    if self.Tech > 0:
                        if randint(0, 1) == 1:
                            self.Char_P2.tech = 5
                        else:
                            self.Char_P2.tech = 0
                    if self.Tech < 0:
                        self.Char_P2.tech = 5
                else:
                    self.Char_P2.tech = 0

                self.Char_P2.act(traininginputs, stage, self.Char_P1,
                                 not (self.pause or self.Char_P1.BOUM or self.Char_P2.BOUM))
                ######################################################################################
            else:
                # Transmission des inputs à l'objet Palyer 2
                self.Char_P2.act(inputs_2, stage, self.Char_P1,
                                 not (self.pause or self.Char_P1.BOUM or self.Char_P2.BOUM))
            if self.Char_P2.die == 30 and not self.training:
                self.stock[1] -= 1
            ########

            # détection des collision
            self.Char_P2.collide(self.Char_P1)
            self.Char_P1.collide(self.Char_P2)

        elif self.pause:
            self.pause_time += time.time() - self.pausefrom  # gestion du chrono en pause
            self.pausefrom = time.time()
            pygame.draw.rect(window,(100,100,100),(width // 2-80, height // 2 - 40 , 160, 80))
            Texte(f"Pause", ("Arial", 60, False, False), (0, 0, 0), width // 2, height // 2, 800).draw(window)
            if not self.training : 
                Texte(f"Attaque + Spécial + Bouclier pour quitter", ("Arial", 25, False, False), (0, 0, 0), 40, 40, 800,format_="left").draw(window)
                inputs_1 = convert_inputs(controls[0], joysticks, 0)[0:-1]
                inputs_2 = convert_inputs(controls[1], joysticks, 1)[0:-1]
                if (inputs_1[6] and inputs_1[7] and inputs_1[8]) or (inputs_2[6] and inputs_2[7] and inputs_2[8]):
                    self.confirm = True
                    Menu = "to char"
                    Play = False
                    self.pause = False
                    self.focusedbutton = 0
                    musicplaying = False
                    # reinitialisation des controles
                    controls = reset_commands(joysticks, commands)
                    clock.tick(10)

        ################### Affichage des éléments ###################

        ### Debug
        for h in self.Char_P1.active_hitboxes:
            h.draw(window)
        for h in self.Char_P2.active_hitboxes:
            h.draw(window)
        #########

        # Fumée de hitstun
        self.smokeframe += 1
        self.smokeframe = self.smokeframe % 4
        if self.Char_P1.hitstun and self.smokeframe == 0:
            self.smoke.append(
                Smoke(self.Char_P1.rect.x + self.Char_P1.rect.w / 2, self.Char_P1.rect.y + self.Char_P1.rect.h / 2))
        if self.Char_P2.hitstun and self.smokeframe == 0:
            self.smoke.append(
                Smoke(self.Char_P2.rect.x + self.Char_P2.rect.w / 2, self.Char_P2.rect.y + self.Char_P2.rect.h / 2))
        for i, s in enumerate(self.smoke):
            s.draw(window)
            if s.duration <= 0:
                del self.smoke[i]

        # Affichage du stage
        stage.draw(window)

        # Affichage des personnages
        self.Char_P2.draw(window)
        self.Char_P1.draw(window)

        # Affichage des degats
        self.Char_P1.damages = float(self.Char_P1.damages)
        Texte(f"{str(round(self.Char_P1.damages, 2)).split('.')[0]}  %", ("Arial", 60, False, False), (
        255 - (self.Char_P1.damages / 5), max(255 - self.Char_P1.damages, 0), max(255 - self.Char_P1.damages * 2, 0)),
              width // 3, height - 50, 800, format_="left").draw(window)
        Texte(f".{str(round(self.Char_P1.damages, 2)).split('.')[1]}", ("Arial", 30, False, False), (
        255 - (self.Char_P1.damages / 5), max(255 - self.Char_P1.damages, 0), max(255 - self.Char_P1.damages * 2, 0)),
              width // 3 + len(str(round(self.Char_P1.damages, 2)).split('.')[0]) * 25, height - 30, 800,
              format_="left").draw(window)

        self.Char_P2.damages = float(self.Char_P2.damages)
        Texte(f"{str(round(self.Char_P2.damages, 2)).split('.')[0]}  %", ("Arial", 60, False, False), (
        255 - (self.Char_P2.damages / 5), max(255 - self.Char_P2.damages, 0), max(255 - self.Char_P2.damages * 2, 0)),
              2 * width // 3, height - 50, 800, format_="left").draw(window)
        Texte(f".{str(round(self.Char_P2.damages, 2)).split('.')[1]}", ("Arial", 30, False, False), (
        255 - (self.Char_P2.damages / 5), max(255 - self.Char_P2.damages, 0), max(255 - self.Char_P2.damages * 2, 0)),
              2 * width // 3 + len(str(round(self.Char_P2.damages, 2)).split('.')[0]) * 25, height - 30, 800,
              format_="left").draw(window)

        # Affichage des vies
        if not self.training:
            for s in range(self.stock[0] // 5 + 1):  # colonnes de 5 icones à côté des dégâts
                for k in range(min(self.stock[0] - 5 * s, 5)):
                    window.blit(pygame.transform.scale(icons[self.Char_P1.name], (16, 16)),
                                (width / 3 - 25 - 20 * s, height - 40 - 20 * k))

            for s in range(self.stock[1] // 5 + 1):
                for k in range(min(self.stock[1] - 5 * s, 5)):
                    window.blit(pygame.transform.scale(icons[self.Char_P2.name], (16, 16)),
                                (2 * width / 3 - 25 - 20 * s, height - 40 - 20 * k))

        #########################################################

        ###################### Gestion de la fin de la partie ######################
        if not self.training:
            s = self.time_game + (self.begin_game - time.time()) + self.pause_time  # calcul du temps restant
            ms = str(round(s * 100) / 100).split(".")[1]
            if len(ms) == 1:
                ms = ms + "0"
            s = str(round(s * 100) / 100).split(".")[0]
            m = int(s) // 60
            s = int(s) - m * 60

            # affichage du temps restant
            if m * 60 + s > 0 and self.game_running < 0:
                if m * 60 + s > 5:
                    s = str(s)
                    if len(s) == 1:
                        s = "0" + str(s)
                    Texte(f"{str(m)}:{str(s)}'{str(ms)}", ("Arial", 60, True, False), (255, 255, 255), width / 2,
                          75).draw(window)
                    s = int(s)
                else:
                    Texte(f"{str(s)}", ("Arial", 180, True, False), (100, 0, 0), width / 2, height / 2).draw(window)

            # fin de la partie
            if (m * 60 + s < 1 or min(self.stock) <= 0) and self.game_running < 0:
                self.game_running = 180  # attente de 3 secondes
                pygame.mixer.music.stop()
            if self.game_running > 0:
                Texte("FIN DU MATCH", ("Arial", 200, True, False), (150, 0, 0), width / 2, height / 2).draw(window)
                self.game_running -= 1
                if self.game_running < 1:
                    Play = False
                    musicplaying = False
                    Menu = "results"

        ############################################ Interface Entraînement ############################################

        if self.training:
            # Combo counter
            pygame.draw.rect(window, (250, 250, 250), (width - 120, height / 2, 120, 60))
            Texte(str(self.Char_P2.combo), ("Arial", 40, False, False), (0, 0, 0), width - 80, height / 2 + 25).draw(
                window)
            pygame.draw.rect(window, (250, 250, 250), (width - 120, height / 2 + 75, 120, 60))
            Texte(str(round(self.Char_P2.combodamages, 2)) + "%", ("Arial", 40, False, False), (0, 0, 0), width - 80,
                  height / 2 + 100).draw(window)

            # Menu
            if self.pause:
                if self.training:
                    # reset des dégâts
                    self.Char_P2.damages = self.basedamages
                    pygame.draw.rect(window, (180, 180, 180), (0, 0, 300, height))
                    # gestion de la confirmation
                    if not convert_inputs(controls[0], joysticks, 0)[6]:
                        self.confirm = False
                    # Haut/Bas pour naviguer dans le menu
                    self.focusedbutton = (self.focusedbutton + 1) % 10 - 1
                    if input_but_no_repeat(2, controls, joysticks, 0):
                        self.focusedbutton -= 1

                    if input_but_no_repeat(3, controls, joysticks, 0):
                        self.focusedbutton += 1

                    # Quitter
                    Bouton = Button(f"Quitter", ("Arial", 20, False, False), "./DATA/Images/Menu/Button.png", 150,
                                    height / 12, 200, 60)
                    if self.focusedbutton == -1:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not self.confirm:
                            self.confirm = True
                            Menu = "to char"
                            Play = False
                            self.pause = False
                            self.focusedbutton = 0
                            musicplaying = False
                            # reinitialisation des controles
                            controls = reset_commands(joysticks, commands)
                            clock.tick(10)
                    Bouton.draw(window)

                    # Bouton réinitialiser
                    Bouton = Button("Réinitialiser", ("Arial", 40, False, False), "./DATA/Images/Menu/Button.png", 150,
                                    2.5 * height / 12, 200, 60)
                    if self.focusedbutton == 0:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not self.confirm:
                            self.confirm = True
                            self.Char_P2 = Training(0, 0, 1)
                    Bouton.draw(window)

                    # Bouton de gestion de DI (Horizontale)
                    Bouton = Button(f"DI Horizontale : {['Aucune', 'Droite', 'Gauche'][self.TrainingHDI]}",
                                    ("Arial", 20, False, False), "./DATA/Images/Menu/Button.png", 150,
                                    3.5 * height / 12, 200, 60)
                    if self.focusedbutton == 1:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not self.confirm:
                            self.confirm = True
                            self.TrainingHDI += 1
                            self.TrainingHDI = (self.TrainingHDI + 1) % 3 - 1
                    Bouton.draw(window)

                    # Bouton de gestion de DI (Verticale)
                    Bouton = Button(f"DI Verticale : {['Aucune', 'Haut', 'Bas'][self.TrainingVDI]}",
                                    ("Arial", 20, False, False), "./DATA/Images/Menu/Button.png", 150,
                                    4.5 * height / 12, 200, 60)
                    if self.focusedbutton == 2:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not self.confirm:
                            self.confirm = True
                            self.TrainingVDI += 1
                            self.TrainingVDI = (self.TrainingVDI + 1) % 3 - 1
                    Bouton.draw(window)

                    # Bouton de probabilité de tech
                    Bouton = Button(f"Tech : {['Jamais', '1/2', 'Toujours'][self.Tech]}", ("Arial", 20, False, False),
                                    "./DATA/Images/Menu/Button.png", 150, 5.5 * height / 12, 200, 60)
                    if self.focusedbutton == 3:
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[6] and not self.confirm:
                            self.confirm = True
                            self.Tech += 1
                            self.Tech = (self.Tech + 1) % 3 - 1
                    Bouton.draw(window)

                    # Bouton de gestion des dégâts
                    Texte(f"Dégâts : {round(self.basedamages)}%", ("Arial", 20, False, False), (0, 0, 0), 150,
                          6.5 * height / 12 - 25).draw(window)
                    pygame.draw.rect(window, (10, 10, 10), (60, 6.5 * height / 12 - 2, 204, 4))
                    Bouton = Button(f"", ("Arial", 20, False, False), "./DATA/Images/Menu/Slider.png",
                                    self.basedamages / 999 * 200 + 60, 6.5 * height / 12, 12, 12)
                    if self.focusedbutton == 4:
                        Bouton.changeImage("./DATA/Images/Menu/Slider_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[1]:
                            self.basedamages += 1
                            if self.basedamages > 999:
                                self.basedamages = 0
                        if convert_inputs(controls[0], joysticks, 0)[0]:
                            self.basedamages -= 1
                            if self.basedamages < 0:
                                self.basedamages = 999
                        self.Char_P2.damages = self.basedamages
                    Bouton.draw(window)

                    ########################### Gestion des statistiques ###########################
                    Texte(f"Caractéristiques :", ("Arial black", 24, False, False), (0, 0, 0), 150,
                          7.5 * height / 12 - 20).draw(window)

                    #### Décélération 

                    Texte(f"Decéleration : {round(self.deceleration, 2)}", ("Arial", 20, True, False), (0, 0, 0), 150,
                          8 * height / 12 - 25).draw(window)
                    pygame.draw.rect(window, (10, 10, 10), (40, 8 * height / 12 + 3, 254, 4))
                    Bouton = Button(f"", ("Arial", 20, False, False), "./DATA/Images/Menu/Slider.png",
                                    (self.deceleration - 0.5) * 500 + 40, 8 * height / 12 + 5, 12, 12)
                    if self.focusedbutton == 5:
                        # Compris entre 0.5 et 1
                        Bouton.changeImage("./DATA/Images/Menu/Slider_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[1]:
                            self.deceleration += 0.005
                            if self.deceleration > 1:
                                self.deceleration = 1
                        if convert_inputs(controls[0], joysticks, 0)[0]:
                            self.deceleration -= 0.005
                            if self.deceleration < 0.5:
                                self.deceleration = 0.5
                    equal = []
                    # affichage des équivalents personnages
                    for p in Chars.decelerations:
                        window.blit(pygame.transform.scale(icons[p], (20, 20)),
                                    ((Chars.decelerations[p] - 0.5) * 500 + 30, 8 * height / 12 + 15))
                        if abs(self.deceleration - Chars.decelerations[p]) < 0.01 and (not (
                                convert_inputs(controls[0], joysticks, 0)[1] or
                                convert_inputs(controls[0], joysticks, 0)[0]) or self.focusedbutton != 5):
                            self.deceleration = Chars.decelerations[p]
                            equal.append(p)
                    if equal:
                        txt = ""
                        for e in equal:
                            txt += e + "/"
                        Texte(f"({txt[:-1]})", ("Arial", 15, False, False), (0, 0, 0), 150, 8 * height / 12 - 10).draw(
                            window)
                    Bouton.draw(window)

                    #### Vitesse aérienne 

                    Texte(f"Vitesse aérienne : {round(self.airspeed, 1)}", ("Arial", 20, True, False), (0, 0, 0), 150,
                          9 * height / 12 - 25).draw(window)
                    pygame.draw.rect(window, (10, 10, 10), (40, 9 * height / 12 + 3, 254, 4))
                    Bouton = Button(f"", ("Arial", 20, False, False), "./DATA/Images/Menu/Slider.png",
                                    (self.airspeed - 0.5) / 1.5 * 250 + 40, 9 * height / 12 + 5, 12, 12)
                    if self.focusedbutton == 6:
                        # Compris entre 0.5 et 2
                        Bouton.changeImage("./DATA/Images/Menu/Slider_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[1]:
                            self.airspeed += 0.05
                            if self.airspeed > 2:
                                self.airspeed = 2
                        if convert_inputs(controls[0], joysticks, 0)[0]:
                            self.airspeed -= 0.05
                            if self.airspeed < 0.5:
                                self.airspeed = 0.5
                    equal = []
                    # affichage des équivalents personnages
                    for p in Chars.airspeeds:
                        window.blit(pygame.transform.scale(icons[p], (20, 20)),
                                    ((Chars.airspeeds[p] - 0.5) / 1.5 * 250 + 30, 9 * height / 12 + 15))
                        if abs(self.airspeed - Chars.airspeeds[p]) < 0.03 and (not (
                                convert_inputs(controls[0], joysticks, 0)[1] or
                                convert_inputs(controls[0], joysticks, 0)[0]) or self.focusedbutton != 6):
                            self.airspeed = Chars.airspeeds[p]
                            equal.append(p)
                    if equal:
                        txt = ""
                        for e in equal:
                            txt += e + "/"
                        Texte(f"({txt[:-1]})", ("Arial", 15, False, False), (0, 0, 0), 150, 9 * height / 12 - 10).draw(
                            window)
                    Bouton.draw(window)

                    #### Vitesse de chute 

                    Texte(f"Vitesse de chute : {round(self.fallspeed, 1)}", ("Arial", 20, True, False), (0, 0, 0), 150,
                          10 * height / 12 - 25).draw(window)
                    pygame.draw.rect(window, (10, 10, 10), (40, 10 * height / 12 + 3, 254, 4))
                    Bouton = Button(f"", ("Arial", 20, False, False), "./DATA/Images/Menu/Slider.png",
                                    (self.fallspeed - 0.25) / 1.25 * 250 + 40, 10 * height / 12 + 5, 12, 12)
                    if self.focusedbutton == 7:
                        # Compris entre 0.25 et 1.5
                        Bouton.changeImage("./DATA/Images/Menu/Slider_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[1]:
                            self.fallspeed += 0.05
                            if self.fallspeed > 1.5:
                                self.fallspeed = 1.5
                        if convert_inputs(controls[0], joysticks, 0)[0]:
                            self.fallspeed -= 0.05
                            if self.fallspeed < 0.25:
                                self.fallspeed = 0.25
                    equal = []
                    # affichage des équivalents personnages
                    for p in Chars.fallspeeds:
                        window.blit(pygame.transform.scale(icons[p], (20, 20)),
                                    ((Chars.fallspeeds[p] - 0.25) / 1.25 * 250 + 30, 10 * height / 12 + 15))
                        if abs(self.fallspeed - Chars.fallspeeds[p]) < 0.03 and (not (
                                convert_inputs(controls[0], joysticks, 0)[1] or
                                convert_inputs(controls[0], joysticks, 0)[0]) or self.focusedbutton != 7):
                            self.fallspeed = Chars.fallspeeds[p]
                            equal.append(p)
                    if equal:
                        txt = ""
                        for e in equal:
                            txt += e + "/"
                        Texte(f"({txt[:-1]})", ("Arial", 15, False, False), (0, 0, 0), 150, 10 * height / 12 - 10).draw(
                            window)
                    Bouton.draw(window)

                    #### Vitesse de fastfall 

                    Texte(f"Vitesse de Fastfall : {round(self.fastfallspeed, 1)}", ("Arial", 20, True, False),
                          (0, 0, 0), 150, 11 * height / 12 - 25).draw(window)
                    pygame.draw.rect(window, (10, 10, 10), (40, 11 * height / 12 + 3, 254, 4))
                    Bouton = Button(f"", ("Arial", 20, False, False), "./DATA/Images/Menu/Slider.png",
                                    (self.fastfallspeed - 0.5) / 1.5 * 250 + 40, 11 * height / 12 + 5, 12, 12)
                    if self.focusedbutton == 8:
                        # Compris entre 0.5 et 2
                        Bouton.changeImage("./DATA/Images/Menu/Slider_focused.png")
                        if convert_inputs(controls[0], joysticks, 0)[1]:
                            self.fastfallspeed += 0.05
                            if self.fastfallspeed > 2:
                                self.fastfallspeed = 2
                        if convert_inputs(controls[0], joysticks, 0)[0]:
                            self.fastfallspeed -= 0.05
                            if self.fastfallspeed < 0.5:
                                self.fastfallspeed = 0.5
                    equal = []
                    # affichage des équivalents personnages
                    for p in Chars.fastfallspeeds:
                        window.blit(pygame.transform.scale(icons[p], (20, 20)),
                                    ((Chars.fastfallspeeds[p] - 0.5) / 1.5 * 250 + 30, 11 * height / 12 + 15))
                        if abs(self.fastfallspeed - Chars.fastfallspeeds[p]) < 0.03 and (not (
                                convert_inputs(controls[0], joysticks, 0)[1] or
                                convert_inputs(controls[0], joysticks, 0)[0]) or self.focusedbutton != 8):
                            self.fastfallspeed = Chars.fastfallspeeds[p]
                            equal.append(p)
                    if equal:
                        txt = ""
                        for e in equal:
                            txt += e + "/"
                        Texte(f"({txt[:-1]})", ("Arial", 15, False, False), (0, 0, 0), 150, 11 * height / 12 - 10).draw(
                            window)
                    Bouton.draw(window)
        #########################################################

        return Play, musicplaying, Menu, controls
