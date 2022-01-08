from DATA.utilities.Base_Char import Char, Hitbox, change_left, signe
import pygame
from math import exp, pi
from DATA.utilities.Sound_manager import playsound

##### Copier

class Renault(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=1.7, dashspeed=5, airspeed=0.9, deceleration=0.7, fallspeed=0.5, fastfallspeed=1, fullhop=13, shorthop=10,
                         doublejumpheight=15,airdodgespeed=6,airdodgetime=3,dodgeduration=15)

        self.rect = pygame.Rect(100,0,48,120) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/SE/jump.wav") # Son test
        self.name = "Renault"
        self.x = x
        self.rect.y = y
        self.player = player
        self.daccord = 0
        self.cling = False
    
    def __str__(self) -> str:
        return "Renault"

    def special(self,inputs):
        if self.dash and self.frame % 6 == 0 and self.grounded and self.attack is None:
            self.active_hitboxes.append(Hitbox(0,80,70,40,pi/3,9,2,0,4,2,self,boum=-1))
        return False

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            if self.frame < 5 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 7 and self.frame < 100 :
                self.vy = -5-self.frame/20
                if self.frame%8 == 0 :
                    playsound("DATA/Musics/SE/wooshs/woosh.mp3")
                    self.active_hitboxes.append(Hitbox(-2,-24,52,20,3*pi/5,8+abs(self.vy),3,0,9,4,self,position_relative=True))
            if self.frame > 100 :
                self.can_act = False # ne peut pas agir après un grounded up B
                self.attack = None
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts

        if attack == "NeutralB":
            if self.frame < 10 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 15 :
                self.projectiles.append(Gear(15*signe(self.direction),self))
            if self.frame > 42: # 10 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownB":
            if self.frame > 15 and self.frame < 40 :
                self.vx = (right-left)*12
                self.vy = (down-up)*12
                self.show = False
                self.intangibility = 4
            if self.frame == 40 :
                self.show = True
                playsound("DATA/Musics/SE/wooshs/other woosh.wav")
                self.active_hitboxes.append(Hitbox(0,0,48,120,pi/2,12,16,1/250,11,2,self,boum=2))
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts
            if self.frame > 70 : # 30 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame < 5 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 8 :
                self.cling = True
            if self.frame > 8 and self.frame < 80 and self.cling:
                self.vx = (8+self.frame/10)*signe(self.direction)
                self.vy = -self.fastfallspeed if self.fastfall else -self.fallspeed
                if special and self.frame%3 == 0 :
                    playsound("DATA/Musics/SE/hits and slap/hitting metal.wav")
                    self.active_hitboxes.append(Hitbox(48,12,64,64,0,2,0.8,0,4,2,self,boum=-1))
                if not special :
                    self.cling = False
                    self.projectiles.append(Drill(4*signe(self.direction),self))
                    self.frame = 10
            if self.frame == 80 :
                self.projectiles.append(Drill(4*signe(self.direction),self))
                self.lag = 30
            if self.frame > 80 or (self.frame > 45 and not self.cling): # 35 frames de lag
                self.can_act = False
                self.attack = None
                self.doublejump = [True for _ in self.doublejump]

        if attack == "Jab":
            if self.frame == 5 :
                self.active_hitboxes.append(Hitbox(64,60,48,48,pi/2,1,0.1,0,8,2,self))
            if self.frame == 10 :
                if attack_button :
                    self.frame = 10
                self.active_hitboxes.append(Hitbox(64,10,48,48,-pi/2,1,1,0,8,2,self))
            if self.frame == 14 :
                if attack_button :
                    self.frame = 6
                self.active_hitboxes.append(Hitbox(64,60,48,48,pi/2,1,0.1,0,8,2,self))
            if self.frame == 20 :
                self.active_hitboxes.append(Hitbox(64,32,64,64,pi/3,4,8,1/200,10,2,self,boum=1))

            if self.frame > 30: # 20 frames de lag
                self.attack = None

        if attack == "DownTilt":
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(64,120-64,16,64,8*pi/17,8,6.4,1/200,12,8,self))

            if self.frame > 20: # 7 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame < 3 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 8 :
                self.daccord += 1
                self.active_hitboxes.append(Hitbox(48,48,64-2*self.daccord,48,pi/4,4*self.daccord,2*self.daccord,self.daccord/500,4*self.daccord,3,self))
            if self.frame == 10 and self.active_hitboxes or other.parried :
                self.daccord = 0
            if self.frame > 30: # 8 frames de lag
                self.attack = None
        elif not attack == "DashAttack":
            self.daccord = 0

        if attack == "UpTilt":
            if self.frame == 9 :
                self.active_hitboxes.append(Hitbox(48,120,66,0,5/3,3,3.3,1/333,9,6,self))
            if self.frame < 12 and self.active_hitboxes :
                self.active_hitboxes[-1].sizey += 22
                self.active_hitboxes[-1].relativey -= 22
            if self.frame == 15 :
                self.active_hitboxes.append(Hitbox(48,54,66,66,5/3,12,6.7,1/333,15,3,self))
            if self.frame > 15 and self.active_hitboxes :
                self.active_hitboxes[-1].sizey += 22
                self.active_hitboxes[-1].relativey -= 22
            if self.frame > 40: # 22 Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(0,0,36,36,pi-exp(1)*pi/5,12,exp(1),exp(-6),14,10,self))
            if self.frame > 8 and self.active_hitboxes :
                self.active_hitboxes[-1].relativex += signe(self.direction)*10
                self.active_hitboxes[-1].relativey -= exp((8-self.frame)/5)*15

            if self.frame > 30: # 22 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 24 and self.frame > 3 :
                    self.lag = 7 # Auto cancel frame 1-3 et 24+, 7 frames de landing lag

        if attack == "ForwardAir":
            if self.frame == 7 :
                self.active_hitboxes.append(Hitbox(50,36,36,36,pi/3,12,6,1/200,7,5,self))
            if self.frame > 7 and self.active_hitboxes :
                self.active_hitboxes[-1].relativex += signe(self.direction)*5
                self.active_hitboxes[-1].relativey += 8

            if self.frame > 25: # 13 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 and self.frame > 2 :
                    self.lag = 9 # Auto cancel frame 1-2 et 22+, 9 frames de landing lag

        if attack == "BackAir":
            if self.frame == 12 :
                self.active_hitboxes.append(Hitbox(change_left(30,72),32,72,52,pi-(pi/1+pi),14,12,1/200,13,2,self))

            if self.frame > 25: # 13 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 22 and self.frame > 2 :
                    self.lag = 8 # Auto cancel frame 1-2 et 22+, 8 frames de landing lag

        if attack == "DownAir":
            if self.frame == 18 :
                self.active_hitboxes.append(Hitbox(52,40,52,28,-pi/3,19,26.6,1/200,14,2,self,boum=5,sound="hits and slap/slap.mp3"))
            if self.frame == 19 and self.active_hitboxes:
                self.active_hitboxes.append(Hitbox(52,72,42,42,-pi/2,2,2.6,1/800,2,8,self,sound="hits and slap/punch.mp3"))
            if self.frame > 19 and self.active_hitboxes :
                self.active_hitboxes[-1].relativex -= self.frame*signe(self.direction)/2
                self.active_hitboxes[-1].relativey += 30-self.frame

            if self.frame > 50: # 23 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 40 and self.frame > 8 :
                    self.lag = 17 # Auto cancel frame 1-8 et 40+, 17 frames de landing lag

        if attack == "NeutralAir":
            if self.frame > 6 and self.frame < 16 :
                playsound("DATA/Musics/SE/other/electric cable sound.wav")
                self.active_hitboxes.append(Hitbox(20,56,8,8,pi/2,1,0.1,0,3,2,self,boum=-2))
            if self.frame > 16 and self.frame < 20 :
                playsound("DATA/Musics/SE/other/electric cable sound.wav")
                self.active_hitboxes.append(Hitbox(-40,-4,128,128,pi/2,2,0.3,0,5,2,self,boum=0))
            if self.frame == 22 :
                playsound("DATA/Musics/SE/other/electric cable sound.wav")
                self.active_hitboxes.append(Hitbox(-44,-8,136,136,pi/2,13,3,1/200,12,2,self,boum=1))

            if self.frame > 40: # 17 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 30 and self.frame > 2 :
                    self.lag = 9 # Auto cancel frame 1-2 et 30+, 9 frames de landing lag

        if attack == "ForwardSmash":
            if self.frame > 6 and self.frame < 9 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 7
                self.animeframe -= 1
                self.charge = self.charge+1
                if self.charge%3 == 2 :
                    self.active_hitboxes.append(Hitbox(48,48,36,36,pi/4,1,0.3,0,5,2,self))
            if self.frame == 20 :
                self.charge = min(100,self.charge)
            if self.frame == 22 :
                self.active_hitboxes.append(Hitbox(48,48,36,36,pi/2,2,1,0,5,3,self,boum=-2,sound="hits and slap/cool hit.wav"))
            if self.frame == 25 :
                self.active_hitboxes.append(Hitbox(72,24,36,36,pi,2,1,0,5,3,self,boum=-2,sound="hits and slap/cool hit.wav"))
            if self.frame == 28 :
                self.active_hitboxes.append(Hitbox(96,48,36,36,-pi/2,2,1,0,5,3,self,boum=-2,sound="hits and slap/cool hit.wav"))
            if self.frame == 31 :
                self.active_hitboxes.append(Hitbox(72,72,36,36,0,2,1,0,5,3,self,boum=-2,sound="hits and slap/cool hit.wav"))
            if self.frame == 34 :
                self.active_hitboxes.append(Hitbox(50,34,64,64,pi/6,18+6*(self.charge/100),8,1/200,17+5*(self.charge/100),3,self,sound="hits and slap/cool hit.wav"))
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
            if self.frame == 20 :
                self.charge = min(100,self.charge)
                self.active_hitboxes.append(Hitbox(54,100,48,22,pi/2,20+8*(self.frame/100),12,1/200,19,5,self,sound="hits and slap/punch.mp3"))
            if self.frame > 20 and self.active_hitboxes:
                self.active_hitboxes[-1].relativey -= 20
                self.active_hitboxes[-1].sizey += 20

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
            if self.frame > 20 and self.frame < 28 and self.frame%2 == 0 :
                self.charge = min(100,self.charge)
                self.active_hitboxes.append(Hitbox(52,90,48,48,-pi/2,2,5,0,7,2,self,boum=-1,sound="hits and slap/cool hit.wav"))
            if self.frame == 30 :
                self.charge = min(100,self.charge)
                self.active_hitboxes.append(Hitbox(52,90,48,48,-pi/3,20+8*(self.charge/100),8,1/300,18+7*(self.charge/100),2,self,boum=2,sound="hits and slap/hitting metal.wav"))

            if self.frame > 40: # 23 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
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

class Drill():
    def __init__(self,vx,own:Char) -> None:
        self.basevx = vx
        self.vx = vx
        self.direction = signe(own.direction)
        if own.look_right :
            self.x = own.x + 48
            self.angle = pi/4
        else :
            self.x = own.x+change_left(48,64)-48
            self.angle = 3*pi/4
        self.y = own.rect.y + 42
        self.duration = 120
        self.damages = 4
        self.stun = 12
        self.knockback = 10
        self.damages_stacking = 1/200
        self.sprite = pygame.image.load(f"./DATA/Images/Sprites/Projectiles/Renault/Drill.png")
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
    
    def update(self):
        self.duration -= 1
        self.vx = self.basevx + (120-self.duration)/5*self.direction
        self.x += self.vx
    
    def deflect(self,modifier):
        self.basevx = -self.basevx*modifier
        self.vx = -self.vx*modifier
        self.duration = 120
        self.damages *= modifier
        self.stun *= modifier
        self.knockback *= modifier

    def draw(self,window):
        window.blit(pygame.transform.flip(self.sprite,self.direction<0,False),(self.x+800,self.y+450))
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))

class Gear():
    def __init__(self,vx,own:Char) -> None:
        self.vx = vx
        self.direction = signe(own.direction)
        if own.look_right :
            self.x = own.x + 48
            self.angle = pi/4
        else :
            self.x = own.x+change_left(48,64)-48
            self.angle = 3*pi/4
        self.y = own.rect.y + 42
        self.duration = 120
        self.damages = 5
        self.stun = 11
        self.knockback = 10
        self.damages_stacking = 1/200
        self.sprite = pygame.image.load(f"./DATA/Images/Sprites/Projectiles/Renault/Gear.png")
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
        self.sound = pygame.mixer.Sound("DATA/Musics/SE/hits and slap/hitting metal.wav")
    
    def update(self):
        self.duration -= 1
        self.x += self.vx
    
    def deflect(self,modifier):
        self.vx = -self.vx*modifier
        self.duration = 120
        self.damages *= modifier
        self.stun *= modifier
        self.knockback *= modifier

    def draw(self,window):
        window.blit(pygame.transform.flip(self.sprite,self.direction<0,False),(self.x+800,self.y+450))
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))

##### Autres skins
