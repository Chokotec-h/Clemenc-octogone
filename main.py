from Misc import Smoke
import pygame
import traceback
import spritesLoader
import Chars
import Stages
from Misc import *
from Interface import *
from Gamepad_gestion import *

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

### Version bêta
def setup_controls(window,width,height,joysticks):
    controls = [[],[]]
    player = 0
    run = True
    # liste des action
    actions = ("Left","Right","Up","Down","Jump","Attack","Special","Shield","C-Stick Left","C-Stick Right","C-Stick Up","C-Stick Down","D-Pad Left","D-Pad Right","D-Pad Up","D-Pad Down","Pause")
    while run :
        window.fill((200,200,200))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            # Récupération des inputs claviers
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if len(controls[player]) > 0:
                        controls[player].pop()
                    else :
                        player = 0
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
    height = 900
    width = 1600
    window = pygame.display.set_mode((width, height))

    # Déclaration des variables
    Char_P1 = Chars.Balan()
    Char_P2 = Chars.Balan2()
    stage = Stages.Stage()
    smoke = list()

    # test de music et de bruitages
    pygame.mixer.music.load("DATA/Musics/main.wav")
    #pygame.mixer.music.play()
    soundReady = True

    try:

        run,controls = setup_controls(window,width,height,joysticks)
        #run = True
        # permettra de modifier les contrôles
        #controls = [[pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN,pygame.K_SPACE,pygame.K_x,pygame.K_c],[pygame.K_q,pygame.K_d,pygame.K_z,pygame.K_s,0,0,0]]
        parry1 = 0
        parry2 = 0
        pause = False
        hold_pause = False
        while run:  # Boucle du programme

            window.fill((200, 220, 250)) # Réinitialisation de l'écran à chaque frame


            # Récupération des events
            for e in pygame.event.get():
                if e.type == pygame.QUIT: # Bouton croix en haut à droite de l'écran
                    run = False

            # Recuperation des touches
            if (convert_inputs(controls[0])[-1] or convert_inputs(controls[1])[-1]):
                if not hold_pause:
                    pause = not pause
                    hold_pause  = True
            else :
                hold_pause = False
            
            if not pause:
                inputs_1 = convert_inputs(controls[0])[0:8]
                if not inputs_1[4]: # Jump
                    Char_P1.jumping = False

                if inputs_1[7] and Char_P1.grounded and not Char_P1.parrying: # Parry
                    parry1 += 1
                    if parry1 > 4: # Fenêtre de 4 frames
                        inputs_1[7] = False
                else:
                    parry1 = 0

                # Transmission des inputs à l'objet Palyer 1
                Char_P1.act(inputs_1, stage)

                # P2
                inputs_2 = convert_inputs(controls[1])[0:8]
                if not inputs_2[4]: # Jump
                    Char_P2.jumping = False

                if inputs_2[7] and Char_P2.grounded and not Char_P2.parrying: # Parry
                    parry2 += 1
                    if parry2 > 4: # Fenêtre de 4 frames
                        inputs_2[7] = False
                else:
                    parry2 = 0
                Char_P2.act(inputs_2, stage)
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
            if Char_P1.hitstun :
                smoke.append(Smoke(Char_P1.rect.x+Char_P1.rect.w/2,Char_P1.rect.y+Char_P1.rect.h/2))
            if Char_P2.hitstun :
                smoke.append(Smoke(Char_P2.rect.x+Char_P2.rect.w/2,Char_P2.rect.y+Char_P2.rect.h/2))
            for i,s in enumerate(smoke):
                s.draw(window)
                if s.duration <= 0:
                    del smoke[i]
            # Chars
            Char_P1.draw(window)
            Char_P2.draw(window)
            # Stage
            stage.draw(window)
            # Damages
            Texte(f"{str(round(Char_P1.damages,2)).split('.')[0]} %",("Arial",60,False,False),(255-(Char_P1.damages/5),max(255-Char_P1.damages,0),max(255-Char_P1.damages*2,0)),width//3,height-50,800,format_="left").draw(window)
            Texte(f".{str(round(Char_P1.damages,2)).split('.')[1]}",("Arial",20,False,False),(255-(Char_P1.damages/5),max(255-Char_P1.damages,0),max(255-Char_P1.damages*2,0)),width//3+len(str(round(Char_P1.damages)))*25,height-30,800,format_="left").draw(window)

            Texte(f"{str(round(Char_P2.damages,2)).split('.')[0]} %",("Arial",60,False,False),(255-(Char_P1.damages/5),max(255-Char_P2.damages,0),max(255-Char_P2.damages*2,0)),2*width//3,height-50,800,format_="left").draw(window)
            Texte(f".{str(round(Char_P2.damages,2)).split('.')[1]}",("Arial",20,False,False),(255-(Char_P2.damages/5),max(255-Char_P2.damages,0),max(255-Char_P2.damages*2,0)),2*width//3+len(str(round(Char_P2.damages)))*25,height-30,800,format_="left").draw(window)

            pygame.display.flip()
            clock.tick(60)  # FPS (à régler sur 60)
            

    except:
        traceback.print_exc()

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
