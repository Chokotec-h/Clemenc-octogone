from random import random, choice
from DATA.utilities.Animations import get_sprite
from DATA.utilities.Base_Char import *
import pygame
from math import pi,cos,sin
from DATA.assets.Chars.Kebab_aux import *
from DATA.utilities.functions import *

##### Kebab
image = pygame.image.load(f"DATA/Images/Sprites/Misc/Sauces/Algerienne.png")
saucesprites = [pygame.transform.scale(pygame.image.load(f"DATA/Images/Sprites/Misc/Sauces/{s}.png"),resize(image.get_size()[0],image.get_size()[1],width,height)) for s in ("Algerienne","Samourai","Blanche","Moutarde","Americaine","Harissa","BBQ","Tabasco")]
del image


class Kebab(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=1.2, dashspeed=2, airspeed=0.7, deceleration=0.75, fallspeed=0.3, fastfallspeed=1, fullhop=8, shorthop=6,
                         doublejumpheight=5,airdodgespeed=6,airdodgetime=3,dodgeduration=18)

        self.rect = pygame.Rect(100,0,48,64) # Crée le rectangle de perso
        self.doublejump = [False,False,False]   # Possède 3 double sauts

        self.name = "Kebab"
        self.x = x
        self.rect.y = y
        self.player = player
        self.damagemodifier = 1
        self.knockbackmodifier = 1
        self.changeframe = 0
        self.sauces = [600,600,600,600,600,600,600,600]
        self.sauce = -1
        self.current_sauce = -1

        self.eatleft = 3
        self.resize_rect()

    def __str__(self) -> str:
        return "Kebab du dimanche soir"

    def special(self,inputs):
        if self.die :
            self.eatleft = 3
            self.sauces = [600,600,600,600,600,600,600,600]
        for i in range(len(self.sauces)):
            self.sauces[i] = min(self.sauces[i]+0.3,600)
        if self.current_sauce < 0 : # Reset stats
            self.speed = 1.3
            self.dashspeed = 2.3
            self.airspeed = 1.9
            self.deceleration = 0.75
            self.fallspeed = 0.3
            self.fastfallspeed = 1.1
            self.fullhop = 9
            self.shorthop = 7
            self.doublejumpheight = 8
            self.airdodgespeed = 6
            self.airdodgetime = 3
            self.damagemodifier = 1
            self.knockbackmodifier = 1
            self.stunmodifier = 1
            self.changeframe = 0
            self.superarmor = 0
        else :
            self.sauces[self.current_sauce] -= 1.3
            if self.sauces[self.current_sauce] <= 0 : # Reset sauce
                self.current_sauce = -1

        if self.current_sauce == 0 : # Algérienne : damages x2
            #print("Algerienne")
            self.damagemodifier = 2

        if self.current_sauce == 1 : # Samouraï : knockback x1.5
            #print("Samourai")
            self.knockbackmodifier = 1.5

        if self.current_sauce == 2 : # Blanche : superarmor
            #print("Blanche")
            self.superarmor = -1
            self.sauces[self.current_sauce] -= 1

        if self.current_sauce == 3 : # Moutarde : -5 frames de lag
            #print("Moutarde")
            self.changeframe = -5

        if self.current_sauce == 4 : # Américaine : Meilleures caractéristiques aériennes
            #print("Americaine")
            self.airspeed = 3
            self.fallspeed = 0.8
            self.fastfallspeed = 1.5
            self.fullhop = 18
            self.shorthop = 14
            self.doublejumpheight = 16

        if self.current_sauce == 5 : # Harissa : Meilleure Vitesse au sol
            #print("Harissa")
            self.speed = 3
            self.dashspeed = 5.5

        if self.current_sauce == 6 : # BBQ : Airdodge plus rapide et moins de frictions
            #print("BBQ")
            self.airdodgespeed = 11
            self.airdodgetime = 1
            self.deceleration = 0.9
            self.speed = 1
            self.dashspeed = 2

        if self.current_sauce == 7 : # "Tabasco : Meilleur stun
            #print("Tabasco")
            self.stunmodifier = 1.8

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            if self.frame == 1 :
                self.animation = "upb"
                self.animeframe = 0
            if self.frame < 11 :
                self.vy = self.fallspeed
            if self.frame == 11: # Saute frame 11
                self.attack = None
                self.can_act = True
                self.doublejump = [False for _ in self.doublejump] # Récupère tout les sauts

        if attack == "NeutralB":
            if self.frame > 3 and self.frame < 6 and special:
                self.frame = 4
                if up and left :
                    self.sauce = 5
                elif up and right :
                    self.sauce = 7
                elif up :
                    self.sauce = 6
                elif down and left :
                    self.sauce = 3
                elif down and right :
                    self.sauce = 1
                elif down :
                    self.sauce = 2
                elif left :
                    self.sauce = 4
                elif right :
                    self.sauce = 0
                else :
                    self.sauce = -1
            if self.frame == 7 :
                self.current_sauce = -1
            if self.frame == 9 :
                if self.sauce != self.current_sauce and self.sauces[self.sauce] >= 599:
                    self.current_sauce = self.sauce
            if self.frame > 15 + self.changeframe: # 10 frames de lag
                self.attack = None

        if attack == "DownB":
            if self.frame == 1 :
                if self.eatleft :
                    self.animation = "downb"
                else :
                    self.animation = "downb_no"
                self.animeframe = 0
            if self.frame == 9 and self.eatleft:
                self.damages = max(self.damages-15.5,0)
                self.eatleft -= 1
            if (self.frame > 20 + self.changeframe and self.eatleft) or self.frame > 25: # 16 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame < 3  + self.changeframe:
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 10 :
                for p in self.projectiles :
                    if isinstance(p,Flaque):
                        p.duration = 0
                self.projectiles.append(Flaque(self,other,stage))
            if self.frame > 20 + self.changeframe : # 10 frames de lag
                self.attack = None

        if attack == "Jab":
            if self.frame == 1 :
                self.animation = "jab"
                self.animeframe = 0
            if self.frame == 3 :
                self.active_hitboxes.append(Hitbox(42,20,40,40,pi,2*self.knockbackmodifier,4*self.damagemodifier,0,12*self.stunmodifier,2,self,sound="hits/punch"))
            if self.frame > 6 and attack_button :
                self.attack = "Jab2"
                self.animeframe = 0
                self.frame = 0

            if self.frame > 15: # 18 frames de lag
                self.attack = None

        if attack == "Jab2":
            if self.frame == 1 :
                self.animation = "jab2"
            if self.frame == 3 :
                self.active_hitboxes.append(Hitbox(42,20,40,40,pi/6,8*self.knockbackmodifier,4*self.damagemodifier,0,12*self.stunmodifier,2,self,sound="hits/punch2"))

            if self.frame > 21: # 18 frames de lag
                self.attack = None

        if attack == "DownTilt":
            if self.frame == 1 :
                self.animation = "dtilt"
                self.animeframe = 0
            if self.frame == 5 :
                self.active_hitboxes.append(Hitbox(20,15,40,40,pi/3,6*self.knockbackmodifier,6*self.damagemodifier,1/300,15*self.stunmodifier,10,self))
                self.vx = 22*signe(self.direction)

            if self.frame > 25 + self.changeframe: # 7 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame == 3 :
                self.animation = "ftilt"
                self.animeframe = 0
            if self.frame < 3  + self.changeframe:
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 7 :
                self.active_hitboxes.append(Hitbox(30,10,55,40,pi/6,8*self.knockbackmodifier,8*self.knockbackmodifier,1/160,16*self.stunmodifier,3,self))

            if self.frame > 30 + self.changeframe: # 8 frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame == 6 :
                self.animation = "utilt"
                self.animeframe = 0
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(0,0,48,52,pi/2,10*self.knockbackmodifier,9*self.damagemodifier,1/220,14*self.stunmodifier,7,self,sound="hits/punch2"))
            if self.frame > 8 and self.active_hitboxes :
                self.active_hitboxes[-1].sizey += 8
                self.active_hitboxes[-1].relativey -= 8
            if self.frame > 25 + self.changeframe: # 11 Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame == 3 :
                self.animation = "uair"
                self.animeframe = 0
            if self.frame == 5 :
                self.active_hitboxes.append(Hitbox(0,0,48,24,pi/2,7*self.knockbackmodifier,3*self.damagemodifier,1/100,15*self.stunmodifier,6,self,sound="wooshs/mini woosh"))
            if self.frame > 5 and self.active_hitboxes :
                self.active_hitboxes[-1].relativey -= 10

            if self.frame > 25 + self.changeframe: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 + self.changeframe and self.frame > 2 :
                    self.lag = 9 + self.changeframe # Auto cancel frame 1-2 et 20+, 15 frames de landing lag

        if attack == "ForwardAir":
            if self.frame == 1 :
                self.animation = "fair"
                self.animeframe = 0
            if self.frame == 5 :
                self.active_hitboxes.append(Hitbox(40,30,24,24,pi/6,4*self.knockbackmodifier,5*self.damagemodifier,1/230,12*self.stunmodifier,10,self,sound="hits/mini hit"))

            if self.frame > 30 + self.changeframe: # 15 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 25 + self.changeframe and self.frame > 2 :
                    self.lag = 12 + self.changeframe # Auto cancel frame 1-2 et 22+, 15 frames de landing lag

        if attack == "BackAir":
            if self.frame == 1 :
                self.animation = "bair"
                self.animeframe = 0
            if self.frame == 12 :
                self.active_hitboxes.append(Hitbox(-40,20,40,12,5*pi/6,13*self.knockbackmodifier,10*self.damagemodifier,1/150,14*self.stunmodifier,2,self,sound="hits/cool hit"))

            if self.frame > 25 + self.changeframe: # 14 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 22 + self.changeframe and self.frame > 2 :
                    self.lag = 11 + self.changeframe # Auto cancel frame 1-2 et 22+, 8 frames de landing lag

        if attack == "DownAir":
            if self.frame == 1 :
                self.animation = "dair"
                self.animeframe = 0
            if self.frame == 4 :
                self.active_hitboxes.append(Hitbox(10,30,28,30,pi/2,2,1*self.damagemodifier,0,8*self.stunmodifier,2,self))
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(10,30,28,30,pi/2,2,1*self.damagemodifier,0,8*self.stunmodifier,2,self))
            if self.frame == 12 :
                self.active_hitboxes.append(Hitbox(10,30,28,30,-pi/2,10*self.knockbackmodifier,4*self.damagemodifier,1/200,16*self.stunmodifier,2,self,sound="hits/cool hit"))

            if self.frame > 25 + self.changeframe: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 22 + self.changeframe and self.frame > 2 :
                    self.lag = 15 + self.changeframe # Auto cancel frame 1-2 et 22+, 8 frames de landing lag

        if attack == "NeutralAir":
            if self.frame == 6 :
                self.animation = "nair"
                self.animeframe = 0
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(-20,-20,88,88,(random()-0.5)*2*pi,12*self.knockbackmodifier,10*self.damagemodifier,1/200,14*self.stunmodifier,3,self,sound="hits/cool hit"))

            if self.frame > 40 + self.changeframe: # 17 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 32 + self.changeframe and self.frame > 2 :
                    self.lag = 13 + self.changeframe # Auto cancel frame 1-2 et 22+, 8 frames de landing lag

        if attack == "ForwardSmash":
            if self.frame == 2 :
                self.animeframe = 0
            if self.frame > 12 and self.frame < 16 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 14
                self.animeframe -= 1
                self.charge = self.charge+1
            if self.frame == 24 :
                self.charge = min(100,self.charge)
                self.active_hitboxes.append(Hitbox(32,0,64,64,pi/3,16*self.knockbackmodifier+5*(self.charge/100),19*self.damagemodifier,1/200,20*self.stunmodifier+8*(self.charge/100),4,self,boum=1,sound=f"hits/punch{choice(('1','2',''))}"))
            if self.frame > 45 + self.changeframe: # 30 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "UpSmash":
            if self.frame == 2 :
                self.animeframe = 0
            if self.frame < 5 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 5 and self.frame < 8  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.animeframe -= 1
                self.frame = 6
                self.charge = self.charge+1
            if self.frame == 24 :
                self.charge = min(100,self.charge)
                self.active_hitboxes.append(Hitbox(32,-48,64,80,pi/2,17*self.knockbackmodifier+5*(self.charge/100),15*self.damagemodifier,1/200,21*self.stunmodifier+8*(self.charge/100),4,self,boum=1,sound=f"hits/punch{choice(('1','2',''))}"))
            if self.frame > 40 + self.changeframe: # 25 frames de lag
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

            if self.frame == 24 :
                self.charge = min(100,self.charge)
                self.active_hitboxes.append(Hitbox(50,0,64,64,-pi/2,22*self.knockbackmodifier+5*(self.charge/100),17*self.damagemodifier,1/200,18*self.stunmodifier+8*(self.charge/100),4,self,boum=1,sound=f"hits/punch{choice(('1','2',''))}"))
            if self.frame > 40 + self.changeframe: # 25 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
            if self.frame == 2:
                self.animation = "dashattack"
                self.animeframe = 0
            if self.frame == 5 :
                self.vx = 23*signe(self.direction)
                self.vy = -10
                self.fastfall = True
                self.active_hitboxes.append(Hitbox(0,0,50,50,pi/4,abs(self.vx)*0.5*self.knockbackmodifier,7*self.damagemodifier,1/220,14*self.stunmodifier,20,self,sound="hits/cool hit"))
            if self.frame > 5 and self.frame < 18 :
                self.vx = (23-self.frame)*signe(self.direction)
            if self.frame == 18 :
                self.fastfall = False
            if self.frame > 50 + self.changeframe: # 24 frames de lag
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

    def draw(self, window): # Dessine aussi les smashes et la jauge sauce

        modifier = resize(4,0,width,height)[0]
        sizescalex,sizescaley = resize(self.sizescale,self.sizescale,width,height)

        drawing_sprite,size,self.animeframe = get_sprite(self.animation,self.name,self.animeframe,self.look_right)
        drawing_sprite = pygame.transform.flip(drawing_sprite.subsurface(size[0],size[1],size[2],size[3]),not self.look_right,False)
        drawing_sprite = pygame.transform.scale(drawing_sprite,(round(drawing_sprite.get_size()[0]*sizescalex),round(drawing_sprite.get_size()[1]*sizescaley))) # Rescale
        size = [size[0] * sizescalex, size[1] * sizescaley, size[2] * sizescalex, size[3] * sizescaley]  # Rescale
        pos = [self.x + resize(800,0,width,height)[0] - size[2]/2, self.rect.y-size[3]+self.rect.h + resize(0,450,width,height)[1]-1] # Position réelle du sprite
        if self.show :
            window.blit(drawing_sprite, pos) # on dessine le sprite
        
        if self.attack == "ForwardSmash" and self.animeframe > 14:
            t = "" if self.look_right else "l"
            drawsmash = Attacks["fsmash"+str(self.current_sauce)+t]
            drawing_smash = pygame.transform.scale(drawsmash[0],(round(drawsmash[0].get_size()[0]*modifier),round(drawsmash[0].get_size()[1]*modifier))) # Rescale
            size = drawsmash[1][min((self.animeframe-14)//4,len(drawsmash[1])-1)]
            size = [size[0]*modifier,size[1]*modifier,size[2]*modifier,size[3]*modifier] # Rescale
            if not self.look_right :
                pos[0] -= size[2] - resize(48,0,width,height)[0]
            window.blit(drawing_smash, pos,size) # on dessine le sprite
            pos[0] += resize(15,0,width,height)[0]*signe(self.direction)
        
        if self.attack == "UpSmash" and self.animeframe > 14:
            t = "" if self.look_right else "l"
            drawsmash = Attacks["usmash"+str(self.current_sauce)+t]
            drawing_smash = pygame.transform.scale(drawsmash[0],(round(drawsmash[0].get_size()[0]*modifier),round(drawsmash[0].get_size()[1]*modifier))) # Rescale
            size = drawsmash[1][min((self.animeframe-14)//4,len(drawsmash[1])-1)]
            size = [size[0]*modifier,size[1]*modifier,size[2]*modifier,size[3]*modifier] # Rescale
            if not self.look_right :
                pos[0] -= size[2] - resize(48,0,width,height)[0]
            pos[0] += resize(40,0,width,height)[0]*signe(self.direction)
            pos[1] -= size[3] - resize(48,0,width,height)[0]
            window.blit(drawing_smash, pos,size) # on dessine le sprite
        
        if self.attack == "DownSmash" and self.animeframe > 6:
            t = "" if self.look_right else "l"
            drawsmash = Attacks["dsmash"+str(self.current_sauce)+t]
            drawing_smash = pygame.transform.scale(drawsmash[0],(round(drawsmash[0].get_size()[0]*modifier),round(drawsmash[0].get_size()[1]*modifier))) # Rescale
            size = drawsmash[1][min((self.animeframe-6)//3,len(drawsmash[1])-1)]
            size = [size[0]*modifier,size[1]*modifier,size[2]*modifier,size[3]*modifier] # Rescale
            if not self.look_right :
                pos[0] -= size[2] - resize(48,0,width,height)[0]
            pos[0] += resize(40,0,width,height)[0]*signe(self.direction)
            pos[1] -= size[3]
            if self.animeframe > 16 :
                pos[1] += (min(self.animeframe-16,8))*resize(0,8,width,height)[1]
            window.blit(drawing_smash, pos,size) # on dessine le sprite
        
        if self.attack == "NeutralAir" and self.animeframe < 12:
            drawsmash = Attacks["nair"+str(self.current_sauce)]
            drawing_smash = pygame.transform.scale(drawsmash[0],(round(drawsmash[0].get_size()[0]*modifier*1.5),round(drawsmash[0].get_size()[1]*modifier*1.5))) # Rescale
            size = drawsmash[1][min((self.animeframe)//2,len(drawsmash[1])-1)]
            size = [size[0]*modifier*1.5,size[1]*modifier*1.5,size[2]*modifier*1.5,size[3]*modifier*1.5] # Rescale
            if not self.look_right :
                pos[0] -= size[2] - resize(48,0,width,height)[0]
            pos[0] -= resize(20,0,width,height)[0]*signe(self.direction)
            pos[1] -= resize(24,0,width,height)[0]
            window.blit(drawing_smash, pos,size) # on dessine le sprite


        for i,s in enumerate(self.smoke_dash):
                    s.draw(window)
                    if s.life_time < 0:
                        del self.smoke_dash[i]
        
        for i,s in enumerate(self.double_jump):
                    s.draw(window)
                    if s.life_time < 0:
                        del self.double_jump[i]
        for p in self.projectiles :
            p.draw(window)
        
        if self.current_sauce != -1 :
            if self.player == 0 :
                x = 550
            else :
                x = 1100
            window.blit(saucesprites[self.current_sauce],resize(x,750,width,height))
            pygame.draw.rect(window,(0,0,0),(resize(x,0,width,height)[0]-1,resize(0,800,width,height)[1]-2,resize(50,0,width,height)[0],5))
            pygame.draw.rect(window,(200,200,100),(resize(x,0,width,height)[0]-1,resize(0,800,width,height)[1]-2,resize(self.sauces[self.current_sauce]/12,0,width,height)[0],5))
        if self.attack == "NeutralB":
            for i in range(8):
                if self.sauces[i] >= 599 :
                    if self.sauce == i :
                        pygame.draw.circle(window,(100,250,100),(cos(i*2*pi/8)*resize(75,0,width,height)[0]+self.rect.x+resize(824,0,width,height)[0],sin(i*2*pi/8)*resize(0,75,width,height)[1]+self.rect.y+resize(0,474,width,height)[1]),resize(30,0,width,height)[0],width=2)
                    window.blit(saucesprites[i],(cos(i*2*pi/8)*resize(75,0,width,height)[0]+self.rect.x+resize(800,0,width,height)[0], sin(i*2*pi/8)*resize(0,75,width,height)[1]+self.rect.y+resize(0,450,width,height)[1]))
###################          
""" Projectiles """
###################

class Flaque():
    def __init__(self,own:Kebab,other:Char,stage) -> None:
        self.sound = SFXDicoEvent['hits']["other hit"]
        self.sauce = str(own.current_sauce)
        self.sprite = pygame.transform.scale(Sauce[self.sauce],resize(1,1,width,height))
        self.x = own.x
        self.y = own.rect.y
        self.own = own
        self.other = other
        self.stage = stage
        self.vx = 8*signe(own.direction)
        self.vy = -9
        self.knockback = 3*own.knockbackmodifier
        self.damages = 9*own.damagemodifier
        self.stun = 5*own.stunmodifier
        self.angle = -pi/2
        self.duration = 1000
        self.damages_stacking = 0
        self.rect = self.sprite.get_rect(bottomleft=(self.x,self.y))
    
    def touch_stage(self,stage,rect):
        if rect.colliderect(stage.mainplat.rect):
            return True
        for p in stage.plats:
            if rect.colliderect(p.rect) and rect.y + rect.h-4 < p.rect.y+self.vy+4:
                return True
        return False

    def update(self):
        self.duration -= 1
        self.y += self.vy
        self.x += self.vx
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
        if self.touch_stage(self.stage,self.rect):
            if self.y < self.stage.mainplat.y :
                self.sprite = Sauce[self.sauce+"f"]
                self.vy = -0.1
                self.vx = 0
            else :
                self.vx = -self.vx
        else :
            self.vy += 1
        
        if self.rect.colliderect(self.other.rect):
            self.other.vx *= 2-self.other.deceleration
            self.other.hitstun = max(4,self.other.hitstun)
    
    def deflect(self,modifier):
        self.vx = -self.vx*modifier
        self.own,self.other = self.other,self.own

    def draw(self,window):
        window.blit(self.sprite, (self.rect.x+800,self.rect.y+450)) # on dessine le sprite
##### Autres skins
