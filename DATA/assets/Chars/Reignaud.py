from DATA.utilities.Base_Char import Char, Hitbox, change_left, signe
import pygame
from math import pi,cos,sin

##### Reignaud

class Reignaud(Char):
    def __init__(self,x,y) -> None:
        super().__init__(speed=2, dashspeed=3, airspeed=0.9, deceleration=0.7, fallspeed=1.15, fastfallspeed=1.9, fullhop=22, shorthop=17,
                         doublejumpheight=23,airdodgespeed=4,airdodgetime=2,dodgeduration=18)

        self.rect = pygame.Rect(100,0,48,120) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav") # Son test
        self.name = "Reignaud"
        self.x = x
        self.rect.y = y
        self.cancelable = False
        self.counter = False
    
    def __str__(self) -> str:
        return "Reignaud"

    def special(self):
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
                    self.active_hitboxes.append(Hitbox(0,0,48,120,3*pi/4,12,15,1/200,14,10,self,True))
                self.charge = 0
            if self.frame > 25 :
                self.attack = None

        if attack == "NeutralB":
            if self.frame > 15: # 10 frames de lag
                self.attack = None
                self.charge = 0

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
                self.vx = signe(self.direction)*25
                self.active_hitboxes.append(Hitbox(24,32,64,32,pi/4,20 if other.look_right == self.look_right else 10,16 if other.look_right == self.look_right else 8,1/250,22 if other.look_right == self.look_right else 11,6,self,False))
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
                self.active_hitboxes.append(Hitbox(40,42,50,42,pi/4,10,10,1/300,12,3,self,False))

            if self.frame > 20: # 14 frames de lag
                self.attack = None

        if attack == "DownTilt":
            if self.frame < 6 :
                self.cancelable = True
            else :
                self.cancelable = False
            if self.frame == 6 :
                self.active_hitboxes.append(Hitbox(40,62,60,42,pi/6,11,9,1/250,17,4,self,False))

            if self.frame > 20: # 15 frames de lag
                self.attack = None

        if attack == "ForwardTilt":

            if self.frame > 30: # 8 frames de lag
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
                self.active_hitboxes.append(Hitbox(42,32,48,48,2*pi/5,14,11,1/200,13,7,self,False))
            if self.frame > 25: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                self.cancelable = False
                if self.frame < 15 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 15+

        if attack == "ForwardAir":

            if self.frame > 50: # 29 frames de lag
                self.attack = None

            if self.grounded :
                self.cancelable = False
                self.attack = None
                if self.frame < 40 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 40+

        if attack == "BackAir":
            if self.frame < 10 :
                self.cancelable = True
            else :
                self.cancelable = False
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(-50,42,60,48,-pi/4,16,18,1/200,15,3,self,False))

            if self.frame > 30: # 17 frames de lag
                self.cancelable = False
                self.attack = None

            if self.grounded :
                self.cancelable = False
                self.attack = None
                if self.frame < 22 :
                    self.lag = self.frame-6 # Auto cancel frame 1-6 et 22+

        if attack == "DownAir":
            if self.frame < 16 :
                self.cancelable = True
            else :
                self.cancelable = False
            if self.frame == 16 :
                self.active_hitboxes.append(Hitbox(-2,64,52,64,-pi/2,15,19,1/150,10,3,self,False))

            if self.frame > 44: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.cancelable = False
                self.attack = None
                if self.frame < 32 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 32+

        if attack == "NeutralAir":
            if self.frame < 10 :
                self.cancelable = True
            else :
                self.cancelable = False
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(64,32,24,24,pi/2,12,7.5,1/250,12,20,self,False))
            if self.frame > 10 :
                if self.active_hitboxes :
                    self.active_hitboxes[-1].relativex += signe(self.direction)*sin(pi*self.frame/10)*176/11
                    self.active_hitboxes[-1].relativey += -cos(pi*self.frame/10)*30
            if self.frame > 40: # 17 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 30 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 30+

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
                self.active_hitboxes.append(Hitbox(32,42,72,32,pi/4,29+8*(self.charge/100),19,1/200,20+7*(self.charge/100),4,self,False))
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
                self.active_hitboxes.append(Hitbox(42,-15,42,98,pi/2,32+5*(self.charge/100),19.5,1/160,18+7*(self.charge/100),4,self,False))
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
                self.active_hitboxes.append(Hitbox(35,52,64,64,pi/6,21+8*(self.charge/100),13,1/200,20+5*(self.charge/100),13,self,False))
                self.active_hitboxes.append(Hitbox(change_left(35,64),52,64,64,5*pi/6,21+8*(self.charge/100),13,1/200,20+5*(self.charge/100),13,self,False))
            if self.frame == 18:
                if self.active_hitboxes :
                    self.active_hitboxes[-1].knockback *= 0.75
                    self.active_hitboxes[-1].damages = 7
            if self.frame > 54: # 23 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
            if self.frame < 26 :
                self.vy = 0
                if self.grounded :
                    self.vx += self.dashspeed*signe(self.direction)
                else :
                    self.vx -= self.dashspeed*signe(self.direction)
            if self.frame > 50: # 24 frames de lag
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
                        self.active_hitboxes.append(Hitbox(32,48,64,64,pi-1,hitbox.knockback,hitbox.damages*2 if other.x*signe(self.direction) < self.x*signe(self.direction) else hitbox.damages,1/250,hitbox.stun,3,self,False))
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
                if (not self.parry) and (not self.intangibility) and (not self.counter) : # Parry
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
                        self.active_hitboxes.append(Hitbox(32,48,64,64,pi-1,projectile.knockback,projectile.damages*2 if other.x*signe(self.direction) < self.x*signe(self.direction) else projectile.damages,1/250,projectile.stun,3,self,False))
                return
###################          
""" Projectiles """
###################

##### Autres skins
