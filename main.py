import pygame
import traceback
import spritesLoader
import Chars
import Stages
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

"""Tests controls, à modifier"""
def setup_controls(window,width,height,joysticks):
     controls = [[],[]]
     player = 0
     run = True
     actions = ("Left","Right","Up","Down","Jump","Attack","Special","Shield","C-Stick Left","C-Stick Right","C-Stick Up","C-Stick Down","D-Pad Left","D-Pad Right","D-Pad Up","D-Pad Down","Pause")
     while run :
         window.fill((200,200,200))
         for e in pygame.event.get():
             if e.type == pygame.QUIT:
                 run = False
             if e.type == pygame.KEYDOWN:
                 if e.key == pygame.K_ESCAPE:
                     if len(controls[player]) > 0:
                         controls[player].pop()
                     else :
                         player = 0
                         controls[player].pop()
                 elif ("Keyboard",e.key) not in controls[int(not player)]:
                     controls[player].append(("Keyboard",e.key))
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
    Balan = Chars.Balan()
    Balan2 = Chars.Balan2()
    stage = Stages.Stage()

    # test de music et de bruitages
    pygame.mixer.music.load("DATA/Musics/main.wav")
    #pygame.mixer.music.play()
    soundReady = True

    try:

        run,controls = setup_controls(window,width,height,joysticks)
        #run = True
        # permettra de modifier les contrôles
        #controls = [[pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN,pygame.K_SPACE,pygame.K_x,pygame.K_c],[pygame.K_q,pygame.K_d,pygame.K_z,pygame.K_s,0,0,0]]
        holding_up1 = False # Gestion du maintien de la touche saut
        holding_up2 = False
        pause = False
        hold_pose = False
        while run:  # Boucle du programme

            window.fill((200, 220, 250)) # Réinitialisation de l'écran à chaque frame


            # Récupération des events
            for e in pygame.event.get():
                if e.type == pygame.QUIT: # Bouton croix en haut à droite de l'écran
                    run = False

            # Recuperation des touches
            if (convert_inputs(controls[0])[-1] or convert_inputs(controls[1])[-1]):
                if not hold_pose:
                    pause = not pause
                    hold_pose  = True
            else :
                hold_pose = False
            
            if not pause:
                inputs_1 = convert_inputs(controls[0])[0:8]
                if inputs_1[4]: #
                    if not holding_up1:
                        holding_up1 = True
                    else:
                        inputs_1[4] = False
                else:
                    holding_up1 = False

                # Transmission des inputs à l'objet Balan
                Balan.act(inputs_1, stage)
                # dessin de Balan

                # ---- Test P2 -------
                inputs_2 = convert_inputs(controls[1])[0:8]
                if inputs_2[4]:
                    if not holding_up2:
                        holding_up2 = True
                    else:
                        inputs_2[4] = False
                else:
                    holding_up2 = False
                Balan2.act(inputs_2, stage)
                ########

                Balan2.collide(Balan)
                Balan.collide(Balan2)
            else :
                Texte(f"Pause",("Arial",60,False,False),(0,0,0),width//2,height//2,800).draw(window)

            """ Draw """
            ### Debug
            for h in Balan.active_hitboxes:
                h.draw(window)
            for h in Balan2.active_hitboxes:
                h.draw(window)

            Balan.draw(window)
            Balan2.draw(window)
            stage.draw(window)
            Texte(f"{round(Balan.damages)} %",("Arial",60,False,False),(255-(Balan.damages/5),max(255-Balan.damages,0),max(255-Balan.damages*2,0)),width//3,height-50,800,format_="left").draw(window)
            Texte(f".{str(round(Balan.damages,2)).split('.')[1]}",("Arial",20,False,False),(255-(Balan.damages/5),max(255-Balan.damages,0),max(255-Balan.damages*2,0)),width//3+len(str(round(Balan.damages)))*25,height-30,800,format_="left").draw(window)
            Texte(f"{round(Balan2.damages)} %",("Arial",60,False,False),(255-(Balan.damages/5),max(255-Balan2.damages,0),max(255-Balan2.damages*2,0)),2*width//3,height-50,800,format_="left").draw(window)
            Texte(f".{str(round(Balan2.damages,2)).split('.')[1]}",("Arial",20,False,False),(255-(Balan2.damages/5),max(255-Balan2.damages,0),max(255-Balan2.damages*2,0)),2*width//3+len(str(round(Balan2.damages)))*25,height-30,800,format_="left").draw(window)

            pygame.display.flip()
            clock.tick(60)  # FPS (à régler sur 60)
            

    except:
        traceback.print_exc()

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
