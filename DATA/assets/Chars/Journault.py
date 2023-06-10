from DATA.utilities.Base_Char import Char, Hitbox, signe, SFXDicoEvent, change_left
import pygame
from math import pi, degrees
from DATA.utilities.functions import *
from DATA.utilities.build import rootDir

##### Copier

class Journault(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=2.2, dashspeed=3.4, airspeed=0.9, deceleration=0.8, fallspeed=0.7, fastfallspeed=1.5, fullhop=15, shorthop=12,
                         doublejumpheight=17,airdodgespeed=6,airdodgetime=3,dodgeduration=15)

        self.rect = [100,0,48,120] # Crée le rectangle de perso

        self.name = "Journault"
        self.x = x
        self.rect[1] = y
        self.player = player
        self.jab = 0

        self.cafe = 0
        self.direction_tuyau = 0
    
    def __str__(self) -> str:
        return "Journault"

    def special(self,inputs):
        
        if self.die :
            self.cafe = 0
        if self.cafe < -3 :
            self.attack = None
            self.cafe += 1
            self.vx += 4*signe(self.direction)
            self.fallspeed = 2
            self.fastfallspeed = 3
        elif self.cafe > 0 :
            self.cafe -= 1
            self.speed = 3
            self.dashspeed = 4.5
            self.airspeed = 1.3
        else :
            self.speed = 2.2
            self.dashspeed = 3.4
            self.airspeed = 0.9
            self.fallspeed = 0.7
            self.fastfallspeed = 1.5
        if self.attack == "DashAttack":
            self.deceleration = 0.9
        else :
            self.deceleration = 0.8
        if self.attack is None :
            self.rect[2],self.rect[3] = 48,120
            self.jab = 0

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            self.animation = "UpB"+str(self.direction_tuyau)
            if up > left and up > right and up:
                self.direction_tuyau = 0
            if down > left and down > right and down:
                self.direction_tuyau = 2
            if right > up and right > down and right:
                self.direction_tuyau = 1
                self.look_right = True
            if left > up and left > down and left:
                self.direction_tuyau = 3
                self.look_right = False
            if 40 > self.frame > 5 :
                self.vx,self.vy = ((0,-15),(15,0),(0,15),(-15,0))[self.direction_tuyau]
                if self.active_hitboxes :
                    self.active_hitboxes[0].angle = (pi/2,0,-pi/2,pi)[self.direction_tuyau]
                    self.active_hitboxes[0].relativex = (0,100,0,change_left(100,48,120))[self.direction_tuyau]
                    self.active_hitboxes[0].relativey = (-10,0,100,0)[self.direction_tuyau]
                    self.rect[2],self.rect[3] = ((48,120),(120,48))[self.direction_tuyau%2]

            if self.frame == 5 :
                self.active_hitboxes.append(Hitbox(0,0,48,48,pi/2,10,6.2,1/800,10,40,self))
            if self.frame > 45 :
                if self.direction_tuyau%2 == 1 :
                    self.rect[2] -= 80
                self.attack = None
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts
                self.can_act = False # ne peut pas agir après un grounded up B

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
            if 19 > self.frame > 8 :
                self.vy = 0
            if self.frame == 6 :
                self.projectiles.append(Electroball(self.x + 20*signe(self.direction), self.rect[1] + 40,self,stage))
            if self.frame > 22: # 10 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownB":
            if self.frame == 20 :
                if self.cafe > 5 :
                    self.cafe = -300
                else :
                    self.cafe = 300
            if self.frame > 28 : # 8 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame < 3 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 10 :
                self.projectiles.append(Automate(self.x + 30*signe(self.direction),self.rect[1],self,other,stage))
            if self.frame > 80 : # 20 frames de lag
                self.attack = None

        if attack == "Jab":

            damage = 3.2 if self.cafe else 1.8
            if self.jab == 0 :
                if self.frame == 4: # Active on 4-7
                    self.active_hitboxes.append(Hitbox(40,60,45,28,pi/4,2,damage,0,14,3,self))
                if 13 > self.frame > 8 and attack_button : # Transition to jab 2 on 9-13
                    self.frame = 0
                    self.jab = 1
                if self.frame > 20 :
                    self.attack = None
            if self.jab == 1 :
                if self.frame == 3: # Active on 3-7
                    self.active_hitboxes.append(Hitbox(50,55,45,28,pi/6,2,damage,0,14,4,self))
                if 14 > self.frame > 9 and attack_button : # Transition to jab 3 on 10-14
                    self.frame = 0
                    self.jab = 2
                if self.frame > 23 :
                    self.attack = None
            if self.jab == 2 :
                if self.frame == 5: # Active on 5-7
                    self.active_hitboxes.append(Hitbox(55,50,45,28,pi/8,10,damage+1,1/900,11,2,self))
                if self.frame > 18 :
                    self.attack = None

        if attack == "DownTilt":
            damage = 6.8 if self.cafe else 4.3
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(40,120,40,30,2*pi/5,9,damage,1/800,9,6,self))
            if self.frame > 20: # 6 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            damage = 10.2 if self.cafe else 5.5
            if self.frame < 3 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True

            if self.frame == 10 : # Active on 10-13
                self.active_hitboxes.append(Hitbox(40,50,50,30,pi/8,12,damage,1/600,7,3,self))
            if self.frame > 28: # 15 frames de lag
                self.attack = None

        if attack == "UpTilt":
            damage = 4.2 if self.cafe else 3.2
            if self.frame == 6 : # Active on 6-10
                self.active_hitboxes.append(Hitbox(45,30,34,34,3*pi/7,11,damage,1/600,12,4,self))
            if 9 > self.frame > 6 and self.active_hitboxes :
                self.active_hitboxes[0].relativex += 3*signe(self.direction)
                self.active_hitboxes[0].relativey -= 15

            if self.frame > 19: # 9 Frames de lag
                self.attack = None

        if attack == "UpAir":
            damage = 4.5 if self.cafe else 3.4
            if self.frame == 8 : # Active on 8-16
                self.active_hitboxes.append(Hitbox(55,30,45,45,3*pi/7,9,damage,1/900,11,8,self))
                
            if 15 > self.frame > 8 and self.active_hitboxes :
                self.active_hitboxes[0].relativex -= (self.frame - 5)*signe(self.direction)
                self.active_hitboxes[0].relativey -= (15-self.frame)*2

            if self.frame > 22: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 15 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 15+

        if attack == "ForwardAir":
            damage = 5.2 if self.cafe else 2.7
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(40,60,10,10,pi/8,3,damage,1/900,14,10,self))
            if 18 > self.frame > 8 and self.active_hitboxes :
                self.active_hitboxes[0].relativex += (self.frame - 5)*signe(self.direction)
                self.active_hitboxes[0].sizex += 4
                self.active_hitboxes[0].sizey += 4
                if not self.look_right :
                    self.active_hitboxes[0].relativex -= 2

            if self.frame > 50: # 29 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 40 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 40+

        if attack == "BackAir":
            damage = 6.8 if self.cafe else 4.8
            if self.frame == 6 : # Active on 6-9
                self.active_hitboxes.append(Hitbox(change_left(55,35),70,35,35,7*pi/9,10,damage,1/700,11,3,self))

            if self.frame > 25: # 14 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 20+

        if attack == "DownAir":
            damage = 12 if self.cafe else 6.5
            if self.frame == 12 : # Active on 12-20
                self.active_hitboxes.append(Hitbox(5,110,50,50,-pi/3,9,damage,1/900,11,8,self))

            if self.frame > 29: # 9 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 26 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 26+

        if attack == "NeutralAir":
            damage = 5.8 if self.cafe else 3.4
            if self.frame == 4 : # Active on 4-7 / 9-12
                self.active_hitboxes.append(Hitbox(change_left(50,40),50,40,40,pi/4,9,damage,1/900,11,3,self))
            if self.frame == 9 :
                self.active_hitboxes.append(Hitbox(50,50,40,40,3*pi/4,9,damage,1/900,11,3,self))

            if self.frame > 25: # 17 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 30 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 30+

        if attack == "ForwardSmash":
            damage = 20.2 if self.cafe else 15.8
            if self.frame > 6 and self.frame < 9 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 7
                self.animeframe -= 1
                self.charge = self.charge+1

            if self.frame == 18 : # Active on 18-20
                self.active_hitboxes.append(Hitbox(65,50,45,70,pi/5,16+12*(self.charge)/100,damage,1/380,19+11*(self.charge),2,self))
            if self.frame > 45: # 25 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "UpSmash":
            damage = 19.3 if self.cafe else 14.2

            if self.frame < 5 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 5 and self.frame < 8  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.animeframe -= 1
                self.frame = 6
                self.charge = self.charge+1

            if self.frame == 12 : # Active on 12-20
                self.active_hitboxes.append(Hitbox(60,10,45,45,3*pi/5,15+10*(self.charge)/100,damage,1/400,17+10*(self.charge),8,self))
                
            if 20 > self.frame > 12 and self.active_hitboxes :
                self.active_hitboxes[0].relativex -= 15*signe(self.direction)
                self.active_hitboxes[0].relativey -= (16-self.frame)*5
            if self.frame == 16 and self.active_hitboxes:
                self.active_hitboxes[0].angle = pi - self.active_hitboxes[0].angle


            if self.frame > 35: # 15 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownSmash":
            damage = 23.4 if self.cafe else 16.4

            if self.frame < 3 :
                if left : # peut reverse netre les frames 1 et 2
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 3 and self.frame < 6  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.animeframe -= 1
                self.frame = 4
                self.charge = self.charge+1

            if self.frame == 19 : # Active on 19-22
                self.active_hitboxes.append(Hitbox(50,100,30,60,pi/3,18+10*(self.charge)/100,14.2,1/500,19+10*(self.charge),3,self))
                self.active_hitboxes.append(Hitbox(change_left(50,30),100,30,60,2*pi/3,18+10*(self.charge)/100,14.2,1/500,19+10*(self.charge),3,self))

            if self.frame > 40: # 23 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
            damage = 9.1 if self.cafe else 5.9
            if self.frame < 3 :
                self.vx = self.dashspeed*signe(self.direction)*8
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(40,100,50,30,4*pi/7,8,damage,1/500,9,30,self))
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

    def draw(self, window): # Dessine aussi les inputs du konami code et la jauge d'explosifs
        super().draw(window)
        if self.player == 0 :
            x = 533
        else :
            x = 1066
        if self.cafe < -3 :
            color = (255,0,0)
        else :
            color = (230,150,0)
        pygame.draw.rect(window,(0,0,0),(resize(x,0,width,height)[0],resize(0,800,width,height)[1],resize(100,0,width,height)[0],resize(0,20,width,height)[1]))
        pygame.draw.rect(window,color,(resize(x,0,width,height)[0],resize(0,800,width,height)[1],resize(abs(self.cafe)/3,0,width,height)[0],resize(0,20,width,height)[1]))
        

###################          
""" Projectiles """
###################

electroball = pygame.image.load(f"{rootDir()}/Images/Sprites/Projectiles/Journault/Thunder.png")
electroball = pygame.transform.scale(electroball,resize(32,32,width,height))

class Electroball():
    def __init__(self,x,y,own,stage) -> None:
        self.id = 0
        self.vx = 8*signe(own.direction)
        self.vy = 0
        self.duration = 50
        self.x = x
        self.y = y
        self.stage = stage

        self.rotate = 0

        self.rect = [0,0,0,0]

        self.damages = 3.6
        self.knockback = 2
        self.stun = 8
        self.damages_stacking = 1/200

        self.angle = pi/4
        if not own.look_right :
            self.angle = pi-self.angle


    def update(self):
        rect = pygame.Rect(self.x,self.y,32,32)

        self.vy += 1.5

        if self.touch_stage(self.stage,rect):
            self.vy = -15
        self.x += self.vx
        self.y += self.vy
        self.duration -= 1
        self.rect = [rect.x,rect.y,rect.w,rect.h]


    def touch_stage(self,stage,rect):
        if rect.colliderect(stage.mainplat.rect):
            return True
        for p in stage.plats:
            if rect.colliderect(p.rect) and rect.y + rect.h < p.rect.y+self.vy+3:
                return True
        return False

        
    def deflect(self,modifier):
        self.vx = -self.vx*modifier
        self.own,self.other = self.other,self.own    

    def draw(self,window):
        self.rotate += self.vx
        sprite = pygame.transform.rotate(electroball,degrees(self.rotate))
        window.blit(sprite, (self.x+width/2,self.y+height/2)) # on dessine le sprite

auto = pygame.image.load(f"{rootDir()}/Images/Sprites/Projectiles/Journault/Auto.png")
auto = pygame.transform.scale(auto,resize(96,48,width,height))

class Automate():
    def __init__(self,x,y,own,other,stage) -> None:
        self.id = 0
        self.x = x
        self.y = y
        self.duration = 200
        self.damages = 0.5
        self.knockback = 3
        self.angle = pi/2
        self.stun = 8
        self.damages_stacking = 0
        self.own = own
        self.other = other
        self.stage = stage
        self.vx = 5 * signe(own.direction)
        self.vy = 0
        self.rect = [0,0,0,0]
        self.right = own.look_right
        self.explode = False
    
    def deflect(self):
        self.own,self.other = self.other,self.own
    
    def update(self):
        rect = pygame.Rect(self.x,self.y,48,48)
        rect.w /= 2
        self.rect = [rect.x,rect.y,rect.w,rect.h]
        self.y += self.vy
        self.x += self.vx
        if self.touch_stage(self.stage,rect) :
            self.vy = -1
        else :
            self.vy += 1.5
        
        if (rect.colliderect(pygame.Rect(self.other.rect)) or self.duration < 3) and not self.explode:
            self.duration = 5
            self.own.projectiles.append(Explosion(self.x-2,self.y-2,8.5,10,pi/3 if self.x < self.other.x else 2*pi/3,15,1/300,52))
            self.explode = True
        self.duration -= 1

    def deflect(self,modifier):
        self.vx *= -1
        self.right = not self.right
        self.own,self.other = self.other,self.own

    def touch_stage(self,stage,rect):
        if rect.colliderect(stage.mainplat.rect):
            return True
        for p in stage.plats:
            if rect.colliderect(p.rect) and rect.y + rect.h < p.rect.y+self.vy+3:
                return True
        return False

    def draw(self,window):
        sprite = pygame.transform.flip(auto,not self.right,False)
        x,y = resize(48,48,width,height)
        window.blit(sprite, resize(self.x+800,self.y+450,width,height),((0,0,x,y),(x,0,x,y))[(self.duration//5)%2]) # on dessine le sprite


class Explosion():
    def __init__(self,x,y,damages,knockback,angle,stun,damages_stacking,size) -> None:
        self.id = 0
        SFXDicoEvent['explosions']["gun shot"].play()
        self.x = x
        self.y = y
        self.damages = damages
        self.knockback = knockback
        self.angle = angle
        self.stun = stun
        self.damages_stacking = damages_stacking
        self.size = size
        self.rect = [0,0,0,0]
        self.spritenumber = 1
        self.duration = 10

    def deflect(self,modifier):
        self.damages = 0
        self.knockback = 0
        self.stun = 0

    def update(self):
        self.spritenumber = (self.duration-6) if self.duration > 6 else (6-self.duration)
        self.duration -= 1
        
    def draw(self,window):
        spritenumber = (self.duration-6) if self.duration > 6 else (6-self.duration)
        self.rect = [self.x,self.y,self.size,self.size]
        sprite = pygame.transform.scale(pygame.image.load(f"{rootDir()}/Images/Sprites/Projectiles/Fire/{spritenumber}.png"),resize(self.size,self.size,width,height))
        window.blit(sprite,(self.x+width/2,self.y+height/2))


##### Autres skins
