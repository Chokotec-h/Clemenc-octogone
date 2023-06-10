from DATA.utilities.Base_Char import Char, Hitbox, signe, SFXDicoEvent
import pygame
from math import pi, cos, sin, atan, degrees
from DATA.utilities.functions import *
from DATA.utilities.build import rootDir

##### Copier

class LeBerre(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=1.2, dashspeed=2.4, airspeed=1.2, deceleration=0.9, fallspeed=0.8, fastfallspeed=1.3, fullhop=15, shorthop=11,
                         doublejumpheight=16,airdodgespeed=6,airdodgetime=3,dodgeduration=15)

        self.rect = [100,0,48,120] # Crée le rectangle de perso

        self.name = "Le Berre"
        self.x = x
        self.rect[1] = y
        self.player = player

        self.oldx = self.x
        self.oldy = self.rect[1] - 1
    
    def __str__(self) -> str:
        return "Le Berre"

    def special(self,inputs): 
        if self.attack == "ForwardSmash" :
            self.deceleration = 0.95
        else :
            self.deceleration = 0.9

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            if self.frame == 11: # Saute frame 11
                self.can_act = False # ne peut pas agir après un grounded up B
                self.vy = -28
                self.attack = None
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts
                self.projectiles.append(Explosion(self.x,self.rect[1]+120,9,10,-pi/2,9,1/200,40))

        if attack == "NeutralB":
            if self.frame < 5 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if 18 >= self.frame >= 10 :
                self.projectiles.append(Rayon(stage,self.x,self.rect[1]+60,0,self))
            if self.frame > 28: # 10 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownB":
            if self.frame == 8 :
                self.projectiles.append(Tornade(self.x+20*signe(self.direction),self.rect[1],self,other))
            if self.frame > 20 : # 15 frames de lag
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
                self.projectiles.append(Eprouvette(self,other,v,stage))
                SFXDicoEvent['wooshs']["mini woosh"].play()
            if self.frame > 30 : # 15 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "Jab":
            if self.frame == 8:
                self.animeframe = 0
            if attack_button and self.frame < 2:
                self.rapidjab = True
            if self.frame > 10 and self.rapidjab:
                if self.look_right:
                    x = 24
                    angle = 3 * pi / 4
                else:
                    x = -29
                    angle = pi / 4
                self.projectiles.append(Sinusoide(self.x + x, self.rect[1] + 50 + 20 * (1 if cos(self.frame/2) > 0 else -1), angle, self))
            if self.rapidjab and not attack_button:
                self.rapidjab = False
                self.frame = 0
            if not self.rapidjab:
                if self.frame == 3:
                    self.active_hitboxes.append(
                        Hitbox(32, 32, 64, 64, pi / 4, 10, 2.5, 1 / 200, 8, 3, self, False))
                if self.frame > 30:  # 24 frames de lag
                    self.attack = None

        if attack == "DownTilt":
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(48,10,12,110,pi/4,12,0.8,1/200,8,2,self,deflect=True,modifier=2.5))
            if self.frame == 11 and attack_button :
                self.frame = 9
            if self.frame > 20: # 7 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame < 3 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True

            if self.frame == 9 :
                self.active_hitboxes.append(Hitbox(24,70,10,24,pi/8,11,7.5,1/200,9,8,self))
            if self.frame > 9 and self.active_hitboxes :
                self.active_hitboxes[0].sizex += 10
                if not self.look_right :
                    self.active_hitboxes[0].relativex -= 10

            if self.frame > 25: # 8 frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame > 6 and self.frame < 15 :
                self.active_hitboxes.append(Hitbox(24-self.frame,-8*(self.frame-10),2*self.frame,2*self.frame,pi/2,2,1,0,3,2,self))
            if self.frame > 25: # 11 Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame == 9 :
                self.active_hitboxes.append(Hitbox(12,0,24,10,3*pi/8,8,8,1/200,12,10,self))
            if self.frame > 9 and self.active_hitboxes :
                self.active_hitboxes[0].sizey += 10
                self.active_hitboxes[0].relativey -= 10

            if self.frame > 27: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 15 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 15+

        if attack == "ForwardAir":

            if self.frame == 9 :
                self.active_hitboxes.append(Hitbox(24,70,10,24,pi/25,16,8,1/200,19,20,self))
            if self.frame > 9 and self.active_hitboxes :
                self.active_hitboxes[0].sizex += 8
                if not self.look_right :
                    self.active_hitboxes[0].relativex -= 10
            if self.frame > 50: # 29 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 40 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 40+

        if attack == "BackAir":

            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(-24,70,10,24,5*pi/6,11,8,1/200,13,6,self))
            if self.frame > 9 and self.active_hitboxes :
                self.active_hitboxes[0].sizex += 10
                if self.look_right :
                    self.active_hitboxes[0].relativex -= 10

            if self.frame > 25: # 14 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 20+

        if attack == "DownAir":
            if self.frame == 12 :
                self.active_hitboxes.append(Hitbox(-16,120,24,24,pi/4,6,5,0,9,3,self))
            if self.frame == 18 :
                self.active_hitboxes.append(Hitbox(2,110,24,24,-pi/2,9,6,1/200,11,3,self))

            if self.frame > 30: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 25 :
                    self.lag = self.frame-5 # Auto cancel frame 1-5 et 20+

        if attack == "NeutralAir":
            if self.frame == 4 :
                self.active_hitboxes.append(Hitbox(2,60,44,44,pi/2,8,12,1/100,15,15,self))
            if self.frame == 6 and self.active_hitboxes:
                self.active_hitboxes[0].damages = 4
                self.active_hitboxes[0].stun = 8
                self.active_hitboxes[0].damage_stacking = 1/250
                self.active_hitboxes[0].knockback = 5

            if self.frame > 30: # 17 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 25 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 30+

        if attack == "ForwardSmash":
            if self.frame == 1 :
                self.oldx = self.x
                self.oldy = self.rect[1] - 5
            if self.frame > 6 and self.frame < 9 and smash and self.charge < 200 and not (self.rect[1] > 1000 or self.rect[1] < -1000 or self.x < -1000 or self.x > 1000): # Chargement jusqu'à 200 frames
                self.frame = 7
                self.animeframe -= 1
                self.charge = self.charge+1
            if self.frame == 15 :
                self.active_hitboxes.append(Hitbox(24,60,45,45,pi/7,15+8*self.charge/100,15,1/200,16+8*self.charge/100,6,self,sound="hits/punch1"))

            if self.frame > 45: # 30 frames de lag
                self.attack = None
                self.charge = 0
                self.x = self.oldx
                self.rect[1] = self.oldy
                self.vx = 0
                self.vy = 0

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
                self.active_hitboxes.append(Hitbox(-30,-50,108,108,pi/2,22+2*self.charge/100,23.5,1/300,20+10*self.charge/100,10,self))

            if self.frame > 60: # 30 frames de lag
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
                self.active_hitboxes.append(Hitbox(20,56,8,8,0,5,0.2,0,2,2,self,position_relative=True))
            if self.frame == 18 :
                SFXDicoEvent['explosions']["Explosion"].play()
                self.active_hitboxes.append(Hitbox(-20,40,88,88,pi/4,20+2*self.charge/100,28.5,1/250,19+10*self.charge/100,4,self,position_relative=True))
                self.damages += 10

            if self.frame > 40: # 23 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
            if 5 < self.frame < 26 :
                self.active_hitboxes.append(Hitbox(2,100,50,20,pi/4,2,0.4,0,8,2,self))
            if self.frame < 26 :
                self.vy = 0
                if self.grounded :
                    self.vx = self.dashspeed*signe(self.direction)
                else :
                    self.vx -= self.dashspeed*signe(self.direction)
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

class Rayon():
    def __init__(self,stage,x,y,angle_fwd,own:LeBerre) -> None:
        self.id = 0
        self.sound = 'lasers/cool lazer'
        self.stage = stage
        self.x = x
        self.y = y
        self.angle_fwd = angle_fwd
        self.v = 20*signe(own.direction)
        self.rect = [x-resize(20,0,width,height)[0],y-resize(0,20,width,height)[1],resize(6,0,width,height)[0],resize(0,22,width,height)[1]]
        self.damages_stacking=1/300
        if own.look_right :
            self.angle = pi/4
        else :
            self.angle = 3*pi/4
        self.knockback = 3
        self.damages = 0.2
        self.stun = 5
        self.duration = 10
        #self.g = -6.74/4
        nextx = self.x + cos(self.angle_fwd)*self.v
        nexty = self.y + sin(self.angle_fwd)*self.v
        #self.g += 0.0981
        self.x = nextx
        self.y = nexty
    
    def touch_stage(self,stage,rect):
        if rect.colliderect(stage.mainplat.rect):
            return True
        for p in stage.plats:
            if rect.colliderect(p.rect) and rect.y + rect.h-4 < p.rect.y+self.v+4:
                return True
        return False

    def update(self):
        rect = pygame.Rect(self.rect)
        if self.touch_stage(self.stage,pygame.Rect(self.x,self.y,5,5)):
            #self.g = -self.g*2
            if rect.y < self.stage.mainplat.rect.y+10 :
                self.angle_fwd = -self.angle_fwd
            else :
                self.angle_fwd = pi-self.angle_fwd


        nextx = self.x + cos(self.angle_fwd)*self.v
        nexty = self.y + sin(self.angle_fwd)*self.v
        #self.g += 0.0981
        self.x = nextx
        self.y = nexty
        self.rect = [self.x,self.y,5,5]
        if self.x < -2000 or self.x > 2000:
            self.duration = 0

    def draw(self,window):
        pygame.draw.rect(window,(250,0,0),list(resize(self.x+800,self.y+450,width,height)) + list(resize(10,10,width,height)))
        
    def deflect(self,modifier):
        self.v *= -modifier

class Sinusoide():
    def __init__(self, x, y, angle, own: LeBerre) -> None:
        self.id = 0
        self.sound = 'hits/hit'
        self.rect = [x, y, 5, 5]
        self.angle = angle
        self.v = 5 * signe(own.direction)
        self.duration = 15
        self.knockback = 0.5
        self.damages = 0.05
        self.stun = 3
        self.damages_stacking = 1 / 550

    def update(self):
        self.rect[0] += self.v
        self.duration -= 1

    def draw(self, window):
        pygame.draw.rect(window, (220, 200, 120), (resize(self.rect[0] + 800,0,width,height)[0], resize(0,self.rect[1] + 450,width,height)[1], self.rect[2], self.rect[3]))

    def deflect(self, modifier):
        self.duration = 0


eprouvette = pygame.image.load(f"{rootDir()}/Images/Sprites/Projectiles/LeBerre/Eprouvette.png")
eprouvette = pygame.transform.scale(eprouvette,resize(round(eprouvette.get_width()*1.5),round(eprouvette.get_height()*1.5),width,height))

class Eprouvette():
    def __init__(self,own:LeBerre,other,speed,stage) -> None:
        self.id = 0
        self.vx = (20+speed)*signe(own.direction)
        self.vy = speed
        self.basevy = self.vy
        self.x = own.x
        self.y = own.rect[1] + 48
        self.own = own
        self.other = other
        self.duration = 80
        self.stage = stage
        self.rect = [0,0,0,0]
        self.rotate = 0
        self.angle = 0
        self.damages = 1.3
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
        rect = eprouvette.get_rect(topleft=(self.x,self.y))
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.8
        if self.touch_stage(self.stage,rect):
            self.duration = 0
        self.duration -= 1
        if self.duration < 1 or rect.colliderect(pygame.Rect(self.other.rect)) :
            self.duration = 0
            self.own.projectiles.append(Explosion(self.x,self.y,12,11,pi/4,9,1/150,64))
        self.rect = [rect.x,rect.y,rect.w,rect.h]
        
    def deflect(self,modifier):
        self.vx = -self.vx*modifier
        self.vy = -10
        self.own,self.other = self.other,self.own    

    def draw(self,window):
        self.rotate += self.vx
        sprite = pygame.transform.rotate(eprouvette,degrees(self.rotate))
        window.blit(sprite, resize(self.x+800,self.y+450,width,height)) # on dessine le sprite

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
        self.duration = 10

    def deflect(self,modifier):
        self.damages = 0
        self.knockback = 0
        self.stun = 0

    def update(self):
        self.duration -= 1
        
    def draw(self,window):
        spritenumber = (self.duration-6) if self.duration > 6 else (6-self.duration)
        self.rect = [self.x,self.y,self.size,self.size]
        sprite = pygame.transform.scale(pygame.image.load(f"{rootDir()}/Images/Sprites/Projectiles/Fire/{spritenumber}.png"),resize(self.size,self.size,width,height))
        window.blit(sprite,resize(self.x+800,self.y+450,width,height))


tornado = pygame.image.load(f"{rootDir()}/Images/Sprites/Projectiles/LeBerre/Tornade.png")
tornado = pygame.transform.scale(tornado,(round(tornado.get_width()*2),round(tornado.get_height()*2)))


class Tornade():
    def __init__(self, x, y, own: LeBerre, other) -> None:
        self.id = 0
        self.sound = 'wooshs/mini woosh'
        self.rect = [x, y,5, 5]
        self.own = own
        self.other = other
        self.angle = pi/2
        self.v = 5 * signe(own.direction)
        self.duration = 60
        self.knockback = 5
        self.damages = 0
        self.stun = 6
        self.damages_stacking = 0
        self.x = x
        self.y = y

    def update(self):
        if self in self.other.immune_to_projectiles :
            self.other.immune_to_projectiles.pop(self.other.immune_to_projectiles.index(self))
        self.x += self.v
        rect = tornado.get_rect(topleft=(self.x,self.y))
        self.rect = [rect.x,rect.y,rect.w,rect.h]
        self.duration -= 1

    def draw(self, window):
        window.blit(pygame.transform.scale(tornado,resize(round(tornado.get_width()),round(tornado.get_height()),width,height)),
                    resize(self.x+800,self.y+450,width,height))

    def deflect(self, modifier):
        self.v *= -modifier


##### Autres skins

