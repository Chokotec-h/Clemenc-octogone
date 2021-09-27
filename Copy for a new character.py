from Base_Char import Char, Hitbox, signe
import pygame
from math import pi

##### Perso

class Nom_Personnage(Char):
    def __init__(self) -> None:
        super().__init__(speed=2, dashspeed=3, airspeed=0.9, deceleration=0.7, fallspeed=0.5, fastfallspeed=1, fullhop=13, shorthop=10,
                         doublejumpheight=15)

        self.rect = pygame.Rect(100,0,10,10) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav") # Son test
        self.name = "Name"


    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up

        if attack == "UpB":
            if self.frame < 6 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 11: # Saute frame 11
                self.sprite_frame = 0
                self.can_act = False # ne peut pas agir après un grounded up B
                self.vy = -20
                self.attack = None
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts

            #if self.frame == 6: # Hitbox frame 6-11
            #    if not self.look_right :
            #        angle = pi/3
            #    else:
            #        angle = 2*pi/3
            #    self.active_hitboxes.append(Hitbox(-1.5,88.5,51,48,angle,18,32,1/150,40,5,self,False))

        if attack == "NeutralB":
            if self.frame > 15: #  frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownB":
            if self.frame > 20 : # 15 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame < 8 :
                if left : # peut reverse netre les frames 1 et 7
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 95 : #  frames de lag
                self.attack = None

        if attack == "Jab":
            if self.frame > 22: #  frames de lag
                self.attack = None

        if attack == "DownTilt":
            if self.frame > 20: #  frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame > 35: #  frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame > 25: #  Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame > 25: #  frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 15 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 15+

        if attack == "ForwardAir":
            if self.frame > 50: #  frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 40 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 40+

        if attack == "BackAir":
            if self.frame > 25: #  frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 20+

        if attack == "DownAir":
            if self.frame > 25: #  frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-5 # Auto cancel frame 1-5 et 20+

        if attack == "NeutralAir":
            if self.frame > 40: #  frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 30 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 30+

        if attack == "ForwardSmash":
            if self.frame > 6 and self.frame < 9 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 7
                self.charge = self.charge+1

            #elif self.frame == 12 : # Active on 12-18
            #    self.charge = min(self.charge,100)
            #    if not self.look_right :
            #        angle = 3*pi/4
            #    else :
            #        angle = pi/4
            #    self.active_hitboxes.append(Hitbox(60*signe(self.direction)+12,16,52,64,angle,12*(self.charge/200+1),14,1/250,8*(self.charge/100+1),4,self,True,True,2))
           
            if self.frame > 45: #  frames de lag
                self.attack = None
                self.charge = 0

        if attack == "UpSmash":
            if self.frame < 5 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 5 and self.frame < 8  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 6
                self.charge = self.charge+1

            #elif self.frame == 10 : # Active on 10-15
            #    self.charge = min(self.charge,100)
            #    if not self.look_right :
            #        angle = 2*pi/6
            #    else :
            #        angle = 4*pi/6
            #    self.active_hitboxes.append(Hitbox(30*signe(self.direction)+12,-10,32,32,angle,10*(self.charge/200+1),13,1/250,6*(self.charge/10+1),6,self,False))

            if self.frame > 40: #  frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownSmash":

            if self.frame < 2 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 3 and self.frame < 6  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 4
                self.charge = self.charge+1
            elif self.frame == 7 : # Active on 7-9
                self.charge = min(self.charge,100)
                if not self.look_right :
                    angle = 5*pi/6
                else :
                    angle = pi/6
                self.active_hitboxes.append(Hitbox(40*signe(self.direction)+12,60,32,32,angle,7*(self.charge/200+1),12.5,1/250,5*(self.charge/50+1),3,self,False))
            
            elif self.frame == 15 : # Active on 15-17
                self.charge = min(self.charge,100)
                if not self.look_right :
                    angle = pi/6
                else :
                    angle = 5*pi/6
                self.active_hitboxes.append(Hitbox(-40*signe(self.direction)+12,60,32,32,angle,9*(self.charge/200+1),14.5,1/250,5*(self.charge/50+1),3,self,False))

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

            if self.frame > 50: #  frames de lag
                self.attack = None

        if attack == "Taunt":
            if self.frame > 30: # Durée de 30 frames
                self.attack = None

###################          
""" Projectiles """
###################

# Objets projectiles si le perso en possède