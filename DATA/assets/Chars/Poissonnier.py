
from DATA.utilities.Animations import get_sprite
from DATA.utilities.Base_Char import *
import pygame
from math import pi, sin
from DATA.utilities.functions import *
from DATA.utilities.build import rootDir

from DATA.utilities.Interface import Texte

##### Poissonnier

class Poissonnier(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=2, dashspeed=3, airspeed=1.7, deceleration=0.78, fallspeed=1, fastfallspeed=1.8, fullhop=19, shorthop=15,
                         doublejumpheight=18,airdodgespeed=6,airdodgetime=3,dodgeduration=15)

        self.rect = [100,0,48,120] # Crée le rectangle de perso
        self.name = "Poissonnier"
        self.x = x
        self.rect[1] = y
        self.player = player
        self.overheat = 0
        self.damagesdealt = 0
        self.damagestaken = 0
        self.otherdamages = 0
    
    def __str__(self) -> str:
        return "Poissonnier"

    def special(self,inputs): 
        if self.damagesdealt < self.otherdamages :
            self.overheat += (self.otherdamages - self.damagesdealt)*1.42
            self.damagesdealt = self.otherdamages
        if self.damagestaken < self.damages :
            self.overheat -= (self.damages - self.damagestaken)*0.2
            self.damagestaken = self.damages
        if self.otherdamages <= 0 :
            self.damagesdealt = 0
        if self.damages <= 0 :
            self.damagestaken = 0
        if self.overheat > 199 :
            SFXDicoEvent['explosions']["Explosion"].play()
            self.projectiles.append(Surchauffe(self.rect[0],self.rect[1],self))
            self.overheat = 0
            self.damages += 20
            self.lag = 25
            self.vy = -50
        self.overheat = min(200,max(0,self.overheat))

        return False

    def animation_attack(self,attack,inputs,stage,other:Char):
        self.otherdamages = other.damages
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            if self.frame < 5 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame < 12 :
                self.vy -= self.fallspeed
            if self.frame == 12: # Hitbox frame 12-15
                self.active_hitboxes.append(Hitbox(-5,90,58,50,-pi/2,20*(self.overheat/200),12*(self.overheat/200),1/150,18*(self.overheat/200),3,self,False))
                self.can_act = False # ne peut pas agir après un grounded up B
                self.vy = -20 - 15*(self.overheat/150)
                self.attack = None
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts
                self.overheat = self.overheat-20

        if attack == "NeutralB":
            if self.frame < 5 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 10 :
                if self.overheat > 190 :
                    self.overheat -= 73
                    self.active_hitboxes.append(Hitbox(80,38,84,84,pi/4,18,22,1/180,21,2,self,boum=3))
                else :
                    self.active_hitboxes.append(Hitbox(64,54,52,52,pi/4,11,12,1/200,13,2,self,boum=2))


            if self.frame > 20: # 10 frames de lag
                self.attack = None

        if attack == "DownB":
            if self.frame < 5 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 20 :
                self.projectiles.append(Cerveau(self,other,stage))
            if self.frame > 40 : # 20 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.overheat > 50 and self.overheat < 199  and self.frame == 16:
                self.projectiles.append(Fireball(self.x,self.rect[1],self.overheat,self))
                self.overheat = 0
            if self.overheat < 50 and self.overheat > 10 and self.frame > 14 and self.frame < 18:
                self.projectiles.append(Smokeball(self.x,self.rect[1],self.frame,self))
                self.overheat = 11
            if self.frame > 19 and self.overheat > 10 :
                self.overheat = 0
            if self.frame > 24 : # 20 frames de lag
                self.attack = None

        if attack == "Jab":
            if self.frame == 4 :
                self.active_hitboxes.append(Hitbox(64,32,48,48,pi/2,1,0.5,0,5,2,self))
            if self.frame == 9 :
                if attack_button :
                    self.frame = 5
                self.active_hitboxes.append(Hitbox(64,32,48,48,pi/2,1,0.5,0,8,2,self))
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(64,32,64,64,pi/4,4,8,1/200,10,2,self,boum=1))

            if self.frame > 30: # 20 frames de lag
                self.attack = None

        if attack == "DownTilt":
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(50,100,64,32,pi/5,8,6.2,1/256,9,2,self,boum=5,deflect=True,modifier=0.5,sound="hits/hit"))

            if self.frame > 20: # 12 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame < 3 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 12 :
                self.active_hitboxes.append(Hitbox(50,50,84,32,pi/10,10,11.1,1/111,11,2,self,boum=5,deflect=True,modifier=1.01,sound="hits/other hit"))

            if self.frame > 40: # 25 frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(50,50,48,24,7*pi/11,14,4,1/256,14,2,self,boum=5,deflect=True,modifier=1.3,sound="hits/cool hit"))
            if self.frame == 11 :
                self.active_hitboxes.append(Hitbox(32,-42,24,24,pi/2,9,6,1/256,12,3,self,boum=3,deflect=True,modifier=0.1,sound="hits/other hit"))
            if self.frame > 11 and self.frame < 15 :
                if self.active_hitboxes :
                    self.active_hitboxes[-1].sizex += 24
                    if self.look_right :
                        self.active_hitboxes[-1].relativex -= 24
            if self.frame == 15 :
                self.active_hitboxes.append(Hitbox(change_left(50,72),50,48,24,4*pi/11,14,4,1/256,14,2,self,boum=5,deflect=True,modifier=1.3,sound="hits/cool hit"))
            if self.frame > 25: # 11 Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(42,42,64,24,3*pi/4,8,4,1/300,8,2,self,boum=1,sound="hits/cool hit"))
            if self.frame == 14 :
                self.active_hitboxes.append(Hitbox(0,-42,48,24,pi/5,14,12,1/200,12,2,self,boum=2,sound="hits/cool hit"))

            if self.frame > 25: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 21 and self.frame > 2 :
                    self.lag = 7 # Auto cancel frame 1-2 et 21+, 7 frames de landing lag

        if attack == "ForwardAir":
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(10,64,80,24,pi/3,5,5,1/256,17,2,self,boum=1))

            if self.frame > 20: # 12 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 16 and self.frame > 4 :
                    self.lag = 9 # Auto cancel frame 1-4 et 16+, 9 frames de landing lag

        if attack == "BackAir":

            if self.frame == 12 :
                self.active_hitboxes.append(Hitbox(-64,48,70,16,2*pi/3,18,12,1/256,17,2,self,boum=1,sound="lasers/cool lazer"))

            if self.frame > 30: # 18 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 26 and self.frame > 2 :
                    self.lag = 10 # Auto cancel frame 1-2 et 26+, 10 frames de landing lag

        if attack == "DownAir":
            if self.frame == 14 :
                self.active_hitboxes.append(Hitbox(-2,-2,72,12,-pi/3,12,9,1/200,11,8,self,sound="hits/hit"))
            if self.frame > 14 and self.active_hitboxes :
                self.active_hitboxes[-1].relativey += 30

            if self.frame > 30: # 16 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 26 and self.frame > 5 :
                    self.lag = 14 # Auto cancel frame 1-5 et 26+, 14 frames de landing lag

        if attack == "NeutralAir":
            if self.frame == 4 :
                SFXDicoEvent['hits']["punch2"].play()
                self.active_hitboxes.append(Hitbox(10,32,64,64,pi/5,2,8,0,8,2,self))
            if self.frame == 7 :
                SFXDicoEvent['hits']["punch2"].play()
                self.active_hitboxes.append(Hitbox(10,32,64,64,pi/3,12,12,1/200,14,2,self))
                self.damages += 0.1

            if self.frame > 20: # 12 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 15 and self.frame > 2 :
                    self.lag = 4 # Auto cancel frame 1-2 et 15+, 4 frames de landing lag

        if attack == "ForwardSmash":
            if self.frame > 4 and self.frame < 7 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 5
                self.animeframe -= 1
                self.charge = self.charge+1
            if self.frame == 24 :
                self.charge = min(self.charge,100)
                self.active_hitboxes.append(Hitbox(42,42,64,64,pi/4,24+5*(self.charge/100),24.2,1/256,23+5*(self.charge/100),3,self,boum=8,sound="hits/slap"))
            if self.frame > 55: # 30 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "UpSmash":

            if self.frame < 3 :
                if left : # peut reverse netre les frames 1 et 2
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 4 and self.frame < 8  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.animeframe -= 1
                self.frame = 5
                self.charge = self.charge+1
            if self.frame == 15 :
                self.vy = -14
                self.active_hitboxes.append(Hitbox(-2,-30,52,42,pi/2,22+2*(self.charge/100),20.4,1/256,19+8*(self.charge/100),10,self,boum=3,sound="hits/cool hit"))
            if self.frame > 15 :
                self.vy += 1

            if self.frame > 50: # 25 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownSmash":

            if self.frame < 3 :
                if left : # peut reverse entre les frames 1 et 2
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 20 and self.frame < 23 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 21
                self.animeframe -= 1
                self.charge = self.charge+1
            if self.frame == 30 :
                self.charge = min(self.charge,100)
                SFXDicoEvent['hits']["hitting metal"].play()
                self.active_hitboxes.append(Hitbox(10,-82,32,84,pi/9,18+8*(self.charge/100),22.2,1/256,24+9*(self.charge/100),6,self,boum=7,deflect=True,modifier=1.5))
            if self.frame > 30 and self.active_hitboxes:
                self.active_hitboxes[-1].relativex += 12*signe(self.direction)
                self.active_hitboxes[-1].relativey += 24+(self.frame-30)*7
                self.active_hitboxes[-1].sizey -= 10
                self.active_hitboxes[-1].sizex += 10
                if not self.look_right :
                    self.active_hitboxes[-1].relativex -= 10
            if self.frame > 70: # 40 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
            if self.frame < 26 :
                self.vy = 0
                if self.grounded :
                    self.vx += self.dashspeed*signe(self.direction)
                else :
                    self.vx -= self.dashspeed*signe(self.direction)
            if self.frame > 9 and self.frame%3 == 1 and self.frame < 23:
                self.active_hitboxes.append(Hitbox(-20,5,88,88,pi/10,abs(self.vx),2,1/1000,4,2,self))
            if self.frame == 25 :
                self.active_hitboxes.append(Hitbox(-20,5,88,88,pi/5,10,4,1/256,9,2,self,boum=1))
            if self.frame > 50: # 25 frames de lag
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

    def draw(self, window): # Dessine aussi la jauge de surchauffe

        super().draw(window)

        if self.player == 0 :
            x = 500
        else :
            x = 1030
        self.overheat = min(200,max(0,self.overheat))
        pygame.draw.rect(window,(self.overheat,100-self.overheat/2,200-self.overheat),(resize(x,0,width,height)[0]-1,resize(0,798,width,height)[1],resize(5,0,width,height)[0],resize(0,50,width,height)[1]))
        pygame.draw.rect(window,(0,0,0),(resize(x,0,width,height)[0]-1,resize(0,798,width,height)[1],resize(5,0,width,height)[0],resize(0,50-self.overheat/4,width,height)[1]))
        Texte(str(round(self.overheat))+"°C",("arial",resize(0,25,width,height)[1],False,False),(0,0,0),resize(x-50,0,width,height)[0],resize(0,800,width,height)[1]).draw(window)


###################          
""" Projectiles """
###################

class Fireball():
    def __init__(self,x,y,charge,own):
        self.id = 0
        self.charge = charge
        self.x = x-charge/4
        self.y = y-charge/4
        self.vx = signe(own.direction)*20
        self.damages_stacking=1/200
        if not own.look_right :
            self.angle = 5*pi/6
        else :
            self.angle = pi/6
        
        self.knockback = 2+16*(charge/200)
        self.damages = round(1+15*(charge/150),1)
        self.stun = 3+14*(charge/150)
        self.duration = 800
        self.rect = [0,0,0,0]

    def update(self):
        self.x = self.x + self.vx
        self.duration -= 1
    
    def deflect(self,modifier):
        self.vx = -self.vx*modifier
        self.damages = self.damages * modifier
        self.knockback = self.damages * modifier
        self.angle = pi-self.angle
        
    def draw(self,window):
        sprite = pygame.image.load(f"{rootDir()}/Images/Sprites/Projectiles/Fire/1.png")
        rect = sprite.get_rect(topleft=(self.x,self.y))
        sprite = pygame.transform.scale(sprite,resize(round(self.charge),round(self.charge),width,height))
        self.rect = [rect.x,rect.y,rect.w,rect.h]
        window.blit(sprite,resize(self.x+800,self.y+450,width,height))


class Smokeball():
    def __init__(self,x,y,i,own):
        self.id = 0
        self.x = x
        self.y = y
        self.vx = signe(own.direction)*20
        self.vy = (i-16)*5
        self.damages_stacking=1/200
        if not own.look_right :
            self.angle = 41*pi/42
        else :
            self.angle = pi/42
        
        self.knockback = 17
        self.damages = 0
        self.stun = 0
        self.duration = 20
        self.rect = [0,0,0,0]

    def update(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        self.duration -= 1
    
    def deflect(self,modifier):
        self.vx = -self.vx*modifier
        self.damages = self.damages * modifier
        self.knockback = self.damages * modifier
        self.angle = pi-self.angle
        
    def draw(self,window):
        sprite = pygame.transform.scale(pygame.image.load(f"{rootDir()}/Images/Sprites/Projectiles/Fire/0.png"),resize(30,30,width,height))
        self.rect = [self.x,self.y,30,30]
        window.blit(sprite,(self.x+width/2,self.y+height/2))

class Surchauffe():
    def __init__(self,x,y,own:Poissonnier):
        self.id = 0
        self.x = x-150+own.rect[2]/2
        self.y = y-150+own.rect[3]/2
        self.damages_stacking=1/180
        if not own.look_right :
            self.angle = 3*pi/4
        else :
            self.angle = pi/4
        self.knockback = 29
        self.damages = 42
        self.stun = 28
        self.duration = 16
        self.rect = [0,0,0,0]

    def deflect(self,modifier):
        self.damages = 0
        self.knockback = 0
        self.stun = 0

    def update(self):
        self.duration -= 1
        
    def draw(self,window):
        spritenumber = (self.duration-8)//2 if self.duration > 8 else (8-self.duration)//2
        sprite = pygame.transform.scale(pygame.image.load(f"{rootDir()}/Images/Sprites/Projectiles/Fire/{spritenumber}.png"),resize(300,300,width,height))
        self.rect = [self.x,self.y,300,300]
        window.blit(sprite,(self.x+width/2,self.y+height/2))

cerveau = pygame.image.load(f"{rootDir()}/Images/Sprites/Projectiles/Poissonnier/Cerveau.png")

class Cerveau():
    def __init__(self,own:Poissonnier,other:Char,stage) -> None:
        self.id = 0
        self.x = own.x
        self.y = own.rect[1]
        self.own = own
        self.other = other
        self.stage = stage
        self.vx = -8*signe(own.direction)
        self.vy = -9
        self.knockback = 0
        self.damages = 4
        self.stun = 0
        self.duration = 60
        self.damages_stacking = 0
        rect = cerveau.get_rect(bottomleft=(self.x,self.y))
        self.rect = [rect.x,rect.y,rect.w,rect.h]
    
    def touch_stage(self,stage,rect):
        if rect.colliderect(stage.mainplat.rect):
            return True
        for p in stage.plats:
            if rect.colliderect(p.rect) and rect.y + rect.h-4 < p.rect.y+self.vy+4:
                return True
        return False
    
    def update(self):
        self.duration -= 1
        self.y = self.y + self.vy
        self.x = self.x + self.vx
        rect = cerveau.get_rect(topleft=(self.x,self.y))
        if self.touch_stage(self.stage,rect):
            if self.y < self.stage.mainplat.y :
                self.vy = 0
                self.vx = 0
            else :
                self.vx = -self.vx
        else :
            self.vy += 1
        
        if rect.colliderect(pygame.Rect(self.other.rect)):
            if not (self.other.lag or self.other.hitstun) :
                self.other.combo = 0
                self.other.combodamages = 0
            self.other.vx = 2*signe(self.other.direction)
            self.other.vy = -4
            self.other.hitstun = 30
        self.rect = [rect.x,rect.y,rect.w,rect.h]
    
    def deflect(self):
        self.vx = -self.vx
        self.own,self.other = self.other,self.own

    def draw(self,window):
        sprite = pygame.transform.scale(cerveau,resize(cerveau.get_size()[0],cerveau.get_size()[1],width,height))
        window.blit(sprite, resize(self.x+800,self.y+450,width,height)) # on dessine le sprite
        

##### Autres skins
