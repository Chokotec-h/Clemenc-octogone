from DATA.utilities.Base_Char import Char, Hitbox, signe
import pygame
from math import exp, pi

##### Copier

class Renault(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=1.7, dashspeed=5, airspeed=0.9, deceleration=0.7, fallspeed=0.5, fastfallspeed=1, fullhop=13, shorthop=10,
                         doublejumpheight=15,airdodgespeed=6,airdodgetime=3,dodgeduration=15)

        self.rect = pygame.Rect(100,0,48,120) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav") # Son test
        self.name = "Renault"
        self.x = x
        self.rect.y = y
        self.player = player
        self.daccord = 0
    
    def __str__(self) -> str:
        return "Renault"

    def special(self):
        if self.dash and self.frame % 6 == 0 and self.grounded and self.attack is None:
            self.active_hitboxes.append(Hitbox(0,0,70,48,pi/3,9,2,0,4,2,self,boum=-1))
        return False

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            if self.frame == 11: # Saute frame 11
                self.can_act = False # ne peut pas agir après un grounded up B
                self.vy = -20
                self.attack = None
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts
            #if self.frame < 6 :
            #    if left : # peut reverse netre les frames 1 et 5
            #        self.look_right = False
            #    if right :
            #        self.look_right = True
            #if self.frame == 6: # Hitbox frame 6-11
            #    self.active_hitboxes.append(Hitbox(-1.5,88.5,51,48,2*pi/3,18,32,1/150,40,5,self,False))

        if attack == "NeutralB":
            if self.frame < 5 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 15: # 10 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownB":
            if self.frame > 15 and self.frame < 40 :
                self.vx = (right-left)*12
                self.vy = (down-up)*12
                self.show = False
                self.intangibility = 4
            if self.frame == 40 :
                self.show = True
                self.active_hitboxes.append(Hitbox(0,0,48,120,pi/2,12,16,1/250,11,2,self,boum=2))
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts
            if self.frame > 70 : # 30 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame > 80 : # 20 frames de lag
                self.attack = None

        if attack == "Jab":

            if self.frame > 22: # 10 frames de lag
                self.attack = None

        if attack == "DownTilt":
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(64,120-64,16,64,8*pi/17,8,6.4,1/200,12,8,self))

            if self.frame > 20: # 7 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame < 3 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 8 :
                self.daccord += 1
                self.active_hitboxes.append(Hitbox(48,48,64-2*self.daccord,48,pi/4,4*self.daccord,2*self.daccord,self.daccord/500,4*self.daccord,3,self))
            if self.frame == 10 and self.active_hitboxes or other.parried :
                self.daccord = 0
            if self.frame > 30: # 8 frames de lag
                self.attack = None
        elif not attack == "DashAttack":
            self.daccord = 0

        if attack == "UpTilt":
            if self.frame > 25: # 11 Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(0,0,36,36,pi-exp(1)*pi/5,10,exp(1),1/exp(3),14,10,self))
            if self.frame > 8 and self.active_hitboxes :
                self.active_hitboxes[-1].relativex += signe(self.direction)*10
                self.active_hitboxes[-1].relativey -= exp((8-self.frame)/5)*15

            if self.frame > 30: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 15 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 15+

        if attack == "ForwardAir":
            if self.frame == 7 :
                self.active_hitboxes.append(Hitbox(50,36,36,36,pi/3,12,6,1/200,7,5,self))
            if self.frame > 7 and self.active_hitboxes :
                self.active_hitboxes[-1].relativex += signe(self.direction)*5
                self.active_hitboxes[-1].relativey += 8

            if self.frame > 25: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-5 # Auto cancel frame 1-5 et 20+

        if attack == "BackAir":

            if self.frame > 25: # 14 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 20+

        if attack == "DownAir":
            if self.frame == 18 :
                self.active_hitboxes.append(Hitbox(52,40,52,28,-pi/3,19,26.6,1/200,14,2,self,boum=5))
            if self.frame == 19 and self.active_hitboxes:
                self.active_hitboxes.append(Hitbox(52,72,42,42,-pi/2,2,2.6,1/800,2,8,self))
            if self.frame > 19 and self.active_hitboxes :
                self.active_hitboxes[-1].relativex -= self.frame*signe(self.direction)/2
                self.active_hitboxes[-1].relativey += 30-self.frame

            if self.frame > 50: # 29 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 40 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 40+

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
                if self.charge%3 == 2 :
                    self.active_hitboxes.append(Hitbox(48,48,36,36,pi/4,1,0.3,0,5,2,self))
            if self.frame == 20 :
                self.charge = min(100,self.charge)
            if self.frame == 22 :
                self.active_hitboxes.append(Hitbox(48,48,36,36,pi/2,2,1,0,5,3,self,boum=-2))
            if self.frame == 25 :
                self.active_hitboxes.append(Hitbox(72,24,36,36,pi,2,1,0,5,3,self,boum=-2))
            if self.frame == 28 :
                self.active_hitboxes.append(Hitbox(96,48,36,36,-pi/2,2,1,0,5,3,self,boum=-2))
            if self.frame == 31 :
                self.active_hitboxes.append(Hitbox(72,72,36,36,0,2,1,0,5,3,self,boum=-2))
            if self.frame == 34 :
                self.active_hitboxes.append(Hitbox(50,34,64,64,pi/6,18+6*(self.charge/100),8,1/200,17+5*(self.charge/100),3,self))
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
            if self.frame == 20 :
                self.charge = min(100,self.charge)
                self.active_hitboxes.append(Hitbox(54,100,48,22,pi/2,20+8*(self.frame/100),12,1/200,19,5,self))
            if self.frame > 20 and self.active_hitboxes:
                self.active_hitboxes[-1].relativey -= 20
                self.active_hitboxes[-1].sizey += 20

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
            if self.frame > 20 and self.frame < 28 and self.frame%2 == 0 :
                self.charge = min(100,self.charge)
                self.active_hitboxes.append(Hitbox(52,90,48,48,-pi/2,2,5,0,7,2,self,boum=-1))
            if self.frame == 30 :
                self.charge = min(100,self.charge)
                self.active_hitboxes.append(Hitbox(52,90,48,48,-pi/3,20+8*(self.charge/100),8,1/300,18+7*(self.charge/100),2,self,boum=2))

            if self.frame > 40: # 23 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
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

###################          
""" Projectiles """
###################

##### Autres skins
