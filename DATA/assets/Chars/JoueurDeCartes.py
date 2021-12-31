from DATA.assets.Stages import Stage
from DATA.utilities.Base_Char import Char, Hitbox, change_left, signe
import pygame
from math import pi, cos, sin, sqrt
from random import randint
from DATA.utilities.Sound_manager import playsound

##### Joueur de Air-Président

class Air_President(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=1.9, dashspeed=3.6, airspeed=1.4, deceleration=0.6, fallspeed=0.5, fastfallspeed=1.6, fullhop=15, shorthop=12,
                         doublejumpheight=18,airdodgespeed=5,airdodgetime=3,dodgeduration=15)

        self.rect = pygame.Rect(100,0,48,120) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/SE/jump.wav") # Son test
        self.name = "Joueur de air-president"
        self.x = x
        self.rect.y = y
        self.player = player
        self.basefallspeed = 0.8
        self.blahaj = ["fatty","flat","flying","spiky"]
        self.currentblahaj = 0
        self.poutre = False
        self.stage = Stage
    
    def __str__(self) -> str:
        return "Joueur de air-president"

    def special(self,inputs): # Spécial
        if self.poutre :
            self.speed = 0.9
            self.airspeed = 0.5
            self.deceleration = 0.2
            self.dashspeed = 1
            self.fallspeed = 2
            self.fastfallspeed = 3
            self.fullhop = 13
            self.shorthop = 10
            if self.hitstun :
                self.projectiles.append(Poutre(0,0,self.stage,self))
                self.poutre = False
        else :
            self.speed = 1.9
            self.airspeed = 1.4
            self.deceleration = 0.6
            self.dashspeed = 3.6
            self.fallspeed = 0.5
            self.fullhop = 15
            self.shorthop = 12
        return False

    def animation_attack(self,attack,inputs,stage,other):
        self.stage = stage
        if self.poutre and attack != "DownB":
            attack = None
            self.attack = None
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up

        if attack == "UpB":
            if self.frame > 11 :
                self.attack = None
                self.upB = True
                self.can_act = False
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts

            if self.frame == 6: # Hitbox frame 6-15
                self.vx = 0
                self.vy = -24
                playsound(f"DATA/Musics/SE/boings/boing ({randint(2,8)}).mp3")
                self.active_hitboxes.append(Hitbox(-1.5,88,51,48,-pi/2,2,6,1/150,3,8,self,False,sound="boings/boing (1).wav"))
            if self.frame > 6 and self.active_hitboxes :
                self.active_hitboxes[-1].sizey -= self.vy

        if attack == "NeutralB":
            if self.frame < 5 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 24 :
                self.active_hitboxes.append(Hitbox(24,-32,256,256,0,0,0,0,0,6,self))
            if self.frame > 24 and self.frame < 30:
                if not self.active_hitboxes:
                    if other.grounded :
                        other.can_act = True
                        other.inputattack("Jab")
                        other.attack = "Jab"
                    else :
                        other.can_act = True
                        other.inputattack("NeutralAir")
                        other.attack = "NeutralAir"
            if self.frame > 33: # 3 frames de lag
                self.attack = None

        if attack == "DownB":
            if self.poutre :
                if self.frame == 25 :
                    self.poutre = False
                    self.projectiles.append(Poutre(signe(self.direction)*15,-15,stage,self))
            else :
                if self.frame == 22 :
                    self.poutre = True
                    self.attack = None
            if self.frame > 45 : # 20 frames de lag
                self.attack = None

        if attack == "SideB":
            if self.frame < 8 :
                if left : # peut reverse netre les frames 1 et 7
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 9 :
                if randint(1,65) == 1:
                    self.rect.y = 10000
                else :
                    if not self.look_right:
                        angle = 3*pi/4
                        x = change_left(64,48)
                    else:
                        angle = pi/4
                        x = 24
                    if randint(1,65) == 1:
                        self.projectiles.append(Carte(x,20,pi/42,"R",self))
                        self.BOUM = 30
                    else :
                        self.projectiles.append(Carte(x,20,angle,randint(1,13),self))

            if self.frame > 30 : # 21 frames de lag
                self.attack = None

        if attack == "Jab":
            if self.frame == 2 : # Frame 2-3
                self.active_hitboxes.append(Hitbox(32,20,44,48,3*pi/4,0.7,0.3,1/1000,5,2,self,False,boum=-2,sound="hits and slap/hit.wav"))
            if self.frame > 4: #  2 frames de lag
                self.attack = None

        if attack == "DownTilt":
            if self.frame == 5 : # Frames 5-10
                self.active_hitboxes.append(Hitbox(24,64,64,64,pi/3,3,1.2,1/750,9,2,self,False,sound="hits and slap/mini hit.wav"))
            if self.frame > 15: # 5 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame < 3 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 12: # Frames 12-15
                self.active_hitboxes.append(Hitbox(24,30,48,48,pi/4,4,12,1/50,12,4,self,False))

            if self.frame > 30: # 15 frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame > 8 and self.frame < 16 :
                if self.active_hitboxes :
                    if self.frame > 12 :
                        self.active_hitboxes[-1].relativey += 24
                    else :
                        self.active_hitboxes[-1].relativey -= 24
                    self.active_hitboxes[-1].relativex += -7*signe(self.direction)
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(24,0,32,32,pi/2,9,8.5,1/500,13,11,self,False,sound="wooshs/mini woosh.wav"))
            if self.frame > 25: # 17 Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame == 5 : #frames 5-11
                self.active_hitboxes.append(Hitbox(-8,-20,12,30,pi/4,5,4,1/300,12,7,self,True,sound="wooshs/mini woosh.wav"))
                if not self.look_right :
                    self.active_hitboxes[-1].sizex *= -1
                    self.active_hitboxes[-1].relativex += 10

            if self.frame > 5 and self.frame < 12 :
                if self.active_hitboxes :
                    self.active_hitboxes[-1].sizex += 10*signe(self.direction)
            if self.frame == 15 : #frames 14-15
                self.active_hitboxes.append(Hitbox(-8,-20,60,30,pi/4,8,7,1/220,16,3,self,True))
            if self.frame > 30: # 15 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 22 and self.frame > 2 :
                    self.lag = 8 # Auto cancel frame 1-2 et 22+, 8 frames de landing lag

        if attack == "ForwardAir":
            if self.frame == 9 : # Frame 9-10
                self.active_hitboxes.append(Hitbox(24,28,64,12,pi/6,12,11.3,1/150,16,2,self,False,sound="other/electric cable sound.wav"))
            if self.frame > 14  and self.frame < 21: # Fame 15-20
                self.active_hitboxes.append(Hitbox(24,28,64,12,pi/42,2,0.5,1/404,3,2,self,False,boum = -1))
            if self.frame > 45: # 25 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 30 and self.frame > 4 :
                    self.lag = 14 # Auto cancel frame 1-4 et 30+, 14 frames de landing lag

        if attack == "BackAir":
            if self.frame == 10: # Active on 10-12
                self.active_hitboxes.append(Hitbox(-48,32,48,52,3,9,9.5,1/250,15,3,self,False))
            if self.frame > 25: # 13 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 and self.frame > 2 :
                    self.lag = 9 # Auto cancel frame 1-2 et 20+, 9 frames de landing lag

        if attack == "DownAir":
            self.vy -= 0.2
            self.vx *= 0.9
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(0,128,48,48,pi/2,1,1.5,0,10,2,self,False))
            if self.frame == 18 :
                self.active_hitboxes.append(Hitbox(0,128,48,48,pi/2,1,1.1,0,10,2,self,False))
            if self.frame == 26 :
                self.active_hitboxes.append(Hitbox(0,128,48,48,pi/2,1,1.2,0,10,2,self,False))
            if self.frame == 34 :
                self.active_hitboxes.append(Hitbox(0,128,48,48,pi/2,1,1.3,0,14,2,self,False))
            if self.frame == 42 :
                self.active_hitboxes.append(Hitbox(-8,128,64,64,-pi/2,5,6.5,1/200,20,2,self,False,sound="hits and slap/cool hit.wav"))
            if self.frame > 55: # 17 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 45 and self.frame > 2 :
                    self.lag = 13 # Auto cancel frame 1-2 et 45+, 13 frames de landing lag

        if attack == "NeutralAir":
            if self.frame == 9:
                self.projectiles.append(Blahaj(self.blahaj[self.currentblahaj],self,stage))
                self.currentblahaj = (self.currentblahaj+1)%4
            if self.frame > 24: # 15 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 and self.frame > 2 :
                    self.lag = 3 # Auto cancel frame 1-2 et 20+, 3 frames de landing lag

        if attack == "ForwardSmash":
            if self.frame > 6 and self.frame < 9 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 7
                self.charge = self.charge+1

            elif self.frame == 19 : # Active on 19-24
                self.charge = min(self.charge,100)
                self.active_hitboxes.append(Hitbox(-26,0,52,52,pi/3,15+12.5*(self.charge/250),17,1/250,20+9*(self.charge/150),5,self,False,sound="hits and slap/punch1.mp3"))
            if self.frame > 18 and self.frame < 23 :
                if self.active_hitboxes :
                    self.active_hitboxes[-1].relativex += (60-self.frame*2)*signe(self.direction)
                    self.active_hitboxes[-1].relativey += 20
           
            if self.frame > 52: # 25 frames de lag
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

            if self.frame == 11 :
                self.active_hitboxes.append(Hitbox(42,50,32,32,3*pi/4,9,3,0,7,4,self,False))
            elif self.frame == 15 : # Active on 15-28
                self.charge = min(self.charge,100)
                self.active_hitboxes.append(Hitbox(0,-50,48,48,pi/3,9+7*(self.charge/150),14,1/80,13+7*(self.charge/100),13,self,False,sound="hits and slap/cool hit.wav"))

            if self.frame > 49: # 21 frames de lag
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
            elif self.frame == 16 : # Active on 16-18
                self.charge = min(self.charge,100)
                self.active_hitboxes.append(Hitbox(35,-20,32,42,-pi/2,12,3,0,8,3,self,False))
            
            elif self.frame == 19 : # Active on 19-27
                self.charge = min(self.charge,100)
                self.active_hitboxes.append(Hitbox(-10,100,100,32,5*pi/13,12+10*(self.charge/200),10.5,1/250,12+8*(self.charge/300+1),8,self,False,sound="hits and slap/punch2.mp3"))

            if self.frame > 50: # 23 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
            if self.frame > 5 and self.frame%10 == 0 and self.frame < 55: # Active on 10-11/20-21/30-31/40-41/50-51/
                self.vy = 0
                if self.grounded :
                    self.vx += self.dashspeed*signe(self.direction)*5
                else :
                    self.vx -= self.dashspeed*signe(self.direction)*5
                self.active_hitboxes.append(Hitbox(10,32,64,64,pi/5,8,3.5,1/350,7,3,self,False,sound="hits and slap/mini hit.wav"))

            if self.frame > 66: # 15 frames de lag
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

class Carte():
    def __init__(self,x,y,angle,number,own:Air_President) -> None:
        if number == "R":
            playsound("DATA/Musics/SE/other/Its-pronounced-rules.mp3")
            self.sound = pygame.mixer.Sound("DATA/Musics/SE/hits and slap/cool hit.wav")
            self.sprite = pygame.transform.scale(pygame.image.load(f"./DATA/Images/Sprites/Projectiles/Air_President/Cartes/RulesCard.png"),(48,64))
            self.knockback = 1000
            self.damages = 999
            self.stun = 1000
            self.damages_stacking = 1
        else :
            self.sound = pygame.mixer.Sound("DATA/Musics/SE/wooshs/woosh.mp3")
            self.number = number + 2
            if self.number > 13 :
                self.number = self.number-13
            self.sprite = pygame.transform.scale(pygame.image.load(f"./DATA/Images/Sprites/Projectiles/Air_President/Cartes/{self.number}.png"),(48,64))
            self.number = number
            self.angle = angle
            self.knockback = (self.number/2+1)*3
            self.damages = 1.5*self.number
            self.stun = self.number+5
            self.damages_stacking = self.number*1/500
        self.duration = 6
        self.rect = self.sprite.get_rect(topleft=(x+own.x,y+own.rect.y))
        self.angle = angle
        self.x = x
        self.y = y
        self.own = own
    
    def update(self):
        self.duration -= 1
    
    def deflect(self,modifier):
        self.duration = 0
    
    def draw(self,window):
        window.blit(self.sprite,(self.x+self.own.x+800,self.y+self.own.rect.y+450))

class Blahaj():
    def __init__(self,color,own:Air_President,stage):
        # Blahaj
        playsound("DATA/Musics/SE/wooshs/encore un woosh.mp3")
        self.sound = pygame.mixer.Sound("DATA/Musics/SE/boings/boing.mp3")
        self.sprite = pygame.transform.scale(pygame.image.load("./DATA/Images/Sprites/Projectiles/Air_President/Blahaj/Blahaj_"+color+".png"),(72,36))
        self.sprite = pygame.transform.flip(self.sprite,not own.look_right,False)
        self.rect = self.sprite.get_rect()
        self.x = own.rect.x
        self.y = own.rect.y + own.rect.h//2
        self.color = color
        if self.color == "flying":
            self.vx = 15*signe(own.direction)
        else :
            self.vx = 10*signe(own.direction)
        if self.color == "flying" :
            self.vy = -6
        else :
            self.vy = -4
        self.duration = 5
        self.stage = stage
        if self.color == "flat":
            self.damages_stacking=1/250
        else :
            self.damages_stacking=1/750
        if self.color == "fatty":
            self.angle = -pi/2
        elif not own.look_right :
            self.angle = 3*pi/4
        else :
            self.angle = pi/4
        if self.color == "flat":
            self.knockback = 7
        elif self.color == "fatty" :
            self.knockback = 5
        else :
            self.knockback = 3
        if self.color == "spiky":
            self.damages = 3.2
        elif self.color == "flying" :
            self.damages = 0.8
        else :
            self.damages = 1.2
        if self.color == "spiky" :
            self.stun = 6
        elif self.color == "flat":
            self.stun = 8
        else :
            self.stun = 3
    
    def touch_stage(self,stage,rect):
        if rect.colliderect(stage.mainplat.rect):
            return True
        for p in stage.plats:
            if rect.colliderect(p.rect) and rect.y + rect.h-4 < p.rect.y+self.vy+4:
                return True
        return False

    def update(self):
        if self.touch_stage(self.stage,self.rect):
            self.duration = 0
        self.x += round(self.vx)
        self.y += self.vy
        if self.color == "fatty":
            self.vy += 0.7
        else :
            self.vy += 0.4
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
        if self.y > 800 :
            self.duration = 0

    def deflect(self,modifier):
        self.vy = -5
        self.vx = -self.vx*modifier
        self.damages = self.damages * modifier
        self.knockback = self.damages * modifier
        self.angle = pi-self.angle

    def draw(self,window):
        window.blit(self.sprite, (self.x+800,self.y+450)) # on dessine le sprite

class Poutre():
    def __init__(self,vx,vy,stage,own:Air_President) -> None:
        self.sprite = pygame.transform.scale(pygame.image.load("./DATA/Images/Sprites/Projectiles/Air_President/Poutre.png"),(48,48))
        self.x = own.x
        self.y = own.rect.y
        self.vx = vx
        self.vy = vy
        self.angle = -signe(vy)*pi/4
        if vx < 0 :
            self.angle = pi-self.angle
        if abs(vx) < 0.01 :
            if vy > 0 :
                self.angle = -pi/2
            else :
                self.angle = pi/2
        self.knockback = sqrt(self.vx**2+self.vy**2)
        self.damages = 24
        self.stun = sqrt(self.vx**2+self.vy**2)
        self.damages_stacking = 1/500
        self.duration = 10
        self.stage = stage
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
        self.sound = pygame.mixer.Sound("DATA/Musics/SE/hits and slap/hitting metal.wav")

    def update(self):
        self.knockback = sqrt(self.vx**2+self.vy**2)
        self.damages = 24
        self.stun = sqrt(self.vx**2+self.vy**2)/3
        self.damages_stacking = 1/500
        self.x += round(self.vx)
        self.y += self.vy
        self.vy += 1.8
        self.vx *= 0.96
        self.angle = -signe(self.vy)*pi/4
        if self.vx < 0 :
            self.angle = pi-self.angle
        if abs(self.vx) < 0.01 :
            if self.vy > 0 :
                self.angle = -pi/2
            else :
                self.angle = pi/2
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
        if self.y > 800 :
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
        window.blit(self.sprite, (self.x+800,self.y+450)) # on dessine le sprite
    