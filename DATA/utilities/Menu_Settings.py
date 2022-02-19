from DATA.utilities.functions import *
from DATA.utilities.Interface import *
from DATA.utilities.Entry import TextInput
import DATA.utilities.commands

class SettingsMenu():
    def __init__(self) -> None:
        self.menu = "settings"
        self.focusedbutton = 0
        self.row = 0
        self.commandconfig = None
        self.confirm = True
        self.inputget = -1
        self.getting = list()
        self.name = ""
        

    def update(self,window,width,height,events,controls,joysticks,musicvolume,soundvolume):
        oldmusicvolume = musicvolume
        oldsoundvolume = soundvolume

        if not convert_inputs(controls[0],joysticks,0)[6]:
            self.confirm = False

        Menu = "settings"
        if self.menu == "settings" :
        # inputs haut et bas pour se déplacer dans le menu
            if input_but_no_repeat(3,controls,joysticks,0):
                self.focusedbutton += 1

            if input_but_no_repeat(2,controls,joysticks,0):
                self.focusedbutton -= 1

            self.focusedbutton = self.focusedbutton%3

            # Bouton "Paramètres audio"
            Bouton = Button("Paramètres audio",("arial",50,True,False),"./DATA/Images/Menu/Button.png",width/2,height/3,600,100)
            if self.focusedbutton == 0:
                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
                    self.menu = "musics"
                    oldmusicvolume = musicvolume
                    oldsoundvolume = soundvolume
                    self.focusedbutton = 0
                    self.confirm = True
            Bouton.draw(window)

            # Bouton "Controles"
            Bouton = Button("Configuration des contrôles",("arial",50,True,False),"./DATA/Images/Menu/Button.png",width/2,2*height/3,600,100)
            if self.focusedbutton == 1:
                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
                    self.menu = "commands"
                    self.focusedbutton = 0
                    self.confirm = True
            Bouton.draw(window)

            # Retour
            Bouton = Button("<--",("arial",50,True,False),"./DATA/Images/Menu/Button.png",100,850,100,60)
            if self.focusedbutton == 2:
                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
                    Menu = "main"
                    self.confirm = True
            Bouton.draw(window)

        ######################################################################################################
        ##########################################  Menu commandes  ##########################################

        if self.menu == "musics":
            # inputs haut et bas pour se déplacer dans le menu
            if input_but_no_repeat(3,controls,joysticks,0):
                self.focusedbutton += 1

            if input_but_no_repeat(2,controls,joysticks,0):
                self.focusedbutton -= 1

            self.focusedbutton = self.focusedbutton%4

            #### Musique

            Texte(f"Volume musique : {round(musicvolume*100)}%",("Arial",20,True,False),(0,0,0),width/2,height/3-25).draw(window)
            pygame.draw.rect(window,(10,10,10),(width/2-122,height/3,254,4))
            Bouton = Button(f"",("Arial",20,False,False),"./DATA/Images/Menu/Slider.png",(musicvolume)*250+width/2-125,height/3,12,12)
            if self.focusedbutton == 0 :
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
            if self.focusedbutton == 1 :
                # Compris entre 0.5 et 1
                Bouton.changeImage("./DATA/Images/Menu/Slider_focused.png")
                if convert_inputs(controls[0],joysticks,0)[1] :
                    soundvolume += 0.01
                    if soundvolume > 1 :
                        soundvolume = 1
                    #if round(soundvolume,1) == round(soundvolume,2):
                        #playsound("DATA/Musics/SE/hits and slap/8bit hit.mp3")
                if convert_inputs(controls[0],joysticks,0)[0] :
                    soundvolume -= 0.01
                    if soundvolume < 0 :
                        soundvolume = 0
                    #if round(soundvolume,1) == round(soundvolume,2):
                        #playsound("DATA/Musics/SE/hits and slap/8bit hit.mp3")
                # Raffraichissement du volume du module qui exécute les sons
                # DATA.utilities.Sound_manager.soundvolume = soundvolume
            Bouton.draw(window)

            # Sauvegarder
            Bouton = Button("Sauvegarder",("arial",40,True,False),"./DATA/Images/Menu/Button.png",150,750,200,60)
            if self.focusedbutton == 2:
                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
                    with open("DATA/utilities/Settings.txt","w") as settings :
                        settings.write(f"Music :\nmusicvolume={round(musicvolume,2)}\nsoundvolume={round(soundvolume,2)}\n")
                    self.menu = "settings"
                    self.focusedbutton = 0
                    self.confirm = True
            Bouton.draw(window)

            # Annuler
            Bouton = Button("Annuler",("arial",40,True,False),"./DATA/Images/Menu/Button.png",150,850,200,60)
            if self.focusedbutton == 3:
                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
                    soundvolume = oldsoundvolume
                    musicvolume = oldmusicvolume
                    # DATA.utilities.Sound_manager.soundvolume = soundvolume
                    self.menu = "settings"
                    self.focusedbutton = 0
                    self.confirm = True
            Bouton.draw(window)


        ######################################################################################################
        ##########################################  Menu commandes  ##########################################

        if self.menu == "commands":

            #### Aucun profil sélectionné

            if self.commandconfig is None:
                # Haut/Bas pour se déplacer dans le menu
                if input_but_no_repeat(3,controls,joysticks,0):
                    self.focusedbutton += 1

                if input_but_no_repeat(2,controls,joysticks,0):
                    self.focusedbutton -= 1
                # bouclage du bouton
                self.focusedbutton = (self.focusedbutton+2)%(len(DATA.utilities.commands.commands)-1)-2
                # liste des commandes
                for i,n in enumerate(DATA.utilities.commands.commands) :
                    # on ne paramètre pas les configurations par défaut et du menu
                    if n not in ["Keyboard","Menu","DefaultKeyboard","Default"]:
                        Bouton = Button(n,("arial",24,False,False),"./DATA/Images/Menu/Button.png",width/2,(i+1)*60-180,120,50)
                        Bouton.resize(Bouton.textobject.width+20,50)
                        if self.focusedbutton == i-3:
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
                                self.commandconfig = n
                                self.inputget = -3
                                self.confirm = True
                        Bouton.draw(window)

                # Ajout d'un profil
                Bouton = Button("+",("arial",50,True,False),"./DATA/Images/Menu/Button.png",100,800,50,50)
                if self.focusedbutton == -2:
                    Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                    if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
                        self.commandconfig = 0
                        self.name = "Player"
                        self.confirm = True
                Bouton.draw(window)

                # Retour
                Bouton = Button("<--",("arial",50,True,False),"./DATA/Images/Menu/Button.png",100,850,100,60)
                if self.focusedbutton == -1:
                    Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                    if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
                        self.menu = "settings"
                        self.focusedbutton = 0
                        self.confirm = True
                Bouton.draw(window)

            #### Création d'un nouveau profil

            elif self.commandconfig == 0:
                # entrée texte pour créer le nom
                Entry = TextInput(self.name)
                enter = Entry.update(events)
                self.name = Entry.get_text()
                Texte("Enter name :  "+Entry.get_text(),("arial",30,False,False),(0,0,0),width/2,height/2).draw(window)
                Texte("<A/Enter to self.confirm>",("arial",30,False,False),(0,0,0),width/2,50+height/2).draw(window)
                if enter :
                    DATA.utilities.commands.commands[self.name] = DATA.utilities.commands.commands["Default"]
                    self.commandconfig = self.name
                    self.inputget = -1
                    self.confirm = True

            #### Modification d'un profil

            else :
                if self.inputget <= -1 :
                    # Haut/Bas/Gauche/Droite pour naviguer dans le menu
                    if input_but_no_repeat(3,controls,joysticks,0):
                        self.focusedbutton += 1

                    if input_but_no_repeat(2,controls,joysticks,0):
                        self.focusedbutton -= 1

                    if input_but_no_repeat(0,controls,joysticks,0):
                        self.row -= 1

                    if input_but_no_repeat(1,controls,joysticks,0):
                        self.row += 1
                # Bouclage de la sélection selon la colonne (donc le nombre de boutons dans la colonne)
                if self.row == 0 :
                    self.focusedbutton = ((self.focusedbutton+1)%5)-1
                if self.row == 1 :
                    self.focusedbutton = ((self.focusedbutton+1)%6)-1
                if self.row == 2 :
                    self.focusedbutton = ((self.focusedbutton+1)%5)-1
                if self.row == 3 :
                    self.focusedbutton = ((self.focusedbutton+1)%6)-1
                self.row = self.row%4 # bouclage de la colonne

                # Paramétrage des inputs
                if self.inputget > -1:

                    # attente de l'input
                    if get_controler_input(events,joysticks) and not self.confirm:
                        add = get_controler_input(events,joysticks)
                        for i in add :
                            if i not in self.getting :
                                self.getting.append(i)
                    # enregistrement de l'input
                    if not get_controler_input(events,joysticks) and self.getting :
                        DATA.utilities.commands.commands[self.commandconfig][self.inputget] = self.getting
                        self.inputget = -1
                        self.confirm = True
                        self.getting = list()

                # Stick
                for i,k in enumerate(DATA.utilities.commands.commands[self.commandconfig][0:4]):
                    draw_input(window,width/6,(i+1)*80,i,k,self.inputget,i,self.focusedbutton,self.row,0)
                    if self.focusedbutton == i and self.row == 0:
                        if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
                            self.inputget = i
                            self.confirm = True
                # Jump, Attack, Special, Shield
                for i,k in enumerate(DATA.utilities.commands.commands[self.commandconfig][4:9]):
                    draw_input(window,2*width/6,(i+1)*80,i+4,k,self.inputget,i,self.focusedbutton,self.row,1)
                    if self.focusedbutton == i and self.row == 1:
                        if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
                            self.inputget = i+4
                            self.confirm = True
                # C-Stick
                for i,k in enumerate(DATA.utilities.commands.commands[self.commandconfig][9:13]):
                    draw_input(window,4*width/6,(i+1)*80,i+9,k,self.inputget,i,self.focusedbutton,self.row,2)
                    if self.focusedbutton == i and self.row == 2:
                        if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
                            self.inputget = i+9
                            self.confirm = True
                # D-Pad + Pause
                for i,k in enumerate(DATA.utilities.commands.commands[self.commandconfig][13:]):
                    draw_input(window,5*width/6,(i+1)*80,i+13,k,self.inputget,i,self.focusedbutton,self.row,3)
                    if self.focusedbutton == i and self.row == 3:
                        if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
                            self.inputget = i+13
                            self.confirm = True
                # Sauvegarde
                Bouton = Button("Sauvegarder",("arial",50,True,False),"./DATA/Images/Menu/Button.png",200,850,250,60)
                if self.focusedbutton == -1 and self.row%2 == 0:
                    Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                    if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
                        with open("./DATA/utilities/commands.py","w") as commandfile :
                            commandfile.write("commands = {\n")
                            for k in DATA.utilities.commands.commands :
                                commandfile.write(f'\t"{k}":{DATA.utilities.commands.commands[k]},\n')
                            commandfile.write("}")

                        self.commandconfig = None
                        self.confirm = True
                Bouton.draw(window)

                # Suppression
                Bouton = Button("Supprimer",("arial",50,True,False),"./DATA/Images/Menu/Button.png",1450,850,200,60)
                if self.focusedbutton == -1 and self.row%2 == 1:
                    Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                    if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
                        del DATA.utilities.commands.commands[self.commandconfig]
                        with open("./DATA/utilities/commands.py","w") as commandfile :
                            commandfile.write("commands = {\n")
                            for k in DATA.utilities.commands.commands :
                                commandfile.write(f'\t"{k}":{DATA.utilities.commands.commands[k]},\n')
                            commandfile.write("}")

                        self.commandconfig = None
                        self.confirm = True
                Bouton.draw(window)
        return Menu#, musicvolume, soundvolume