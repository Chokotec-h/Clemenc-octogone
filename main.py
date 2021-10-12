import pygame
import traceback

from pygame.constants import MOUSEBUTTONDOWN
import DATA.assets.CharsLoader as Chars
import DATA.assets.Stages as Stages
from DATA.assets.Misc import *
from DATA.utilities.Interface import *
from DATA.utilities.Gamepad_gestion import *
from DATA.assets.animations import icons
from commands import *
from DATA.utilities.Entry import *

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

def get_controler_input():
    controls = []
    for joystick in joysticks:
        inputs = get_inputs(joystick)
        for i in inputs :
            if len(i) > 3 :
                if i[0] == "D-Pad":
                    if i not in controls[0] + controls[1]:
                        controls.append(i)
                else :
                    if abs(i[-1]) > 0.3 and abs(i[-1]) != 1:
                        move = list(i[0:3])+[signe(i[-1])]
                        if move not in controls[0] + controls[1]:
                            controls.append(move)
            else :
                if i not in controls[0] + controls[1]:
                    controls.append(i)
    if controls :
        controls[0].pop(1)
        return controls[0]

### Version bêta
def setup_controls(window,width,height,joysticks):
    controls = [[],[]]
    player = 0
    run = True
    # liste des action
    actions = ("Left","Right","Up","Down","Fullhop","Shorthop","Attack","Special","Shield","C-Stick Left","C-Stick Right","C-Stick Up","C-Stick Down","D-Pad Left","D-Pad Right","D-Pad Up","D-Pad Down","Pause")
    while run :
        window.fill((200,220,200))
        events = pygame.event.get
        for e in events:
            if e.type == pygame.QUIT:
                run = False
            # Récupération des inputs claviers
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if len(controls[player]) > 0:
                        controls[player].pop()
                    else :
                        player = 0
                        if len(controls[player]) > 0:
                            controls[player].pop()
                elif ("Keyboard",e.key) not in controls[int(not player)]:
                    controls[player].append(("Keyboard",e.key))
        # récupération des inputs manette
        for joystick in joysticks:
            inputs = get_inputs(joystick)
            for i in inputs :
                if len(i) > 3 :
                    if i[0] == "D-Pad":
                        if i not in controls[0] + controls[1]:
                           controls[player].append(i)
                    else :
                        if abs(i[-1]) > 0.3 and abs(i[-1]) != 1:
                            move = list(i[0:3])+[signe(i[-1])]
                            if move not in controls[0] + controls[1]:
                                controls[player].append(move)
                else :
                    if i not in controls[0] + controls[1]:
                        controls[player].append(i)
        # affichage des contrôles
        for i,action in enumerate(actions):
            Texte(action,("Arial",18,False,False),(0,0,0),width//3,(i+1)*height//20,800).draw(window)
            if len(controls[0]) > i :
                Texte(str(controls[0][i]),("Arial",18,False,False),(0,0,0),width//2,(i+1)*height//20,800).draw(window)
            elif len(controls[0]) == i :
                Texte("<input>",("Arial",18,False,True),(0,0,0),width//2,(i+1)*height//20,800).draw(window)
            if len(controls[1]) > i :
                Texte(str(controls[1][i]),("Arial",18,False,False),(0,0,0),2*width//3,(i+1)*height//20,800).draw(window)
            elif len(controls[1]) == i and player == 1:
                Texte("<input>",("Arial",18,False,True),(0,0,0),2*width//3,(i+1)*height//20,800).draw(window)
        if len(controls[0]) >= len(actions):
            player = 1
        if len(controls[1]) >= len(actions):
            return run, controls
        pygame.display.flip()
    return run, controls



def main():
    """"""""""""""""""""""""""""""""""""
    """""""""Progamme Principal"""""""""
    """"""""""""""""""""""""""""""""""""

    # initialisation de la fenêtre
    width = 1600
    height = 900
    window = pygame.display.set_mode((width, height))

    # Déclaration des variables
    smoke = list()
    smokeframe  = 0

    # test de music et de bruitages
    pygame.mixer.music.load("DATA/Musics/intro_.mp3")
    #pygame.mixer.music.play()
    soundReady = True

    try:

        #run,controls = setup_controls(window,width,height,joysticks) # Version test de modif des contrôles
        run = True
        controls = [commands["Default"],commands["Default"]]
        pause = False
        hold_pause = False
        Play = False
        Menu = "main"
        commandconfig = None
        musicplaying = False
        while run:  # Boucle du programme

            click = False
            # Récupération des events
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT: # Bouton croix en haut à droite de l'écran
                    run = False
                if e.type == pygame.MOUSEBUTTONDOWN:
                    click = True

            if not Play :
                window.fill((153,102,255))
                if Menu == "main":
                    Bouton = Button("Play",("arial",50,True,False),"./DATA/Images/Menu/Button.png",width/2,height/4,250,100)
                    if Bouton.is_focused():
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                    Bouton.draw(window)
                    if Bouton.is_clicked(click):
                        Menu = "stage"
                        click = False
                    Bouton = Button("Settings",("arial",50,True,False),"./DATA/Images/Menu/Button.png",width/2,height/2,250,100)
                    if Bouton.is_focused():
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                    Bouton.draw(window)
                    if Bouton.is_clicked(click):
                        Menu = "commands"
                        click = False

                # MENU COMMANDES
                if Menu == "commands":
                    if commandconfig is None:
                        for i,n in enumerate(commands) :
                            if n != "Default":
                                Bouton = Button(n,("arial",24,False,False),"./DATA/Images/Menu/Button.png",100,(i+1)*60,120,50)
                                if Bouton.is_focused():
                                    Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                                if Bouton.is_clicked(click):
                                    commandconfig = n
                                    inputget = -1
                                Bouton.draw(window)
                        Bouton = Button("+",("arial",50,True,False),"./DATA/Images/Menu/Button.png",100,800,50,50)
                        if Bouton.is_focused():
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        Bouton.draw(window)
                        if Bouton.is_clicked(click):
                            commandconfig = 0
                            name = "Player"
                        Bouton = Button("Back",("arial",50,True,False),"./DATA/Images/Menu/Button.png",100,850,100,60)
                        if Bouton.is_focused():
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if Bouton.is_clicked(click):
                            Menu = "main"
                        Bouton.draw(window)
                    elif commandconfig == 0:
                        Entry = TextInput(name)
                        Entry.update(events)
                        name = Entry.get_text()
                        Texte("Enter name :  "+Entry.get_text(),("arial",30,False,False),(0,0,0),width/2,height/2).draw(window)
                        Bouton = Button("OK",("arial",50,True,False),"./DATA/Images/Menu/Button.png",100,850,50,50)
                        if Bouton.is_focused():
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        Bouton.draw(window)
                        if Bouton.is_clicked(click):
                            commands[name] = commands["Default"]
                            commandconfig = name
                            inputget = -1
                    else :
                        if inputget > -1:
                            if get_controler_input():
                                commands[commandconfig][inputget] = get_controler_input()
                                inputget = -1
                        # Stick
                        for i,k in enumerate(commands[commandconfig][0:4]):
                            if inputget == i :
                                text = "[input]"
                            else :
                                text = str(k)
                            Bouton = Button(text,("arial",24,True,False),"./DATA/Images/Menu/Button.png",width/6,(i+1)*80,200,60)
                            if Bouton.is_focused():
                                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            if Bouton.is_clicked(click):
                                inputget = i
                            Bouton.draw(window)
                        # Jump, Attack, Special, Shield
                        for i,k in enumerate(commands[commandconfig][4:9]):
                            if inputget == i+4 :
                                text = "[input]"
                            else :
                                text = str(k)
                            Bouton = Button(text,("arial",24,True,False),"./DATA/Images/Menu/Button.png",2*width/6,(i+1)*80,200,60)
                            if Bouton.is_focused():
                                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            if Bouton.is_clicked(click):
                                inputget = i+4
                            Bouton.draw(window)
                        # C-Stick
                        for i,k in enumerate(commands[commandconfig][9:13]):
                            if inputget == i+9 :
                                text = "[input]"
                            else :
                                text = str(k)
                            Bouton = Button(text,("arial",24,True,False),"./DATA/Images/Menu/Button.png",4*width/6,(i+1)*80,200,60)
                            if Bouton.is_focused():
                                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            if Bouton.is_clicked(click):
                                inputget = i+9
                            Bouton.draw(window)
                        # D-Pad + Pause
                        for i,k in enumerate(commands[commandconfig][13:]):
                            if inputget == i+13 :
                                text = "[input]"
                            else :
                                text = str(k)
                            Bouton = Button(text,("arial",24,True,False),"./DATA/Images/Menu/Button.png",5*width/6,(i+1)*80,200,60)
                            if Bouton.is_focused():
                                Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            if Bouton.is_clicked(click):
                                inputget = i+13
                            Bouton.draw(window)
                        Bouton = Button("Save",("arial",50,True,False),"./DATA/Images/Menu/Button.png",100,850,100,60)
                        if Bouton.is_focused():
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        if Bouton.is_clicked(click):
                            with open("./commands.py","w") as commandfile :
                                commandfile.write("commands = {\n")
                                for k in commands :
                                    commandfile.write(f'\t"{k}":{commands[k]},\n')
                                commandfile.write("}")

                            commandconfig = None
                        Bouton.draw(window)
                            
                                
                if Menu == "stage":
                    Bouton = Button("",("arial",50,True,False),"./DATA/Images/Menu/Button.png",100,100,100,100)
                    if Bouton.is_focused() :
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                        Bouton.resize(100,100)
                    Bouton.draw(window)
                    if Bouton.is_clicked(click):
                        Menu = "char"
                        selectchar_1 = 0
                        selectchar_2 = 0
                        selected_1 = False
                        selected_2 = False
                        stage = 0
                        click = False
                        names = [0,0]
                        namelist = [k for k in commands]
                if Menu == "char":
                    chars = ["Balan","Joueur de air-president","Millet","Gregoire","Balan"]
                    ### P1
                    for i in range(len(chars)):
                        Bouton = Button("",("arial",50,True,False),"./DATA/Images/Menu/Button.png",200,105*(i-selectchar_1-len(chars)+4),400,100)
                        Bouton.draw(window)
                        Bouton = Button("",("arial",50,True,False),"./DATA/Images/Menu/Button.png",200,105*(i-selectchar_1+len(chars)+4),400,100)
                        Bouton.draw(window)
                        Bouton = Button("",("arial",50,True,False),"./DATA/Images/Menu/Button.png",200,105*(i-selectchar_1+4),400,100)
                        if selectchar_1 == i :
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            Bouton.resize(400,100)
                        Bouton.draw(window)
                    for i in range(len(chars)):
                        window.blit(pygame.transform.scale(pygame.image.load(icons[chars[i]]),(64,64)),(168,105*(i-selectchar_1+4)-32))
                        window.blit(pygame.transform.scale(pygame.image.load(icons[chars[i]]),(64,64)),(168,105*(i-selectchar_1+4-len(chars))-32))
                        window.blit(pygame.transform.scale(pygame.image.load(icons[chars[i]]),(64,64)),(168,105*(i-selectchar_1+4+len(chars))-32))
                    Bouton = Button("",("arial",50,True,False),"./DATA/Images/Menu/Down.png",width/3,800,20,20,not selected_1)
                    Bouton.draw(window)
                    if Bouton.is_clicked(click) and not selected_1:
                        selectchar_1 += 1
                        if selectchar_1 >= len(chars) :
                            selectchar_1 = 0
                        click = False
                    Bouton = Button("",("arial",50,True,False),"./DATA/Images/Menu/Up.png",width/3,50,20,20,not selected_1)
                    Bouton.draw(window)
                    if Bouton.is_clicked(click) and not selected_1:
                        selectchar_1 -= 1
                        if selectchar_1 < 0 :
                            selectchar_1 = len(chars) - 1
                        click = False

                    ### P2
                    for i in range(len(chars)):
                        # Buttons
                        Bouton = Button("",("arial",50,True,False),"./DATA/Images/Menu/Button.png",width-200,105*(i-selectchar_2-len(chars)+4),400,100)
                        Bouton.draw(window)
                        Bouton = Button("",("arial",50,True,False),"./DATA/Images/Menu/Button.png",width-200,105*(i-selectchar_2+len(chars)+4),400,100)
                        Bouton.draw(window)
                        Bouton = Button("",("arial",50,True,False),"./DATA/Images/Menu/Button.png",width-200,105*(i-selectchar_2+4),400,100)
                        if selectchar_2 == i :
                            Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                            Bouton.resize(400,100)
                        Bouton.draw(window)
                    # Sprites
                    for i in range(len(chars)):
                        window.blit(pygame.transform.scale(pygame.image.load(icons[chars[i]]),(64,64)),(width-232,105*(i-selectchar_2+4)-32))
                        window.blit(pygame.transform.scale(pygame.image.load(icons[chars[i]]),(64,64)),(width-232,105*(i-selectchar_2+4-len(chars))-32))
                        window.blit(pygame.transform.scale(pygame.image.load(icons[chars[i]]),(64,64)),(width-232,105*(i-selectchar_2+4+len(chars))-32))
                    # Arrows
                    Bouton = Button("",("arial",50,True,False),"./DATA/Images/Menu/Down.png",2*width/3,800,20,20,not selected_2)
                    Bouton.draw(window)
                    if Bouton.is_clicked(click) and not selected_2:
                        selectchar_2 += 1
                        if selectchar_2 >= len(chars) :
                            selectchar_2 = 0
                        click = False
                    Bouton = Button("",("arial",50,True,False),"./DATA/Images/Menu/Up.png",2*width/3,50,20,20,not selected_2)
                    Bouton.draw(window)
                    if Bouton.is_clicked(click) and not selected_2:
                        selectchar_2 -= 1
                        if selectchar_2 < 0 :
                            selectchar_2 = len(chars) - 1
                        click = False
                    
                    # OK Buttons
                    if convert_inputs(controls[0],joysticks[0])[6]:
                        selected_1 = True
                    if convert_inputs(controls[0],joysticks[0])[7]:
                        selected_1 = False
                    if convert_inputs(controls[1],joysticks[0])[6]:
                        selected_2 = True
                    if convert_inputs(controls[1],joysticks[0])[7]:
                        selected_2 = False
                    
                    # Names
                    if names[0] == 0 :
                        text = "Player 1"
                    else :
                        text = namelist[names[0]]
                    Bouton = Button(text,("arial",24,True,False),"./DATA/Images/Menu/Button.png",3*width/10,height-150,200,32)
                    if Bouton.is_focused():
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                    if Bouton.is_clicked(click):
                        names[0] += 1
                        if names[0] >= len(namelist):
                            names[0] = 0
                    Bouton.draw(window)

                    if names[1] == 0 :
                        text = "Player 2"
                    else :
                        text = namelist[names[1]]
                    Bouton = Button(text,("arial",24,True,False),"./DATA/Images/Menu/Button.png",7*width/10,height-150,200,32)
                    if Bouton.is_focused():
                        Bouton.changeImage("./DATA/Images/Menu/Button_focused.png")
                    if Bouton.is_clicked(click):
                        names[1] += 1
                        if names[1] >= len(namelist):
                            names[1] = 0
                    Bouton.draw(window)

                    #Texte(names[0],("arial",24,True,False),(0,0,0),width/4,height-150,format_="center").draw(window)
                    #Texte(names[1],("arial",24,True,False),(0,0,0),3*width/4,height-150,format_="center").draw(window)
                    # Text
                    if selected_1 :
                        pygame.draw.rect(window,(230,230,230),(width/8,height-120,width/4,30))
                        Texte("READY",("arial",24,True,False),(0,0,0),width/4,height-110,format_="center").draw(window)
                    if selected_2 :
                        pygame.draw.rect(window,(230,230,230),(5*width/8,height-120,width/4,30))
                        Texte("READY",("arial",24,True,False),(0,0,0),3*width/4,height-110,format_="center").draw(window)
                    
                    pygame.draw.rect(window,(200,200,200),(0,height-90,width,90))
                    Texte(str(Chars.charobjects[chars[selectchar_1]]()),("arial",64,True,False),(0,0,0),width/2-30,height-50,format_="right").draw(window)
                    Texte(str(Chars.charobjects[chars[selectchar_2]]()),("arial",64,True,False),(0,0,0),width/2+30,height-50,format_="left").draw(window)
                    Texte("|",("arial",80,True,False),(0,0,0),width/2,height-50,format_="center").draw(window)

                    if selected_2 and selected_1 :
                        Play = True
                        Menu = "stage"
                        Char_P1 = Chars.charobjects[chars[selectchar_1]]()
                        Char_P2 = Chars.charobjects[chars[selectchar_2]]()
                        #run,controls = setup_controls(window,width,height,joysticks) # Version test de modif des contrôles
                        controls = [commands[namelist[names[0]]],commands[namelist[names[1]]]]
                        stage = Stages.Stage([(-400,100,100,10,(150,150,150)),(300,100,100,10,(150,150,150))])
            else :
                if not musicplaying :
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("DATA/Musics/intro_2.mp3")
                    pygame.mixer.music.play()
                    musicplaying = True

                window.fill((180, 180, 250)) # Réinitialisation de l'écran à chaque frame

                # Recuperation des touches
                if (convert_inputs(controls[0])[-1] or convert_inputs(controls[1])[-1]):
                    if not hold_pause:
                        pause = not pause
                        hold_pause  = True
                else :
                    hold_pause = False
                
                if not pause:
                    # P1
                    inputs_1 = convert_inputs(controls[0])[0:-1]
                    if not (inputs_1[4] or inputs_1[5]): # Jump
                        Char_P1.jumping = False

                    # Transmission des inputs à l'objet Palyer 1
                    Char_P1.act(inputs_1, stage, Char_P2,not(pause or Char_P1.BOUM or Char_P2.BOUM))

                    # P2
                    inputs_2 = convert_inputs(controls[1])[0:-1]
                    if not (inputs_2[4] or inputs_2[5]): # Jump
                        Char_P2.jumping = False

                    Char_P2.act(inputs_2, stage, Char_P1,not(pause or Char_P1.BOUM or Char_P2.BOUM))
                    ########

                    Char_P2.collide(Char_P1)
                    Char_P1.collide(Char_P2)
                else :
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
                # Chars
                Char_P2.draw(window)
                Char_P1.draw(window)
                # Stage
                stage.draw(window)
                # Damages
                Char_P1.damages = float(Char_P1.damages)
                Texte(f"{str(round(Char_P1.damages,2)).split('.')[0]}  %",("Arial",60,False,False),(255-(Char_P1.damages/5),max(255-Char_P1.damages,0),max(255-Char_P1.damages*2,0)),width//3,height-50,800,format_="left").draw(window)
                Texte(f".{str(round(Char_P1.damages,2)).split('.')[1]}",("Arial",30,False,False),(255-(Char_P1.damages/5),max(255-Char_P1.damages,0),max(255-Char_P1.damages*2,0)),width//3+len(str(round(Char_P1.damages,2)).split('.')[0])*25,height-30,800,format_="left").draw(window)

                Char_P2.damages = float(Char_P2.damages)
                Texte(f"{str(round(Char_P2.damages,2)).split('.')[0]}  %",("Arial",60,False,False),(255-(Char_P2.damages/5),max(255-Char_P2.damages,0),max(255-Char_P2.damages*2,0)),2*width//3,height-50,800,format_="left").draw(window)
                Texte(f".{str(round(Char_P2.damages,2)).split('.')[1]}",("Arial",30,False,False),(255-(Char_P2.damages/5),max(255-Char_P2.damages,0),max(255-Char_P2.damages*2,0)),2*width//3+len(str(round(Char_P2.damages,2)).split('.')[0])*25,height-30,800,format_="left").draw(window)

            pygame.display.flip()
            clock.tick(60)  # FPS (à régler sur 60)


    except:
        traceback.print_exc()

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
