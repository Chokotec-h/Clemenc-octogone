import pygame
from math import cos,sin,pi

from DATA.utilities.Animations import get_sprite

def signe(val):
    if val == 0:
        return 0
    else :
        return val/abs(val)

def change_left(x,size):
    return -x-size+48

class Hitbox():
    def __init__(self,x,y,sizex,sizey,angle,knockback,damages,damage_stacking,stun,duration,own,position_relative=True,deflect=False,modifier=1) -> None:
        self.relativex = x # Position relative 
        self.relativey = y
        self.sizex = sizex
        self.sizey = sizey
        self.angle = angle
        self.knockback = knockback
        self.damages = damages
        self.damages_stacking = damage_stacking
        self.stun = stun
        self.duration = duration + 1 # Because duration is reduced on init (line 26)
        self.own = own
        self.position_relative = position_relative # Est-ce que l'ange d'éjection dépend de la position de l'adversaire par rapport à la hitbox ?
        self.deflect = deflect
        self.modifier = modifier
        if not own.look_right :
            self.relativex = change_left(x,sizex)
            self.angle = pi - angle
        self.update()

    def update(self):
        self.x = self.relativex + self.own.rect.x
        self.y = self.relativey + self.own.rect.y
        self.hit = pygame.Rect(self.x,self.y,self.sizex,self.sizey)
        self.duration -= 1
    
    def draw(self,window): # debug
        x = self.x
        sizex = self.sizex
        if sizex < 0 :
            x =  self.x + self.sizex
            sizex = abs(self.sizex)
        pygame.draw.rect(window,(255,0,0),(x+800,self.y+450,sizex,self.sizey))

class Char(pygame.sprite.Sprite):  # Personnage de base, possédant les caractéristiques communes à tous les persos
    def __init__(self, speed, dashspeed, airspeed, deceleration, fallspeed, fastfallspeed, fullhop, shorthop, doublejumpheight,airdodgespeed,airdodgetime,dodgeduration):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.damages = 0.0
        self.direction = 90
        self.vx = 0           # vitesse (x,y)
        self.vy = 0
        self.grounded = False       # Le personnage touche-t-il le sol ?
        self.fastfall = False       # Le personnage fastfall-t-il ?
        self.doublejump = [False]   # Liste des double sauts, ainsi que de leur utilisation

        self.speed = speed          # vitesse au sol
        self.dashspeed = dashspeed          # vitesse de dash
        self.airspeed = airspeed    # vitesse aérienne
        self.deceleration = deceleration  # vitesse de décélération (peut permettre de faire un perso qui glisse ;) )
        self.fallspeed = fallspeed  # vitesse de chute
        self.fastfallspeed = fastfallspeed  # vitesse de fastfall
        self.fullhop = fullhop # Hauteur de saut (full hop)
        self.shorthop = shorthop # Hauteur de saut (short hop)
        self.doublejumpheight = doublejumpheight  # Hauteur des double sauts

        self.collidegroup = pygame.sprite.GroupSingle() # Groupe de collision (spécial à pygame)
        self.collidegroup.add(self)
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav")  # Son test, peut être modifié via <Personnage>.py

        self.frame = 0              # Frames écoulées depuis le début de la précédente action
        self.attack = None          # Attaque en cours
        self.can_act = True         # Le personnage peut-il agir ?
        self.upB = False            # Le personnage peut-il agir ?
        self.look_right = True

        self.hitstun = 0            # Frames de hitstun
        self.totalhitstun = 0
        self.active_hitboxes = list() # Liste des hitbox actives
        self.projectiles = list()
        self.last_hit = 0
        self.lag = 0
        self.charge = 0
        self.parry = False
        self.lenght_parry = 0
        self.tumble = False
        self.parried = False

        self.jumping = False
        self.dash = False # Unused

        self.animeframe = 0
        self.animation = "idle"
        self.name = "Name"

        self.airdodgespeed = airdodgespeed
        self.airdodgetime = airdodgetime
        self.airdodgeduration = dodgeduration
        self.airdodge = False
        self.can_airdodge = True

        self.intangibility = False
        self.dodgex = 0
        self.dodgey = 0

        self.BOUM = 0
        self.superarmor = 0

    def inputattack(self,attack):
        if self.attack != attack :
            self.animeframe = 0
            self.tumble = False
            if self.can_act :
                self.frame = 0  # on démarre à la frame 0
                self.attack = attack  # on update l'action en cours
                if attack == "UpB":
                    self.fastfall = False
                    self.can_act = False # Ne peut pas attaquer après le up B
                    self.upB = True # Effets spéciaux après upB (uniquement grounded)
    
    def animation_attack(self,attack,inputs,stage,other):
        pass # à modifier pour chaque personnage dans <Personnage>.py

    def special(self):
        return False # cancel, pour Reignaud

    def act(self, inputs,stage,other,continuer):
        if continuer :
            if self.attack is None :
                self.lag = max(0,self.lag-1)
            self.hitstun = max(0, self.hitstun-1)
            self.frame += 1
            self.animeframe += 1
            cancel = self.special()
            self.last_hit = max(self.last_hit-1,0)
            self.get_inputs(inputs,stage,other,cancel)
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
        else :
            self.BOUM = max(0,self.BOUM-1)
        


    def get_inputs(self, inputs, stage, other, cancel): # Cancel spécial pour reignaud (pour pas avoir à tout copier coller)
        self.direction = 90 if self.look_right else -90

        left, right, up, down, fullhop, shorthop, attack, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        jump = fullhop or shorthop

        if not (left or right) or (left and self.look_right) or (right and not self.look_right): # Cancel le dash au changement de direction
            self.dash = False
        if not self.grounded and self.vy > -3 and down and not (attack or special or C_Left or C_Right or C_Up or C_Down) and not self.tumble: # si le personnage est en fin de saut
            if not self.fastfall:  # fastfall
                self.vy = self.vy + self.fastfallspeed * 5
            self.fastfall = True
        if self.hitstun: # Directional Influence
            if self.totalhitstun-self.hitstun < 5 :
                if right:
                    self.vx += self.airspeed/5
                if left:
                    self.vx -= self.airspeed/5
                if up:
                    self.vy -= self.fallspeed/5
                if down:
                    self.vy += self.fallspeed/5
        else :
            if (not shield) and self.parry :
                self.lag = 3
            if self.grounded and self.attack is None and not self.lag and shield:
                if right or left:
                    self.dash = True
                    self.parry = False
                    self.lenght_parry = -10
                elif self.lenght_parry > 1 and self.lenght_parry < 8:
                    self.parry = True
                elif self.lenght_parry > 8 :
                    self.parry = False
                    if not self.parried :
                        self.lag = 10
                self.lenght_parry = self.lenght_parry+1
            else :
                self.parry = False
                if not shield :
                    self.parried = False
                    self.lenght_parry = 0
            if shield and (not self.grounded) and (self.can_airdodge) and self.attack is None and self.can_act and not self.jumping:
                self.animation = "airdodge"
                self.can_airdodge = False
                self.airdodge = True
                self.dodgex = (right-left)*self.airdodgespeed
                self.dodgey = (down-up)*self.airdodgespeed
                if not self.tumble :
                    self.vx = 0
                    self.vy = 0
                self.vx += self.dodgex*(self.airdodgeduration-self.airdodgetime)/2
                self.vy += self.dodgey*(self.airdodgeduration-self.airdodgetime)/2
                self.frame = 0
            if self.attack is None :
                self.active_hitboxes = list()
            if (self.attack is None or cancel) and not self.lag and not(self.airdodge): # Si aucune attaque n'est en cours d'exécution et si on n'est pas dans un lag (ex:landing lag)
                if self.grounded :
                    self.animation = "idle"
                elif self.vy > 0 :
                    self.animation = "fall"
                else :
                    self.animation = "jump"
                if (D_Left or D_Right or D_Up or D_Down) and self.grounded:
                    self.inputattack("Taunt")

                if right:            # Si on input à droite
                    if special :
                        self.inputattack("SideB")
                    if attack :
                        if self.grounded:
                            self.inputattack("ForwardTilt")
                        else :
                            if not self.look_right :
                                self.inputattack("BackAir")
                            else :
                                self.inputattack("ForwardAir")
                    if self.grounded and not cancel: # Si le personnage est au sol
                        self.animation = "run" if self.dash else "walk"
                        self.look_right = True  # tourne à droite et se déplace de la vitesse au sol
                        self.vx += self.dashspeed if self.dash else self.speed
                    else:             # Sinon, se déplace de la vitesse aérienne
                        if not self.tumble:
                            self.vx += self.airspeed

                if left:            # Si on input à gauche
                    if special :
                        self.inputattack("SideB")
                    if attack :
                        if self.grounded:
                            self.inputattack("ForwardTilt")
                        else :
                            if self.look_right :
                                self.inputattack("BackAir")
                            else :
                                self.inputattack("ForwardAir")
                    
                    if self.grounded and not cancel: # la même, mais vers la gauche
                        self.animation = "run" if self.dash else "walk"
                        self.look_right = False
                        self.vx -= self.dashspeed if self.dash else self.speed
                    else:
                        if not self.tumble:
                            self.vx -= self.airspeed
                if up:         # si on input vers le haut
                    if special : # si la touche spécial est pressée, et que le up b n'a pas été utilisé
                        self.inputattack("UpB")  # on input un upB
                        jump = False  # On input pas un saut en plus
                    if attack :
                        jump = False
                        if self.grounded:
                            self.inputattack("UpTilt")
                        else :
                            self.inputattack("UpAir")

                if jump and not self.jumping:        # si on input un saut
                    if self.grounded:  # Si le personnage est au sol
                        self.animeframe = 0
                        self.tumble = False
                        self.jumping = True
                        if fullhop :
                            self.vy = -self.fullhop # il utilise son premier saut
                        else :
                            self.vy = -self.shorthop # il utilise son premier saut
                        self.jumpsound.play() # joli son

                    else:  # Si le personnage est en l'air
                        self.fastfall = False  # il cesse de fastfall
                        if not self.doublejump[-1]:  # Si il possède un double saut
                            self.animeframe = 0
                            self.tumble = False
                            self.jumping = True
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
                    if special :
                        self.inputattack("DownB")

                if not (left or right or up or down):
                    if special :
                        self.inputattack("NeutralB")
                    if attack :
                        if self.grounded:
                            self.inputattack("Jab")
                        else :
                            self.inputattack("NeutralAir")

                if attack and self.dash and self.grounded:
                    self.inputattack("DashAttack")
                    self.dash = False

                if C_Left : # C-Stick inputs
                    if self.grounded: # Smash
                        self.look_right = False
                        self.inputattack("ForwardSmash")
                    else : # Aerial
                        if not self.look_right :
                            self.inputattack("ForwardAir")
                        else :
                            self.inputattack("BackAir")
                if C_Right:
                    if self.grounded : # Smash
                        self.look_right = True
                        self.inputattack("ForwardSmash")
                    else : # Aerial
                        if self.look_right :
                            self.inputattack("ForwardAir")
                        else :
                            self.inputattack("BackAir")
                if C_Down:
                    if self.grounded: # Smash
                        self.inputattack("DownSmash")
                    else : # Aerial
                        self.inputattack("DownAir")
                if C_Up:
                    if self.grounded: # Smash
                        self.inputattack("UpSmash")
                    else : # Aerial
                        self.inputattack("UpAir")

            if self.attack is not None : # si une attaque est exécutée, on anime la frame suivante
                self.animation_attack(self.attack,inputs,stage,other)
                if not self.grounded:
                    if right: # drift en l'air
                        self.vx += self.airspeed/10
                    if left:
                        self.vx -= self.airspeed/10
            if self.airdodge:
                if self.frame > self.airdodgetime and self.frame < self.airdodgeduration:
                    self.intangibility = True
                    self.tumble = False
                    #self.vx = self.dodgex*(self.airdodgeduration/self.frame)
                    #self.vy = self.dodgey*(self.airdodgeduration/self.frame)
                elif self.frame > self.airdodgeduration:
                    self.intangibility = False
                    self.airdodge = False
                    self.lag = 10

    def touch_stage(self,stage,rect):
        if rect.colliderect(stage.mainplat.rect):
            return True
        for p in stage.plats:
            if rect.colliderect(p.rect) and rect.y + rect.h < p.rect.y+self.vy+3:
                return True
        return False

    def move(self, stage):
        if not self.airdodge :
            if self.hitstun :
                self.vy = self.vy + self.fastfallspeed/2
            elif self.fastfall : # gravité
                self.vy = self.vy + self.fastfallspeed
            else :
                self.vy = self.vy + self.fallspeed
        else :
            self.vy *= 0.8
        
        # détection de collisions à la frame suivante
        nextframe = self.rect.move(self.vx,-signe(self.vy))
        if nextframe.colliderect(stage.mainplat.rect):
            while not self.rect.move(signe(self.vx),-signe(self.vy)).colliderect(stage.mainplat.rect):
                self.rect.x += signe(self.vx)
                self.x += signe(self.vx)
            self.x -= signe(self.vx)
            self.vx = 0
        nextframe = self.rect.move(0,self.vy)
        if self.touch_stage(stage,nextframe):
            while not self.touch_stage(stage,self.rect.move(0,signe(self.vy))):
                self.rect.y += signe(self.vy)
            if self.hitstun:
                self.vy = -self.vy*0.5
            else :
                self.vy = 0

        # Déplacement
        self.rect.y += self.vy
        self.x += round(self.vx)
        if self.airdodge:
            self.vx *= 0.8
        elif (not self.hitstun) and (not self.tumble):
            # déceleration et vitesse max
            if self.grounded :
                self.vx *= self.deceleration
            elif self.vx < -3*self.airspeed:
                self.vx = (self.vx - 3*self.airspeed)/2
            elif self.vx > 3*self.airspeed:
                self.vx = (self.vx + 3*self.airspeed)/2
            if abs(self.vx) < 0.01 :
                self.vx = 0
        if abs(self.vx)+abs(self.vy) < 0.5 :
            self.hitstun = 0

        # Détection de si le personnage est au sol
        if self.touch_stage(stage,self.rect.move(0,1)):
            if self.hitstun : # diminue la vitesse de hitstun
                self.vx *= 0.8
            if not self.can_act : # permet de jouer après un upb
                self.can_act = True
            if self.upB: # reset le upb
                self.upB = False
            self.grounded = True
            self.fastfall = False
            if self.airdodge :
                self.airdodge = False
                self.intangibility = False
            self.can_airdodge = True
            if self.tumble :
                self.tumble = False
                self.lag = 20
            for dj in range(len(self.doublejump)):
                self.doublejump[dj] = False
        else :
            self.grounded = False

        # respawn
        if self.rect.y > 800 or self.rect.y < -800 or self.rect.x < -900 or self.rect.x > 900 :
            self.rect.y = -200
            self.x = 0
            self.damages = 0.
            self.vy = 0
            self.vx = 0
            self.hitstun = 0
        self.rect.x = self.x - self.rect.w/2


    def draw(self, window):
        drawing_sprite,size,self.animeframe = get_sprite(self.animation,self.name,self.animeframe,self.look_right)

        drawing_sprite = pygame.transform.scale(drawing_sprite,(round(drawing_sprite.get_size()[0]*4),round(drawing_sprite.get_size()[1]*4))) # Rescale
        size = [size[0]*4,size[1]*4,size[2]*4,size[3]*4] # Rescale
        pos = [self.x + 800 - size[2]/2, self.rect.y-size[3]+self.rect.h + 449] # Position réelle du sprite
        window.blit(drawing_sprite, pos,size) # on dessine le sprite
        #self.rect.y -=  size[3] - self.rect.h # Reste à la surface du stage

        # debug
        if self.parry:
            pygame.draw.rect(window,(200,200,200),(pos[0],pos[1],self.rect.w,self.rect.h))

        # draw projectiles
        for p in self.projectiles :
            p.draw(window)

    def collide(self,other):
        for i,hitbox in enumerate(other.active_hitboxes): # Détection des hitboxes
            if self.rect.colliderect(hitbox.hit):
                if (not self.parry) and (not self.intangibility): # Parry
                    if hitbox.position_relative : # Reverse hit
                        if self.x > hitbox.hit.x+hitbox.hit.w//2 and hitbox.own.direction < 0:
                            hitbox.angle = pi - hitbox.angle
                        if self.x < hitbox.hit.x-hitbox.hit.w//2 and hitbox.own.direction > 0:
                            hitbox.angle = pi - hitbox.angle
                    if not self.superarmor :
                        self.vx = hitbox.knockback*cos(hitbox.angle)*(self.damages*hitbox.damages_stacking+1) # éjection x
                        self.vy = -hitbox.knockback*sin(hitbox.angle)*(self.damages*hitbox.damages_stacking+1) # éjection y
                        self.hitstun = hitbox.stun*(self.damages*hitbox.damages_stacking+2) # hitstun
                        self.totalhitstun = self.hitstun
                        self.damages += hitbox.damages # dommages
                        self.rect.y -= 1
                        self.attack = None # cancel l'attacue en cours
                        self.upB = False
                        self.can_act = True
                        self.can_airdodge = True
                        self.fastfall = False
                        if abs(self.vx) + abs(self.vy) > 5 :
                            self.tumble = True
                    else :
                        if self.superarmor != -1 :
                            self.superarmor = max(self.superarmor - hitbox.damages,0)
                        self.damages += hitbox.damages/2
                else :
                    if self.parry :
                        self.parried = True
                        other.attack = None
                        other.lag = max(hitbox.damages*hitbox.knockback/10,15)
                del other.active_hitboxes[i] # Supprime la hitbox
                return
        for i,projectile in enumerate(other.projectiles): # Détection des projectiles
            for h in self.active_hitboxes :
                if h.deflect and h.hit.colliderect(projectile.rect):
                    projectile.deflect(h.modifier)
                    self.projectiles.append(projectile)
                    del other.projectiles[i] # Supprime la hitbox
                    return

            if self.rect.colliderect(projectile.rect) and not self.last_hit:
                self.last_hit = 10 # invincibilité aux projectiles de 10 frames
                if (not self.parry) and (not self.intangibility): # Parry
                    if not self.superarmor :
                        self.vx = projectile.knockback*cos(projectile.angle)*(self.damages*projectile.damages_stacking+1) # éjection x
                        self.vy = -projectile.knockback*sin(projectile.angle)*(self.damages*projectile.damages_stacking+1) # éjection y
                        self.hitstun = projectile.stun*(self.damages*projectile.damages_stacking/2+1) # hitstun
                        self.totalhitstun = self.hitstun
                        self.damages += projectile.damages # dommages
                        self.rect.y -= 1
                        self.attack = None
                        self.upB = False
                        self.can_act = True
                        self.can_airdodge = True
                        self.fastfall = False
                        if abs(self.vx) + abs(self.vy) > 5 :
                            self.tumble = True
                    else :
                        if self.superarmor != -1 :
                            self.superarmor = max(self.superarmor - projectile.damages,0)
                        self.damages += projectile.damages/2
                else :
                    if self.parry :
                        self.parried = True
                        other.attack = None
                        other.lag = max(projectile.damages*projectile.knockback/10,15)
                return