import pygame
import traceback
import spritesLoader
import Chars
import Stages

####################################
########## Initialisation ##########
####################################

pygame.init() # Initialisation de pygame
clock=pygame.time.Clock() # Horloge


pygame.joystick.init()  # Initialisation des manettes
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

for j in joysticks:
    j.init()

####################################
####################################



def main():
    """"""""""""""""""""""""""""""""""""
    """""""""Progamme Principal"""""""""
    """"""""""""""""""""""""""""""""""""


    # initialisation de la fenêtre
    h = 600
    l = 800
    window = pygame.display.set_mode((l,h))

    # Déclaration des variables
    Balan = Chars.Balan()
    Balan2 = Chars.Balan2()
    Balan3 = Chars.Balan2() # Test
    stage = Stages.Stage()

    try :
        
        run = True
        while run :  # Boucle du programme

            window.fill((200,220,250))

            camera = [(Balan.Rect.x+Balan2.Rect.x)/10,(Balan.Rect.y+Balan2.Rect.y)/2]

            # Récupération des events
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    run = False
                right = False
            
            # Recuperation des touches
            key = pygame.key.get_pressed()
            if key[pygame.K_RIGHT]:
                right = True
            else :
                right = False
            if key[pygame.K_LEFT]:
                left = True
            else :
                left = False
            if key[pygame.K_UP]:
                up = True
            else :
                up = False
            if key[pygame.K_DOWN]:
                down = True
            else :
                down = False
            

            Balan.move([right,left,up,down])
            Balan.draw(window,camera,0)
            
            ####### Test
            if key[pygame.K_d]:
                right = True
            else :
                right = False
            if key[pygame.K_q]:
                left = True
            else :
                left = False
            if key[pygame.K_z]:
                up = True
            else :
                up = False
            if key[pygame.K_s]:
                down = True
            else :
                down = False
            Balan2.move([right,left,up,down])
            Balan2.draw(window,camera,0)
            stage.draw(window,camera)
            ########
            Balan3.move([False,False,False,False])
            Balan3.draw(window,camera,0)
            Balan.collide(Balan2)
            Balan.collide(Balan3)
            Balan2.collide(Balan)
            Balan2.collide(Balan3)
            Balan3.collide(Balan2)
            Balan3.collide(Balan)


            pygame.display.flip()
            clock.tick(20) # FPS (à régler sur 60)
        
    except:
        traceback.print_exc()

    finally:
        pygame.quit()

main()
