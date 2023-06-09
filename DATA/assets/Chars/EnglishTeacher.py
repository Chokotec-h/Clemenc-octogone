from DATA.utilities.Base_Char import Char, Hitbox, signe, SFXDicoEvent
import pygame
from math import pi, degrees, atan
from DATA.utilities.functions import *

##### Copier

class EnglishTeacher(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=2, dashspeed=3, airspeed=0.9, deceleration=0.7, fallspeed=0.5, fastfallspeed=1, fullhop=13, shorthop=10,
                         doublejumpheight=15,airdodgespeed=6,airdodgetime=3,dodgeduration=15)

        self.rect = [100,0,48,120] # Crée le rectangle de perso

        self.name = "EnglishTeacher"
        self.x = x
        self.rect[1] = y
        self.player = player
        self.prof = 0 # 0 = Lentsch ; 1 = Chevalier ; 2 = Leclerc ; 3 = Mauvieux
    
    def __str__(self) -> str:
        return "English Teacher"

    def special(self,inputs): 
        pass

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            if self.frame == 7 :
                self.vy = -3
            if 7 < self.frame < 16: # Saute frame 11
                self.can_act = False # ne peut pas agir après un grounded up B
                self.vy -= 2
                self.vx = 6*signe(self.direction)
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts
                self.active_hitboxes.append(Hitbox(20,120,36,36,0,5,0.8,0,2,2,self))
            if self.frame == 16 :
                self.active_hitboxes.append(Hitbox(20,117,42,42,pi/3,8,1.1,0,5,2,self))
                self.attack = None
            #if self.frame < 6 :
            #    if left : # peut reverse netre les frames 1 et 5
            #        self.look_right = False
            #    if right :
            #        self.look_right = True
            #if self.frame == 6: # Hitbox frame 6-11
            #    self.active_hitboxes.append(Hitbox(-1.5,88.5,51,48,2*pi/3,18,32,1/150,40,5,self,False))

        if attack == "NeutralB":
            self.prof = 3
            if self.frame > 4: # 10 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownB":
            self.prof = 1
            if self.frame > 6 and self.frame < 9 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 7
                self.animeframe -= 1
                self.charge = self.charge+1
            if self.frame == 10 :
                self.active_hitboxes.append(Fleche(self.x+24,self.y+60,self.charge,self))

            if self.frame > 20 : # 15 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            self.prof = 0
            if self.frame == 6 :
                self.projectiles.append(Etoile(self.x,self.y+60,pi/4,self))
            if self.frame > 12 : # 10 frames de lag
                self.attack = None

        if attack == "Jab":
            if self.frame == 6 :
                self.active_hitboxes.append(Hitbox(50,50,24,48,pi/4,2,3,1/400,7,6,self,linked=True))
                self.active_hitboxes.append(Hitbox(74,50,24,48,7*pi/8,4,4.5,1/200,14,6,self,sound="hits/cool hit",linked=True)) # Tipper

            if self.frame > 22: # 10 frames de lag
                self.attack = None

        if attack == "DownTilt":
            self.prof = 1
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(24,120,70,24,pi/3,4,4,1/400,8,5,self,linked=True))
                self.active_hitboxes.append(Hitbox(94,120,12,24,pi/20,8,6,1/200,16,5,self,sound="hits/cool hit",linked=True)) # Tipper

            if self.frame > 20: # 7 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            self.prof = 0
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(24+48,60,40,24,pi/6,6,4,1/400,10,4,self,linked=True))
                self.active_hitboxes.append(Hitbox(64+48,60,12,24,pi/10,12,9,1/200,20,4,self,sound="hits/cool hit",linked=True)) # Tipper
            if self.frame < 3 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True

            if self.frame > 30: # 8 frames de lag
                self.attack = None

        if attack == "UpTilt":
            self.prof = 2
            if self.frame == 9 :
                self.active_hitboxes.append(Hitbox(2,0,44,44,4*pi/9,6,4,1/400,8,4,self,position_relative=True))
            if self.frame > 20: # 11 Frames de lag
                self.attack = None

        if attack == "UpAir":
            self.prof = 2
            if self.frame == 12 :
                self.vy = 0
                self.active_hitboxes.append(Hitbox(8,8,40,24,3*pi/7,7,5,1/400,9,4,self,position_relative=True,linked=True))
                self.active_hitboxes.append(Hitbox(-2,-4,52,12,pi/2,14,7.5,1/200,18,4,self,sound="hits/cool hit",linked=True)) # Tipper
            if self.frame > 25: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 15 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 15+

        if attack == "ForwardAir":
            self.prof = 0
            if 10 < self.frame < 20 and self.frame%6 == 1 :
                self.active_hitboxes.append(Hitbox(52,70,48,12,pi/3,3,2,0,6,4,self))
            if 10 < self.frame < 20 and self.frame%6 == 4 :
                self.active_hitboxes.append(Hitbox(52,70,48,12,2*pi/3,3,2,0,6,4,self))
            if self.frame == 21 :
                self.active_hitboxes.append(Hitbox(50,68,50,16,pi/3,8,2.5,1/200,8,4,self,sound="hits/cool hit"))
            if self.frame > 45: # 29 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 40 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 40+

        if attack == "BackAir":
            self.prof = 0
            if self.frame == 8 :
                self.vx = 8*signe(self.direction)
                self.active_hitboxes.append(Hitbox(-35,60,36,36,2*pi/3,9,7,1/400,10,3,self,linked=True))
                self.active_hitboxes.append(Hitbox(-45,60,10,36,7*pi/8,18,10.5,1/200,20,3,self,sound="hits/cool hit",linked=True)) # Tipper

            if self.frame > 25: # 14 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 20+

        if attack == "DownAir":
            self.prof = 1
            if self.frame == 12 :
                self.active_hitboxes.append(Hitbox(10,120,38,45,pi/3,6,6,1/400,9,30,self,position_relative=True,linked=True))
                self.active_hitboxes.append(Hitbox(10,165,38,16,-pi/2,12,9,1/200,18,30,self,sound="hits/cool hit",linked=True)) # Tipper
            if self.frame > 60: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 50 :
                    self.lag = self.frame-5 # Auto cancel frame 1-5 et 20+

        if attack == "NeutralAir":
            self.prof = 0
            if self.frame == 6 :
                self.active_hitboxes.append(Hitbox(0+48,60,36,36,2*pi/3,4,7,0,9,3,self,linked=True))
                self.active_hitboxes.append(Hitbox(36+48,60,10,36,pi,6,6,0,18,3,self,sound="hits/cool hit",linked=True)) # Tipper
            if self.frame == 12 :
                self.active_hitboxes.append(Hitbox(-35,60,36,36,2*pi/3,6,5,1/400,8,3,self,linked=True))
                self.active_hitboxes.append(Hitbox(-45,60,10,36,7*pi/8,12,7.5,1/200,16,3,self,sound="hits/cool hit",linked=True)) # Tipper
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
            if self.frame == 15 :
                self.active_hitboxes.append(Hitbox(50,60,45,24,pi/6,12+8*self.charge/100,14,1/300,14+3*self.charge/100,3,self,linked=True))
                self.active_hitboxes.append(Hitbox(95,60,8,24,-pi/2,8+2*self.charge/100,21,1/150,28+3*self.charge/100,3,self,sound="hits/cool hit",linked=True)) # Tipper
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
            if self.frame == 18 :
                self.active_hitboxes.append(Hitbox(-8,-8,68,68,pi/4,14+8*self.charge/100,16,1/200,13+3*self.charge/100,4,self,position_relative=True))

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
            if self.frame == 16 :
                self.active_hitboxes.append(Hitbox(48,70,64,48,-pi/4,15+9*self.charge/100,16.8,1/200,15+6*self.charge/100,4,self,position_relative=True))

            if self.frame > 40: # 23 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
            if self.frame < 15 :
                self.vy = 0
                if self.grounded :
                    self.vx += self.dashspeed*signe(self.direction)
                else :
                    self.vx -= self.dashspeed*signe(self.direction)
            if self.frame == 16 and self.prof == 0:
                self.active_hitboxes.append(Hitbox(48,60,38,24,pi/5,2,5,1/500,11,3,self,linked=True))
                self.active_hitboxes.append(Hitbox(78,60,10,24,pi/12,3,8,1/250,22,3,self,sound="hits/cool hit",linked=True)) # Tipper
            if self.frame == 16 and self.prof == 1:
                    self.active_hitboxes.append(Hitbox(48,60,58,24,pi/5,5,10,1/500,7,3,self,linked=True))
                    self.active_hitboxes.append(Hitbox(106,67,10,10,pi/12,7.5,15,1/250,14,3,self,sound="hits/cool hit",linked=True)) # Tipper
            if 8 < self.frame < 16 and self.frame%3 == 0 and self.prof == 2:
                    self.active_hitboxes.append(Hitbox(48,60,28,24,pi/6,6,6,1/500,4,3,self,linked=True))
                    self.active_hitboxes.append(Hitbox(76,60,12,24,pi/10,9,9,1/250,8,3,self,sound="hits/cool hit",linked=True)) # Tipper
            if self.frame == 18 and self.prof == 2:
                    self.active_hitboxes.append(Hitbox(48,60,28,24,pi/6,10,6,1/500,5,3,self,linked=True))
                    self.active_hitboxes.append(Hitbox(76,60,12,24,pi/15,15,9,1/250,10,3,self,sound="hits/cool hit",linked=True)) # Tipper
            if self.frame == 18 and self.prof == 3:
                    self.active_hitboxes.append(Hitbox(48,60,28,24,4*pi/9,12,7,1/500,6,3,self,linked=True))
                    self.active_hitboxes.append(Hitbox(76,60,12,24,pi/15,18,10.5,1/250,12,3,self,sound="hits/cool hit",linked=True)) # Tipper

            if self.frame > 38: # 24 frames de lag
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

etoile = pygame.image.load("DATA/Images/Sprites/Projectiles/LeBerre/Eprouvette.png")


class Etoile():
    def __init__(self, x, y, angle, own: EnglishTeacher) -> None:
        self.id = 0
        self.sound = 'hits/8bit hit'
        self.rect = [x+5, y+5]
        self.angle = angle
        self.x,self.y = x,y
        self.vx = 5 * signe(own.direction)
        self.duration = 25
        self.knockback = 0.5
        self.damages = 0.8
        self.stun = 8
        self.damages_stacking = 1 / 550

    def update(self):
        rect = etoile.get_rect(topleft=(self.x,self.y))
        self.vx += 2
        self.x += self.v
        self.duration -= 1
        self.rect = [rect.x,rect.y,rect.w,rect.h]

    def draw(self, window):
        sprite = pygame.transform.scale(etoile,resize(round(etoile.get_width()),round(etoile.get_height()),width,height))
        window.blit(sprite, (resize(self.x+800,self.y+450,width,height))) # on dessine le sprite

    def deflect(self, modifier):
        self.vx *= -modifier
        self.damages *= modifier



fleche = pygame.image.load("DATA/Images/Sprites/Projectiles/English/Fleche.png")
fleche = pygame.transform.scale(fleche,resize(fleche.get_width(),fleche.get_height(),width,height))

class Fleche():
    def __init__(self, x, y, charge, own: EnglishTeacher) -> None:
        self.id = 0
        self.sound = 'hits/hit'
        self.rect = [x+5, y+5]
        self.vx = charge/15 * signe(own.direction)
        self.vy = -charge/25
        self.x = x
        self.y = y
        self.duration = 90
        self.knockback = charge/20
        self.damages = 1.2
        self.stun = 8
        self.charge = charge
        self.damages_stacking = 1 / 550

    def update(self):
        self.vy += 2
        self.rect[0] += self.vx
        self.rect[1] += self.vy
        self.duration -= 1

    def deflect(self,modifier):
        self.vx *= -modifier
        self.vy = -8
        self.damages *= modifier

    def draw(self, window):
        if self.vy == 0 :
            self.vx = 0.000001
        if self.vx < 0 :
            sprite = pygame.transform.rotate(fleche,degrees(pi-atan(self.vy/self.vx)))
        else :
            sprite = pygame.transform.rotate(fleche,degrees(pi-atan(self.vy/self.vx))+180)
        rect = sprite.get_rect(topleft=(self.x,self.y))
        if rect.colliderect(self.stage.mainplat.rect):
            sprite = pygame.transform.rotate(fleche,90)
        sprite = pygame.transform.scale(sprite,(resize(sprite.get_width(),0,width,height),resize(0,sprite.get_height(),width,height),))
        self.rect = [rect.x,rect.y,rect.w,rect.h]
        window.blit(sprite, resize(self.x+800,self.y+450,width,height)) # on dessine le sprite

##### Autres skins
