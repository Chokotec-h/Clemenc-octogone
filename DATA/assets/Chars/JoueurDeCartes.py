from DATA.utilities.Base_Char import Char, Hitbox, change_left, signe
import pygame
from math import pi, cos, sin
from random import randint

##### Perso

class Air_President(Char):
    def __init__(self,x,y) -> None:
        super().__init__(speed=1.9, dashspeed=3.6, airspeed=1.4, deceleration=0.6, fallspeed=0.5, fastfallspeed=1.6, fullhop=15, shorthop=12,
                         doublejumpheight=18,airdodgespeed=5,airdodgetime=3,dodgeduration=15)

        self.rect = pygame.Rect(100,0,48,120) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav") # Son test
        self.name = "Joueur de air-president"
        self.x = x
        self.rect.y = y
        self.mao = False
        self.mao_used = False
        self.basefallspeed = 0.8
        self.stylo = ["Bleu","Violet","Vert","Noir"]
        self.currentstylo = 0
    
    def __str__(self) -> str:
        return "Joueur de air-president"

    def special(self): # Spécial
        return False

    def animation_attack(self,attack,inputs,stage,other):
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
                self.active_hitboxes.append(Hitbox(-1.5,88,51,48,-pi/2,2,6,1/150,3,8,self,False))
            if self.frame > 6 and self.active_hitboxes :
                self.active_hitboxes[-1].sizey -= self.vy

        if attack == "NeutralB":
            if self.frame == 18 :
                self.active_hitboxes.append(Hitbox(24,-32,256,256,0,0,0,0,0,6,self))
            if self.frame > 18 and self.frame < 22:
                if self.active_hitboxes and self.active_hitboxes[-1].hit.colliderect(other.rect):
                    if other.grounded :
                        other.can_act = True
                        other.inputattack("Jab")
                    else :
                        other.can_act = True
                        other.inputattack("NeutralAir")
                    self.active_hitboxes.pop()
            if self.frame > 25: # 3 frames de lag
                self.attack = None

        if attack == "DownB":
            if self.frame == 5 :
                self.mao = True
                self.mao_used = False
            if self.frame > 28 :
                if self.mao and not self.mao_used :
                    self.damages += 20
                self.mao = False
            if self.frame > 45 : # 18 frames de lag
                self.attack = None

        if attack == "SideB":
            if self.frame < 8 :
                if left : # peut reverse netre les frames 1 et 7
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 9 :
                if randint(1,208) == 1:
                    self.rect.y = 10000
                else :
                    if not self.look_right:
                        angle = 3*pi/4
                        x = change_left(64,48)
                    else:
                        angle = pi/4
                        x = 24
                    self.active_hitboxes.append(Hitbox(24,20,68,48,0,0,0,0,0,8,self))
                    self.active_hitboxes[-1].update()
                    if self.active_hitboxes[-1].hit.colliderect(other.rect):
                        if randint(1,208) == 1:
                            other.rect.y = 10000
                            self.projectiles.append(Carte(x,20,pi/42,"R",self))
                            self.BOUM = 30
                        else :
                            self.projectiles.append(Carte(x,20,angle,randint(1,13),self))

            if self.frame > 30 : # 21 frames de lag
                self.attack = None

        if attack == "Jab":
            if self.frame == 2 : # Frame 2-3
                self.active_hitboxes.append(Hitbox(32,20,44,48,3*pi/4,0.7,0.3,1/1000,3,2,self,False))
            if self.frame > 5: #  2 frames de lag
                self.attack = None

        if attack == "DownTilt":
            if self.frame == 5 : # Frames 5-10
                self.active_hitboxes.append(Hitbox(24,64,64,64,pi/3,3,1.2,1/750,9,2,self,False))
            if self.frame > 15: # 5 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
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
                self.active_hitboxes.append(Hitbox(24,0,32,32,pi/2,9,8.5,1/500,13,11,self,False))
            if self.frame > 25: # 17 Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame == 5 : #frames 5-11
                self.active_hitboxes.append(Hitbox(-8,-20,12,30,pi/4,5,4,1/300,12,7,self,True))
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
                if self.frame < 24 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 24+

        if attack == "ForwardAir":
            if self.frame == 9 : # Frame 9-10
                self.active_hitboxes.append(Hitbox(24,28,64,12,pi/6,12,11.3,1/150,16,2,self,False))
            if self.frame > 14  and self.frame < 21: # Fame 15-20
                self.active_hitboxes.append(Hitbox(24,28,64,12,pi/42,2,0.5,1/404,3,2,self,False))
            if self.frame > 45: # 25 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 25 :
                    self.lag = self.frame # Auto cancel frame 25+

        if attack == "BackAir":
            if self.frame == 10: # Active on 10-12
                self.active_hitboxes.append(Hitbox(-48,32,48,52,3,9,9.5,1/250,15,3,self,False))
            if self.frame > 25: # 13 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 20+

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
                self.active_hitboxes.append(Hitbox(-8,128,64,64,-pi/2,5,6.5,1/200,20,2,self,False))
            if self.frame > 55: # 17 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 45 :
                    self.lag = self.frame-4 # Auto cancel frame 1-4 et 45+

        if attack == "NeutralAir":
            if self.frame == 9:
                self.projectiles.append(Stylo(self.stylo[self.currentstylo],self,stage))
                self.currentstylo = (self.currentstylo+1)%4
            if self.frame > 24: # 15 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 20+

        if attack == "ForwardSmash":
            if self.frame > 6 and self.frame < 9 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 7
                self.charge = self.charge+1

            elif self.frame == 19 : # Active on 19-24
                self.charge = min(self.charge,100)
                self.active_hitboxes.append(Hitbox(-26,0,52,52,pi/3,15+12.5*(self.charge/250),17,1/250,20+9*(self.charge/150),5,self,False))
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
                self.active_hitboxes.append(Hitbox(0,-50,48,48,pi/3,9+7*(self.charge/150),14,1/80,13+7*(self.charge/100),13,self,False))

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
                self.active_hitboxes.append(Hitbox(-10,100,100,32,5*pi/13,12+10*(self.charge/200),10.5,1/250,12+8*(self.charge/300+1),8,self,False))

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
                self.active_hitboxes.append(Hitbox(10,32,64,64,pi/5,8,3.5,1/350,7,3,self,False))

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


    def collide(self,other):
        self.parrying = False
        for i,hitbox in enumerate(other.active_hitboxes): # Détection des hitboxes
            if self.rect.colliderect(hitbox.hit):
                if (not self.parry) and (not self.intangibility) and not (self.mao): # Parry and counter
                    self.tumble = True
                    if hitbox.position_relative : # Reverse hit
                        if self.x > hitbox.hit.x+hitbox.hit.w//2 and hitbox.own.direction < 0:
                            hitbox.angle = pi - hitbox.angle
                        if self.x < hitbox.hit.x-hitbox.hit.w//2 and hitbox.own.direction > 0:
                            hitbox.angle = pi - hitbox.angle
                        
                    self.vx = hitbox.knockback*cos(hitbox.angle)*(self.damages*hitbox.damages_stacking+1) # éjection x
                    self.vy = -hitbox.knockback*sin(hitbox.angle)*(self.damages*hitbox.damages_stacking+1) # éjection y
                    self.hitstun = hitbox.stun*(self.damages*hitbox.damages_stacking/2+1) # hitstun
                    self.damages += hitbox.damages # dommages
                    self.rect.y -= 1
                    self.attack = None # cancel l'attacue en cours
                else :
                    if self.parry :
                        self.parrying = True
                    if self.mao :
                        self.damages = max(0,self.damages - hitbox.damages) # heal
                        self.mao_used = True
                del other.active_hitboxes[i] # Supprime la hitbox
                return
        for i,projectile in enumerate(other.projectiles): # Détection des projectiles
            for h in self.active_hitboxes :
                if h.deflect and h.hit.colliderect(projectile.rect):
                    projectile.deflect(h.modifier)
                    self.projectiles.append(projectile)
                    del other.projectiles[i] # Supprime la hitbox
                    return

            if self.rect.colliderect(projectile.rect) and not self.last_hit:
                self.last_hit = 10 # invincibilité aux projectiles de 10 frames
                if (not self.parry) and (not self.intangibility) and (not self.mao) : # Parry
                    self.tumble = True
                    self.vx = projectile.knockback*cos(projectile.angle)*(self.damages*projectile.damages_stacking+1) # éjection x
                    self.vy = -projectile.knockback*sin(projectile.angle)*(self.damages*projectile.damages_stacking+1) # éjection y
                    self.hitstun = projectile.stun*(self.damages*projectile.damages_stacking/2+1) # hitstun
                    self.damages += projectile.damages # dommages
                    self.rect.y -= 1
                    self.attack = None
                else :
                    if self.parry :
                        self.parrying = True
                    if self.mao :
                        self.damages = max(0.,self.damages - projectile.damages) # heal
                        self.mao_used = True
                return

###################          
""" Projectiles """
###################

class Carte():
    def __init__(self,x,y,angle,number,own) -> None:
        if number == "R":
            self.sprite = pygame.image.load(f"./DATA/Images/Sprites/Projectiles/Cartes/Revolution.png")
            self.knockback = 0
            self.damages = 999
            self.stun = 0
            self.damages_stacking = 0
        else :
            self.number = number + 2
            if self.number > 13 :
                self.number = self.number-13
            self.sprite = pygame.transform.scale(pygame.image.load(f"./DATA/Images/Sprites/Projectiles/Cartes/{self.number}.png"),(48,64))
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

class Stylo():
    def __init__(self,color,own,stage):
        # Stylos d'Elsa
        self.sprite = pygame.image.load("./DATA/Images/Sprites/Projectiles/Stylo/Stylo_"+color+".png")
        self.rect = self.sprite.get_rect()
        self.x = own.rect.x
        self.y = own.rect.y + own.rect.h//2
        self.color = color
        if self.color == "Vert":
            self.vx = 15*signe(own.direction)
        else :
            self.vx = 10*signe(own.direction)
        if self.color == "Vert" :
            self.vy = -6
        else :
            self.vy = -4
        self.duration = 5
        self.stage = stage
        if self.color == "Violet":
            self.damages_stacking=1/250
        else :
            self.damages_stacking=1/750
        if self.color == "Bleu":
            self.angle = -pi/2
        elif not own.look_right :
            self.angle = 3*pi/4
        else :
            self.angle = pi/4
        if self.color == "Violet":
            self.knockback = 7
        elif self.color == "Bleu" :
            self.knockback = 5
        else :
            self.knockback = 3
        if self.color == "Noir":
            self.damages = 3.2
        elif self.color == "Vert" :
            self.damages = 0.8
        else :
            self.damages = 1.2
        if self.color == "Noir" :
            self.stun = 6
        elif self.color == "Violet":
            self.stun = 8
        else :
            self.stun = 3

    def update(self):
        if self.rect.colliderect(self.stage.mainplat.rect) :
            self.duration = 0
        self.x += round(self.vx)
        self.y += self.vy
        if self.color == "Bleu":
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
