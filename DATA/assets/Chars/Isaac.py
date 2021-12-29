from DATA.utilities.Base_Char import Char, Hitbox, change_left, signe
import pygame
from math import pi, sqrt
from DATA.utilities.Sound_manager import playsound

##### Isaac Newton

class Isaac(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=1.3, dashspeed=2.6, airspeed=1.5, deceleration=0.8, fallspeed=0.3, fastfallspeed=2, fullhop=12, shorthop=8,
                         doublejumpheight=11,airdodgespeed=7,airdodgetime=3,dodgeduration=15)

        self.rect = pygame.Rect(100,0,48,120) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/SE/jump.wav") # Son test
        self.name = "Isaac"
        self.x = x
        self.rect.y = y
        self.player = player
        self.antigravity = False
        self.otherfallspeed = 0
        self.otherfastfallspeed = 0
    
    def __str__(self) -> str:
        return "Isaac"

    def special(self,inputs):
        pass

    def animation_attack(self,attack,inputs,stage,other:Char):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            if self.frame == 10: # Saute frame 11
                self.fallspeed = -self.fallspeed
                self.fastfallspeed = -self.fastfallspeed
                self.fullhop = -self.fullhop
                self.shorthop = -self.shorthop
                self.doublejumpheight = -self.doublejumpheight
                self.attack = None
                self.can_act = True
                self.upB = False
                self.vy *= 0.75
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
            if self.frame > 20 : # 15 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame > 80 : # 20 frames de lag
                self.attack = None

        if attack == "Jab":

            if self.frame > 22: # 10 frames de lag
                self.attack = None

        if attack == "DownTilt":

            if self.frame > 20: # 7 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame < 3 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True

            if self.frame > 30: # 8 frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame > 25: # 11 Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame == 0 :
                self.antigravity = False
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(48,48,36,4,pi/2,14,8,1/200,18,7,self))
            if self.frame > 10 and self.frame < 17 :
                if self.active_hitboxes:
                    self.active_hitboxes[-1].sizey += 10
                    self.active_hitboxes[-1].relativey -= 10
                elif not self.antigravity :
                    self.otherfallspeed = other.fallspeed
                    self.otherfastfallspeed = other.fastfallspeed
                    self.antigravity = True
                
            if self.frame > 1 and self.frame < 25 and self.antigravity :
                other.fallspeed = 0
                print("Upair")
                other.fastfallspeed = 0

            if self.frame > 25 and self.antigravity: # 8 frames de lag
                print("Reset",self.otherfastfallspeed)
                other.fallspeed = self.otherfallspeed
                other.fastfallspeed = self.otherfastfallspeed
                self.attack = None

            if self.grounded :
                if self.antigravity :
                    print("Reset",self.otherfastfallspeed)
                    other.fallspeed = self.otherfallspeed
                    other.fastfallspeed = self.otherfastfallspeed
                self.attack = None
                if self.frame < 40 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 40+

        if attack == "ForwardAir":
            if self.frame == 1 :
                self.antigravity = False
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(48,48,4,36,0,14,8,1/200,18,7,self))
            if self.frame > 10 and self.frame < 17 :
                if self.active_hitboxes:
                    self.active_hitboxes[-1].sizex += 10
                    if not self.look_right :
                        self.active_hitboxes[-1].relativex -= 10
                elif not self.antigravity :
                    self.otherfallspeed = other.fallspeed
                    self.otherfastfallspeed = other.fastfallspeed
                    self.antigravity = True
                
            if self.frame > 1 and self.frame < 25 and self.antigravity :
                print("ForwardAir")
                other.fallspeed = 0
                other.fastfallspeed = 0

            if self.frame > 25 and self.antigravity: # 8 frames de lag
                print("Reset",self.otherfastfallspeed)
                other.fallspeed = self.otherfallspeed
                other.fastfallspeed = self.otherfastfallspeed
                self.attack = None

            if self.grounded :
                if self.antigravity :
                    print("Reset",self.otherfastfallspeed)
                    other.fallspeed = self.otherfallspeed
                    other.fastfallspeed = self.otherfastfallspeed
                self.attack = None
                if self.frame < 40 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 40+

        if attack == "BackAir":
            if self.frame == 1 :
                self.gravity_hit = False
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(change_left(48,64)+60,48,4,36,pi,14,8,1/200,18,7,self))
            if self.frame > 10 and self.frame < 17 :
                if self.active_hitboxes:
                    self.active_hitboxes[-1].sizex += 10
                    if self.look_right :
                        self.active_hitboxes[-1].relativex -= 10
                elif not self.antigravity :
                    self.otherfallspeed = other.fallspeed
                    self.otherfastfallspeed = other.fastfallspeed
                    self.antigravity = True
                
            if self.frame > 1 and self.frame < 25 and self.antigravity :
                print("BackAir")
                other.fallspeed = 0
                other.fastfallspeed = 0

            if self.frame > 25 and self.antigravity: # 8 frames de lag
                print("Reset",self.otherfastfallspeed)
                other.fallspeed = self.otherfallspeed
                other.fastfallspeed = self.otherfastfallspeed
                self.attack = None

            if self.grounded :
                if self.antigravity :
                    print("Reset",self.otherfastfallspeed)
                    other.fallspeed = self.otherfallspeed
                    other.fastfallspeed = self.otherfastfallspeed
                self.attack = None
                if self.frame < 40 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 40+

        if attack == "DownAir":
            if self.frame == 1 :
                self.antigravity = False
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(48,48,36,4,-pi/2,14,8,1/200,18,7,self))
            if self.frame > 10 and self.frame < 17 :
                if self.active_hitboxes:
                    self.active_hitboxes[-1].sizey += 10
                elif not self.antigravity :
                    self.otherfallspeed = other.fallspeed
                    self.otherfastfallspeed = other.fastfallspeed
                    self.antigravity = True
                
            if self.frame > 10 and self.frame < 25 and self.antigravity :
                print("DownAir")
                other.fallspeed = 0
                other.fastfallspeed = 0

            if self.frame > 25 and self.antigravity: # 8 frames de lag
                print("Reset",self.otherfastfallspeed)
                other.fallspeed = self.otherfallspeed
                other.fastfallspeed = self.otherfastfallspeed
                self.attack = None

            if self.grounded :
                if self.antigravity :
                    print("Reset",self.otherfastfallspeed)
                    other.fallspeed = self.otherfallspeed
                    other.fastfallspeed = self.otherfastfallspeed
                self.attack = None
                if self.frame < 40 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 40+

        if attack == "NeutralAir":
            if self.frame > 4 and self.frame < 21 : # Windbox frame 5-20
                self.active_hitboxes.append(Hitbox(-216,-180,480,480,0,0,0,0,0,2,self,boum=-20))
                if self.active_hitboxes[-1].hit.colliderect(other.rect):
                    force = min(-6.67*2*200/max(((sqrt(self.rect.x**2+self.rect.y**2))-sqrt(other.rect.x**2+other.rect.y**2))**2,0.1),12)
                    if (sqrt(self.rect.x**2+self.rect.y**2))-sqrt(other.rect.x**2+other.rect.y**2) == 0 :
                        fx = 0
                        fy = 0
                    else :
                        fx = min(max((self.rect.x-other.rect.x)/abs(((sqrt(self.rect.x**2+self.rect.y**2))-sqrt(other.rect.x**2+other.rect.y**2))),-1),1)
                        fy = min(max((self.rect.y - other.rect.y)/abs(((sqrt(self.x**2+self.rect.y**2))-sqrt(other.x**2+other.rect.y**2))),-1),1)

                    other.vx += force * fx
                    other.vy += force * fy
                    print(other.vx,other.vy)
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(-5,-5,58,130,pi/4,16,8,1/200,15,10,self))

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
