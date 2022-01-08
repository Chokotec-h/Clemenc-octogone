from random import choice, randint
from DATA.utilities.Base_Char import Char, Hitbox, change_left, signe
import pygame
from math import pi,cos,sin
from DATA.utilities.Sound_manager import playsound

##### Reignaud

class Reignaud(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=2.2, dashspeed=4.1, airspeed=1, deceleration=0.5, fallspeed=1.15, fastfallspeed=1.9, fullhop=22, shorthop=17,
                         doublejumpheight=23,airdodgespeed=4,airdodgetime=2,dodgeduration=18)

        self.rect = pygame.Rect(100,0,48,120) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/SE/jump.wav") # Son test
        self.name = "Reignaud"
        self.x = x
        self.rect.y = y
        self.cancelable = False
        self.counter = False
        self.duration_mot_invasif = 0
        self.player = player
    
    def __str__(self) -> str:
        return "Reignaud"

    def special(self,inputs):
        if self.attack is None :
            self.cancelable = False
        return self.cancelable

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            self.cancelable = False
            if self.frame < 8 and self.frame > 6 and special and self.charge < 24:
                self.frame = 6
                self.vy = 0
                self.vx = 0
                self.charge += 1
            if self.frame == 15: # Saute frame 15
                self.can_act = False # ne peut pas agir après un grounded up B
                self.vy = -self.charge - 10
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts
                if self.charge // 6 == 4 :
                    self.active_hitboxes.append(Hitbox(0,0,48,120,3*pi/4,12,15,1/200,14,10,self,True,sound="hits and slap/cool hit.wav"))
                self.charge = 0
            if self.frame > 25 :
                self.attack = None

        if attack == "NeutralB":
            if self.frame < 5 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if not self.projectiles:
                if self.frame < 5 :
                    self.cancelable = True
                else :
                    self.cancelable = False
                if self.frame == 5 :
                    self.duration_mot_invasif = 5
                    self.projectiles.append(Mot_invasif(self.x,self.rect.y,other,self,stage))
                if self.frame > 15: # 10 frames de lag
                    self.attack = None
            else :
                if self.frame > 15 :
                    self.attack = None

        if attack == "DownB":
            if self.frame < 8 :
                self.cancelable = True
            else :
                self.cancelable = False
            if self.frame == 8 :
                self.counter = True
            if self.frame > 29 :
                self.counter = False
            if self.frame > 67 : # 46 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame < 16 :
                self.cancelable = True
                if self.frame < 8 :
                    if left :
                        self.look_right = False
                    else :
                        self.look_right = True
            else :
                self.cancelable = False
            if self.frame == 16 :
                self.vx = signe(self.direction)*30
                self.active_hitboxes.append(Hitbox(24,32,64,32,pi/4,20 if other.look_right == self.look_right else 10,16 if other.look_right == self.look_right else 8,1/250,22 if other.look_right == self.look_right else 11,6,self,False,sound="hits and slap/mini hit.wav"))
            if self.frame < 25 :
                self.vy = -self.fallspeed
            if self.frame > 66 : # 44 frames de lag
                self.attack = None

        if attack == "Jab":
            if self.frame < 7 :
                self.cancelable = True
            else :
                self.cancelable = False
            if self.frame == 7 :
                self.active_hitboxes.append(Hitbox(40,42,50,42,pi/4,10,10,1/300,12,3,self,False,sound="hits and slap/punch.mp3"))

            if self.frame > 20: # 14 frames de lag
                self.attack = None

        if attack == "DownTilt":
            if self.frame < 6 :
                self.cancelable = True
            else :
                self.cancelable = False
            if self.frame == 6 :
                self.active_hitboxes.append(Hitbox(40,62,60,42,pi/6,11,9,1/250,17,4,self,False,sound="hits and slap/cool hit.wav"))

            if self.frame > 20: # 15 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame < 3 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame < 8 :
                self.cancelable = True
            else :
                self.cancelable = False
            if self.frame > 8 and self.frame < 24 :
                self.intangibility = True
            else :
                self.intangibility = False
            if self.frame == 24:
                self.active_hitboxes.append(Hitbox(32,8,48,70,pi/4,13,10,1/240,13,8,self,False,sound="hits and slap/punch1.mp3"))

            if self.frame > 52: # 20 frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame < 8 :
                self.cancelable = True
            else :
                self.cancelable = False
            if self.frame >= 8 and self.frame < 17 and self.frame%4 == 0:
                self.active_hitboxes.append(Hitbox(-5,-25,58,32,pi/2,1,1.2,0,6,3,self,False))
            if self.frame == 20:
                self.active_hitboxes.append(Hitbox(-6,-25,60,32,pi/2,15,4.8,1/200,15,3,self,False))
            if self.frame > 27: # 11 Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame < 8 :
                self.cancelable = True
            else :
                self.cancelable = False
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(20,-5,68,80,2*pi/5,14,11,1/200,13,7,self,False,sound="hits and slap/punch1.mp3"))
            if self.frame > 25: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 23 and self.frame > 8 :
                    self.lag = 10 # Auto cancel frame 1-8 et 23+, 8 frames de landing lag

        if attack == "ForwardAir":
            if self.frame < 8 :
                self.cancelable = True
            else :
                self.cancelable = False
            if self.frame == 8:
                self.active_hitboxes.append(Hitbox(22,42,64,64,-pi/6,11,9,1/250,12,8,self,False,sound="hits and slap/cool hit.wav"))

            if self.frame > 28: # 12 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 26 and self.frame > 8 :
                    self.lag = 11 # Auto cancel frame 1-8 et 26+, 11 frames de landing lag

        if attack == "BackAir":
            if self.frame < 10 :
                self.cancelable = True
            else :
                self.cancelable = False
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(-50,42,60,48,-3*pi/4,16,18,1/200,15,3,self,False,sound="hits and slap/punch2.mp3"))

            if self.frame > 30: # 17 frames de lag
                self.cancelable = False
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 28 and self.frame > 10 :
                    self.lag = 16 # Auto cancel frame 1-10 et 28+, 16 frames de landing lag

        if attack == "DownAir":
            if self.frame < 16 :
                self.cancelable = True
            else :
                self.cancelable = False
            if self.frame == 16 :
                self.active_hitboxes.append(Hitbox(-2,64,52,64,-pi/2,15,19,1/150,10,3,self,False,sound="hits and slap/cool hit.wav"))

            if self.frame > 44: # 28 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 30 and self.frame > 16 :
                    self.lag = 19 # Auto cancel frame 1-16 et 30+, 19 frames de landing lag

        if attack == "NeutralAir":
            if self.frame < 10 :
                self.cancelable = True
            else :
                self.cancelable = False
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(64,32,24,24,pi/2,12,7.5,1/250,12,20,self,False,sound="hits and slap/hit.wav"))
            if self.frame > 10 :
                if self.active_hitboxes :
                    self.active_hitboxes[-1].relativex += signe(self.direction)*sin(pi*self.frame/10)*176/11
                    self.active_hitboxes[-1].relativey += -cos(pi*self.frame/10)*30
            if self.frame > 40: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 38 and self.frame > 2 :
                    self.lag = 10 # Auto cancel frame 1-2 et 38+, 10 frames de landing lag

        if attack == "ForwardSmash":
            if self.frame < 8 :
                self.cancelable = True
            else :
                self.cancelable = False
            if self.frame > 14 and self.frame < 16 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 14
                self.animeframe -= 1
                self.charge = self.charge+1
            if self.frame == 20:
                self.charge = min(self.charge,100)
                self.active_hitboxes.append(Hitbox(32,42,72,32,pi/4,19+8*(self.charge/100),19,1/200,20+7*(self.charge/100),4,self,False,sound="hits and slap/punch.mp3"))
            if self.frame > 45: # 21 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "UpSmash":
            if self.frame < 8 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
                self.cancelable = True
            else :
                self.cancelable = False
            if self.frame > 7 and self.frame < 10 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 8
                self.animeframe -= 1
                self.charge = self.charge+1
            if self.frame == 14:
                self.charge = min(self.charge,100)
                self.active_hitboxes.append(Hitbox(42,-15,42,98,pi/2,19+5*(self.charge/100),19.5,1/160,18+7*(self.charge/100),4,self,False,sound="hits and slap/punch1.mp3"))
            if self.frame > 45: # 27 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownSmash":
            if self.frame < 3 :
                self.cancelable = True
            else :
                self.cancelable = False

            if self.frame < 3 :
                if left : # peut reverse netre les frames 1 et 2
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 3 and self.frame < 6  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.animeframe -= 1
                self.frame = 4
                self.charge = self.charge+1
            if self.frame == 15 :
                self.charge = min(self.charge,100)
                self.active_hitboxes.append(Hitbox(35,52,64,64,pi/6,15+8*(self.charge/100),13,1/200,20+5*(self.charge/100),13,self,False,sound="hits and slap/punch2.mp3"))
                self.active_hitboxes.append(Hitbox(change_left(35,64),52,64,64,5*pi/6,21+8*(self.charge/100),13,1/200,20+5*(self.charge/100),13,self,False,sound="hits and slap/punch2.mp3"))
            if self.frame == 18:
                if self.active_hitboxes :
                    self.active_hitboxes[-1].knockback *= 0.75
                    self.active_hitboxes[-1].damages = 7
            if self.frame > 54: # 23 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(20,-5,40,125,pi/4,12,13,1/250,14,20,self,False))
            if self.frame > 5 and self.frame < 40 :
                self.vy = 0
                if self.grounded :
                    self.vx += self.dashspeed*signe(self.direction)/(self.frame-2)*12
                else :
                    self.vx -= self.dashspeed*signe(self.direction)
            if self.frame > 40: # 24 frames de lag
                self.attack = None

        if attack == "UpTaunt":
            
            if self.frame > 30: # Durée de 30 frames
                self.attack = None

        if attack == "DownTaunt":
            
            if self.frame > 30: # Durée de 30 frames
                self.attack = None

        if attack == "LeftTaunt":
            
            if self.frame > 30: # Durée de 30 frames
                self.attack = None

        if attack == "RightTaunt":
            
            if self.frame > 30: # Durée de 30 frames
                self.attack = None


    def collide(self,other): # Gestion du contre
        self.parrying = False
        for i,hitbox in enumerate(other.active_hitboxes): # Détection des hitboxes
            if self.rect.colliderect(hitbox.hit):
                if (not self.parry) and (not self.intangibility) and not (self.counter): # Parry and counter
                    self.tumble = True
                    if hitbox.position_relative : # Reverse hit
                        if self.x > hitbox.hit.x+hitbox.hit.w//2 and hitbox.own.direction < 0:
                            hitbox.angle = pi - hitbox.angle
                        if self.x < hitbox.hit.x-hitbox.hit.w//2 and hitbox.own.direction > 0:
                            hitbox.angle = pi - hitbox.angle
                        
                    self.vx = hitbox.knockback*cos(hitbox.angle)*(self.damages*hitbox.damages_stacking+1) # éjection x
                    self.vy = -hitbox.knockback*sin(hitbox.angle)*(self.damages*hitbox.damages_stacking+1) # éjection y
                    self.hitstun = hitbox.stun*(self.damages*hitbox.damages_stacking/2+1) # hitstun
                    self.damages += hitbox.damages # dommages
                    self.rect.y -= 1
                    self.attack = None # cancel l'attacue en cours
                else :
                    if self.parry :
                        self.parrying = True
                    if self.counter :
                        self.active_hitboxes.append(Hitbox(-32,-32,112,164,pi-1,hitbox.knockback,hitbox.damages*2 if other.x*signe(self.direction) < self.x*signe(self.direction) else hitbox.damages,1/250,hitbox.stun,3,self,False))
                del other.active_hitboxes[i] # Supprime la hitbox
                return
        for i,projectile in enumerate(other.projectiles): # Détection des projectiles
            for h in self.active_hitboxes :
                if h.deflect and h.hit.colliderect(projectile.rect):
                    projectile.deflect(h.modifier)
                    self.projectiles.append(projectile)
                    del other.projectiles[i] # Supprime la hitbox
                    return

            if self.rect.colliderect(projectile.rect) and projectile not in self.immune_to_projectiles:
                if (not self.parry) and (not self.intangibility) and (not self.counter) : # Parry
                    self.immune_to_projectiles.append(projectile)
                    self.tumble = True
                    self.vx = projectile.knockback*cos(projectile.angle)*(self.damages*projectile.damages_stacking+1) # éjection x
                    self.vy = -projectile.knockback*sin(projectile.angle)*(self.damages*projectile.damages_stacking+1) # éjection y
                    self.hitstun = projectile.stun*(self.damages*projectile.damages_stacking/2+1) # hitstun
                    self.damages += projectile.damages # dommages
                    self.rect.y -= 1
                    self.attack = None
                else :
                    if self.parry :
                        self.parrying = True
                    if self.counter :
                        self.active_hitboxes.append(Hitbox(-32,-32,112,164,pi-1,projectile.knockback,projectile.damages*2 if other.x*signe(self.direction) < self.x*signe(self.direction) else projectile.damages,1/250,projectile.stun,3,self,False))
                return
###################          
""" Projectiles """
###################

class Mot_invasif():
    # Mots invasifs à ajouter : Construction, Problématique, Prendre des notes,
    def __init__(self,x,y,other,own:Reignaud,stage) -> None:
        self.other = other
        self.own = own
        self.duration=5
        Texte = choice(["Ressenti","Construction"])
        self.sprite = pygame.transform.scale(pygame.image.load(f"./DATA/Images/Sprites/Projectiles/Mot_invasif/{Texte}.png"),(32,128))
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vy = 0
        self.stage = stage
        self.damages = 0.4
        self.stun = 0
        self.knockback = 0
        self.damages_stacking = 0
        self.angle = 0
        self.projectile_immune = []
    
    def touch_stage(self,stage,rect):
        if rect.colliderect(stage.mainplat.rect):
            return True
        for p in stage.plats:
            if rect.colliderect(p.rect) and rect.y + rect.h-4 < p.rect.y+self.vy+4:
                return True
        return False


    def touch_stage(self,stage,rect):
        if rect.colliderect(stage.mainplat.rect):
            return True
        for p in stage.plats:
            if rect.colliderect(p.rect) and rect.y + rect.h < p.rect.y+self.vy+3:
                return True
        return False

    def update(self):
        self.duration=self.own.duration_mot_invasif
        if self.touch_stage(self.stage,self.rect):
            self.vy = -1
        else :
            self.vy += 1
        self.rect.y += self.vy
        for hitbox in self.other.active_hitboxes :
            if self.rect.colliderect(hitbox.hit):
                self.other.vx = (hitbox.knockback)*cos(hitbox.angle)*(self.damages*hitbox.damages_stacking+1)/max((self.other.superarmor/5),1) # éjection x
                self.other.vy = -(hitbox.knockback)*sin(hitbox.angle)*(self.damages*hitbox.damages_stacking+1)/max((self.other.superarmor/5),1) # éjection y
                self.other.hitstun = hitbox.stun*(self.other.damages*hitbox.damages_stacking+2)-(self.other.superarmor/5) # hitstun
                self.other.totalhitstun = self.other.hitstun
                self.other.damages += hitbox.damages # dommages
                self.other.rect.y -= 1
                self.other.attack = None # cancel l'attaque en cours
                self.other.upB = False
                self.other.can_act = True
                self.other.can_airdodge = True
                self.other.fastfall = False
                if abs(self.other.vx) + abs(self.other.vy) > 5 :
                    self.other.tumble = True
                self.own.duration_mot_invasif -= 1
                self.own.projectiles.append(Mot_invasif(randint(-300,300),0,self.other,self.own,self.stage))
                self.other.active_hitboxes = list()
                return
        for projectile in self.other.projectiles: # Détection des projectiles
            if self.rect.colliderect(projectile.rect) and projectile not in self.projectile_immune:
                self.projectile_immune.append(projectile)
                self.own.duration_mot_invasif -= 1
                self.own.projectiles.append(Mot_invasif(randint(-300,300),0,self.other,self.own,self.stage))
                self.own.projectiles[-1].projectile_immune.append(projectile)


    def deflect(self,modifier):
        self.own.projectiles.append(self)
        self.other.projectiles.pop(-1)
    def draw(self,window):
        window.blit(self.sprite, (self.rect.x+800,self.rect.y+450)) # on dessine le sprite

##### Autres skins
