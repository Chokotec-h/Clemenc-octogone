import pygame
import traceback
import spritesLoader
import Chars
import Stages
from Interface import *

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
def setup_controls(window,joysticks):
    P1_controls = []
    P2_controls = []


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
    pygame.mixer.music.play()
    soundReady = True

    try:

        run = True
        holding_up1 = False # Gestion du maintien de la touche saut
        holding_up2 = False
        while run:  # Boucle du programme

            window.fill((200, 220, 250)) # Réinitialisation de l'écran à chaque frame


            # Récupération des events
            for e in pygame.event.get():
                if e.type == pygame.QUIT: # Bouton croix en haut à droite de l'écran
                    run = False

            # Recuperation des touches
            key = pygame.key.get_pressed()
            if key[pygame.K_UP]: # Gestion du saut
                if not holding_up1:
                    holding_up1 = True
                    up = True
                else:
                    up = False
            else:
                holding_up1 = False
                up = False

            # Transmission des inputs à l'objet Balan
            Balan.act([key[pygame.K_RIGHT], key[pygame.K_LEFT], key[pygame.K_UP], key[pygame.K_DOWN], up, key[pygame.K_x]], stage)
            # dessin de Balan
            Balan.draw(window)

            # ---- Test P2 -------
            if key[pygame.K_z]:
                if not holding_up2:
                    holding_up2 = True
                    up = True
                else:
                    up = False
            else:
                holding_up2 = False
                up = False
            Balan2.act([key[pygame.K_d], key[pygame.K_q], key[pygame.K_z], key[pygame.K_s], up, False], stage)
            Balan2.draw(window)
            stage.draw(window)
            ########

            Balan2.collide(Balan)
            Balan.collide(Balan2)

            ### Debug
            for h in Balan.active_hitboxes:
                h.draw(window)

            Texte(f"{Balan.damages}%",("Arial",60,False,False),(255-(Balan.damages/5),max(255-Balan.damages,0),max(255-Balan.damages*2,0)),width//3,height-20,800).draw(window)
            Texte(f"{Balan2.damages}%",("Arial",60,False,False),(255-(Balan2.damages/5),max(255-Balan2.damages,0),max(255-Balan2.damages*2,0)),2*width//3,height-20,800).draw(window)

            pygame.display.flip()
            clock.tick(60)  # FPS (à régler sur 60)
            

    except:
        traceback.print_exc()

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
