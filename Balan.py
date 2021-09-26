from Base_Char import Char, Hitbox, signe
import pygame
from math import pi

exposant_sprite = [pygame.image.load(f"DATA/Images/Sprites/Exposants/{i}.png") for i in range(5)]

##### M Balan

class Balan(Char):
    def __init__(self) -> None:
        super().__init__(speed=2, dashspeed=3, airspeed=0.9, deceleration=0.7, fallspeed=0.5, fastfallspeed=1, fullhop=13, shorthop=10,
                         doublejumpheight=15)

        self.rect = pygame.Rect(100,0,10,10) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav") # Son test
        self.name = "Balan"


    def act(self, inputs,stage,other): # Spécial à Balan, pour son upB
        self.last_hit = max(self.last_hit-1,0)
        self.get_inputs(inputs,stage,other)
        self.move(stage)
        for i,hitbox in enumerate(self.active_hitboxes) :
            hitbox.update()
            if hitbox.duration <= 0:
                del self.active_hitboxes[i]
        for i,projectile in enumerate(self.projectiles) :
            self.projectiles[i].update()
            if projectile.duration <= 0:
                del self.projectiles[i]
        self.damages = min(999,self.damages)
        if self.upB: # Vitesse de merde après upB
            self.vx *= 0.3
        if self.hitstun: # Arrête la charge du neutral B et des smashs en hitstun
            self.charge = 0

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            if self.frame == 11: # Saute frame 11
                self.sprite_frame = 0
                self.can_act = False # ne peut pas agir après un grounded up B
                self.vy = -20
                self.attack = None
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts
            elif self.frame > 6 : # Sort frame 7
                self.rect.move_ip(0,-6)
                self.sprite_frame = 1
            if self.frame < 6 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 6: # Hitbox frame 6-11
                if not self.look_right :
                    angle = pi/3
                else:
                    angle = 2*pi/3
                self.active_hitboxes.append(Hitbox(-1.5,88.5,51,48,angle,18,32,1/150,40,5,self,False))

        if attack == "NeutralB":
            #self.can_act = False
            if self.frame < 5 and special : # Chargement jusqu'à 100 frames
                self.frame = 0
                self.animeframe -= 1
                self.charge = min(100,self.charge+1)
                if left : # peut changer de direction
                    self.look_right = False
                if right :
                    self.look_right = True
            elif self.frame == 5 : # 5 frames après relache
                    for i in range(0,(self.charge-1)//20+1):
                        self.projectiles.append(Projo_Craie(i,self,stage))
            if self.frame > 15: # 10 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownB":
            if self.frame < 5 and special: # Chargement jusqu'à 200 frames
                self.frame = 0
                self.animeframe -= 1
                self.charge = min(199,self.charge+1)
                if left : # peut changer de direction
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 5 : # 5 frames après relache
                self.active_hitboxes.append(Hitbox(40*signe(self.direction),32,32,64,0,0,0,0,0,20,self))
                self.active_hitboxes[-1].update()
                if self.active_hitboxes[-1].hit.colliderect(other.rect):
                    self.projectiles.append(Exposant(other,self,self.charge//40))
            if self.frame > 20 : # 15 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame < 8 :
                if left : # peut reverse netre les frames 1 et 7
                    self.look_right = False
                if right :                    
                    self.look_right = True
            if self.frame == 8 :
                if not self.look_right:
                    angle = 3*pi/4
                else:
                    angle = pi/4
                self.active_hitboxes.append(Hitbox(16,30,32,32,angle,30,10,0,12,3,self,False))
            if self.frame == 10 : # Active on 10-70
                if not self.look_right:
                    angle = 3*pi/4
                else:
                    angle = pi/4
                self.active_hitboxes.append(Hitbox(8,82,32,10,angle,3,4,1/250,3,60,self,False))
            if self.frame > 9 and self.frame < 71: # Déplacement
                self.vx = 15*signe(self.direction)/(self.frame/10)
                self.vy = 1
            if self.frame > 95 : # 25 frames de lag
                self.attack = None

        if attack == "Jab":
            if self.frame == 5 : # 1er hit frame 5-10
                if not self.look_right:
                    angle = pi/4
                else:
                    angle = 3*pi/4
                self.active_hitboxes.append(Hitbox(40*signe(self.direction)+12,64,24,10,angle,2,0.6,0,5,5,self))
            if self.frame == 10 : # 2e hit frame 10-15
                if not self.look_right:
                    angle = 3*pi/4
                else:
                    angle = pi/4
                self.active_hitboxes.append(Hitbox(40*signe(self.direction)+19,52,10,24,angle,4.5,1.4,1/1000,8,5,self,False))

            if self.frame > 22: # 7 frames de lag
                self.attack = None

        if attack == "DownTilt":
            if self.frame == 8 : # Frame 8-13
                if not self.look_right:
                    angle = 3*pi/5
                else:
                    angle = 2*pi/5
                self.active_hitboxes.append(Hitbox(35*signe(self.direction)+11,80,24,10,angle,8,3.8,1/200,10,5,self,False))

            if self.frame > 20: # 7 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame == 6 : # 1er hit frame 6-12
                angle = pi/2
                self.active_hitboxes.append(Hitbox(40*signe(self.direction)+12,58,24,24,angle,2,0.6,0,5,6,self))
            if self.frame == 14 : # 2e hit frame 14-22
                if not self.look_right:
                    angle = 3*pi/4
                else:
                    angle = pi/4
                self.active_hitboxes.append(Hitbox(40*signe(self.direction)+12,58,24,24,angle,6,8,1/150,12,6,self,False))

            if self.frame > 30: # 8 frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame == 6 : # Frame 6-14
                angle = pi/2
                self.active_hitboxes.append(Hitbox(-20*signe(self.direction)+12,8,16,16,angle,9,8.2,1/250,10,8,self,False))
            # Dessin du cercle
            if self.active_hitboxes :
                if self.frame < 9 : # Frames 7-8
                    self.active_hitboxes[-1].y -= 8
                    self.active_hitboxes[-1].sizey += 8
                    self.active_hitboxes[-1].sizex += 8*signe(self.direction)
                if self.frame < 11 : # Frames 9-10
                    self.active_hitboxes[-1].sizex += 8*signe(self.direction)
                if self.frame < 13 : # Frames 11-12
                    self.active_hitboxes[-1].sizey += 8
            if self.frame > 25: # 11 Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame == 5 : # Frame 5-10
                angle = pi/2
                self.active_hitboxes.append(Hitbox(-1,-10,50,10,angle,0,2.5,1/1000,4,5,self))
            if self.frame == 10 : # Frame 10-15
                if not self.look_right:
                    angle = 4*pi/6
                else:
                    angle = 2*pi/6
                self.active_hitboxes.append(Hitbox(15,-20,16,25,angle,10,5,1/80,18,5,self))

            if self.frame > 25: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 15 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 15+

        if attack == "ForwardAir":
            if self.frame == 15 : # Frame 15-16
                if not self.look_right:
                    angle = -3*pi/4
                else:
                    angle = -pi/4
                self.active_hitboxes.append(Hitbox(40*signe(self.direction)+12,32,16,32,angle,10,14,1/150,18,6,self,False))
            if self.frame == 17 : # Frame 17-21
                if not self.look_right:
                    angle = 4*pi/6
                else:
                    angle = 2*pi/6
                if self.active_hitboxes : # late hitbox
                    self.active_hitboxes[-1].angle = angle
                    self.active_hitboxes[-1].knockback = 3
                    self.active_hitboxes[-1].damages = 10
                    self.active_hitboxes[-1].damage_stacking = 1/250
                    self.active_hitboxes[-1].stun = 10


            if self.frame > 50: # 29 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 40 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 40+

        if attack == "BackAir":
            if self.frame == 6 : # Frame 6-8
                if not self.look_right:
                    angle = 0
                else:
                    angle = pi
                self.active_hitboxes.append(Hitbox(-40*signe(self.direction)+12,32,16,16,angle,10,12,1/150,15,6,self,False))
            if self.frame == 9 : # Frame 9-11
                if not self.look_right:
                    angle = 0
                else:
                    angle = pi
                if self.active_hitboxes : # Late hitbox
                    self.active_hitboxes[-1].angle = angle
                    self.active_hitboxes[-1].knockback = 3
                    self.active_hitboxes[-1].damages = 8
                    self.active_hitboxes[-1].damage_stacking = 1/250
                    self.active_hitboxes[-1].stun = 10

            if self.frame > 25: # 14 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 20+

        if attack == "DownAir":
            if self.frame == 10 : # Frame 10
                if not self.look_right:
                    angle = -pi/3
                else:
                    angle = -2*pi/3
                self.active_hitboxes.append(Hitbox(16,90,24,32,angle,2,12,1/20,5,5,self,False))
            if self.frame == 11 : # Frame 11-15
                if not self.look_right:
                    angle = 4*pi/6
                else:
                    angle = 2*pi/6
                if self.active_hitboxes : # late hitbox
                    self.active_hitboxes[-1].angle = angle
                    self.active_hitboxes[-1].knockback = 3
                    self.active_hitboxes[-1].damages = 7
                    self.active_hitboxes[-1].damage_stacking = 1/1000
                    self.active_hitboxes[-1].stun = 10

            if self.frame > 25: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-5 # Auto cancel frame 1-5 et 20+

        if attack == "NeutralAir":
            if self.frame == 3 : # Frame 3-6
                if not self.look_right:
                    angle = 0
                else:
                    angle = pi
                self.active_hitboxes.append(Hitbox(-32+12,16,64+8+8,64,angle,10,2,0,8,20,self))
                self.active_hitboxes.append(Hitbox(8,16,32,64,pi/2,12,8,1/200,10,20,self,False))
            if self.frame == 7 : # Frame 7-23
                if self.active_hitboxes : # late hitbox
                    if self.active_hitboxes[-1].angle == pi/2:
                        self.active_hitboxes[-1].knockback = 3
                        self.active_hitboxes[-1].damages = 3
                        self.active_hitboxes[-1].damage_stacking = 1/250
                        self.active_hitboxes[-1].stun = 6

            if self.frame > 40: # 17 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 30 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 30+

        if attack == "ForwardSmash":
            if self.frame < 5 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 6 and self.frame < 9 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 7
                self.animeframe -= 1
                self.charge = self.charge+1
            elif self.frame == 12 : # Active on 12-18
                self.charge = min(self.charge,100)
                if not self.look_right :
                    angle = 3*pi/4
                else :
                    angle = pi/4
                self.active_hitboxes.append(Hitbox(60*signe(self.direction)+12,16,52,64,angle,12*(self.charge/200+1),14,1/50,8*(self.charge/100+3),4,self,True,True,2))
            if self.frame > 45: # 30 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "UpSmash":

            if self.active_hitboxes: # Moving hitbox
                self.active_hitboxes[-1].relativex -= 20*signe(self.direction)
                if self.frame > 11 :
                    if self.look_right : # Reverse angle
                        self.active_hitboxes[-1].angle = 2*pi/6
                    else :
                        self.active_hitboxes[-1].angle = 4*pi/6
                    self.active_hitboxes[-1].relativey -= 3
                else :
                    self.active_hitboxes[-1].relativey += 3

            if self.frame < 5 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 5 and self.frame < 8  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.animeframe -= 1
                self.frame = 6
                self.charge = self.charge+1
            elif self.frame == 10 : # Active on 10-15
                self.charge = min(self.charge,100)
                if not self.look_right :
                    angle = 2*pi/6
                else :
                    angle = 4*pi/6
                self.active_hitboxes.append(Hitbox(30*signe(self.direction)+12,-10,32,32,angle,10*(self.charge/200+1),13,1/250,6*(self.charge/10+1),6,self,False))

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
                
            if self.frame < 21 and self.frame%5 == 0 and self.frame > 4: # active on 5/10/15/20
                if not self.look_right :
                    angle = 11*pi/12
                else :
                    angle = pi/12
                self.active_hitboxes.append(Hitbox(40*signe(self.direction)+12,32,32,32,angle,abs(self.vx),1.5,0,5,2,self,False))
            if self.frame == 26: # active on 26
                if not self.look_right :
                    angle = 3*pi/4
                else :
                    angle = pi/4
                self.active_hitboxes.append(Hitbox(40*signe(self.direction)+12,32,64,64,angle,9,3.5,1/250,10,3,self,False))
            if self.frame > 50: # 24 frames de lag
                self.attack = None

        if attack == "Taunt":
            if self.frame > 30: # Durée de 30 frames
                self.attack = None

###################          
""" Projectiles """
###################

class Projo_Craie():
    def __init__(self,id,own,stage):
        # Craies de M Balan
        self.id = id+1
        self.sprite = pygame.image.load("./DATA/Images/Sprites/Craies/Craie_"+["blanche","rouge","bleue","verte","jaune"][id]+".png")
        self.rect = self.sprite.get_rect()
        self.x = own.rect.x
        self.y = own.rect.y + own.rect.h//2
        self.vx = 10*signe(own.direction)
        self.vy = -3*(self.id)
        self.duration = 5
        self.stage = stage
        self.damages_stacking=0
        if not own.look_right :
            self.angle = 3*pi/4
        else :
            self.angle = pi/4
        self.knockback = 3
        self.damages = 1.2
        self.stun = 4

    def update(self):
        if self.rect.colliderect(self.stage.rect) :
            self.sprite = pygame.image.load("./DATA/Images/Sprites/Craies/Explosion_"+["blanche","rouge","bleue","verte","jaune"][self.id-1]+".png")
            self.y -= 3
            self.duration -= 1
            self.vx = 0
            self.vy = 0
            self.damages = 2.5
            self.stun = 12
            self.knockback = 5
        self.x += round(self.vx)
        self.y += self.vy
        self.vy += 0.3
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
        self.rect.w *= 3 # Rescale
        self.rect.h *= 3 # Rescale
        if self.y > 800 :
            self.duration = 0

    def deflect(self,modifier):
        self.vy = -(self.id)
        self.vx = -self.vx*modifier
        self.damages = self.damages * modifier
        self.knockback = self.damages * modifier
        self.angle = pi-self.angle

    def draw(self,window):
        window.blit(self.sprite, (self.x+800,self.y+450)) # on dessine le sprite

class Exposant():
    def __init__(self,opponent,own,charge) -> None:
        self.opponent = opponent
        self.charge = charge + 1
        self.duration = (charge+1)*120
        self.own = own
        self.rect = pygame.Rect(-1000,1000,0,0)
    
    def update(self):
        if self.opponent.rect.y > 750 or  self.opponent.rect.y < -750 or  self.opponent.rect.x > 750 or  self.opponent.rect.x < -750:
            self.duration = 0
            self.charge = 0
        if self.duration == 1 :
            self.own.active_hitboxes.append(Hitbox(20,20,20,20,-pi/2,5*self.charge,10*self.charge,1/250,8*self.charge,5,self.opponent,False))
        self.duration -= 1

    def draw(self,window):
        self.x = self.opponent.rect.x+self.opponent.rect.w
        self.y = self.opponent.rect.y-30
        window.blit(exposant_sprite[self.duration//120],(self.x+800,self.y+450))

##### Autres skins

class Balan2(Balan):
    def __init__(self) -> None:
        super().__init__()
        
