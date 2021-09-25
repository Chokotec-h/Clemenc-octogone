import pygame
from math import cos,sin,pi

def signe(val):
    if val == 0:
        return 0
    else :
        return val/abs(val)

class Hitbox():
    def __init__(self,x,y,sizex,sizey,angle,knockback,damages,damage_stacking,stun,duration,own,position_relative=True) -> None:
        self.relativex = x # Position relative 
        self.relativey = y
        self.sizex = sizex
        self.sizey = sizey
        self.angle = angle
        self.knockback = knockback
        self.damages = damages
        self.damages_stacking = damage_stacking
        self.stun = stun
        self.duration = duration
        self.own = own
        self.position_relative = position_relative # Est-ce que l'ange d'éjection dépend de la position de l'adversaire par rapport à la hitbox ?
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
        self.damages = 0.0
        self.direction = 90         # direction (permet de savoir si le sprite doit être orienté à gauche ou à droite)
        self.vx = 0           # vitesse (x,y)
        self.vy = 0
        self.grounded = False       # Le personnage touche-t-il le sol ?
        self.fastfall = False       # Le personnage fastfall-t-il ?
        self.doublejump = [False]   # Liste des double sauts, ainsi que de leur utilisation
        self.sprite = []            # Sprite vide (à remplir via <Personnage>.py)

        self.speed = speed          # vitesse au sol
        self.airspeed = airspeed    # vitesse aérienne
        self.deceleration = deceleration  # vitesse de décélération (peut permettre de faire un perso qui glisse ;) )
        self.fallspeed = fallspeed  # vitesse de chute
        self.fastfallspeed = fastfallspeed  # vitesse de fastfall
        self.jumpheight = jumpheight # Hauter de saut
        self.doublejumpheight = doublejumpheight  # Hauteur des double sauts

        self.collidegroup = pygame.sprite.GroupSingle() # Groupe de collision (spécial à pygame)
        self.collidegroup.add(self)
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav")  # Son test, peut être modifié via <Personnage>.py

        self.frame = 0              # Frames écoulées depuis le début de la précédente action
        self.attack = None          # Attaque en cours
        self.sprite_frame = 0       # numéro de l'image à afficher
        self.can_act = True         # Le personnage peut-il agir ?
        self.upB = False         # Le personnage peut-il agir ?

        self.hitstun = 0            # Frames de hitstun
        self.active_hitboxes = list() # Liste des hitbox actives
        self.projectiles = list()
        self.last_hit = 0
        self.lag = 0
        self.charge = 0
        self.parry = False
        self.parrying = False

        self.dash = False # Unused

    def inputattack(self,attack):
        if self.can_act :
            self.frame = 0  # on démarre à la frame 0
            self.attack = attack  # on update l'action en cours
            if attack == "UpB":
                self.can_act = False # Ne peut pas attaquer après le up B
                self.upB = True # Effets spéciaux après upB (uniquement grounded)
    
    def animation_attack(self,attack,inputs,stage):
        pass # à modifier pour chaque personnage dans <Personnage>.py

    def act(self, inputs,stage):
        self.last_hit = max(self.last_hit-1,0)
        self.get_inputs(inputs,stage)
        self.move(stage)
        for i,hitbox in enumerate(self.active_hitboxes) :
            hitbox.update()
            if hitbox.duration <= 0:
                del self.active_hitboxes[i]
        for i,projectile in enumerate(self.projectiles) :
            self.projectiles[i].update()
            if projectile.duration <= 0:
                del self.projectiles[i]
        self.damages = min(999.,self.damages)
        if self.hitstun: # Arrête la charge des smashs en hitstun
            self.charge = 0


    def get_inputs(self, inputs, stage):
        self.lag = max(0,self.lag-1)
        self.hitstun = max(0, self.hitstun-1)
        left, right, up, down,jump, attack, special, shield = inputs # dissociation des inputs
        if self.hitstun: # Directional Influence
            if right:
                self.vx += self.airspeed/10
            if left:
                self.vx -= self.airspeed/10
            if up:
                self.vy -= self.fallspeed/10
            if down:
                self.vy += self.fallspeed/10
        else :
            if self.grounded and self.attack is None and not self.lag:
                self.parry = shield
            else :
                self.parry = False
            if self.attack is None and not self.lag: # Si aucune attaque n'est en cours d'exécution et si on n'est pas dans un lag (ex:landing lag)
                
                if right:            # Si on input à droite
                    if attack :
                        if self.grounded:
                            self.inputattack("ForwardTilt")
                        else :
                            if self.direction < 0 :
                                self.inputattack("BackAir")
                            else :
                                self.inputattack("ForwardAir")
                    if self.grounded: # Si le personnage est au sol
                        self.direction = 90  # tourne à droite et se déplace de la vitesse au sol
                        self.vx += self.speed
                    else:             # Sinon, se déplace de la vitesse aérienne
                        self.vx += self.airspeed

                if left:            # Si on input à gauche
                    if attack :
                        if self.grounded:
                            self.inputattack("ForwardTilt")
                        else :
                            if self.direction > 0 :
                                self.inputattack("BackAir")
                            else :
                                self.inputattack("ForwardAir")
                    if self.grounded: # la même, mais vers la gauche
                        self.direction = -90
                        self.vx -= self.speed
                    else:
                        self.vx -= self.airspeed
                if up and self.can_act:         # si on input vers le haut
                    if special and not self.upB : # si la touche spécial est pressée, et que le up b n'a pas été utilisé
                        self.inputattack("UpB")  # on input un upB
                        jump = False  # On input pas un saut en plus
                    if attack :
                        if self.grounded:
                            pass
                        else :
                            self.inputattack("UpAir")

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
                    
                    if attack :
                        if self.grounded :
                            self.inputattack("DownTilt")
                        else :
                            self.inputattack("DownAir")
                    elif not self.grounded and self.vy > -3: # si le personnage est en fin de saut
                        if not self.fastfall:  # on fastfall
                            self.vy = self.vy + self.fastfallspeed * 5
                        self.fastfall = True

                if not (left or right or up or down):
                    if special :
                        self.inputattack("NeutralB")
                    if attack :
                        if self.grounded:
                            self.inputattack("Jab")
            else : # si une attaque est exécutée, on anime la frame suivante
                self.animation_attack(self.attack,inputs,stage)
                if not self.grounded:
                    if right: # drift en l'air
                        self.vx += self.airspeed/10
                    if left:
                        self.vx -= self.airspeed/10
            self.frame += 1


    def move(self, stage):
        if self.fastfall : # gravité
            self.vy = self.vy + self.fastfallspeed
        else :
            self.vy = self.vy + self.fallspeed
        
        # détection de collisions à la frame suivante
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
            if self.hitstun:
                self.vy = -self.vy
            else :
                self.vy = 0

        # Déplacement
        self.rect.y += self.vy
        self.rect.x += round(self.vx)
        if not self.hitstun :
            # déceleration et vitesse max
            if self.grounded :
                self.vx *= self.deceleration
            elif self.vx < -5*self.airspeed:
                self.vx = self.airspeed*-5
            elif self.vx > 5*self.airspeed:
                self.vx = self.airspeed*5
            if abs(self.vx) < 0.01 :
                self.vx = 0

        # Détection de si le personnage est au sol
        if self.rect.move(0,1).colliderect(stage.rect):
            if self.hitstun : # annule la vitesse de hitstun
                self.vx *= 0.5
            if not self.can_act : # permet de jouer après un upb
                self.can_act = True
            if self.upB: # reset le upb
                self.upB = False
            self.grounded = True
            self.fastfall = False
            for dj in range(len(self.doublejump)):
                self.doublejump[dj] = False
        else :
            self.grounded = False

        # respawn
        if self.rect.y > 800 or self.rect.y < -800 or self.rect.x < -900 or self.rect.x > 900 :
            self.rect.y = -200
            self.rect.x = 0
            self.damages = 0.
            self.vy = 0
            self.vx = 0


    def draw(self, window):

        ### à supprimer, provisoire pour le retournement
        if self.direction < 0:
            sprite = pygame.transform.flip(self.sprite[self.sprite_frame], True, False)
        else:
            sprite = self.sprite[self.sprite_frame]
        ####
        sprite = pygame.transform.scale(sprite,(round(sprite.get_size()[0]*1.5),round(sprite.get_size()[1]*1.5))) # Rescale
        pos = [self.rect.x + 800, self.rect.y + 449] # Position réelle du sprite
        window.blit(sprite, pos) # on dessine le sprite
        self.rect = self.sprite[self.sprite_frame].get_rect(topleft=(self.rect.x,self.rect.y))
        self.rect.w *= 1.5 # Rescale
        self.rect.h *= 1.5 # Rescale

        # debug
        if self.parry:
            pygame.draw.rect(window,(200,200,200),(pos[0],pos[1],self.rect.w,self.rect.h))

        # draw projectiles
        for p in self.projectiles :
            p.draw(window)

    def collide(self,other):
        self.parrying = False
        for i,hitbox in enumerate(other.active_hitboxes): # Détection des hitboxes
            if self.rect.colliderect(hitbox.hit):
                if not self.parry : # Parry
                    if hitbox.position_relative : # Reverse hit
                        if self.rect.x > hitbox.hit.x+hitbox.hit.w//2 and hitbox.own.direction < 0:
                            hitbox.angle = pi - hitbox.angle
                        if self.rect.x < hitbox.hit.x-hitbox.hit.w//2 and hitbox.own.direction > 0:
                            hitbox.angle = pi - hitbox.angle
                        
                    self.vx = hitbox.knockback*cos(hitbox.angle)*(self.damages*hitbox.damages_stacking+1) # éjection x
                    self.vy = -hitbox.knockback*sin(hitbox.angle)*(self.damages*hitbox.damages_stacking+1) # éjection y
                    self.hitstun = hitbox.stun*(self.damages*hitbox.damages_stacking/2+1) # hitstun
                    self.damages += hitbox.damages # dommages
                    self.rect.y -= 1
                    self.attack = None # cancel l'attacue en cours
                else :
                    self.parrying = True

                del other.active_hitboxes[i] # Supprime la hitbox
                return
        for projectile in other.projectiles: # Détection des projectiles
            if self.rect.colliderect(projectile.rect) and not self.last_hit:
                self.last_hit = 10 # invincibilité aux projectiles de 10 frames
                if not self.parry : # Parry
                    self.vx = projectile.knockback*cos(projectile.angle)*(self.damages*projectile.damages_stacking+1) # éjection x
                    self.vy = -projectile.knockback*sin(projectile.angle)*(self.damages*projectile.damages_stacking+1) # éjection y
                    self.hitstun = projectile.stun*(self.damages*projectile.damages_stacking/2+1) # hitstun
                    self.damages += projectile.damages # dommages
                    self.rect.y -= 1
                    self.attack = None
                else :
                    self.parrying = True
                return