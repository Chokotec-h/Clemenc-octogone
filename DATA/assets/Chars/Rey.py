from random import random
import DATA.utilities.Animations as Animations
from DATA.utilities.Base_Char import Char, Hitbox, change_left, signe
import pygame
from math import pi
from DATA.utilities.Sound_manager import playsound

##### Rey

class Rey(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=2.3, dashspeed=3.4, airspeed=1.1, deceleration=0.68, fallspeed=0.9, fastfallspeed=1.7, fullhop=15, shorthop=12,
                         doublejumpheight=18,airdodgespeed=6,airdodgetime=3,dodgeduration=15)

        self.rect = pygame.Rect(100,0,48,120) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/SE/jump.wav") # Son test
        self.name = "Rey"
        self.x = x
        self.rect.y = y
        self.player = player
        self.foodvy = 0
        self.door = None
    
    def __str__(self) -> str:
        return "Rey"

    def special(self,inputs): 
        pass

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            if self.frame > 5 and self.frame < 51: # Saute frame 11
                self.vy = -9
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts
                if left :
                    self.vx -= self.airspeed
                if right :
                    self.vx += self.airspeed
                if self.frame%10 == 0 :
                    playsound("DATA/Musics/SE/wooshs/woosh.mp3")
            if self.frame > 51 :
                self.attack = None
                self.can_act = True

        if attack == "NeutralB":
            if self.frame < 5 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 5 : # active on 5-25
                self.active_hitboxes.append(Hitbox(50,42,32,32,pi/4,3,16,1/200,12,20,self,False))
                self.foodvy = -14
            if self.frame > 5 and self.frame < 30 :
                if self.active_hitboxes :
                    self.active_hitboxes[-1].relativex += 11*signe(self.direction)
                    self.active_hitboxes[-1].relativey += self.foodvy
                    self.active_hitboxes[-1].sizex += 2
                    self.active_hitboxes[-1].sizey += 2
                    self.active_hitboxes[-1].knockback += 1
                    self.foodvy += 3
            if self.frame > 35: # 10 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownB":
            if self.frame == 6 :
                if self.door is None :
                    playsound("DATA/Musics/SE/other/Door-Slam.wav")
                    self.door = Door(self.rect.x,self.rect.y,self)
                    self.projectiles.append(self.door)
                else :
                    playsound("DATA/Musics/SE/other/Door-Slam.wav")
                    self.door.in_use = True
                    self.x = self.door.x + self.rect.w/2
                    self.rect.y = self.door.y
                    self.vx = 0
                    self.vy = 0
            if self.frame > 20 : # 14 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame < 3 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 5 :
                self.projectiles.append(Spectre_de_rey(self,other))
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts
                self.can_act = False
            if self.frame > 30 : # 25 frames de lag
                self.attack = None

        if attack == "Jab":
            if self.frame == 3 :
                self.active_hitboxes.append(Hitbox(42,42,64,42,pi/6,2,4,1/1000,12,2,self,False,sound="hits and slap/mini hit.wav"))
            if self.frame > 6 and attack_button :
                self.attack = "Jab2"
                self.frame = 0

            if self.frame > 21: # 18 frames de lag
                self.attack = None

        if attack == "Jab2":
            if self.frame == 3 :
                self.active_hitboxes.append(Hitbox(42,42,64,42,pi/4,2,4,1/1000,12,2,self,False,sound="hits and slap/mini hit.wav"))
            if self.frame > 5 and attack_button :
                self.attack = "Jab3"
                self.frame = 0

            if self.frame > 23: # 18 frames de lag
                self.attack = None

        if attack == "Jab3":
            if self.frame == 4 :
                self.active_hitboxes.append(Hitbox(42,42,64,42,pi/3,10,8,1/200,14,2,self,False,sound="hits and slap/other hit.mp3"))

            if self.frame > 35: # 18 frames de lag
                self.attack = None

        if attack == "DownTilt":
            if self.frame == 8 : # Frame 8-13
                self.active_hitboxes.append(Hitbox(24,80,75,24,5*pi/13,12,1.2,1/200,20,3,self,False,sound="hits and slap/hit.wav"))

            if self.frame > 20: # 7 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame < 3 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True

            if self.frame == 4 :
                self.active_hitboxes.append(Hitbox(42,42,48,64,pi/4,3,9,1/1000,12,3,self,False))

            if self.frame > 10 and attack_button :
                self.attack = "ForwardTilt2"
                self.frame = 0

            if self.frame > 31: # 8 frames de lag
                self.attack = None

        if attack == "ForwardTilt2":
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(42,40,50,50,pi/4,14,11,1/250,14,2,self,False,sound="hits and slap/cool hit.wav"))

            if self.frame > 30: # 8 frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame == 6 :
                self.rect.y -= 60
                self.active_hitboxes.append(Hitbox(0,0,48,128,6*pi/13,17,14,1/200,18,8,self,False,sound="hits and slap/punch.mp3"))
            if self.frame > 25: # 11 Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(-8,-30,32,48,3*pi/10,10,9,1/250,14,8,self,False,sound="hits and slap/punch2.mp3"))
            if self.frame == 12 :
                if self.active_hitboxes :
                    self.active_hitboxes[-1] = Hitbox(24,-30,32,48,pi/3,10,9,1/250,14,4,self,False,sound="hits and slap/punch2.mp3")

            if self.frame > 22: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 18 and self.frame > 2 :
                    self.lag = 9 # Auto cancel frame 1-2 et 18+, 9 frames de landing lag

        if attack == "ForwardAir":
            if self.frame == 14 :
                self.active_hitboxes.append(Hitbox(32,42,48,48,pi/6,18,22,1/180,17,16,self,sound="hits and slap/cool hit.wav"))
            if self.frame == 16 :
                if self.active_hitboxes :
                    self.active_hitboxes[-1].damages = 3
                    self.active_hitboxes[-1].stun = 8
                    self.active_hitboxes[-1].knockback = 7
                    self.active_hitboxes[-1].sound = pygame.mixer.Sound("DATA/Musics/SE/hits and slap/8bit hit.mp3")

            if self.frame > 45: # 15 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 38 and self.frame > 3 :
                    self.lag = 14 # Auto cancel frame 1-3 et 38+, 14 frames de landing lag

        if attack == "BackAir":
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(-64,42,64,64,pi/50,7,3,1/1000,12,2,self,False))
            if self.frame > 10 and self.frame%5 == 3 and self.frame < 28:
                if self.frame%2 == 0 :
                    self.active_hitboxes.append(Hitbox(-72,42,112,48,pi/50,7,3,1/1000,12,2,self,False,sound="hits and slap/punch2.mp3"))
                else :
                    self.active_hitboxes.append(Hitbox(change_left(-72,112),42,112,48,49*pi/50,7,3,1/1000,12,2,self,False,sound="hits and slap/punch2.mp3"))
            if self.frame == 30 :
                    self.active_hitboxes.append(Hitbox(-100,42,100,48,pi,13,3.4,1/220,12,2,self,False,sound="hits and slap/punch1.mp3"))
            

            if self.frame > 40: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 35 and self.frame > 2 :
                    self.lag = 12 # Auto cancel frame 1-2 et 35+, 12 frames de landing lag

        if attack == "DownAir":
            if self.frame > 15 :
                self.vx = 15*signe(self.direction)
                self.vy += 2*self.fastfallspeed
            if self.frame == 16 :
                self.vy = 3*self.fastfallspeed
                self.active_hitboxes.append(Hitbox(24,70,72,72,-pi/3,15,8,1/190,15,40,self,False,sound="hits and slap/cool hit.wav"))


            if self.grounded or self.frame > 60 :
                self.attack = None
                self.lag = 12 # Ne s'arrète qu'au sol ou au bout de 60 frames
                if self.active_hitboxes :
                    self.active_hitboxes.pop()

        if attack == "NeutralAir":
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(-20,-20,88,140,pi/2,1,4,0,10,2,self,False))
            if self.frame == 15 :
                self.active_hitboxes.append(Hitbox(-20,-20,88,140,pi/2,1,4,0,10,2,self,False))
            if self.frame == 20 :
                self.active_hitboxes.append(Hitbox(-20,-20,88,140,pi/4,10,8,0,12,2,self,True))

            if self.frame > 38: # 18 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 30 and self.frame > 2 :
                    self.lag = 8 # Auto cancel frame 1-2 et 30+, 8 frames de landing lag

        if attack == "DownSmash":

            if self.frame < 5 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 5 and self.frame < 8 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 6
                self.animeframe -= 1
                self.charge = self.charge+1
            if self.frame < 20 :
                self.superarmor = -1
            else :
                self.superarmor = 0
            if self.frame == 20 :
                self.charge = min(100,self.charge)
                self.active_hitboxes.append(Hitbox(32,50,72,48,pi/10,22+9*(self.charge/100),17,1/130,20+11*(self.charge/100),3,self,False,sound="hits and slap/cool hit.wav"))
            if self.frame > 65: # 42 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "UpSmash":

            if self.frame < 5 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 10 and self.frame < 13  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.animeframe -= 1
                self.frame = 11
                self.charge = self.charge+1
            if self.frame == 21 :
                self.active_hitboxes.append(Hitbox(-32,-20,64,64,5*pi/9,28+8*(self.charge/100),16,1/150,26+10*(self.charge/100),5,self,False,sound="hits and slap/punch1.mp3"))
            if self.frame == 23 :
                if self.active_hitboxes :
                    self.active_hitboxes[-1] = Hitbox(change_left(-32,64),-20,64,64,4*pi/9,28+8*(self.charge/100),16,1/150,26+10*(self.charge/100),2,self,False,sound="hits and slap/punch1.mp3")
            if self.frame > 40: # 25 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "ForwardSmash":
            if self.frame > 7 and self.frame < 10  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.animeframe -= 1
                self.frame = 8
                self.charge = self.charge+1
            
            if self.frame == 24 :
                self.charge = min(100,self.charge)
                self.active_hitboxes.append(Hitbox(64,42,48,48,29/60,25+8*(self.charge/100),18,1/190,14+7*(self.charge/100),2,self,False,sound="hits and slap/hitting metal.wav"))

            if self.frame > 47: # 23 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
            if self.frame == 6 :
                self.active_hitboxes.append(Hitbox(24,80,70,50,pi/4,14,8,1/200,13,20,self,False))
            if self.frame == 10 :
                if self.active_hitboxes :
                    self.active_hitboxes[-1].knockback = 7
                    self.active_hitboxes[-1].damages = 6
                    self.active_hitboxes[-1].damages_stacking = 1/250
                    self.active_hitboxes[-1].stun = 7
                    if self.look_right :
                        self.active_hitboxes[-1].angle = pi/6
                    else :
                        self.active_hitboxes[-1].angle = 5*pi/6
            if self.frame > 4 and self.frame < 26 :
                self.vy = 0
                if self.grounded :
                    self.vx += self.dashspeed*signe(self.direction)/(self.frame-2)*10
                else :
                    self.vx -= self.dashspeed*signe(self.direction)
            if self.frame > 40: # 24 frames de lag
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

doorsprites = [pygame.image.load(f"./DATA/Images/Sprites/Projectiles/Rey/Porte/Open{6-i}.png") for i in range(6)]

class Door():
    def __init__(self,x,y,own:Rey) -> None:
        self.sound = pygame.mixer.Sound("DATA/Musics/SE/other/Door-Slam.wav")
        self.x = x
        self.y = y
        self.own = own
        self.in_use = False
        self.damages = 0
        self.stun = 0
        self.knockback = 0
        self.damages_stacking = 0
        self.angle = 0
        self.sprite = pygame.image.load(f"./DATA/Images/Sprites/Projectiles/Rey/Porte/Close.png")
        self.duration = 7
        self.rect = pygame.Rect(0,0,0,0)

    def update(self):
        if self.in_use :
            self.duration -= 0.5
            self.own.rect.x = self.x
            self.own.rect.y = self.y
            self.own.vx = 0
            self.own.vy = 0
            self.own.door = None

    def draw(self,window):
        sprite = self.sprite if self.duration > 6 else doorsprites[round(self.duration)-1] if self.duration > 2 else doorsprites[0]
        window.blit(sprite, (self.x+800-8,self.y+450-8)) # on dessine le sprite

    def deflect(self,modifier):
        return

class Spectre_de_rey():
    def __init__(self,own:Rey,other) -> None:
        self.sound = pygame.mixer.Sound("DATA/Musics/SE/lasers/cool lazer.mp3")
        self.x = own.rect.x
        self.y = own.rect.y+own.rect.h/12
        self.own = own
        self.sprite = Animations.get_sprite(own.animation,own.name,own.animeframe+1,own.look_right)[0]
        self.sprite = pygame.transform.scale(self.sprite,(self.sprite.get_size()[0]*3,self.sprite.get_size()[1]*3))
        self.vx = 20*signe(own.direction)
        self.other = other
        self.damages = 2
        self.stun = 5
        self.knockback = 8
        self.damages_stacking = 0
        self.angle = random()*pi
        self.rect = self.sprite.get_rect(topleft = (self.x,self.y))
        self.duration = 2

    
    def update(self):
        self.x += self.vx
        self.rect = self.sprite.get_rect(topleft = (self.x,self.y))
        if self.rect.colliderect(self.other.rect):
            self.duration -= 1
        if self.duration < 1 :
            self.own.x,self.own.rect.y,self.other.x,self.other.rect.y = self.other.x-abs(self.own.vx),self.other.rect.y-abs(self.own.vy),self.own.x-abs(self.other.vx),self.own.rect.y-abs(self.other.vy)
            # inverse les positions
    def draw(self,window):
        window.blit(self.sprite, (self.x+800,self.y+450)) # on dessine le sprite
    def deflect(self,modifier):
        self.own, self.other = self.other,self.own
        self.vx *= -modifier
        self.damages *= modifier
        self.stun *= modifier
        self.knockback *= modifier



##### Autres skins
