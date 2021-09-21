import pygame
from copy import deepcopy
from math import cos,sin

def signe(val):
    if val == 0:
        return 0
    else :
        return val/abs(val)

class Hitbox():
    def __init__(self,x,y,sizex,sizey,angle,knockback,damages,stun,duration,own) -> None:
        self.relativex = x # Position relative 
        self.relativey = y
        self.sizex = sizex
        self.sizey = sizey
        self.angle = angle
        self.knockback = knockback
        self.damages = damages
        self.stun = stun
        self.duration = duration
        self.own = own
        self.update()

    def update(self):
        self.x = self.relativex + self.own.rect.x
        self.y = self.relativey + self.own.rect.y
        self.hit = pygame.Rect(self.x,self.y,self.sizex,self.sizey)
        self.duration -= 1
    
    def draw(self,window): # debug
        pygame.draw.rect(window,(255,0,0),(self.x+800,self.y+450,self.sizex,self.sizey))

class Char(pygame.sprite.Sprite):  # Personnage de base, possédant les caractéristiques communes à tous les persos
    def __init__(self, speed, airspeed, deceleration, fallspeed, fastfallspeed, jumpheight, doublejumpheight):
        pygame.sprite.Sprite.__init__(self)
        self.direction = 90         # direction (permet de savoir si le sprite doit être orienté à gauche ou à droite)
        self.vx = 0           # vitesse (x,y)
        self.vy = 0
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
        self.can_act = True         # Le personnage peut-il agir ?

        self.hitstun = 0            # Frames de hitstun
        self.active_hitboxes = list() # Liste des hitbox actives

    def inputattack(self,attack):
        if attack == "UpB": # si on input un up B
            self.frame = 0  # on démarre à la frame 0
            self.attack = "UpB"  # l'action en cours est le up B
            self.can_act = False # Ne peut pas attaquer après le up B
    
    def animation_attack(self,attack):
        pass # à modifier pour chaque personnage dans Chars.py

    def act(self, inputs,stage):
        self.get_inputs(inputs)
        self.move(stage)
        for i,hitbox in enumerate(self.active_hitboxes) :
            hitbox.update()
            if hitbox.duration <= 0:
                del self.active_hitboxes[i]


    def get_inputs(self, inputs):
        self.hitstun = max(0, self.hitstun-1)
        right, left, up, down, jump, special = inputs # dissociation des inputs
        if self.hitstun:
            if right:
                self.vx += self.airspeed/10
            if left:
                self.vx -= self.airspeed/10
            if up:
                self.vy += self.airspeed/10
            if down:
                self.vy -= self.airspeed/10
        else :
            if self.attack is None : # Si aucune attaque n'est en cours d'exécution
                if right:            # Si on input à droite
                    if self.grounded: # Si le personnage est au sol
                        self.direction = 90  # tourne à droite et se déplace de la vitesse au sol
                        self.vx += self.speed
                    else:             # Sinon, se déplace de la vitesse aérienne
                        self.vx += self.airspeed

                if left:            # Si on input à gauche
                    if self.grounded: # la même, mais vers la gauche
                        self.direction = -90
                        self.vx -= self.speed
                    else:
                        self.vx -= self.airspeed
                if up and self.can_act:         # si on input vers le haut
                    if special : # si la touche spécial est pressée, et que le up b n'a pas été utilisé
                        self.inputattack("UpB")  # on input un upB
                        jump = False  # On input pas un saut en plus

                if jump:        # si on input un saut
                    if self.grounded:  # Si le personnage est au sol
                        self.vy = -self.jumpheight # il utilise son premier saut
                        self.jumpsound.play() # joli son

                    else:  # Si le personnage est en l'air
                        self.fastfall = False  # il cesse de fastfall
                        if not self.doublejump[-1]:  # Si il possède un double saut
                            self.jumpsound.play()  # joli son
                            self.vy = -self.doublejumpheight # il saute

                            i = 0   # il montre qu'il utilise le premier saut disponible dans la liste
                            while self.doublejump[i]:  # cette boucle a une fin, qui est testée ligne 70
                                i += 1
                            self.doublejump[i] = True

                if down : # Si on input vers le bas
                    if not self.grounded and self.vy < 5: # si le personnage est en fin de saut
                        if not self.fastfall:  # on fastfall
                            self.vy = self.vy + self.fastfallspeed * 5
                        self.fastfall = True
            else : # si une attaque est exécutée, on anime la frame suivante
                self.animation_attack(self.attack)
            self.frame += 1


    def move(self, stage):
        if self.fastfall :
            self.vy = self.vy + self.fastfallspeed
        else :
            self.vy = self.vy + self.fallspeed
        
        nextframe = self.rect.move(self.vx,-signe(self.vy))
        if nextframe.colliderect(stage.rect):
            while not self.rect.move(signe(self.vx),-signe(self.vy)).colliderect(stage.rect):
                self.rect.x += signe(self.vx)
            self.rect.x -= signe(self.vx)
            self.vx = 0
        nextframe = self.rect.move(0,self.vy)
        if nextframe.colliderect(stage.rect):
            while not self.rect.move(0,signe(self.vy)).colliderect(stage.rect):
                self.rect.y += signe(self.vy)
            self.vy = 0

        self.rect.y += self.vy
        self.rect.x += round(self.vx)
        if not self.hitstun :
            self.vx *= self.deceleration
            if abs(self.vx) < 0.01 :
                self.vx = 0

        if self.rect.move(0,1).colliderect(stage.rect):
            if self.hitstun :
                self.vx = 0
            if not self.can_act :
                self.can_act = True
            self.grounded = True
            self.fastfall = False
            for dj in range(len(self.doublejump)):
                self.doublejump[dj] = False
        else :
            self.grounded = False

        # debug
        if self.rect.y > 800 :
            self.rect.y = -200
            self.rect.x = 0
            self.vy = 0


    def draw(self, window):

        ### à supprimer, provisoire pour le retournement
        if self.direction < 0:
            sprite = pygame.transform.flip(self.sprite[self.sprite_frame], True, False)
        else:
            sprite = self.sprite[self.sprite_frame]
        ####

        pos = [self.rect.x + 800, self.rect.y + 449] # Position réelle du sprite
        window.blit(sprite, pos) # on dessine le sprite

    def collide(self,other):
        for hitbox in other.active_hitboxes:
            if self.rect.colliderect(hitbox.hit):
                self.vx = hitbox.knockback*cos(hitbox.angle)
                self.vy = -hitbox.knockback*sin(hitbox.angle)
                self.hitstun = hitbox.stun
                self.rect.y -= 1