from random import randint,choice
from DATA.utilities.Base_Char import Char, Hitbox, signe
import pygame
from math import pi,cos,sin,asin, sqrt
import DATA.utilities.Animations as Animations

def incertitude(x):
    return x + randint(round(-x/(2*sqrt(3)))*10,round(x/(2*sqrt(3)))*10)/10

##### Perso

class Gregoire(Char):
    def __init__(self) -> None:
        super().__init__(speed=1.8, dashspeed=3, airspeed=1.3, deceleration=0.75, fallspeed=0.6, fastfallspeed=1.4, fullhop=13, shorthop=10,
                         doublejumpheight=13,airdodgespeed=6,airdodgetime=3,dodgeduration=15)

        self.rect = pygame.Rect(100,0,48,128) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav") # Son test
        self.name = "Gregoire"
        self.angle_rayon = -pi/300000
        self.rapidjab = False

    def special(self):
        if self.attack is None :
            self.angle_rayon = -pi/300000

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up

        if attack == "UpB":
            if self.frame < 12 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 12 :
                self.projectiles.append(Quantique(self.x,self.rect.y,self))
            if self.frame > 12 and self.frame < 25: # Saute frame 12
                self.can_act = False # ne peut pas agir après un grounded up B
                self.vx = (right-left)*20
                self.vy = (down-up)*20
                self.airdodge = True
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts
            if self.frame > 35:
                self.airdodge = False
                self.vy = 0
                self.vx = 0
            if self.frame > 45: # 10 frames de lag
                self.attack = None
            if self.grounded :
                self.lag += 1

        if attack == "NeutralB":
            if self.frame < 25 :
                if up :
                    self.angle_rayon = pi/4
                if down :
                    self.angle_rayon = -pi/6
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 25 and self.frame < 45:
                self.vy = 0
                self.projectiles.append(Rayon(stage,self.x,self.rect.y+24,-self.angle_rayon*signe(self.direction),self)) # l'angle est chelou parce que j'ai géré la vitesse du rayon de façon merdique  # Mais on s'en fout ça marche
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
                self.active_hitboxes.append(Hitbox(32,32,64,64,pi/4,20,68.29,1/100,9,5,self,False))
            if self.frame > 120 : # 15 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame < 8 :
                if left : # peut reverse netre les frames 1 et 7
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 23 and self.frame < 48:
                self.projectiles.append(Thunder(self.x+24*signe(self.direction)-48,self.rect.y+24,self)) 
            if self.frame == 47 :
                self.active_hitboxes.append(Hitbox(32,32,32,64,pi/4,12,incertitude(7),1/150,15,3,self,False))
            if self.frame > 48 and self.frame < 90 :
                if self.active_hitboxes :
                    self.active_hitboxes[-1].duration += 1
                    self.active_hitboxes[-1].relativex += 32*signe(self.direction)
            if self.frame > 92 : # 44 frames de lag
                self.attack = None

        if attack == "Jab":
            if attack_button and self.frame < 2 :
                self.rapidjab = True
            if self.frame > 10 and self.rapidjab:
                if self.look_right:
                    x = 24
                    angle = 3*pi/4
                else :
                    x = -29
                    angle = pi/4
                self.projectiles.append(Sinusoide(self.x+x,self.rect.y+50+20*cos(self.frame/2),angle,self))
            if self.rapidjab and not attack_button :
                self.rapidjab = False
                self.frame = 0
            if not self.rapidjab :
                if self.frame == 3:
                    self.active_hitboxes.append(Hitbox(32,32,64,64,pi/4,10,incertitude(2.5),1/200,8,3,self,False))
                if self.frame > 30: # 24 frames de lag
                    self.attack = None

        if attack == "DownTilt":
            if self.frame == 16 :
                self.active_hitboxes.append(Hitbox(32,64,48,48,-2*pi/5,15,incertitude(9),1/200,13,3,self,False))
            if self.frame > 35: # 19 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame == 10 :
                self.active_hitboxes.append(Hitbox(48,52,32,32,pi/4,12,incertitude(8),1/225,10,3,self,False))
            if self.frame > 33: # 27 frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame == 8:
                self.vy = -6
                angle = pi/2
                self.active_hitboxes.append(Hitbox(-5,-48,58,58,angle,10,incertitude(10),1/300,13,3,self,False))
            if self.frame > 25: #  Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame < 25 :
                self.vy = 0
                self.vx *= 0.8
            if self.frame == 12: #12-15
                x = 24
                angle = 3*pi/5
                self.active_hitboxes.append(Hitbox(24,64,64,16,3*pi/5,10,incertitude(5),0,8,3,self,False))
                self.active_hitboxes.append(Hitbox(-40,64,64,16,2*pi/5,10,incertitude(5),0,8,3,self,False))
            if self.frame == 15: # 15-23
                self.active_hitboxes.append(Hitbox(8,-64,32,64,pi/2,12,incertitude(7),1/90,12,8,self,False))

            if self.frame > 45: # 22 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 40 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 15+

        if attack == "ForwardAir":
            if self.frame == 45:
                self.active_hitboxes.append(Hitbox(48,45,16,16,pi/2,3,95.45,1/1000,25,3,self))
            if self.frame == 46 :
                if not self.active_hitboxes:
                    self.BOUM = 30
                else :
                    self.active_hitboxes.pop()
            if self.frame > 69: # 24 frames de lag
                self.attack = None
            
            # Pas d'auto cancel. Agit même après avoir atterri

        if attack == "BackAir":
            if self.frame == 13:
                self.active_hitboxes.append(Hitbox(-48,64,32,32,pi/6,13,incertitude(13),1/200,14,5,self,False))
            if self.frame > 27: #  frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 20+

        if attack == "DownAir":
            self.vx = min(self.frame/10,15)*signe(self.direction)
            if self.frame < 14 :
                self.vy = 0
            self.vy *= 1.1
            if self.frame == 17 :
                self.active_hitboxes.append(Hitbox(0,0,48,128,-pi/2,15,incertitude(10),1/200,15,4096,self))
            if self.frame > 19 :
                if self.active_hitboxes :
                    self.active_hitboxes[-1].knockback = 8
                    self.active_hitboxes[-1].damages = incertitude(7)
                    self.active_hitboxes[-1].damages_stacking = 1/500
                    self.active_hitboxes[-1].hitstun = 5
                    if self.frame %2 == 0 :
                        self.active_hitboxes[-1].angle = 0 if self.look_right else pi
                    else :
                        self.active_hitboxes[-1].angle = pi if self.look_right else 0

            if self.grounded :
                if self.active_hitboxes :
                    self.active_hitboxes = list()
                self.attack = None
                self.lag = 10 # Ne se termine que lorsqu'il touche le sol

        if attack == "NeutralAir":
            if self.frame == 12 :
                self.active_hitboxes.append(Hitbox(48,48,32,32,0,0,incertitude(6),0,20,3,self))
            if self.frame == 18 :
                self.active_hitboxes.append(Hitbox(48,48,48,48,2*pi/5,20,incertitude(10),1/250,12,3,self,False))

            if self.frame > 40: # 26 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 30 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 30+

        if attack == "ForwardSmash":
            if self.frame > 3 and self.frame < 6 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 4
                self.charge = self.charge+1

            elif self.frame == 24 : # Active on 24-27
                self.vx = 10*signe(self.direction)
                self.charge = min(self.charge,100)
                self.active_hitboxes.append(Hitbox(48,16,48,48,pi/4,22+12*(self.charge/200),incertitude(20),1/250,9+8*(self.charge/100),5,self))
            elif self.frame == 24: # Late hitbox
                if self.active_hitboxes :
                    self.active_hitboxes[-1].knockback *= 0.5
            if self.frame > 69: # 42 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "UpSmash":

            if self.active_hitboxes: # Moving hitbox
                self.active_hitboxes[-1].relativex -= 20*signe(self.direction)
                if self.frame == 12 :
                    self.active_hitboxes[-1].relativey += 10
                if self.frame == 13:
                    self.active_hitboxes[-1].relativey -= 10
                if self.frame < 14 :
                    if self.look_right :
                        self.active_hitboxes[-1].relativex += 50
                    
                    else :
                        self.active_hitboxes[-1].relativex -= 50

            if self.frame < 5 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 4 and self.frame < 8  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 5
                self.charge = self.charge+1

            elif self.frame == 11 : # Active on 11-13
                self.charge = min(self.charge,100)
                self.active_hitboxes.append(Hitbox(-50,-16,64,64,pi/4,13+10*(self.charge/200),13,1/90,10+7*(self.charge/100),5,self,False))

            if self.frame > 57: # 44 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownSmash":

            if self.frame < 2 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 4 and self.frame < 6  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 4
                self.charge = self.charge+1
            elif self.frame == 10 : # Active on 10-16
                self.charge = min(self.charge,100)
                self.active_hitboxes.append(Hitbox(30,60,60,32,pi/5,12+7*(self.charge/200),incertitude(13),1/250,9+5*(self.charge/150),6,self,False))
            

            if self.frame > 35: # 19 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
            if self.frame == 9 :
                self.active_hitboxes.append(Hitbox(0,32,64,48,pi/5,9,incertitude(9),1/250,8,15,self))
            if self.frame == 24 :
                self.active_hitboxes.append(Hitbox(48,32,48,48,-2*pi/5,12,incertitude(12),1/150,12,2,self))
            if self.frame < 21 :
                self.vy = 0
                if self.grounded :
                    self.vx += self.dashspeed*signe(self.direction)/2
                else :
                    self.vx -= self.dashspeed*signe(self.direction)/2

            if self.frame > 55: # 27 frames de lag
                self.attack = None

        if attack == "Taunt":
            if self.frame > 30: # Durée de 30 frames
                self.attack = None

###################          
""" Projectiles """
###################

class Rayon():
    def __init__(self,stage,x,y,angle_fwd,own) -> None:
        self.stage = stage
        self.x = x
        self.y = y
        self.angle_fwd = angle_fwd
        self.v = 9*signe(own.direction)
        self.rect = pygame.Rect(x-20,y-20,25,25)
        self.damages_stacking=1/300
        if own.look_right :
            self.angle = pi/4
        else :
            self.angle = 3*pi/4
        self.knockback = 3
        self.damages = incertitude(2)
        self.stun = 4
        self.duration = 10
        self.g = -6.74/4
        nextx = self.x + cos(self.angle_fwd)*self.v
        nexty = self.y + sin(self.angle_fwd)*self.v + self.g
        self.g += 0.0981
        self.x = nextx
        self.y = nexty

    def update(self):
        nexty = self.y + sin(self.angle_fwd)*self.v + self.g
        if pygame.Rect(self.x,nexty,5,5).colliderect(self.stage.rect):
            self.g = -self.g*0.8
            if self.rect.y < self.stage.rect.y-self.g+abs(self.v)+5 :
                self.angle_fwd = -self.angle_fwd
            else :
                self.angle_fwd = pi-self.angle_fwd


        nextx = self.x + cos(self.angle_fwd)*self.v
        self.g += 0.981
        self.x = nextx
        self.y = nexty
        self.rect = pygame.Rect(self.x,self.y,5,5)
        if self.x < -800 or self.x > 800:
            self.duration = 0

    def draw(self,window):
        pygame.draw.rect(window,(250,0,0),(self.x+800,self.y+450,10,10))
        
    def deflect(self,modifier):
        self.v *= -modifier


thundersprite = pygame.transform.scale(pygame.image.load(f"./DATA/Images/Sprites/Projectiles/Thunder.png"),(64,64))

class Thunder():
    def __init__(self,x,y,own) -> None:
        self.size = 2
        self.x = x
        self.y = y
        self.vx = 32*signe(own.direction)
        self.duration = 50
        self.knockback = 1
        self.damages = incertitude(2.4)
        self.stun = 12
        self.damages_stacking = 0
        if own.look_right :
            self.angle = pi/4
        else :
            self.angle = 3*pi/4
        self.rect = pygame.Rect(x,y,2,2)
        if not own.look_right :
            self.x += 32
    
    def update(self):
        self.rect = thundersprite.get_rect(topleft=(self.x,self.y))
        self.x += self.vx
        self.duration -= 1

    def draw(self,window):
        window.blit(thundersprite,(self.x+800,self.y+450))
    
    def deflect(self,modifier):
        self.vx = -self.vx
        self.damages *= modifier
        self.angle = -self.angle

class Sinusoide():
    def __init__(self,x,y,angle,own) -> None:
        self.rect = pygame.Rect(x,y,5,5)
        self.angle = angle
        self.v = 5*signe(own.direction)
        self.duration = 15
        self.knockback = 0.5
        self.damages = incertitude(0.5)
        self.stun = 3
        self.damages_stacking = 1/550
    
    def update(self):
        self.rect.x += self.v
        self.duration -= 1
    
    def draw(self,window):
        pygame.draw.rect(window,(220,200,120),(self.rect.x+800,self.rect.y+450,self.rect.w,self.rect.h))

    def deflect(self,modifier):
        self.duration = 0

class Quantique():
    def __init__(self,x,y,own) -> None:
        self.rect = pygame.Rect(own.rect.x,own.rect.y,own.rect.w,own.rect.h)
        self.x = x
        self.y = y
        self.own = own
        self.animeframe = self.own.animeframe
        self.duration = 60
        self.angle = pi/2
        self.knockback = 7
        self.damages = incertitude(3)
        self.stun = 15
        self.damages_stacking = 1/250
        self.vy = 0
        self.g = False
    
    def update(self):
        self.duration -= 1
        if self.g :
            self.vy += 1
        self.y += self.vy
    
    def deflect(self,modifier):
        self.vy = modifier*10
        self.g = True

    def draw(self, window):
        drawing_sprite,size,self.animeframe = Animations.get_sprite(self.own.animation,self.own.name,self.animeframe+1,self.own.look_right)

        drawing_sprite = pygame.transform.scale(drawing_sprite,(round(drawing_sprite.get_size()[0]*4),round(drawing_sprite.get_size()[1]*4))) # Rescale
        size = [size[0]*4,size[1]*4,size[2]*4,size[3]*4] # Rescale
        pos = [self.x + 800 - size[2]/2, self.y-size[3]+self.rect.h + 449] # Position réelle du sprite
        window.blit(drawing_sprite, pos,size)