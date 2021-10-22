from DATA.utilities.Base_Char import Char, Hitbox, signe
import pygame
from math import pi

##### Copier

class Pyro_Aubin(Char):
    def __init__(self,x,y) -> None:
        super().__init__(speed=2, dashspeed=3, airspeed=0.9, deceleration=0.7, fallspeed=0.5, fastfallspeed=1, fullhop=13, shorthop=10,
                         doublejumpheight=15,airdodgespeed=6,airdodgetime=3,dodgeduration=15)

        self.rect = pygame.Rect(100,0,48,120) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav") # Son test
        self.name = "Pyro-Aubin"
        self.konamiadd = False
        self.x = x
        self.rect.y = y
        self.konami = []
    
    def __str__(self) -> str:
        return "Pyro-Aubin"

    def special(self): 
        if self.konami == ["Up","Up","Down","Down","Left","Right","Left","Right","B","A"]:
            self.inputattack("Superspecial")

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
            if self.konami == ["Up","Up","Down","Down","Left","Right","Left","Right"] and not self.konamiadd:
                self.konamiadd = True
                print("B")
                self.konami.append("B")
            elif not self.konamiadd :
                self.konami = []

            if self.frame > 15: # 10 frames de lag
                self.attack = None
                self.konamiadd = False
                self.charge = 0

        if attack == "DownB":
            if self.frame > 20 : # 15 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame > 80 : # 20 frames de lag
                self.attack = None

        if attack == "Jab":
            if self.konami == ["Up","Up","Down","Down","Left","Right","Left","Right","B"] and not self.konamiadd:
                self.konamiadd = True
                print("A")
                self.konami.append("A")
                self.attack = None
            elif not self.konamiadd :
                self.konami = []

            if self.frame > 22: # 10 frames de lag
                self.attack = None

        if attack == "DownTilt":

            if self.frame > 20: # 7 frames de lag
                self.attack = None

        if attack == "ForwardTilt":

            if self.frame > 30: # 8 frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame > 25: # 11 Frames de lag
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

            if self.frame > 25: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-5 # Auto cancel frame 1-5 et 20+

        if attack == "NeutralAir":
            if self.konami == ["Up","Up","Down","Down","Left","Right","Left","Right","B"] and not self.konamiadd:
                self.konamiadd = True
                print("A")
                self.konami.append("A")
                self.attack = None
            elif not self.konamiadd :
                self.konami = []

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
        
        if attack == "UpTaunt":
            if (self.konami == [] or self.konami == ["Up"]) and not self.konamiadd:
                print("Up")
                self.konamiadd = True
                self.konami.append("Up")
                self.attack = None
            elif not self.konamiadd :
                self.konami = []
            
            if self.frame > 30: # Durée de 30 frames
                self.attack = None
                self.konamiadd = False

        if attack == "DownTaunt":
            if (self.konami == ["Up","Up"] or self.konami == ["Up","Up","Down"]) and not self.konamiadd:
                self.konamiadd = True
                print("Down")
                self.konami.append("Down")
            elif not self.konamiadd :
                self.konami = []
            
            if self.frame > 30: # Durée de 30 frames
                self.attack = None
                self.konamiadd = False

        if attack == "LeftTaunt":
            if (self.konami == ["Up","Up","Down","Down"] or self.konami == ["Up","Up","Down","Down","Left","Right"]) and not self.konamiadd:
                self.konamiadd = True
                print("Left")
                self.konami.append("Left")
            elif not self.konamiadd :
                self.konami = []
            
            if self.frame > 30: # Durée de 30 frames
                self.attack = None
                self.konamiadd = False

        if attack == "RightTaunt":
            if (self.konami == ["Up","Up","Down","Down","Left"] or self.konami == ["Up","Up","Down","Down","Left","Right","Left"]) and not self.konamiadd:
                self.konamiadd = True
                print("Right")
                self.konami.append("Right")
            elif not self.konamiadd :
                self.konami = []
            
            if self.frame > 30: # Durée de 30 frames
                self.attack = None
                self.konamiadd = False

        if (not (D_Up or D_Down or D_Left or D_Right) and self.attack in ("RightTaunt","LeftTaunt","UpTaunt","DownTaunt")
            or (self.attack == "NeutralB" and attack_button)):
                self.frame = 150

        if attack == "Superspecial":
            if self.frame == 8 :
                print("boum")
                self.konami = []
                self.konamiadd = False
                self.active_hitboxes.append(Hitbox(-140,-100,328,320,pi/4,35,120,1/100,40,10,self,True))
            if self.frame > 30: # Durée de 30 frames
                self.attack = None

###################          
""" Projectiles """
###################

##### Autres skins
