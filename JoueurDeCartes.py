from Base_Char import Char, Hitbox, signe
import pygame
from math import pi
from random import randint

##### Perso

class Air_President(Char):
    def __init__(self) -> None:
        super().__init__(speed=1.9, dashspeed=3.6, airspeed=1.4, deceleration=0.6, fallspeed=0.8, fastfallspeed=1.6, fullhop=13, shorthop=10,
                         doublejumpheight=15)

        self.rect = pygame.Rect(100,0,48,120) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav") # Son test
        self.name = "Air President"
        self.mao = False
        self.chaises = 0
        self.basefallspeed = 0.8
        self.canchaise = True

    def inputattack(self, attack):
        self.animeframe = 0
        if self.can_act or (self.canchaise and attack == "UpB"): # Spam la chaise
            self.frame = 0  # on démarre à la frame 0
            self.attack = attack  # on update l'action en cours
            if attack == "UpB":
                self.can_act = False # Ne peut pas attaquer après le up B
                self.upB = True # Effets spéciaux après upB (uniquement grounded)

    def special(self): # Spécial à Airpresidentman, pour son upB
        if not self.upB: # reset la fallspeed
            self.lag = self.chaises*10
            self.chaises = 0
            self.canchaise = True
        self.fallspeed = (1+self.chaises) * self.basefallspeed

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up

        if attack == "UpB":
            if self.frame == 8: # Saute frame 8
                self.vy = -20 # monte sur la chaise
            if self.frame > 11 :
                self.attack = None
                self.upB = True
                self.projectiles.append(Chaise(0,26*(self.chaises)+120,self,stage))
                self.chaises += 1
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
            if self.frame == 15 :
                if randint(1,208) == 1:
                    self.y = 10000
                else :
                    if not self.look_right:
                        angle = 3*pi/4
                        x = -56
                    else:
                        angle = pi/4
                        x = 24
                    self.active_hitboxes.append(Hitbox(x,20,68,48,0,0,0,0,0,8,self))
                    self.active_hitboxes[-1].update()
                    if self.active_hitboxes[-1].hit.colliderect(other.rect):
                        if randint(1,208) == 1:
                            other.y = 10000
                            self.projectiles.append(Carte(x,20,pi/42,"R",self))
                        else :
                            self.projectiles.append(Carte(x,20,angle,randint(1,13),self))

            if self.frame > 20 : #  frames de lag
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

class Carte():
    def __init__(self,x,y,angle,number,own) -> None:
        if number == "R":
            self.sprite = pygame.image.load(f"./DATA/Images/Sprites/Cartes/Revolution.png")
        else :
            self.number = number + 2
            if self.number > 13 :
                self.number = self.number-13
            self.sprite = pygame.transform.scale(pygame.image.load(f"./DATA/Images/Sprites/Cartes/{self.number}.png"),(48,64))
            self.number = number
            self.angle = angle
            self.knockback = self.number*0.9
            self.damages = 1.5*self.number
            self.stun = self.number
            self.damages_stacking = self.number*1/500
        self.duration = 6
        self.rect = self.sprite.get_rect(topleft=(x+own.x,y+own.rect.y))
        self.angle = angle
        self.x = x
        self.y = y
        self.own = own
    
    def update(self):
        self.duration -= 1
    
    def deflect(self):
        self.duration = 0
    
    def draw(self,window):
        window.blit(self.sprite,(self.x+self.own.x+800,self.y+self.own.rect.y+450))

class Chaise():
    def __init__(self,x,y,own,stage) -> None:
        self.sprite = pygame.image.load("./DATA/Images/Sprites/Chaise.png")
        self.own = own
        self.xvar = x
        self.yvar = y
        self.x = self.own.rect.x + self.xvar
        self.y = self.own.rect.y + self.yvar
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
        self.duration = 10
        self.stage = stage

        self.angle = -pi/2
        self.knockback = 3
        self.damages = 2.2
        self.stun = 4
        self.damages_stacking = 1/350
    
    def update(self):
        self.x = self.own.rect.x + self.xvar
        self.y = self.own.rect.y + self.yvar
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
        if self.stage.rect.colliderect(self.rect):
            self.own.canchaise = False
            self.own.can_act = False
            self.duration = 0
    
    def deflect(self):
            self.own.canchaise = False
            self.own.can_act = False
            self.duration = 0

    def draw(self,window):
        window.blit(self.sprite,(self.x+800,self.y+450))