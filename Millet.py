from random import randint
from Base_Char import Char, Hitbox, signe
import pygame
from math import pi,cos,sin,asin

##### Perso

class Millet(Char):
    def __init__(self) -> None:
        super().__init__(speed=2, dashspeed=3, airspeed=0.9, deceleration=0.7, fallspeed=0.5, fastfallspeed=1, fullhop=13, shorthop=10,
                         doublejumpheight=15,airdodgespeed=8,airdodgetime=3,dodgeduration=15)

        self.rect = pygame.Rect(100,0,48,128) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav") # Son test
        self.name = "Millet"
        self.angle_rayon = -pi/300000

    def special(self):
        if self.attack is None :
            self.angle_rayon = -pi/300000

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
            if self.frame < 25 :
                if up :
                    self.angle_rayon = pi/4
                if down :
                    self.angle_rayon = -pi/4
            if self.frame == 25:
                self.projectiles.append(Rayon(stage,self.x,self.rect.y,-self.angle_rayon*signe(self.direction),self)) # l'angle est chelou parce que j'ai géré la vitesse du rayon de façon merdique  # Mais on s'en fout ça marche
            if self.frame > 50: # 25 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownB":
            if self.frame < 10 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 70 :
                if self.look_right :
                    angle = pi/4
                    x = 32
                else :
                    angle = 3*pi/4
                    x = -64
                self.active_hitboxes.append(Hitbox(x,32,64,64,angle,20,68.29,1/100,9,5,self,False))
            if self.frame > 120 : # 15 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame < 8 :
                if left : # peut reverse netre les frames 1 et 7
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame%5 == 1 and self.frame > 15 and self.frame < 58:
                if self.look_right :
                    angle = pi/3
                    x = 0
                else :
                    angle = 2*pi/3
                    x = -48
                #self.active_hitboxes.append(Hitbox(x,32,64,32,angle,2,1.7+randint(-5,5)/10,0,8,3,self))
                self.projectiles.append(Fire(self.x+x,self.rect.y+32,self))
            if self.frame > 84 : #  frames de lag
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

class Rayon():
    def __init__(self,stage,x,y,angle_fwd,own) -> None:
        self.len = 20
        self.stage = stage
        self.x = [x for _ in range(self.len)]
        self.y = [y for _ in range(self.len)]
        self.angle_fwd = [angle_fwd for _ in range(self.len)]
        self.v = 9*signe(own.direction)
        self.rect = pygame.Rect(x-20,y-20,25,25)
        self.damages_stacking=1/300
        if own.look_right :
            self.angle = pi/4
        else :
            self.angle = 3*pi/4
        self.knockback = 3
        self.damages = 4 + randint(-12,12)/10
        self.stun = 4
        self.duration = 10
        #self.g = [-6.74/4 for _ in range(self.len)]
        for i in range(self.len) :
            for _ in range(self.len-i):
                nextx = self.x[i] + cos(self.angle_fwd[i])*self.v
                nexty = self.y[i] + sin(self.angle_fwd[i])*self.v #+ self.g[i]
                #self.g[i] += 0.0981
                self.x[i] = nextx
                self.y[i] = nexty

    def update(self):
        for i in range(self.len) :
            if pygame.Rect(self.x[i],self.y[i],5,5).colliderect(self.stage.rect):
                #self.g[i] = -6.74/2
                if self.rect.y < self.stage.rect.y+10 :
                    self.angle_fwd[i] = -self.angle_fwd[i]
                else :
                    self.angle_fwd[i] = pi-self.angle_fwd[i]


            nextx = self.x[i] + cos(self.angle_fwd[i])*self.v
            nexty = self.y[i] + sin(self.angle_fwd[i])*self.v #+ self.g[i]
            #self.g[i] += 0.0981
            self.x[i] = nextx
            self.y[i] = nexty
        self.rect.x = self.x[0]
        self.rect.y = self.y[0]
        if self.x[-1] < -800 or self.x[-1] > 800:
            self.duration = 0

    def draw(self,window):
        for i in range(self.len):
            pygame.draw.rect(window,(250,0,0),(self.x[i]+800,self.y[i]+450,10,10))

firesprite = [pygame.image.load(f"./DATA/Images/Sprites/Fire/{i}.png") for i in range(6)]
for i in range(len(firesprite)):
    firesprite[i] = pygame.transform.scale(firesprite[i],(3*firesprite[i].get_size()[0],3*firesprite[i].get_size()[1]))

class Fire():
    def __init__(self,x,y,own) -> None:
        self.size = 2
        self.x = x
        self.y = y
        self.vx = 14*signe(own.direction)
        self.vy = randint(-10,10)/10
        self.duration = 11
        self.knockback = 2
        self.damages = 2 + randint(-6,6)/10
        self.stun = 4
        self.damages_stacking = 0
        if own.look_right :
            self.angle = pi/4
        else :
            self.angle = 3*pi/4
        self.rect = pygame.Rect(x,y,2,2)
    
    def update(self):
        self.rect = firesprite[self.duration//2].get_rect(topleft=(self.x,self.y))
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.8
        self.duration -= 1

    def draw(self,window):
        window.blit(firesprite[self.duration//2],(self.x+800,self.y+450))