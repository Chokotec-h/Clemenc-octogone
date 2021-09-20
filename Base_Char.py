import pygame


class Char(pygame.sprite.Sprite):  # Personnage de base, possédant les caractéristiques communes à tous les persos
    def __init__(self, speed, airspeed, deceleration, fallspeed, fastfallspeed, jumpheight, doublejumpheight):
        pygame.sprite.Sprite.__init__(self)
        self.direction = 90         # direction (permet de savoir si le sprite doit être orienté à gauche ou à droite)
        self.vel = [0, 0]           # vitesse (x,y)
        self.grounded = False       # Le personnage touche-t-il le sol ?
        self.fastfall = False       # Le personnage fastfall-t-il ?
        self.doublejump = [False]   # Liste des double sauts, ainsi que de leur utilisation
        self.sprite = []            # Sprite vide (à remplir via Chars.py)

        self.speed = speed          # vitesse au sol
        self.airspeed = airspeed    # vitesse aérienne
        self.deceleration = deceleration  # vitesse de décélération (peut permettre de faire un perso qui glisse ;) )
        self.fallspeed = fallspeed  # vitesse de chute
        self.fastfallspeed = fastfallspeed  # vitesse de fastfall
        self.jumpheight = jumpheight # Hauter de saut
        self.doublejumpheight = doublejumpheight  # Hauteur des double sauts

        self.collidegroup = pygame.sprite.GroupSingle() # Groupe de collision (spécial à pygame)
        self.collidegroup.add(self)
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav")  # Son test, peut être modifié via Chars.py

        self.frame = 0              # Frames écoulées depuis le début de la précédente action
        self.attack = None          # Attaque en cours
        self.sprite_frame = 0       # numéro de l'image à afficher
        self.up_b = False           # Le personnage a-t-il up b ?
        self.can_act = True         # Le personnage peut-il agir ?

    def inputattack(self,attack):
        if attack == "UpB": # si on input un up B
            self.up_b = True  # le up b a été utilisé
            self.frame = 0  # on démarre à la frame 0
            self.attack = "UpB"  # l'action en cours est le up B
            self.can_act = False # Ne peut pas attaquer après le up B
    
    def animation_attack(self,attack):
        pass # à modifier pour chaque personnage dans Chars.py

    def move(self, inputs, stage):
        right, left, up, down, jump, special = inputs # dissociation des inputs
        if self.attack is None : # Si aucune attaque n'est en cours d'exécution
            if right:            # Si on input à droite
                if self.grounded: # Si le personnage est au sol
                    self.direction = 90  # tourne à droite et se déplace de la vitesse au sol
                    self.vel[0] += self.speed
                else:             # Sinon, se déplace de la vitesse aérienne
                    self.vel[0] += self.airspeed

            if left:            # Si on input à gauche
                if self.grounded: # la même, mais vers la gauche
                    self.direction = -90
                    self.vel[0] -= self.speed
                else:
                    self.vel[0] -= self.airspeed
            if up and self.can_act:         # si on input vers le haut
                if special and not self.up_b: # si la touche spécial est pressée, et que le up b n'a pas été utilisé
                    self.inputattack("UpB")  # on input un upB
                    jump = False  # On input pas un saut en plus

            if jump:        # si on input un saut
                if self.grounded:  # Si le personnage est au sol
                    self.vel[1] = self.jumpheight # il utilise son premier saut
                    self.jumpsound.play() # joli son

                else:  # Si le personnage est en l'air
                    self.fastfall = False  # il cesse de fastfall
                    if not self.doublejump[-1]:  # Si il possède un double saut
                        self.jumpsound.play()  # joli son
                        self.vel[1] = self.doublejumpheight # il saute

                        i = 0   # il montre qu'il utilise le premier saut disponible dans la liste
                        while self.doublejump[i]:  # cette boucle a une fin, qui est testée ligne 70
                            i += 1
                        self.doublejump[i] = True

            if down : # Si on input vers le bas
                if not self.grounded and self.vel[1] < 5: # si le personnage est en fin de saut
                    if not self.fastfall:  # on fastfall
                        self.vel[1] = self.vel[1] - self.fastfallspeed * 5
                    self.fastfall = True
        else : # si une attaque est exécutée, on anime la frame suivante
            self.animation_attack(self.attack)
        self.frame += 1


        # Mouvements
        self.rect = self.rect.move(self.vel[0], -self.vel[1]) # Déplace le personnage

        self.vel[0] *= self.deceleration # décélération
        self.rect.move_ip(0,5) # Le personnage est considéré comme au sol 5 pixel plus haut (permet d'éviter les bugs de double sauts)
        # si le personnage touche le stage
        if ( pygame.sprite.spritecollide( stage, self.collidegroup, False, collided=pygame.sprite.collide_mask ) ):
            if self.rect.y+self.rect.h-5 < stage.rect.y + stage.rect.h//3: # si le personnage est sur le stage
                if self.vel[1] < -1 : # si une attaque aérienne a été input (ex : up B/ nair), et que le personnage touche le sol
                    self.can_act = True # l'attaque est cancel
                    self.attack = None
                    """On peut rajouter du lag ici en ajoutant un self.lag"""
                    
                self.grounded = True # Le personnage est considéré au sol
                self.fastfall = False # reset des stats liées aux sauts
                self.up_b = False
                for dj in range(len(self.doublejump)):
                    self.doublejump[dj] = False

        self.rect.move_ip(0,-4) # on remonte le carré de 4 (permet d'éviter les bugs dûs au test juste en-dessous

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""   Collisions avec le stage   """""""""""""""
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        if ( pygame.sprite.spritecollide( stage, self.collidegroup, False, collided=pygame.sprite.collide_mask ) ): # Si le personnage touche le stage
            # Personnage sur le stage
            if self.rect.y+self.rect.h-5 < stage.rect.y + stage.rect.h//2 :
                while self.rect.y + self.rect.h > stage.rect.y +1: # on place le personnage sur le stage
                    self.rect.move_ip(0,-1)
                self.vel[1] = 0 # on annule se vitesse verticale

            # Personnage sous le stage
            elif self.rect.y > stage.rect.y + stage.rect.h//2:
                while self.rect.y < stage.rect.y+stage.rect.h//2-1: # on descend le personnage bien sous le stage
                    self.rect.move_ip(0,1)
                self.vel[1] = -1 # on met sa vitesse verticale à -1

            # Personnage à côté du stage
            elif self.rect.x > stage.rect.x + stage.rect.w//2: # si il est à droite du stage
                self.vel[0] = 5 # on le décale à droite
            elif self.rect.x < stage.rect.x + stage.rect.w//2: # si il est à gauche du stage
                self.vel[0] = -5 # on le décale à gauche
        else :  # Si le personnage ne touche pas le stage
            self.vel[1] -= self.fastfallspeed if self.fastfall else self.fallspeed # il est soumis à la gravité
            self.grounded = False # il est considéré dans les airs

    def draw(self, window, camera):

        ### à supprimer, provisoire pour le retournement
        if self.direction < 0:
            sprite = pygame.transform.flip(self.sprite[self.sprite_frame], True, False)
        else:
            sprite = self.sprite[self.sprite_frame]
        ####

        pos = [self.rect.x - camera[0] + 400, self.rect.y - camera[1] + 300] # Position réelle du sprite
        window.blit(sprite, pos) # on dessine le sprite

    def collide(self, other):
        if self.rect.colliderect(other.rect):
            if self.rect.x < other.rect.x:
                self.vel[0] = -1
            if self.rect.x > other.rect.x:
                self.vel[0] = 1
            if self.rect.y < (other.rect.y - 2 * other.rect.h // 3):
                self.vel[1] = self.doublejumpheight

