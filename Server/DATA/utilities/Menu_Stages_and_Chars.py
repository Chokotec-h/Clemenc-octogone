from DATA.utilities.functions import *
from DATA.utilities.Interface import *
from DATA.utilities.commands import commands
from DATA.assets.Stages import stages
import DATA.assets.CharsLoader as Chars
from DATA.assets.animations import icons64

from DATA.utilities.Voicename import voicename

class StagesMenu:
    def __init__(self, training, UIDicoEvent) -> None:
        self.actualstages = None
        self.training = training
        self.focused_button = 0
        self.confirm = True
        self.stage = 0

        self.basicstages = stages

        self.UIDicoEvent = UIDicoEvent

    def update(self, window, controls, joysticks, width, height):

        # ajout du pandadrome (terrain d'entraînement)
        if self.training:
            self.actualstages = ["Pandadrome"] + stages
        else:
            self.actualstages = stages
        Menu = "stage"

        if not convert_inputs(controls[0], joysticks, 0)[6]:
            self.confirm = False

        # haut/bas/gauche/droite pour naviguer dans le menu
        if input_but_no_repeat(3, controls, joysticks, 0):
            self.UIDicoEvent["UI1 selection 2"].play()
            if self.focused_button == -1:
                self.focused_button = 0
            else :
                self.focused_button += 5
                if self.focused_button > len(self.actualstages) :
                    self.focused_button = -1

        if input_but_no_repeat(2, controls, joysticks, 0):
            self.UIDicoEvent["UI1 selection 2"].play()
            if self.focused_button == -1:
                self.focused_button = len(self.actualstages)-1
            else :
                self.focused_button -= 5
                if self.focused_button < -1 :
                    self.focused_button = -1

        if input_but_no_repeat(0, controls, joysticks, 0):
            self.UIDicoEvent["UI1 selection 2"].play()
            if self.focused_button != -1 :
                self.focused_button -= 1
                if self.focused_button < 0:
                    self.focused_button = len(self.actualstages)-1

        if input_but_no_repeat(1, controls, joysticks, 0):
            self.UIDicoEvent["UI1 selection 2"].play()
            if self.focused_button != -1 :
                self.focused_button += 1
                if self.focused_button > len(self.actualstages)-1:
                    self.focused_button = 0

        # bouclage de la navigation
        self.focused_button = ((self.focused_button + 1) % (len(self.actualstages) + 1)) - 1

        # retour
        Bouton = Button("<--", ("arial", resize(0,50,width,height)[1], True, False), "DATA/Images/Menu/Button.png", 100, height-resize(0,50,width,height)[1], resize(100,60,width,height))
        if self.focused_button == -1:
            Bouton.changeImage("DATA/Images/Menu/Button_focused.png")
            if convert_inputs(controls[0], joysticks, 0)[6] and not self.confirm:
                self.UIDicoEvent["UI1 back"].play()
                Menu = "to char"
                self.confirm = True
        else:
            # Affichage du nom du stage sélectionné
            Texte(self.actualstages[self.focused_button], ("arial", resize(0,50,width,height)[1]*0.8, True, False), (0, 0, 0), resize(20,0,width,height)[0], height // 2,
                  format_="left").draw(window)
        Bouton.draw(window)

        # Boutons de sélection du stage
        for i in range(len(self.actualstages)):
            Bouton = Button("", ("arial", 50, True, False), "DATA/Images/Menu/Button.png",
                            ((i % 5) * resize(250,0,width,height)[0]) + resize(450,0,width,height)[0], (i // 5 * resize(0,250,width,height)[1]) + resize(0,200,width,height)[1], resize(225,225,width,height))
            if self.focused_button == i:
                Bouton.changeImage("DATA/Images/Menu/Button_focused.png")

                # setup du mennu personnage
                if convert_inputs(controls[0], joysticks, 0)[6] and not self.confirm:
                    self.UIDicoEvent["UI1 ready"].play()

                    Menu = "game"
                    self.stage = i
            Bouton.draw(window)
            # image du stage
            window.blit(pygame.transform.scale(
                pygame.image.load(f"DATA/Images/Stages/{self.actualstages[i]}/{self.actualstages[i]}.png"), resize(216,216,width,height)),
                ((i % 5 * resize(250,0,width,height)[0]) - resize(108,0,width,height)[0] + resize(450,0,width,height)[0], (i // 5 * resize(0,250,width,height)[1]) - resize(0,108,width,height)[1] + resize(0,200,width,height)[1]))
        
        if self.focused_button == -1 :
            stage_sprite = pygame.image.load(f"DATA/Images/Stages/{self.actualstages[0]}/{self.actualstages[0]}.png")
            pygame.draw.rect(window,(0,0,0),(resize(50,0,width,height)[0],height//4,resize(stage_sprite.get_size()[0]*0.66,0,width,height)[0], resize(0,stage_sprite.get_size()[1]*0.66,width,height)[1]))
        else:
            stage_sprite = pygame.image.load(f"DATA/Images/Stages/{self.actualstages[self.focused_button]}/{self.actualstages[self.focused_button]}.png")
            window.blit(pygame.transform.scale(stage_sprite, (resize(stage_sprite.get_size()[0]*0.66,0,width,height)[0], resize(0,stage_sprite.get_size()[1]*0.66,width,height)[1])),
                (resize(50,0,width,height)[0], height//4))
        return Menu


class CharsMenu:

    def __init__(self, training, UIDicoEvent):
        self.scroll1 = 0  # permet un scroll continu
        self.scroll2 = 0
        self.selectchar_1 = 0  # numéro du personnage sélectionné
        self.selectchar_2 = 0
        self.selected_1 = False  # le joueur a-t-il choisi ?
        self.selected_2 = False
        # sens dans lequel le joueur défile les noms (gestion de la compatibilité entre la configuration et la manette)
        self.movename1 = -1
        self.movename2 = -1
        self.names = [0, 0]  # numéro des configurations
        self.namelist = [k for k in commands]  # nom des configurations
        self.namelist.pop(0)
        self.b = 0  # temps de maintien du bouton B pour le retour
        self.confirm = True

        self.training = training

        self.alt = [0, 0]

        self.UIDicoEvent = UIDicoEvent

    def update(self, window, width, height, controls, joysticks):
        chars = Chars.chars
        Menu = "char"

        if not convert_inputs(controls[0], joysticks, 0)[6]:
            self.confirm = False

        # retour
        Bouton = Button("", ("arial", 30, True, False), "DATA/Images/Menu/Button.png", width / 2, resize(0,40,width,height)[1], resize(100,75,width,height))
        # le retour se fait en maintenant le bouton B
        if not convert_inputs(controls[0], joysticks, 0)[7]:
            self.b = 0
        else:
            self.b += 1
        if self.b > 0:
            Bouton.changeImage("DATA/Images/Menu/Button_focused.png")
        if self.b >= 10:
            self.UIDicoEvent["UI1 back"].play()
            Menu = "main"
        Bouton.draw(window)
        Texte("<--", ("arial", resize(0,30,width,height)[1], True, False), (0, 0, 0), width / 2, resize(0,25,width,height)[1]).draw(window)
        key = "B" if len(joysticks) > 0 else "X"
        Texte(f"({key})", ("arial", resize(0,30,width,height)[1], True, False), (0, 0, 0), width / 2, resize(0,50,width,height)[1]).draw(window)

        # Haut/Bas pour choisir un personnage
        if convert_inputs(controls[0], joysticks, 0)[3] and not self.selected_1 and self.scroll1 == self.selectchar_1:
            self.UIDicoEvent["UI1 selection"].play()
            self.alt[0] = 0
            self.selectchar_1 += 1
            self.scroll1 += 1
            self.scroll1 = self.scroll1 % len(chars)
            self.scroll1 -= 1
            if self.selectchar_1 >= len(chars):
                self.selectchar_1 = 0
        if convert_inputs(controls[0], joysticks, 0)[2] and not self.selected_1 and self.scroll1 == self.selectchar_1:
            self.UIDicoEvent["UI1 selection"].play()
            self.alt[0] = 0
            self.selectchar_1 -= 1
            self.scroll1 -= 1
            self.scroll1 = self.scroll1 % len(chars)
            self.scroll1 += 1
            if self.selectchar_1 < 0:
                self.selectchar_1 = len(chars) - 1
        # scroll continu
        if round(self.scroll1, 1) < self.selectchar_1:
            self.scroll1 += 0.25
            self.scroll1 = round(self.scroll1, 3)
        if round(self.scroll1, 1) > self.selectchar_1:
            self.scroll1 -= 0.25
            self.scroll1 = round(self.scroll1, 3)
        if round(self.scroll1, 1) == self.selectchar_1:
            self.scroll1 = self.selectchar_1

        # Confirmation / Annulation
        if convert_inputs(controls[0], joysticks, 0)[6] and not self.confirm:
            if not self.selected_1:
                self.UIDicoEvent["UI1 validation"].play()
                self.UIDicoEvent["Voix"]["Personnages"][voicename[str(Chars.charobjects[chars[self.selectchar_1][self.alt[0]]](0, 0, 0))]].play()
            self.selected_1 = True
        if convert_inputs(controls[0], joysticks, 0)[7]:
            if self.selected_1:
                self.UIDicoEvent["UI1 error"].play()
            self.selected_1 = False

        if self.training:

            ### Interface personnages P1
            for i in range(len(chars)):
                # Roulette
                if i < 5:
                    Bouton = Button("", ("arial", 50, True, False), standard, 0,
                                    resize(0,105,width,height)[1] * (i - self.scroll1 + len(chars) + 4), resize(384,100,width,height))
                    Bouton.draw(window)
                if len(chars) - i < 5:
                    Bouton = Button("", ("arial", 50, True, False), standard, 0,
                                    resize(0,105,width,height)[1] * (i - self.scroll1 - len(chars) + 4), resize(384,100,width,height))
                    Bouton.draw(window)
                Bouton = Button("", ("arial", 50, True, False), standard, 0, resize(0,105,width,height)[1] * (i - self.scroll1 + 4), resize(384,100,width,height))
                if self.selectchar_1 == i:
                    Bouton.changeImage("DATA/Images/Menu/Button_focused.png")
                    Bouton.resize(resize(400,100,width,height)[0], resize(400,100,width,height)[1])
                Bouton.draw(window)
            for i in range(len(chars)):
                # icones sur la roulette
                if self.selectchar_1 == i:
                    window.blit(icons64[chars[i][self.alt[0]]], (resize(64,0,width,height)[0], resize(0,105,width,height)[1] * (i - self.scroll1 + 4) - resize(0,32,width,height)[1]))
                else:
                    window.blit(icons64[chars[i][0]], (resize(64,0,width,height)[0], resize(0,105,width,height)[1] * (i - self.scroll1 + 4) - resize(0,32,width,height)[1]))
                if i < 5:
                    window.blit(icons64[chars[i][0]], (resize(64,0,width,height)[0], resize(0,105,width,height)[1] * (i - self.scroll1 + 4 + len(chars)) - resize(0,32,width,height)[1]))
                if len(chars) - i < 5:
                    window.blit(icons64[chars[i][0]], (resize(64,0,width,height)[0], resize(0,105,width,height)[1] * (i - self.scroll1 + 4 - len(chars)) - resize(0,32,width,height)[1]))

            ### Interface personnages P2
            # Pandapluche (Peluche Panda des A-L)
            Bouton = Button("", ("arial", 50, True, False), standard, width, height / 2, resize(384,100,width,height))
            Bouton.draw(window)
            window.blit(
                pygame.transform.scale(pygame.image.load("DATA/Images/Sprites/Misc/Training/Training_icon.png"),
                                        resize(64,64,width,height)), (width - resize(64,0,width,height)[0] - resize(0,64,width,height)[1], height / 2 - resize(0,32,width,height)[1]))

        else:

            for i in range(len(chars)):
                ### Interface personnages P1
                # Roulette
                if i < 4:
                    Bouton = Button("", ("arial", 50, True, False), standard, 0,
                                    resize(0,105,width,height)[1] * (i - self.scroll1 + len(chars) + 4), resize(384,100,width,height))
                    Bouton.draw(window)
                if i - len(chars) > -5:
                    Bouton = Button("", ("arial", 50, True, False), standard, 0,
                                    resize(0,105,width,height)[1] * (i - self.scroll1 - len(chars) + 4), resize(384,100,width,height))
                    Bouton.draw(window)
                Bouton = Button("", ("arial", 50, True, False), standard, 0, resize(0,105,width,height)[1] * (i - self.scroll1 + 4), resize(384,100,width,height))
                if self.selectchar_1 == i:
                    Bouton.changeImage("DATA/Images/Menu/Button_focused.png")
                    Bouton.resize(resize(400,100,width,height)[0], resize(400,100,width,height)[1])
                Bouton.draw(window)

                ### Interface personnages P2
                # Roulette
                if i < 4:
                    Bouton = Button("", ("arial", 50, True, False), standard, width,
                                    resize(0,105,width,height)[1] * (i - self.scroll2 + len(chars) + 4), resize(384,100,width,height))
                    Bouton.draw(window)
                if i - len(chars) > -5:
                    Bouton = Button("", ("arial", 50, True, False), standard, width,
                                    resize(0,105,width,height)[1] * (i - self.scroll2 - len(chars) + 4), resize(384,100,width,height))
                    Bouton.draw(window)
                Bouton = Button("", ("arial", 50, True, False), standard, width, resize(0,105,width,height)[1] * (i - self.scroll2 + 4), resize(384,100,width,height))
                if self.selectchar_2 == i:
                    Bouton.changeImage("DATA/Images/Menu/Button_focused.png")
                    Bouton.resize(resize(400,100,width,height)[0], resize(400,100,width,height)[1])
                Bouton.draw(window)

            for i in range(len(chars)):
                # icones sur la roulette
                if self.selectchar_1 == i:
                    window.blit(icons64[chars[i][self.alt[0]]], (resize(64,0,width,height)[0], resize(0,105,width,height)[1] * (i - self.scroll1 + 4) - resize(0,32,width,height)[1]))
                else:
                    window.blit(icons64[chars[i][0]], (resize(64,0,width,height)[0], resize(0,105,width,height)[1] * (i - self.scroll1 + 4) - resize(0,32,width,height)[1]))
                if self.selectchar_2 == i:
                    window.blit(icons64[chars[i][self.alt[1]]], (width - resize(64,0,width,height)[0] - resize(0,64,width,height)[1], resize(0,105,width,height)[1] * (i - self.scroll2 + 4) - resize(0,32,width,height)[1]))
                else:
                    window.blit(icons64[chars[i][0]], (width - resize(64,0,width,height)[0] - resize(0,64,width,height)[1], resize(0,105,width,height)[1] * (i - self.scroll2 + 4) - resize(0,32,width,height)[1]))

                if i - len(chars) > -5:
                    window.blit(icons64[chars[i][0]], (resize(64,0,width,height)[0], resize(0,105,width,height)[1] * (i - self.scroll1 + 4 - len(chars)) - resize(0,32,width,height)[1]))
                    window.blit(icons64[chars[i][0]], (width - resize(64,0,width,height)[0] - resize(0,64,width,height)[1], resize(0,105,width,height)[1] * (i - self.scroll2 + 4 - len(chars)) - resize(0,32,width,height)[1]))

                if i < 4:
                    window.blit(icons64[chars[i][0]], (resize(64,0,width,height)[0], resize(0,105,width,height)[1] * (i - self.scroll1 + 4 + len(chars)) - resize(0,32,width,height)[1]))
                    window.blit(icons64[chars[i][0]], (width - resize(64,0,width,height)[0] - resize(0,64,width,height)[1], resize(0,105,width,height)[1] * (i - self.scroll2 + 4 + len(chars)) - resize(0,32,width,height)[1]))

            # Haut/Bas pour choisir un personnage
            if convert_inputs(controls[1], joysticks, 1)[
                3] and not self.selected_2 and self.scroll2 == self.selectchar_2:
                self.UIDicoEvent["UI1 selection 2"].play()
                self.alt[1] = 0
                self.selectchar_2 += 1
                self.scroll2 += 1
                self.scroll2 = self.scroll2 % len(chars)
                self.scroll2 -= 1
                if self.selectchar_2 >= len(chars):
                    self.selectchar_2 = 0
            if convert_inputs(controls[1], joysticks, 1)[
                2] and not self.selected_2 and self.scroll2 == self.selectchar_2:
                self.UIDicoEvent["UI1 selection 2"].play()
                self.alt[1] = 0
                self.selectchar_2 -= 1
                self.scroll2 -= 1
                self.scroll2 = self.scroll2 % len(chars)
                self.scroll2 += 1
                if self.selectchar_2 < 0:
                    self.selectchar_2 = len(chars) - 1
            # scroll continu
            if round(self.scroll2, 1) < self.selectchar_2:
                self.scroll2 += 0.25
                self.scroll2 = round(self.scroll2, 3)
            if round(self.scroll2, 1) > self.selectchar_2:
                self.scroll2 -= 0.25
                self.scroll2 = round(self.scroll2, 3)
            if round(self.scroll2, 1) == self.selectchar_2:
                self.scroll2 = self.selectchar_2

            # Confirmation / Annulation
            if convert_inputs(controls[1], joysticks, 1)[6] and not self.confirm:
                if not self.selected_2:
                    self.UIDicoEvent["UI1 validation"].play()
                    self.UIDicoEvent["Voix"]["Personnages"][voicename[str(Chars.charobjects[chars[self.selectchar_2][self.alt[1]]](0, 0, 0))]].play()
                self.selected_2 = True
            if convert_inputs(controls[1], joysticks, 1)[7]:
                if self.selected_2:
                    self.UIDicoEvent["UI1 error"].play()
                self.selected_2 = False

        # Choix du nom
        if self.names[0] == 0:
            name = "Player 1"
        else:
            name = self.namelist[self.names[0]]
        Bouton = Button(name, ("arial", resize(0,24,width,height)[1], True, False), "DATA/Images/Menu/Button.png", 3 * width / 10, height - resize(0,200,width,height)[1],
                        resize(200,32,width,height))
        Bouton.draw(window)
        # Test de compatibilité entre le nom et la manette
        try:
            convert_inputs(commands[self.namelist[self.names[0]]], joysticks, 0)
            if self.names[0] == 1:
                self.names[0] += self.movename1
        except:
            self.names[0] += self.movename1
            if self.names[0] >= len(self.namelist):
                self.names[0] = 0
        # Choix du nom avec les gâchettes
        if input_but_no_repeat(10, controls, joysticks, 0):
            self.names[0] += 1
            self.movename1 = 1
            if self.names[0] == 1:  # Configuration du menu
                self.names[0] += 1
            if self.names[0] >= len(self.namelist):
                self.names[0] = 0
        if input_but_no_repeat(9, controls, joysticks, 0):
            self.names[0] -= 1
            self.movename1 = -1
            if self.names[0] == 1:  # Configuration du menu
                self.names[0] -= 1
            if self.names[0] < 0:
                self.names[0] = len(self.namelist) - 1

        # Choix du nom
        if self.names[1] == 0:
            name = "Player 2"
        else:
            name = self.namelist[self.names[1]]
        Bouton = Button(name, ("arial", resize(0,24,width,height)[1], True, False), "DATA/Images/Menu/Button.png", 7 * width / 10, height - resize(0,200,width,height)[1],
                        resize(200,32,width,height))
        Bouton.draw(window)
        # Test de compatibilité entre le nom et la manette
        try:
            convert_inputs(commands[self.namelist[self.names[1]]], joysticks, 1)
            if self.names[1] == 1:
                self.names[1] += self.movename2
        except:
            self.names[1] += self.movename2
            if self.names[1] >= len(self.namelist):
                self.names[1] = 0
        # Choix du nom avec les gâchettes
        if input_but_no_repeat(10, controls, joysticks, 1):
            self.names[1] += 1
            self.movename2 = 1
            if self.names[1] == 1:  # Configuration du menu
                self.names[1] += 1
            if self.names[1] >= len(self.namelist):
                self.names[1] = 0
        if input_but_no_repeat(9, controls, joysticks, 1):
            self.names[1] -= 1
            self.movename2 = -1
            if self.names[1] == 1:  # Configuration du menu
                self.names[1] -= 1
            if self.names[1] < 0:
                self.names[1] = len(self.namelist) - 1

        # Changement de costume
        if input_but_no_repeat(4, controls, joysticks, 0):
            self.alt[0] += 1
            if self.alt[0] >= len(chars[self.selectchar_1]):
                self.alt[0] = 0
        if input_but_no_repeat(5, controls, joysticks, 0):
            self.alt[0] -= 1
            if self.alt[0] < 0:
                self.alt[0] = len(chars[self.selectchar_1]) - 1

        if input_but_no_repeat(4, controls, joysticks, 1):
            self.alt[1] += 1
            if self.alt[1] >= len(chars[self.selectchar_2]):
                self.alt[1] = 0
        if input_but_no_repeat(5, controls, joysticks, 1):
            self.alt[1] -= 1
            if self.alt[1] < 0:
                self.alt[1] = len(chars[self.selectchar_2]) - 1
        ##

        # Affichage si le joueur est prêt
        if self.selected_1:
            pygame.draw.rect(window, (230, 230, 230), (width / 8, height - resize(0,150,width,height)[1], width / 4, 30))
            Texte("PRET", ("arial", 24, True, False), (0, 0, 0), width / 4, height - resize(0,110+24,width,height)[1], format_="center").draw(window)
        if self.selected_2:
            pygame.draw.rect(window, (230, 230, 230), (5 * width / 8, height - resize(0,150,width,height)[1], width / 4, 30))
            Texte("PRET", ("arial", 24, True, False), (0, 0, 0), 3 * width / 4, height - resize(0,110+24,width,height)[1], format_="center").draw(
                window)

        # Affichage des noms
        pygame.draw.rect(window, (200, 200, 200), (0, height - resize(0,90,width,height)[1], width, resize(0,90,width,height)[1]))
        Texte(str(Chars.charobjects[chars[self.selectchar_1][self.alt[0]]](0, 0, 0)), ("arial", resize(0,64,width,height)[1], True, False),
              (0, 0, 0), width / 2 - 30, height - resize(0,50,width,height)[1], format_="right").draw(window)
        if self.training:
            Texte("Pandapluche", ("arial", resize(0,64,width,height)[1], True, False), (0, 0, 0), width / 2 + 30, height - resize(0,50,width,height)[1],
                  format_="left").draw(window)
        else:
            Texte(str(Chars.charobjects[chars[self.selectchar_2][self.alt[1]]](0, 0, 0)), ("arial", resize(0,64,width,height)[1], True, False),
                  (0, 0, 0), width / 2 + 30, height - resize(0,50,width,height)[1], format_="left").draw(window)
        Texte("|", ("arial", resize(0,80,width,height)[1], True, False), (0, 0, 0), width / 2, height - resize(0,50,width,height)[1], format_="center").draw(window)
        ##

        if (self.selected_2 or self.training) and self.selected_1:
            Menu = "to stage"
            # reset la confirmation du menu personnage (conserve en mémoire le dernier personnage et le nom choisi)
            self.selected_2 = False
            self.selected_1 = False

        return Menu
