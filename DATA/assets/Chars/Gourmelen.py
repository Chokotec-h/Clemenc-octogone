from DATA.utilities.Base_Char import Char, Hitbox, signe, SFXDicoEvent
import pygame
from math import pi, atan, degrees
from DATA.utilities.functions import *

##### Copier

class Gourmelen(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=2.2, dashspeed=3.2, airspeed=1.1, deceleration=0.7, fallspeed=0.8, fastfallspeed=1.3, fullhop=14, shorthop=12,
                         doublejumpheight=15,airdodgespeed=7,airdodgetime=3,dodgeduration=15)

        self.rect = [100, 0, 48, 120] # Crée le rectangle de perso

        self.name = "Gourmelen"
        self.x = x
        self.rect[1] = y
        self.player = player
        self.temoin = False
        self.jab = 0
        self.grab = False
        self.resize_rect()
        
    def __str__(self) -> str:
        return "Gourmelen"

    def special(self,inputs):
        if self.attack is None :
            self.jab = 0
        self.temoin = False
        for p in self.projectiles :
            if isinstance(p,Temoin):
                self.temoin = True

    def deleteTemoin(self):
        for p in self.projectiles :
            if isinstance(p,Temoin):
                p.duration = 0

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            if self.temoin :

                self.vx = -(self.rect[0] - other.rect[0])/max(12-self.frame,1)
                self.vy = -(self.rect[1] - other.rect[1])/max(12-self.frame,1)
                if pygame.Rect(self.rect).colliderect(pygame.Rect(other.rect)) :
                    self.attack = None
                    self.deleteTemoin()
            else :
                
                if 8 < self.frame < 16: # Active frame 8-16
                    if self.frame%2 == 1 :
                        self.active_hitboxes.append(Hitbox(40, 100, 32, 32, pi/3, 4, 0.5, 1/800, 3, 3, self))
                    self.vy = -16
                    self.vx = 12*signe(self.direction)
                if self.frame > 18 :
                    self.can_act = False # ne peut pas agir après un grounded up B
                    self.attack = None
                    self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts
            if self.frame < 6 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True

        if attack == "NeutralB":

            if self.grab and not pygame.Rect(self.rect).colliderect(pygame.Rect(other.rect)) :
                self.attack = None

            if self.frame < 5 : # Reverse frames 1-5
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.temoin :
                # Grab
                if self.frame == 5 :
                    self.grab = False
                    self.active_hitboxes.append(Hitbox(60, 52, 32, 32, 0, 0, 0, 0, 0, 5, self))
                if 5 < self.frame < 9 and len(self.active_hitboxes) <= 0 :
                    self.grab = True
                    other.hitstun = 10
                    other.vx = 0
                if self.frame > 8 and self.grab :
                    if self.frame > (other.damages/2 + 5) :
                        self.attack = None
                        self.deleteTemoin()
                    elif not self.grounded :
                        self.active_hitboxes.append(Hitbox(60,52,48,48,pi/3,13,4,1/200,12,3,self))
                        self.vx = -10*signe(self.direction)
                        self.vy = -15
                        self.lag = 10
                        self.attack = None
                        self.deleteTemoin()
                    else :
                        other.hitstun = 10
                        other.damages += 0.4
                        self.vx += 5*signe(self.direction)
                        other.rect[1] = self.rect[1] - resize(0,32,width,height)[1]
                        other.x = self.x + (self.rect[2]-2)*signe(self.direction)
                        other.vy = -1
                        other.vx = self.vx
            else :
                # Set Temoin
                if self.frame == 8 :
                    self.grab = False
                    self.active_hitboxes.append(Hitbox(60, 52, 32, 32, 0, 0, 0, 0, 0, 5, self))
                if 8 < self.frame < 12 and len(self.active_hitboxes) <= 0 :
                    self.projectiles.append(Temoin(other,self))
            if self.frame > 20 and not self.grab: # 15 frames de lag
                self.attack = None
                self.charge = 0


        if attack == "DownB":
            if self.frame == 12 :
                self.damages = max(0,self.damages-3.4)
            if self.frame > 30 : # 18 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame == 10:
                if up :
                    v = -15
                elif down :
                    v = -6
                else :
                    v = -10
                self.projectiles.append(Biere(self,other,v,stage))
                SFXDicoEvent['wooshs']["mini woosh"].play()
            if self.frame > 20 : # 15 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "Jab":
            jab = [0,40,10,100,60,48,50,80,16]
            if self.frame % 3 == 0 and self.frame > 5 and self.frame < 31 :
                self.active_hitboxes.append(Hitbox(40, jab[self.jab], 24, 24, pi / 3, 3, 0.6, 0, 10, 6, self))
                self.jab += 1
            if not attack_button and self.frame > 6:
                self.frame = 39
            if self.frame == 38 :
                self.active_hitboxes.append(Hitbox(40, 46, 48, 40, pi / 4, 8, 1.2, 0, 10, 8, self))
            if self.frame < 38 :
                self.vx = 3*signe(self.direction)

            if self.frame > 48:  # 10 frames de lag
                self.attack = None

        if attack == "DownTilt":
            if self.frame == 10:  # 1er hit frame 10-13
                self.active_hitboxes.append(Hitbox(40, 70, 48, 48, pi / 2.5, 14, 8, 1/300, 16, 4, self))

            if self.frame > 20: # 7 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame < 3 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True

            if self.frame == 12:  # 1er hit frame 12-16
                self.active_hitboxes.append(Hitbox(40, 46, 48, 48, pi / 8, 8, 9, 1/250, 18, 4, self))
            if self.frame > 30: # 14 frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame == 7:  # 1er hit frame 7-10
                self.active_hitboxes.append(Hitbox(10, -5, 48, 52, pi / 2, 8, 4.5, 1/300, 13, 4, self))
            if self.frame > 23: # 13 Frames de lag
                self.attack = None

        if attack == "UpAir":

            if self.frame > 8 and self.frame < 16 :
                if self.active_hitboxes :
                    if self.frame > 12 :
                        self.active_hitboxes[-1].relativey += 14
                    else :
                        self.active_hitboxes[-1].relativey -= 14
                    self.active_hitboxes[-1].relativex += -7*signe(self.direction)
            if self.frame == 8 : # Active on 8-19
                if self.temoin :
                    self.active_hitboxes.append(Hitbox(24,0,24,32,pi/2,12,13.5,1.5/500,22,11,self,False))
                else :
                    self.active_hitboxes.append(Hitbox(24,0,24,32,pi/2,9,9,1/500,13,11,self,False))

            if self.frame > 28: # 9 Frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 24 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 24+

        if attack == "ForwardAir":

            if self.frame == 8 : # Active on 8-12
                if self.temoin :
                    self.active_hitboxes.append(Hitbox(40,52,48,24,-pi/6,14,11.5,1/555,17,3,self))
                else :
                    self.active_hitboxes.append(Hitbox(40,52,48,24,pi/6,10,8.4,1/600,11,3,self))

            if self.frame > 22: # 29 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 15 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 15+

        if attack == "BackAir":

            if self.frame == 17 : # Active on 17-20
                if self.temoin :
                    self.active_hitboxes.append(Hitbox(-52,40,48,24,pi,19,18.6,1.5/280,23,3,self))
                else :
                    self.active_hitboxes.append(Hitbox(-52,40,48,24,7*pi/8,12,13.4,1/280,17,3,self))
            if self.frame > 30: # 11 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 25 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 25+

        if attack == "DownAir":

            if self.frame == 16 : # Active on 16-19
                if self.temoin :
                    self.active_hitboxes.append(Hitbox(0,100,28,48,-pi/2,18,18.6,1.5/280,24,3,self))
                else :
                    self.active_hitboxes.append(Hitbox(0,100,28,48,-pi/2,12,12.4,1/280,16,3,self))
            if self.frame > 30: # 11 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 25 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 25+

        if attack == "NeutralAir":
            if self.frame == 3 : # Active on 3-30
                self.active_hitboxes.append(Hitbox(0,64,80,34,pi/3,8,10.5,1/200,18,27,self))
            if self.frame > 40: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 28 :
                    self.lag = self.frame-5 # Auto cancel frame 1-2 et 28+

        if attack == "ForwardSmash":
            if self.frame > 8 and self.frame < 11 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 9
                self.animeframe -= 1
                self.charge = self.charge+1


            elif self.frame == 25 : # Active on 25-27
                self.charge = min(self.charge,100)
                if self.temoin :
                    self.active_hitboxes.append(Hitbox(40,80,80,30,0.05,19+12.5*(self.charge/250),16.4,1/250,22+9*(self.charge/150),2,self,False,sound="hits/cool hit"))
                else :
                    self.active_hitboxes.append(Hitbox(40,80,80,30,0.05,10+8*(self.charge/250),8.8,1/250,12+8*(self.charge/150),2,self,False,sound="hits/cool hit"))

            if self.temoin and 24 < self.frame < 27 and not self.active_hitboxes :
                self.deleteTemoin()

            if self.frame > 35: # 8 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "UpSmash":
            if self.temoin and 10 < self.frame < 15 and not self.active_hitboxes :
                self.deleteTemoin()
            if self.frame < 5:
                if left:  # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right:
                    self.look_right = True
            if 5 < self.frame < 8 and smash and self.charge < 200:  # Chargement jusqu'à 200 frames
                self.animeframe -= 1
                self.frame = 6
                self.charge = self.charge + 1
            elif self.frame == 14:  # Active on 14-19
                self.charge = min(self.charge, 100)
                self.vy = -8
                if self.temoin :
                    self.active_hitboxes.append(
                        Hitbox(40, 40, 48, 48, 3 * pi / 8, 30 + 13 * (self.charge / 100), 25, 1 / 60,
                            34 + 10 * (self.charge / 100), 6, self, False, sound="hits/punch1"))
                else :
                    self.active_hitboxes.append(
                        Hitbox(40, 40, 48, 48, 3 * pi / 8, 16 + 8 * (self.charge / 100), 14, 1 / 100,
                            18 + 6 * (self.charge / 100), 6, self, False, sound="hits/punch1"))

            if self.frame > 35:  # 26 frames de lag
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

            elif self.frame == 20 : # Active on 20-25
                self.charge = min(self.charge,100)
                self.active_hitboxes.append(Hitbox(45,80,49,49,-pi/3,12+9*(self.charge/250),19,1/250,27+9*(self.charge/150),5,self,False,sound="hits/punch2"))
            
            if self.frame > 45: # 20 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
            if self.frame < 29 :
                self.vy = 0
                if self.grounded :
                    self.vx += self.dashspeed*signe(self.direction)
                else :
                    self.vx -= self.dashspeed*signe(self.direction)
            if 9 < self.frame < 23 and self.frame%3 == 1 :
                self.active_hitboxes.append(Hitbox(45,60,32,32,0,abs(self.vx),1.4,0,6,3,self))
            if self.frame == 25 :
                self.active_hitboxes.append(Hitbox(45,60,32,32,pi/6,10,3.4,1/600,9,3,self))
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


temoin = pygame.transform.scale(pygame.image.load(f"DATA/Images/Sprites/Projectiles/Gourmelen/Temoin.png"), resize(36, 36, width, height))

class Temoin:
    def __init__(self, opponent, own: Gourmelen) -> None:
        self.id = 0
        self.opponent = opponent
        self.duration = 5
        self.own = own
        self.rect = [-1000, 1000, 0, 0]

    def update(self):
        if self.opponent.rect[1] > 750 or self.opponent.rect[1] < -750 or self.opponent.rect[0] > 750 or self.opponent.rect[0] < -750:
            self.duration = 0

    def draw(self, window):
        x = self.opponent.rect[0]
        y = self.opponent.rect[1] - resize(0,50,width,height)[1]
        window.blit(temoin, (x + resize(800,0,width,height)[0], y + resize(0,450,width,height)[1]))


biere = pygame.image.load("DATA/Images/Sprites/Projectiles/Gourmelen/Biere.png")
biere = pygame.transform.scale(biere,resize(biere.get_width(),biere.get_height(),width,height))

class Biere():
    def __init__(self,own:Gourmelen,other,speed,stage) -> None:
        self.id = 0
        self.vx = 8*signe(own.direction)
        self.vy = speed
        self.basevy = self.vy
        self.x = own.x
        self.y = own.rect[1] + resize(0,48,width,height)[1]
        self.own = own
        self.other = other
        self.duration = 80
        self.stage = stage
        self.rect = [0,0,0,0]
        self.rotate = 0
        self.angle = 0
        self.damages = 4.3
        self.stun = 3
        self.knockback = 2
        self.damages_stacking = 1/200
    
    def touch_stage(self,stage,rect):
        if rect.colliderect(stage.mainplat.rect):
            return True
        for p in stage.plats:
            if rect.colliderect(p.rect) and rect.y + rect.h-4 < p.rect.y+self.vy+4:
                return True
        return False
    
    def update(self):
        dx = (self.x - self.other.x)
        dy = (self.y - self.other.rect[1])
        if dx == 0 :
            dx = 0.001
        self.angle = atan(dy/dx)
        rect = biere.get_rect(topleft=(self.x,self.y))
        self.x += resize(self.vx,0,width,height)[0]
        self.y += resize(0,self.vy,width,height)[1]
        self.vy += 0.8
        if self.touch_stage(self.stage,rect):
            self.duration = 0
        self.rect = [rect.x,rect.y,rect.w,rect.h]
        self.duration -= 1
        
    def deflect(self,modifier):
        self.vx = -self.vx*modifier
        self.vy = -10
        self.own,self.other = self.other,self.own    

    def draw(self,window):
        self.rotate += self.vx
        sprite = pygame.transform.rotate(biere,degrees(self.rotate))
        window.blit(sprite, (self.x+width/2,self.y+height/2)) # on dessine le sprite


##### Autres skins
