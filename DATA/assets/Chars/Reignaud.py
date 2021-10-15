from DATA.utilities.Base_Char import Char, Hitbox, signe
import pygame
from math import factorial, pi,cos,sin

##### Reignaud

class Reignaud(Char):
    def __init__(self,x,y) -> None:
        super().__init__(speed=2, dashspeed=3, airspeed=0.9, deceleration=0.7, fallspeed=1.2, fastfallspeed=2, fullhop=20, shorthop=15,
                         doublejumpheight=21,airdodgespeed=6,airdodgetime=3,dodgeduration=15)

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
        return self.cancelable

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            self.cancelable = False
            if self.frame < 8 and self.frame > 6 and special and self.charge < 24:
                self.frame = 6
                self.vy = 0
                self.charge += 1
            if self.frame == 15: # Saute frame 15
                self.can_act = False # ne peut pas agir après un grounded up B
                self.vy = -self.charge - 10
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts
                if self.charge // 6 == 4 :
                    self.active_hitboxes.append(Hitbox(0,0,48,120,3*pi/4,12,15,1/200,14,10,self))
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
            
            if self.frame > 66 : # 44 frames de lag
                self.attack = None

        if attack == "Jab":

            if self.frame > 22: # 10 frames de lag
                self.attack = None

        if attack == "DownTilt":

            if self.frame > 20: # 7 frames de lag
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
                self.active_hitboxes.append(Hitbox(-5,-25,58,32,pi/2,1,3,0,6,3,self,False))
            if self.frame == 20:
                self.active_hitboxes.append(Hitbox(-6,-25,60,32,pi/2,15,6,1/200,15,3,self,False))
            if self.frame > 27: # 11 Frames de lag
                self.attack = None

        if attack == "UpAir":

            if self.frame > 25: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 15 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 15+

        if attack == "ForwardAir":

            if self.frame > 50: # 29 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 40 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 40+

        if attack == "BackAir":

            if self.frame > 25: # 14 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 20+

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
                self.attack = None
                if self.frame < 32 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 32+

        if attack == "NeutralAir":

            if self.frame > 40: # 17 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 30 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 30+

        if attack == "ForwardSmash":
            if self.frame > 6 and self.frame < 9 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 7
                self.animeframe -= 1
                self.charge = self.charge+1
            if self.frame > 45: # 30 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "UpSmash":

            if self.frame < 5 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 5 and self.frame < 8  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.animeframe -= 1
                self.frame = 6
                self.charge = self.charge+1

            if self.frame > 40: # 25 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownSmash":

            if self.frame < 3 :
                if left : # peut reverse netre les frames 1 et 2
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 3 and self.frame < 6  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.animeframe -= 1
                self.frame = 4
                self.charge = self.charge+1

            if self.frame > 40: # 23 frames de lag
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

        if attack == "Taunt":
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
