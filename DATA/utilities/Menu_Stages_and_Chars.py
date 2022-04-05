from DATA.utilities.functions import *
from DATA.utilities.Interface import *
from DATA.utilities.commands import commands
from DATA.assets.Stages import stages
import DATA.assets.CharsLoader as Chars
from DATA.assets.animations import icons64

class StagesMenu():
    def __init__(self,training,UIDicoEvent) -> None:
        self.training = training
        self.focused_button = 0
        self.confirm = True
        self.stage = 0

        if self.training :
            self.actualstages = ["Pandadrome"] + stages
        else :
            self.actualstages = stages
        
        self.UIDicoEvent = UIDicoEvent

    def update(self,window,controls,joysticks,width,height):
        Menu = "stage"

        if not convert_inputs(controls[0],joysticks,0)[6]:
            self.confirm = False
        
        # ajout du pandadrome (terrain d'entraînement)
        # haut/bas/gauche/droite pour naviguer dans le menu
        if input_but_no_repeat(3,controls,joysticks,0):
            self.focused_button += 9

        if input_but_no_repeat(2,controls,joysticks,0):
            self.focused_button -= 9

        if input_but_no_repeat(0,controls,joysticks,0):
            self.focused_button -= 1

        if input_but_no_repeat(1,controls,joysticks,0):
            self.focused_button += 1

        # bouclage de la navigation
        self.focused_button = ((self.focused_button+1)%(len(self.actualstages)+1))-1

        # retour
        Bouton = Button("<--",("arial",50,True,False),"./DATA/Images/Menu/Button.png",100,850,100,60)
        if self.focused_button == -1:
            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
            if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
                self.UIDicoEvent["UI1 back'"].play()
                Menu = "to char"
                self.confirm = True
        else :
            # Affichage du nom du stage sélectionné
            Texte(self.actualstages[self.focused_button],("arial",50,True,False),(0,0,0),30,height//2,format_="left").draw(window)
        Bouton.draw(window)

        # Boutons de sélection du stage
        for i in range(len(self.actualstages)):
            Bouton = Button("",("arial",50,True,False),"./DATA/Images/Menu/Button.png",((i%9)*150)+250,(i//9*150)+100,100,100)
            if self.focused_button == i :
                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")

                # setup du mennu personnage
                if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
                    self.UIDicoEvent["UI1 validation'"].play()
                    Menu = "game"
                    self.stage = i
            Bouton.draw(window)
            # image du stage
            window.blit(pygame.transform.scale(pygame.image.load(f"./DATA/Images/Stages/{self.actualstages[i]}/{self.actualstages[i]}.png"),(90,90)),((i%9*150)+205,(i//9*150)+55))
        return Menu

class CharsMenu():

    def __init__(self,training,UIDicoEvent):
        self.scroll1 = 0 # permet un scroll continu
        self.scroll2 = 0
        self.selectchar_1 = 0 # numéro du personnage sélectionné
        self.selectchar_2 = 0
        self.selected_1 = False # le joueur a-t-il choisi ?
        self.selected_2 = False
        # sens dans lequel le joueur défile les noms (gestion de la compatibilité entre la configuration et la manette)
        self.movename1 = -1
        self.movename2 = -1
        self.names = [0,0] # numéro des configurations
        self.namelist = [k for k in commands] # nom des configurations
        self.namelist.pop(0)
        self.b = 0 # temps de maintien du bouton B pour le retour
        self.confirm = True

        self.training = training

        self.alt = [0,0]

        self.UIDicoEvent = UIDicoEvent
    
    def update(self,window,width,height,controls,joysticks):
        chars = Chars.chars
        Menu = "char"

        if not convert_inputs(controls[0],joysticks,0)[6]:
            self.confirm = False

        # retour
        Bouton = Button("",("arial",30,True,False),"./DATA/Images/Menu/Button.png",width/2,40,100,60)
        # le retour se fait en maintenant le bouton B
        if not convert_inputs(controls[0],joysticks,0)[7]:
            self.b = 0
        else :
            self.b += 1
        if self.b > 0:
            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
        if self.b >= 10:
            self.UIDicoEvent["UI1 back'"].play()
            Menu = "main"
        Bouton.draw(window)
        Texte("<--",("arial",30,True,False),(0,0,0),width/2,25).draw(window)
        Texte("(B)",("arial",30,True,False),(0,0,0),width/2,50).draw(window)


        # Haut/Bas pour choisir un personnage
        if convert_inputs(controls[0],joysticks,0)[3] and not self.selected_1 and self.scroll1 == self.selectchar_1:
            self.UIDicoEvent["UI1 selection'"].play()
            self.alt[0] = 0
            self.selectchar_1 += 1
            self.scroll1 += 1
            self.scroll1 = self.scroll1%len(chars)
            self.scroll1 -= 1
            if self.selectchar_1 >= len(chars) :
                self.selectchar_1 = 0
        if convert_inputs(controls[0],joysticks,0)[2] and not self.selected_1 and self.scroll1 == self.selectchar_1:
            self.UIDicoEvent["UI1 selection'"].play()
            self.alt[0] = 0
            self.selectchar_1 -= 1
            self.scroll1 -= 1
            self.scroll1 = self.scroll1%len(chars)
            self.scroll1 += 1
            if self.selectchar_1 < 0 :
                self.selectchar_1 = len(chars) - 1
        # scroll continu
        if round(self.scroll1,1) < self.selectchar_1 :
            self.scroll1 += 0.25
            self.scroll1 = round(self.scroll1,3)
        if round(self.scroll1,1) > self.selectchar_1 :
            self.scroll1 -= 0.25
            self.scroll1 = round(self.scroll1,3)
        if round(self.scroll1,1) == self.selectchar_1 :
            self.scroll1 = self.selectchar_1

        # Confirmation / Annulation
        if convert_inputs(controls[0],joysticks,0)[6] and not self.confirm:
            if not self.selected_1:
                self.UIDicoEvent["UI1 validation'"].play()
            self.selected_1 = True
        if convert_inputs(controls[0],joysticks,0)[7]:
            if self.selected_1 :
                self.UIDicoEvent["UI1 error'"].play()
            self.selected_1 = False

        if self.training :

            ### Interface personnages P1
            for i in range(len(chars)):
                # Roulette
                if i < 5 :
                    Bouton = Button("",("arial",50,True,False),standard,0,105*(i-self.scroll1+len(chars)+4),384,100)
                    Bouton.draw(window)
                if len(chars) - i < 5 :
                    Bouton = Button("",("arial",50,True,False),standard,0,105*(i-self.scroll1-len(chars)+4),384,100)
                    Bouton.draw(window)
                Bouton = Button("",("arial",50,True,False),standard,0,105*(i-self.scroll1+4),384,100)
                if self.selectchar_1 == i :
                    Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                    Bouton.resize(400,100)
                Bouton.draw(window)
            for i in range(len(chars)):
                # icones sur la roulette
                if self.selectchar_1 == i :
                    window.blit(icons64[chars[i][self.alt[0]]],(64,105*(i-self.scroll1+4)-32))
                else :
                    window.blit(icons64[chars[i][0]],(64,105*(i-self.scroll1+4)-32))
                if i < 5 :
                    window.blit(icons64[chars[i][0]],(64,105*(i-self.scroll1+4+len(chars))-32))
                if len(chars) - i < 5 :
                    window.blit(icons64[chars[i][0]],(64,105*(i-self.scroll1+4-len(chars))-32))
            
            ### Interface personnages P2
            # Pandapluche (Peluche Panda des A-L)
            Bouton = Button("",("arial",50,True,False),standard,width,height/2,384,100)
            Bouton.draw(window)
            window.blit(pygame.transform.scale(pygame.image.load("./DATA/Images/Sprites/Misc/Training/Training_icon.png"),(64,64)),(width-128,height/2-32))
        
        else :   
             
            for i in range(len(chars)):
                ### Interface personnages P1
                # Roulette
                if i < 4 :
                    Bouton = Button("",("arial",50,True,False),standard,0,105*(i-self.scroll1+len(chars)+4),384,100)
                    Bouton.draw(window)
                if i - len(chars) > -5 :
                    Bouton = Button("",("arial",50,True,False),standard,0,105*(i-self.scroll1-len(chars)+4),384,100)
                    Bouton.draw(window)
                Bouton = Button("",("arial",50,True,False),standard,0,105*(i-self.scroll1+4),384,100)
                if self.selectchar_1 == i :
                    Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                    Bouton.resize(400,100)
                Bouton.draw(window)
        
                ### Interface personnages P2
                # Roulette
                if i < 4 :
                    Bouton = Button("",("arial",50,True,False),standard,width,105*(i-self.scroll2+len(chars)+4),384,100)
                    Bouton.draw(window)
                if i - len(chars) > -5 :
                    Bouton = Button("",("arial",50,True,False),standard,width,105*(i-self.scroll2-len(chars)+4),384,100)
                    Bouton.draw(window)
                Bouton = Button("",("arial",50,True,False),standard,width,105*(i-self.scroll2+4),384,100)
                if self.selectchar_2 == i :
                    Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                    Bouton.resize(400,100)
                Bouton.draw(window)

            for i in range(len(chars)):
                # icones sur la roulette
                if self.selectchar_1 == i :
                    window.blit(icons64[chars[i][self.alt[0]]],(64,105*(i-self.scroll1+4)-32))
                else :
                    window.blit(icons64[chars[i][0]],(64,105*(i-self.scroll1+4)-32))
                if self.selectchar_2 == i :
                    window.blit(icons64[chars[i][self.alt[1]]],(width-128,105*(i-self.scroll2+4)-32))
                else :
                    window.blit(icons64[chars[i][0]],(width-128,105*(i-self.scroll2+4)-32))

                if i - len(chars) > -5 :
                    window.blit(icons64[chars[i][0]],(64,105*(i-self.scroll1+4-len(chars))-32))
                    window.blit(icons64[chars[i][0]],(width-128,105*(i-self.scroll2+4-len(chars))-32))
                    
                if i < 4 :
                    window.blit(icons64[chars[i][0]],(64,105*(i-self.scroll1+4+len(chars))-32))
                    window.blit(icons64[chars[i][0]],(width-128,105*(i-self.scroll2+4+len(chars))-32))


            # Haut/Bas pour choisir un personnage
            if convert_inputs(controls[1],joysticks,1)[3] and not self.selected_2 and self.scroll2 == self.selectchar_2:
                self.UIDicoEvent["UI1 selection'"].play()
                self.alt[1] = 0
                self.selectchar_2 += 1
                self.scroll2 += 1
                self.scroll2 = self.scroll2%len(chars)
                self.scroll2 -= 1
                if self.selectchar_2 >= len(chars) :
                    self.selectchar_2 = 0
            if convert_inputs(controls[1],joysticks,1)[2] and not self.selected_2 and self.scroll2 == self.selectchar_2:
                self.UIDicoEvent["UI1 selection'"].play()
                self.alt[1] = 0
                self.selectchar_2 -= 1
                self.scroll2 -= 1
                self.scroll2 = self.scroll2%len(chars)
                self.scroll2 += 1
                if self.selectchar_2 < 0 :
                    self.selectchar_2 = len(chars) - 1
            # scroll continu
            if round(self.scroll2,1) < self.selectchar_2 :
                self.scroll2 += 0.25
                self.scroll2 = round(self.scroll2,3)
            if round(self.scroll2,1) > self.selectchar_2 :
                self.scroll2 -= 0.25
                self.scroll2 = round(self.scroll2,3)
            if round(self.scroll2,1) == self.selectchar_2 :
                self.scroll2 = self.selectchar_2

            # Confirmation / Annulation
            if convert_inputs(controls[1],joysticks,1)[6] and not self.confirm:
                if not self.selected_2:
                    self.UIDicoEvent["UI1 validation'"].play()
                self.selected_2 = True
            if convert_inputs(controls[1],joysticks,1)[7]:
                if self.selected_2:
                    self.UIDicoEvent["UI1 error'"].play()
                self.selected_2 = False

        # Choix du nom
        if self.names[0] == 0 :
            text = "Player 1"
        else :
            text = self.namelist[self.names[0]]
        Bouton = Button(text,("arial",24,True,False),"./DATA/Images/Menu/Button.png",3*width/10,height-150,200,32)
        Bouton.draw(window)
        # Test de compatibilité entre le nom et la manette
        try :
            convert_inputs(commands[self.namelist[self.names[0]]],joysticks,0)
        except :
            self.names[0] += self.movename1
            if self.names[0] >= len(self.namelist):
                self.names[0] = 0
        # Choix du nom avec les gâchettes
        if input_but_no_repeat(10,controls,joysticks,0):
            self.names[0] += 1
            self.movename1 = 1
            if self.names[0] == 1 : # Configuration du menu
                self.names[0] += 1
            if self.names[0] >= len(self.namelist):
                self.names[0] = 0
        if input_but_no_repeat(9,controls,joysticks,0):
            self.names[0] -= 1
            self.movename1 = -1
            if self.names[0] == 1 : # Configuration du menu
                self.names[0] -= 1
            if self.names[0] < 0:
                self.names[0] = len(self.namelist)-1

        # Choix du nom
        if self.names[1] == 0 :
            text = "Player 2"
        else :
            text = self.namelist[self.names[1]]
        Bouton = Button(text,("arial",24,True,False),"./DATA/Images/Menu/Button.png",7*width/10,height-150,200,32)
        Bouton.draw(window)
        # Test de compatibilité entre le nom et la manette
        try :
            convert_inputs(commands[self.namelist[self.names[1]]],joysticks,1)
        except :
            self.names[1] += self.movename2
            if self.names[1] >= len(self.namelist):
                self.names[1] = 0
        # Choix du nom avec les gâchettes
        if input_but_no_repeat(10,controls,joysticks,1):
            self.names[1] += 1
            self.movename2 = 1
            if self.names[1] == 1 : # Configuration du menu
                self.names[1] += 1
            if self.names[1] >= len(self.namelist):
                self.names[1] = 0
        if input_but_no_repeat(9,controls,joysticks,1):
            self.names[1] -= 1
            self.movename2 = -1
            if self.names[1] == 1 : # Configuration du menu
                self.names[1] -= 1
            if self.names[1] < 0:
                self.names[1] = len(self.namelist)-1

        # Changement de costume
        if input_but_no_repeat(4,controls,joysticks,0):
            self.alt[0] += 1
            if self.alt[0] >= len(chars[self.selectchar_1]) :
                self.alt[0] = 0
        if input_but_no_repeat(5,controls,joysticks,0):
            self.alt[0] -= 1
            if self.alt[0] < 0 :
                self.alt[0] = len(chars[self.selectchar_1])-1

        if input_but_no_repeat(4,controls,joysticks,1):
            self.alt[1] += 1
            if self.alt[1] >= len(chars[self.selectchar_2]) :
                self.alt[1] = 0
        if input_but_no_repeat(5,controls,joysticks,1):
            self.alt[1] -= 1
            if self.alt[1] < 0 :
                self.alt[1] = len(chars[self.selectchar_2])-1
        ##

        # Affichage si le joueur est prêt
        if self.selected_1 :
            pygame.draw.rect(window,(230,230,230),(width/8,height-120,width/4,30))
            Texte("PRET",("arial",24,True,False),(0,0,0),width/4,height-110,format_="center").draw(window)
        if self.selected_2 :
            pygame.draw.rect(window,(230,230,230),(5*width/8,height-120,width/4,30))
            Texte("PRET",("arial",24,True,False),(0,0,0),3*width/4,height-110,format_="center").draw(window)

        ## Affichage des noms
        pygame.draw.rect(window,(200,200,200),(0,height-90,width,90))
        Texte(str(Chars.charobjects[chars[self.selectchar_1][self.alt[0]]](0,0,0)),("arial",64,True,False),(0,0,0),width/2-30,height-50,format_="right").draw(window)
        if self.training :
            Texte("Pandapluche",("arial",64,True,False),(0,0,0),width/2+30,height-50,format_="left").draw(window)
        else :
            Texte(str(Chars.charobjects[chars[self.selectchar_2][self.alt[1]]](0,0,0)),("arial",64,True,False),(0,0,0),width/2+30,height-50,format_="left").draw(window)
        Texte("|",("arial",80,True,False),(0,0,0),width/2,height-50,format_="center").draw(window)
        ##
        
        if (self.selected_2 or self.training) and self.selected_1 :
            Menu = "to stage"
            # reset la confirmation du menu personnage (conserve en mémoire le dernier personnage et le nom choisi)
            self.selected_2 = False
            self.selected_1 = False
        
        return Menu