from random import randint,choice
from DATA.utilities.Base_Char import Char, Hitbox, signe
import pygame
from math import pi,cos,sin,asin, sqrt
import DATA.utilities.Animations as Animations

def incertitude(x):
    return x + randint(round(-x/(2*sqrt(3)))*10,round(x/(2*sqrt(3)))*10)/10

##### Millet

class Millet(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=1, dashspeed=2, airspeed=1.3, deceleration=0.92, fallspeed=0.55, fastfallspeed=1.34, fullhop=14, shorthop=11,
                         doublejumpheight=14,airdodgespeed=8,airdodgetime=3,dodgeduration=15)

        self.rect = pygame.Rect(100,0,48,128) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/SE/jump.wav") # Son test
        self.name = "Millet"
        self.x = x
        self.rect.y = y
        self.player = player
        self.angle_rayon = -pi/300000
        self.rapidjab = False
        self.strongfair = False
    
    def __str__(self) -> str:
        return "Millet"

    def special(self,inputs):
        if self.attack is None :
            self.angle_rayon = -pi/300000
        if self.strongfair:
            self.superarmor = -1
        else :
            self.superarmor = 14
        return False

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
            if self.frame < 5 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
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
                self.active_hitboxes.append(Hitbox(32,32,64,64,pi/4,20,68.29,1/100,25,5,self,False))
            if self.frame > 120 : # 15 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame < 8 :
                if left : # peut reverse netre les frames 1 et 7
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame%4 == 1 and self.frame > 15 and self.frame < 58:
                self.projectiles.append(Fire(self.x+24*signe(self.direction)-48,self.rect.y+24,self))
            if self.frame > 84 : #  frames de lag
                self.attack = None

        if attack == "Jab":
            if attack_button and self.frame < 2 :
                self.rapidjab = True
            if self.frame > 10 and self.rapidjab:
                if self.look_right:
                    x = 24
                    angle = 0
                else :
                    x = -29
                    angle = pi
                self.projectiles.append(Sinusoide(self.x+x,self.rect.y+50+20*sin(self.frame/2),angle,self))
            if self.rapidjab and not attack_button :
                self.rapidjab = False
                self.frame = 0
            if not self.rapidjab :
                if self.frame == 3:
                    self.active_hitboxes.append(Hitbox(32,32,64,64,pi/4,10,incertitude(2.5),1/200,18,3,self,False))
                if self.frame > 20: # 14 frames de lag
                    self.attack = None

        if attack == "DownTilt":
            if self.frame == 16 :
                self.active_hitboxes.append(Hitbox(32,64,48,48,-2*pi/5,15,incertitude(6),1/200,18,3,self,False))
            if self.frame > 30: # 14 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame < 3 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 6 :
                self.active_hitboxes.append(Hitbox(48,64,32,32,pi/4,10,incertitude(8),1/250,25,3,self,False))
            if self.frame > 33: # 27 frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame == 8:
                self.vy = -6
                angle = pi/2
                self.active_hitboxes.append(Hitbox(-5,-25,58,58,angle,9,incertitude(10),1/300,20,3,self,False))
            if self.frame > 25: # 17 Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame < 25 :
                self.vy = 0
                self.vx *= 0.8
            if self.frame == 12: #12-15
                x = 24
                angle = 3*pi/5
                self.active_hitboxes.append(Hitbox(24,64,64,16,3*pi/5,10,incertitude(5),0,12,3,self,False))
                self.active_hitboxes.append(Hitbox(-40,64,64,16,2*pi/5,10,incertitude(5),0,12,3,self,False))
            if self.frame == 15: # 15-23
                self.active_hitboxes.append(Hitbox(8,-64,32,64,pi/2,12,incertitude(7),1/90,19,8,self,False))

            if self.frame > 45: # 22 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 30 and self.frame > 2 :
                    self.lag = 6 # Auto cancel frame 1-2 et 30+, 6 frames de landing lag

        if attack == "ForwardAir":
            if self.frame == 7 :
                if shield :
                    self.strongfair = True
                else :
                    self.strongfair = False
                    self.active_hitboxes.append(Hitbox(48,32,36,16,pi/4,12,9,1/200,13,3,self))
            if self.frame < 10 and self.active_hitboxes :
                self.active_hitboxes[-1].sizey += 16
            if self.frame == 45:
                self.active_hitboxes.append(Hitbox(48,45,16,16,pi/2,3,incertitude(2),1/3,1,3,self,False,boum=30))
            if self.frame > 69 or (self.frame > 40 and not self.strongfair): # 24 frames de lag
                self.attack = None
            
            # Pas d'auto cancel. Agit même après avoir atterri

        if attack == "BackAir":
            if self.frame == 10:
                self.active_hitboxes.append(Hitbox(-48,64,32,32,5*pi/6,8,incertitude(13),1/200,14,5,self,False))
            if self.frame > 25: # 15 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 and self.frame > 2 :
                    self.lag = 5 # Auto cancel frame 1-2 et 22+, 5 frames de landing lag

        if attack == "DownAir":
            self.vx = 0
            if self.frame < 14 :
                self.vy = 0
            self.vy *= 1.1
            if self.frame == 17 :
                self.active_hitboxes.append(Hitbox(-26,64,100,48,-pi/2,15,incertitude(10),1/200,25,4096,self,False))
            if self.frame == 19 :
                if self.active_hitboxes :
                    self.active_hitboxes[-1].knockback = 4
                    self.active_hitboxes[-1].damages = incertitude(6)
                    self.active_hitboxes[-1].damages_stacking = 1/500
                    self.active_hitboxes[-1].hitstun = 7
                    self.active_hitboxes[-1].angle = 0 if self.look_right else pi

            if self.grounded :
                if self.active_hitboxes :
                    self.active_hitboxes = list()
                self.attack = None
                self.lag = 10 # Ne se termine que lorsqu'il touche le sol

        if attack == "NeutralAir":
            if self.frame == 9 :
                self.active_hitboxes.append(Hitbox(48,48,32,32,0,0,incertitude(6),0,20,3,self,False))
            if self.frame == 14 :
                self.active_hitboxes.append(Hitbox(48,48,48,48,2*pi/5,12,incertitude(10),1/250,18,3,self,False))

            if self.frame > 40: # 26 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 28 and self.frame > 3 :
                    self.lag = 11 # Auto cancel frame 1-3 et 28+, 12 frames de landing lag

        if attack == "ForwardSmash":
            if self.frame > 3 and self.frame < 6 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 4
                self.charge = self.charge+1

            elif self.frame == 22 : # Active on 22-27
                self.vx = 20*signe(self.direction)
                self.charge = min(self.charge,100)
                self.active_hitboxes.append(Hitbox(48,16,64,64,pi/4,19+12*(self.charge/200),incertitude(20),1/250,22+18*(self.charge/100),5,self,True))
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
                self.active_hitboxes.append(Hitbox(-50,-16,64,64,pi/4,13+10*(self.charge/200),13,1/90,15+8*(self.charge/100),5,self,False))

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
                self.active_hitboxes.append(Hitbox(30,60,60,32,pi/6,12+7*(self.charge/200),incertitude(13),1/250,13+8*(self.charge/50),6,self,False))
            

            if self.frame > 35: # 19 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
            if self.frame == 9 :
                self.active_hitboxes.append(Hitbox(0,32,64,48,pi/5,9,incertitude(9),1/250,8,15,self,False))
            if self.frame == 24 :
                self.active_hitboxes.append(Hitbox(48,32,48,48,-2*pi/5,12,incertitude(12),1/150,15,2,self,False))
            if self.frame < 21 :
                self.vy = 0
                if self.grounded :
                    self.vx += self.dashspeed*signe(self.direction)/2
                else :
                    self.vx -= self.dashspeed*signe(self.direction)/2

            if self.frame > 55: # 27 frames de lag
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
    def __init__(self,stage,x,y,angle_fwd,own:Millet) -> None:
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
        self.damages = incertitude(0.2)
        self.stun = 5
        self.duration = 10
        #self.g = -6.74/4
        nextx = self.x + cos(self.angle_fwd)*self.v
        nexty = self.y + sin(self.angle_fwd)*self.v #+ self.g
        #self.g += 0.0981
        self.x = nextx
        self.y = nexty

    def update(self):
        if pygame.Rect(self.x,self.y,5,5).colliderect(self.stage.mainplat.rect):
            #self.g = -self.g*2
            if self.rect.y < self.stage.mainplat.rect.y+10 :
                self.angle_fwd = -self.angle_fwd
            else :
                self.angle_fwd = pi-self.angle_fwd


        nextx = self.x + cos(self.angle_fwd)*self.v
        nexty = self.y + sin(self.angle_fwd)*self.v #+ self.g
        #self.g += 0.0981
        self.x = nextx
        self.y = nexty
        self.rect = pygame.Rect(self.x,self.y,5,5)
        if self.x < -800 or self.x > 800:
            self.duration = 0

    def draw(self,window):
        pygame.draw.rect(window,(250,0,0),(self.x+800,self.y+450,10,10))
        
    def deflect(self,modifier):
        self.v *= -modifier


firesprite = [pygame.image.load(f"./DATA/Images/Sprites/Projectiles/Fire/{i}.png") for i in range(6)]
for i in range(len(firesprite)):
    firesprite[i] = pygame.transform.scale(firesprite[i],(3*firesprite[i].get_size()[0],3*firesprite[i].get_size()[1]))

class Fire():
    def __init__(self,x,y,own:Millet) -> None:
        self.size = 2
        self.x = x
        self.y = y
        self.vx = 15*signe(own.direction)
        self.vy = randint(-10,10)/10
        self.duration = 11
        self.knockback = 2
        self.damages = incertitude(0.8)
        self.stun = 7
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
    
    def deflect(self,modifier):
        self.vx = -self.vx
        self.damages *= modifier
        self.angle = -self.angle

class Sinusoide():
    def __init__(self,x,y,angle,own:Millet) -> None:
        self.rect = pygame.Rect(x,y,5,5)
        self.angle = angle
        self.v = 5*signe(own.direction)
        self.duration = 15
        self.knockback = 0.5
        self.damages = incertitude(0.05)
        self.stun = 3
        self.damages_stacking = 1/550
    
    def update(self):
        self.rect.x += self.v
        self.duration -= 1
    
    def draw(self,window):
        pygame.draw.rect(window,(20,130,100),(self.rect.x+800,self.rect.y+450,self.rect.w,self.rect.h))

    def deflect(self,modifier):
        self.duration = 0

class Quantique():
    def __init__(self,x,y,own:Millet) -> None:
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