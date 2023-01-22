from DATA.utilities.Base_Char import Char, Hitbox, signe, SFXDicoEvent
import pygame
from math import pi, atan, degrees, sqrt
from DATA.utilities.functions import *

##### Copier

class Thevenet(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=2, dashspeed=3, airspeed=0.9, deceleration=0.7, fallspeed=0.5, fastfallspeed=1, fullhop=13, shorthop=10,
                         doublejumpheight=15,airdodgespeed=6,airdodgetime=3,dodgeduration=15)

        self.rect = pygame.Rect(100,0,48,120) # Crée le rectangle de perso

        self.name = "Thevenet"
        self.x = x
        self.rect.y = y
        self.player = player
        self.navet = False
        self.holdb = False
    
    def __str__(self) -> str:
        return "Thévenet"

    def special(self,inputs):
        if not self.navet :
            delete = False
            for h in self.active_hitboxes :
                for p in self.projectiles:
                    if h.hit.colliderect(p.rect):
                        delete = p
                        self.navet = True
            if delete :
                del delete

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up

        if self.navet :
            if attack in ["UpTilt","UpAir","UpSmash"] :
                vy = -20
                vx = 0
                self.projectiles.append(Radis(0,-30,self,other,vx,vy,stage))
                self.navet = False
            if attack in ["DownTilt","DownAir","DownSmash"] :
                vy = 20
                vx = 0
                self.projectiles.append(Radis(0,58,self,other,vx,vy,stage))
                self.navet = False
            if attack in ["ForwardTilt","ForwardSmash"]:
                if left :
                    self.look_right = False
                if right : 
                    self.look_right = True
                if self.look_right :
                    x = 24
                else :
                    x = -50
                vx = 15*signe(self.look_right-0.5)
                vy = -2
                self.projectiles.append(Radis(x,58,self,other,vx,vy,stage,0.1))
                self.navet = False
            if attack == "BackAir" :
                vx = -15*signe(self.direction)
                vy = -2
                self.projectiles.append(Radis(-50,58,self,other,vx,vy,stage,0.1))
                self.navet = False
            if attack == "ForwardAir" :
                vx = 15*signe(self.direction)
                vy = -2
                self.projectiles.append(Radis(24,58,self,other,vx,vy,stage,0.1))
                self.navet = False
            if attack in ["Jab","NeutralAir"]:
                vx = 9*signe(self.direction)
                vy = -4
                self.projectiles.append(Radis(24,58,self,other,vx,vy,stage))
                self.navet = False
            self.attack = None
            if not self.navet :
                self.lag = 3
                
        else :
            if attack == "UpB":
                if 4 < self.frame < 12 :
                    self.vy -= 4
                if self.frame == 12:
                    self.can_act = False # ne peut pas agir après un grounded up B
                    self.attack = None
                    self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts

            if attack == "NeutralB":
                if self.frame < 5 :
                    if left :
                        self.look_right = False
                    if right :
                        self.look_right = True
                if self.frame == 8 :
                    self.projectiles.append(PQ(stage,self))
                if self.frame > 15: # 10 frames de lag
                    self.attack = None

            if attack == "DownB":
                if self.frame == 8 :
                    self.navet = True
                if self.frame > 18 : # 15 frames de lag
                    self.attack = None

            if attack == "SideB":
                if self.frame > 14 :
                    self.active_hitboxes.append(Hitbox(-8,100,64,64,pi/4,6,4,1/600,7,50,self,position_relative=True,boum=-2))
                    self.holdb = True
                    if self.holdb and not special :
                        self.holdb = False
                    if not self.holdb and special :
                        self.attack = None
                        self.active_hitboxes = list()
                    self.vx += 3*signe(self.direction)
                if self.frame > 80 : # 20 frames de lag
                    self.attack = None

            if attack == "Jab":
                if self.frame == 10:
                    self.active_hitboxes.append(Hitbox(48,70,48,48,pi/6,6,2.6,1/300,8,3,self))
                if self.frame > 20: # 10 frames de lag
                    self.attack = None

            if attack == "DownTilt":
                if self.frame == 11:
                    self.active_hitboxes.append(Hitbox(48,120,68,28,-6*pi/13,14,3.7,1/100,11,3,self))

                if self.frame > 23: # 7 frames de lag
                    self.attack = None

            if attack == "ForwardTilt":
                if self.frame < 3 :
                    if left :
                        self.look_right = False
                    if right :
                        self.look_right = True
                if self.frame == 13:
                    self.active_hitboxes.append(Hitbox(48,60,50,50,pi/3,6,5.3,1/300,10,3,self))

                if self.frame > 30: # 8 frames de lag
                    self.attack = None

            if attack == "UpTilt":
                if self.frame == 11:
                    self.active_hitboxes.append(Hitbox(8,-30,32,68,pi/2,8,4.1,1/200,8,3,self))
                if self.frame > 25: # 11 Frames de lag
                    self.attack = None

            if attack == "UpAir":
                if self.frame == 7:
                    self.active_hitboxes.append(Hitbox(-16,0,48,48,5*pi/11,6,2.8,1/400,12,10,self))
                if self.active_hitboxes and self.frame > 7 :
                    self.active_hitboxes[0].relativex += 10*signe(self.direction)
                    if self.frame < 12 :
                        self.active_hitboxes[0].relativey -= 8
                    else:
                        self.active_hitboxes[0].relativey += 8
                if self.frame > 25: # 10 frames de lag
                    self.attack = None

                if self.grounded :
                    self.attack = None
                    if self.frame < 20 :
                        self.lag = self.frame-2 # Auto cancel frame 1-2 et 15+

            if attack == "ForwardAir":
                if self.frame == 10 :
                    self.projectiles.append(Machine(stage,self))

                if self.frame > 30: # 20 frames de lag
                    self.attack = None

                if self.grounded :
                    self.attack = None
                    if self.frame < 25 :
                        self.lag = self.frame-3 # Auto cancel frame 1-3 et 40+

            if attack == "BackAir":
                if self.frame == 4 :
                    self.active_hitboxes.append(Hitbox(-40,60,40,28,6*pi/7,6,4.8,1/30,4,3,self))

                if self.frame > 20: # 14 frames de lag
                    self.attack = None

                if self.grounded :
                    self.attack = None
                    if self.frame < 20 :
                        self.lag = self.frame-2 # Auto cancel frame 1-2 et 20+

            if attack == "DownAir":
                if self.frame == 6 :
                    self.active_hitboxes.append(Hitbox(2,120,44,72,-pi/2,15,11.4,1/150,10,8,self))
                if self.frame == 9 and self.active_hitboxes :
                    self.active_hitboxes[0] = Hitbox(2,120,44,72,pi/3,6,8,1/300,7,15,self,position_relative=True)
                if not self.active_hitboxes and 6 < self.frame < 23:
                    self.vy = -8
                    self.lag = 10
                    self.attack = None

                if self.frame > 50: # 10 frames de lag
                    self.attack = None

                if self.grounded :
                    self.attack = None
                    if self.frame < 30 :
                        self.lag = self.frame-5 # Auto cancel frame 1-5 et 20+

            if attack == "NeutralAir":
                if self.frame == 3:
                    self.active_hitboxes.append(Hitbox(48,70,48,48,pi/6,4,2.8,1/300,9,3,self))
                if self.frame == 6:
                    self.active_hitboxes.append(Hitbox(-48,70,48,48,5*pi/6,4,2.8,1/300,9,3,self))

                if self.frame > 20: # 17 frames de lag
                    self.attack = None

                if self.grounded :
                    self.attack = None
                    if self.frame < 14 :
                        self.lag = self.frame-2 # Auto cancel frame 1-2 et 30+

            if attack == "ForwardSmash":
                if self.frame > 6 and self.frame < 9 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                    self.frame = 7
                    self.animeframe -= 1
                    self.charge = self.charge+1
                if self.frame == 15:
                    self.active_hitboxes.append(Hitbox(48,70,48,48,pi/4,12+8*self.charge/100,12.4,1/200,18+6*self.charge/100,3,self,sound="hits/hitting metal"))
                if self.frame > 32: # 30 frames de lag
                    self.attack = None
                    self.charge = 0

            if attack == "DownSmash":

                if self.frame < 5 :
                    if left : # peut reverse netre les frames 1 et 5
                        self.look_right = False
                    if right :
                        self.look_right = True
                if self.frame > 5 and self.frame < 8  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                    self.animeframe -= 1
                    self.frame = 6
                    self.charge = self.charge+1
                if self.frame == 16:
                    self.active_hitboxes.append(Hitbox(68,30,24,115,-4*pi/7,13+8*self.charge/100,18.8,1/200,12+6*self.charge/100,3,self,sound="hits/hitting metal"))

                if self.frame > 40: # 25 frames de lag
                    self.attack = None
                    self.charge = 0

            if attack == "UpSmash":

                if self.frame < 3 :
                    if left : # peut reverse netre les frames 1 et 2
                        self.look_right = False
                    if right :
                        self.look_right = True
                if self.frame > 3 and self.frame < 6  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                    self.animeframe -= 1
                    self.frame = 4
                    self.charge = self.charge+1
                if self.frame == 14:
                    self.active_hitboxes.append(Hitbox(64,100,48,48,pi/2,14+9*self.charge/100,16.3,1/180,16+self.charge/100,10,self))
                if self.active_hitboxes and self.frame > 14 :
                    self.active_hitboxes[0].relativex -= 10*signe(self.direction)
                    if self.frame < 19 :
                        self.active_hitboxes[0].relativey -= 30
                    else:
                        self.active_hitboxes[0].relativey += 30

                if self.frame > 45: # 23 frames de lag
                    self.attack = None
                    self.charge = 0

            if attack == "DashAttack":
                if self.frame == 12:
                    self.active_hitboxes.append(Hitbox(48,70,48,48,pi/15,3,3.8,0,10,3,self))
                if self.frame == 15:
                    self.active_hitboxes.append(Hitbox(48,70,48,48,pi/15,8,3.8,1/400,10,3,self))
                if self.frame < 16 :
                    self.vy = 0
                    if self.grounded :
                        self.vx += self.dashspeed*signe(self.direction)
                    else :
                        self.vx -= self.dashspeed*signe(self.direction)
                if self.frame > 24: # 24 frames de lag
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


radis = pygame.image.load("DATA/Images/Sprites/Projectiles/Thevenet/Radis.png")
radis = pygame.transform.scale(radis,resize(radis.get_width()*3,radis.get_height()*3,width,height))

class Radis():
    def __init__(self,x,y,own:Thevenet,other,vx,vy,stage,g=0.8) -> None:
        self.vx = vx*signe(own.direction)
        self.vy = vy
        self.basevy = self.vy
        self.x = own.x + resize(x,0,width,height)[0]
        self.y = own.rect.y + resize(0,y,width,height)[1]
        self.own = own
        self.other = other
        self.duration = 120
        self.stage = stage
        self.rect = pygame.Rect((0,0,0,0))
        self.g = g
        self.rotate = 0
        self.angle = pi/4 if own.look_right else 3*pi/4
        self.damages = 4.4
        self.stun = 9
        self.knockback = 2
        self.damages_stacking = 1/800
    
    def touch_stage(self,stage,rect):
        if rect.colliderect(stage.mainplat.rect):
            return True
        for p in stage.plats:
            if rect.colliderect(p.rect) and rect.y + rect.h-4 < p.rect.y+self.vy+4:
                return True
        return False
    
    def update(self):
        dx = (self.x - self.other.x)
        dy = (self.y - self.other.rect.y)
        if dx == 0 :
            dx = 0.001
        self.angle = atan(dy/dx)
        self.rect = radis.get_rect(topleft=(self.x,self.y))
        self.x += resize(self.vx,0,width,height)[0]
        self.y += resize(0,self.vy,width,height)[1]
        self.vy += self.g
        if self.touch_stage(self.stage,self.rect):
            self.vy = -abs(self.vy)/2
            self.duration -= 20
        if self.rect.colliderect(self.other.rect):
            self.vy = -6
            self.vx = 5*-signe(self.vx)
            self.duration -= 20
        self.duration -= 1
        
    def deflect(self,modifier):
        self.vx = -self.vx*modifier
        self.vy = -10
        self.own,self.other = self.other,self.own    

    def draw(self,window):
        self.rotate += sqrt(self.vx**2 + self.vy**2)
        sprite = pygame.transform.rotate(radis,degrees(self.rotate))
        window.blit(sprite, (self.x+width/2,self.y+height/2)) # on dessine le sprite

class PQ():
    def __init__(self,stage,own:Thevenet) -> None:
        self.sprite = pygame.transform.scale(pygame.image.load("DATA/Images/Sprites/Projectiles/Thevenet/PQ.png"),(resize(36,36,width,height)))
        self.x = own.x+24
        self.y = own.rect.y+50
        self.vx = 6*signe(own.direction)
        self.vy = -8
        self.angle = -pi/2
        self.knockback = 3
        self.damages = 2
        self.stun = 4
        self.damages_stacking = 1/900
        self.duration = 10
        self.stage = stage
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
        self.sound = SFXDicoEvent['hits']["hit"]

    def update(self):
        vx,vy = resize(self.vx,self.vy,width,height)
        self.x += vx
        self.y += vy
        self.vy += 1.4
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
        if self.y > resize(800,0,width,height)[0] :
            self.duration = 0
        if self.rect.colliderect(self.stage.mainplat.rect) :
            self.duration -= 1
            self.vx = 0
            self.vy = 0

    def deflect(self,modifier):
        self.vy = -self.vy*modifier
        self.vx = -self.vx*modifier
        self.damages = self.damages * modifier
        self.knockback = self.damages * modifier
        self.angle = pi-self.angle

    def draw(self,window):
        window.blit(self.sprite, (self.x+resize(800,0,width,height)[0],self.y+resize(0,450,width,height)[1])) # on dessine le sprite

class Machine():
    def __init__(self,stage,own:Thevenet) -> None:
        self.sprite = pygame.transform.scale(pygame.image.load("DATA/Images/Sprites/Projectiles/Thevenet/Machine.png"),(resize(52,52,width,height)))
        if own.look_right :
            self.x = own.x + 24
        else :
            self.x = own.x - 24 - 48
        self.y = own.rect.y+50
        self.vy = -1
        self.angle = -pi/2
        self.knockback = 3
        self.damages = 2
        self.stun = 4
        self.damages_stacking = 1/900
        self.duration = 5
        self.stage = stage
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
        self.sound = SFXDicoEvent['hits']["hitting metal"]

    def update(self):
        vy = resize(0,self.vy,width,height)[1]
        self.y += vy
        self.vy += 4
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
        if self.y > resize(800,0,width,height)[0] :
            self.duration = 0
        if self.rect.colliderect(self.stage.mainplat.rect) :
            self.duration -= 1
            self.vx = 0
            self.vy = 0

    def deflect(self,modifier):
        self.vy = -8
        self.damages = self.damages * modifier
        self.knockback = self.damages * modifier
        self.angle = pi-self.angle

    def draw(self,window):
        window.blit(self.sprite, (self.x+resize(800,0,width,height)[0],self.y+resize(0,450,width,height)[1])) # on dessine le sprite


##### Autres skins
