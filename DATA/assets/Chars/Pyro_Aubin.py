from DATA.utilities.Animations import get_sprite
from DATA.utilities.Base_Char import Char, Hitbox, signe
import pygame
from math import atan, degrees, floor, pi, sqrt, sin, cos

from DATA.utilities.Interface import Texte


##### Aubin

class Pyro_Aubin(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=2, dashspeed=3, airspeed=1.2, deceleration=0.8, fallspeed=0.6, fastfallspeed=1.2, fullhop=13, shorthop=10,
                         doublejumpheight=15,airdodgespeed=6,airdodgetime=3,dodgeduration=15)

        self.rect = pygame.Rect(100,0,48,120) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/SE/jump.wav") # Son test
        self.name = "Pyro-Aubin"
        self.konamiadd = False
        self.x = x
        self.rect.y = y
        self.konami = []
        self.player = player
        self.explosifs = 25
        self.angle_fusee = 0
    
    def __str__(self) -> str:
        return "Pyro-Aubin"

    def special(self): 
        if self.konami == ["Up","Up","Down","Down","Left","Right","Left","Right","B","A"]:
            self.inputattack("Superspecial")
        self.explosifs = min(self.explosifs+0.5/60,50)

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            if self.frame == 2 :
                self.angle_fusee = pi/2
            if self.angle_fusee > -1 and self.frame > 5: # Saute frame 11
                if special :
                    self.frame -= 1
                    if self. explosifs > 0.08 :
                        self.explosifs -= 0.08
                    else :
                        self.frame = 20
                    if left :
                        self.angle_fusee += 0.05
                        if self.angle_fusee < 0 :
                            self.angle_fusee = 2*pi
                    if right :
                        self.angle_fusee -= 0.05
                        if self.angle_fusee > 2*pi :
                            self.angle_fusee = 0
                self.vx = cos(self.angle_fusee) * 10
                self.vy = -sin(self.angle_fusee) * 10
            if self.frame > 18 :
                self.can_act = False # ne peut pas agir après un grounded up B
                self.attack = None
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts

        if attack == "NeutralB":
            if self.frame < 5 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.konami == ["Up","Up","Down","Down","Left","Right","Left","Right"] and not self.konamiadd:
                self.konamiadd = True
                print("B")
                self.konami.append("B")
            #elif not self.konamiadd :
            #    self.konami = []
            if self.frame == 5 :
                launch = False
                for p in self.projectiles :
                    if isinstance(p,Fusee) and not p.done:
                        launch = True
                if launch :
                    for p in self.projectiles:
                        if isinstance(p,Fusee) and not p.done and self.explosifs > 4.5 and not p.homing :
                            self.explosifs -= 4.5
                            p.homing = True
                elif self.explosifs > 0.5:
                    self.explosifs -= 0.5
                    self.projectiles.append(Fusee(stage,self,other))

            if self.frame > 15: # 10 frames de lag
                self.attack = None
                self.konamiadd = False
                self.charge = 0

        if attack == "DownB":
            if self.frame > 20 : # 15 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame > 80 : # 20 frames de lag
                self.attack = None

        if attack == "Jab":
            if self.konami == ["Up","Up","Down","Down","Left","Right","Left","Right","B"] and not self.konamiadd:
                self.konamiadd = True
                print("A")
                self.konami.append("A")
                self.attack = None
            #elif not self.konamiadd :
            #    self.konami = []

            if self.frame > 22: # 10 frames de lag
                self.attack = None

        if attack == "DownTilt":
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(48,80,48,48,-pi/3,10,6,1/200,8,15,self))
            if self.frame > 8 and self.active_hitboxes:
                self.active_hitboxes[-1].relativey += self.frame

            if self.frame > 33: # 10 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame < 3 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True

            if self.frame > 30: # 8 frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame > 25: # 11 Frames de lag
                self.attack = None

        if attack == "UpAir":

            if self.frame > 25: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 15 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 15+

        if attack == "ForwardAir":

            if self.frame > 50: # 29 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 40 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 40+

        if attack == "BackAir":

            if self.frame > 25: # 14 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 20+

        if attack == "DownAir":

            if self.frame > 25: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-5 # Auto cancel frame 1-5 et 20+

        if attack == "NeutralAir":
            if self.konami == ["Up","Up","Down","Down","Left","Right","Left","Right","B"] and not self.konamiadd:
                self.konamiadd = True
                print("A")
                self.konami.append("A")
                self.attack = None
            #elif not self.konamiadd :
            #    self.konami = []

            if self.frame > 40: # 17 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 30 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 30+

        if attack == "ForwardSmash":
            if self.frame > 6 and self.frame < 9 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 7
                self.animeframe -= 1
                self.charge = self.charge+1
            if self.frame == 40 :
                self.charge = min(100,self.charge,self.explosifs*12)
                if self.explosifs > 5:
                    self.explosifs -= max(self.charge/12,3)
                    self.projectiles.append(Boulet(self.charge,stage,self))
                self.vx = -signe(self.direction)*self.charge*0.5
                self.active_hitboxes.append(Hitbox(-10,0,24,120,5*pi/6,8,3,1/200,8,self.charge/10,self))
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
            if self.frame > 50: # 24 frames de lag
                self.attack = None
        
        if attack == "UpTaunt":
            if (self.konami == [] or self.konami == ["Up"]) and not self.konamiadd:
                print("Up")
                self.konamiadd = True
                self.konami.append("Up")
                self.attack = None
            #elif not self.konamiadd :
            #    self.konami = []
            
            if self.frame > 30: # Durée de 30 frames
                self.attack = None
                self.konamiadd = False

        if attack == "DownTaunt":
            if (self.konami == ["Up","Up"] or self.konami == ["Up","Up","Down"]) and not self.konamiadd:
                self.konamiadd = True
                print("Down")
                self.konami.append("Down")
            #elif not self.konamiadd :
            #    self.konami = []
            
            if self.frame > 30: # Durée de 30 frames
                self.attack = None
                self.konamiadd = False

        if attack == "LeftTaunt":
            if (self.konami == ["Up","Up","Down","Down"] or self.konami == ["Up","Up","Down","Down","Left","Right"]) and not self.konamiadd:
                self.konamiadd = True
                print("Left")
                self.konami.append("Left")
            #elif not self.konamiadd :
            #    self.konami = []
            
            if self.frame > 30: # Durée de 30 frames
                self.attack = None
                self.konamiadd = False

        if attack == "RightTaunt":
            if (self.konami == ["Up","Up","Down","Down","Left"] or self.konami == ["Up","Up","Down","Down","Left","Right","Left"]) and not self.konamiadd:
                self.konamiadd = True
                print("Right")
                self.konami.append("Right")
            #elif not self.konamiadd :
            #    self.konami = []
            
            if self.frame > 30: # Durée de 30 frames
                self.attack = None
                self.konamiadd = False

        if (not (D_Up or D_Down or D_Left or D_Right) and self.attack in ("RightTaunt","LeftTaunt","UpTaunt","DownTaunt")
            or (self.attack == "NeutralB" and attack_button)):
                self.frame = 150

        if attack == "Superspecial":
            if self.frame == 8 :
                if self.explosifs > 49.5 :
                    self.explosifs = 0
                    print("boum")
                    self.konami = []
                    self.konamiadd = False
                    self.active_hitboxes.append(Hitbox(-140,-100,328,320,pi/4,35,120,1/100,40,10,self,True))
                else :
                    self.konami = []
                    self.konamiadd = False
                    self.active_hitboxes.append(Hitbox(-40,-4,128,128,pi/4,2,2,0,2,2,self,True))
            if self.frame > 30: # Durée de 30 frames
                self.attack = None

    def draw(self, window): # Dessine aussi les inputs du konami code et la jauge d'explosifs
            drawing_sprite,size,self.animeframe = get_sprite(self.animation,self.name,self.animeframe,self.look_right)

            drawing_sprite = pygame.transform.scale(drawing_sprite,(round(drawing_sprite.get_size()[0]*4),round(drawing_sprite.get_size()[1]*4))) # Rescale
            size = [size[0]*4,size[1]*4,size[2]*4,size[3]*4] # Rescale
            pos = [self.x + 800 - size[2]/2, self.rect.y-size[3]+self.rect.h + 449] # Position réelle du sprite
            window.blit(drawing_sprite, pos,size) # on dessine le sprite
            #self.rect.y -=  size[3] - self.rect.h # Reste à la surface du stage

            for p in self.projectiles :
                p.draw(window)

            for i,s in enumerate(self.smoke_dash):
                        s.draw(window)
                        if s.life_time < 0:
                            del self.smoke_dash[i]
            
            for i,s in enumerate(self.double_jump):
                        s.draw(window)
                        if s.life_time < 0:
                            del self.double_jump[i]
            if self.player == 0 :
                x = 533
            else :
                x = 1066
            
            for i,key in enumerate(self.konami) :
                window.blit(pygame.image.load(f"./DATA/Images/Sprites/Misc/Konami_Code/{key}.png"),(i*20+x,800))
            pygame.draw.rect(window,(0,0,0),(x,770,100,20))
            pygame.draw.rect(window,(100,100,0),(x,770,self.explosifs*2,20))
            Texte(str(floor(self.explosifs))+"/50",("Arial",12,True,False),(200,200,200),x+50,780).draw(window)
###################          
""" Projectiles """
###################

boulet = pygame.image.load("./DATA/Images/Sprites/Projectiles/Boulet.png")

class Boulet():
    def __init__(self,charge,stage,own:Pyro_Aubin) -> None:
        self.x = own.x + 48*signe(own.direction)
        self.y = own.rect.y + 48
        self.charge = charge
        self.vx = (10+charge)*signe(own.direction)*0.2
        self.vy = -5-charge*0.1
        self.damages = 28
        self.stun = 19+8*(self.charge/100)
        self.knockback = sqrt(abs(self.vy)+abs(self.vx))/2
        self.damages_stacking = 1/200
        if not own.look_right :
            self.angle = 3*pi/4
        else :
            self.angle = pi/4
        self.rect = pygame.Rect((0,0,0,0))
        self.stage = stage
        self.duration = 80

    def update(self):
        self.knockback = (abs(self.vy)+abs(self.vx))/2
        self.x += self.vx
        self.y += self.vy
        self.rect = boulet.get_rect(topleft=(self.x,self.y))
        if self.rect.colliderect(self.stage.mainplat.rect) :
            self.vy = -1
            self.vx *= 0.9
        else :
            self.vy += 3
        self.duration -= 1

    def deflect(self,modifier):
        self.vx = -self.vx*modifier
        self.damages = self.damages * modifier
        self.angle = pi-self.angle

    def draw(self,window):
        window.blit(boulet, (self.x+800,self.y+450)) # on dessine le sprite

fusee = pygame.image.load("./DATA/Images/Sprites/Projectiles/Fusee.png")

class Fusee():
    def __init__(self,stage,own:Pyro_Aubin,other:Char) -> None:
        self.x = own.x + signe(own.direction)*48
        self.y = own.rect.y + 86
        self.vx = 0.5*signe(own.direction)
        self.vy = -10
        self.damages = 5
        self.stun = 12
        self.knockback = 12
        self.damages_stacking = 1/200
        self.angle = pi/2
        self.rect = pygame.Rect((0,0,0,0))
        self.stage = stage
        self.duration = 20
        self.frame = 1
        self.homing = False
        self.other = other
        self.done = False
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.frame += 1
        if not self.done :
            if not self.homing :
                self.vy += 0.005*self.frame
            else :
                dx = (self.x - self.other.x)
                dy = (self.y - self.other.rect.y)
                angle = atan(dy/dx)
                self.vx = -abs(cos(angle))*5*signe(dx) - 0.005*self.frame*signe(dx)
                self.vy = -abs(sin(angle))*5*signe(dy) - 0.005*self.frame*signe(dy)
                self.duration -= 0.01
        else:
            self.frame += 1
            self.vy += 0.005*self.frame
        if self.rect.colliderect(self.stage.mainplat.rect) or abs(self.y) > 1000 or abs(self.x) > 1000:
            self.done = True
            self.vy = 0
            self.duration -= 1
        if self.rect.colliderect(self.other.rect):
            self.done = True
            self.frame = 0
            self.homing = False
    
    def draw(self,window):
        if self.vy == 0 :
            self.vx = 0.000001
        if self.vx < 0 :
            sprite = pygame.transform.rotate(fusee,degrees(pi-atan(self.vy/self.vx)))
        else :
            sprite = pygame.transform.rotate(fusee,degrees(pi-atan(self.vy/self.vx))+180)
        self.rect = sprite.get_rect(topleft=(self.x,self.y))
        if self.rect.colliderect(self.stage.mainplat.rect):
            sprite = fusee
        window.blit(sprite, (self.x+800,self.y+450)) # on dessine le sprite

    def deflect(self,modifier):
        self.vx = -self.vx*modifier
        self.vy = -self.vy*modifier
        self.damages = self.damages * modifier
        self.angle = pi-self.angle
        self.homing = False
        self.done = True
        self.frame = 0


##### Autres skins
