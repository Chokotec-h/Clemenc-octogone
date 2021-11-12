from DATA.utilities.Animations import get_sprite
from DATA.utilities.Base_Char import Char, Hitbox, signe
import pygame
from math import pi,cos,sin

##### Kebab
saucesprites = [pygame.image.load(f"./DATA/Images/Sprites/Misc/Sauces/{s}.png") for s in ("Algerienne","Samourai","Blanche","Moutarde","Americaine","Harissa","BBQ","Ketchup")]

class Kebab(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=1.3, dashspeed=2.3, airspeed=1.9, deceleration=0.75, fallspeed=0.3, fastfallspeed=1.3, fullhop=9, shorthop=7,
                         doublejumpheight=8,airdodgespeed=6,airdodgetime=3,dodgeduration=15)

        self.rect = pygame.Rect(100,0,48,64) # Crée le rectangle de perso
        self.doublejump = [False,False,False]   # Possède 3 double sauts
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav") # Son test
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

    def __str__(self) -> str:
        return "Kebab du dimanche soir"

    def special(self):
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
            self.changeframe = 0
            self.superarmor = 0
        else :
            self.sauces[self.current_sauce] -= 1.3
            if self.sauces[self.current_sauce] <= 0 : # Resete sauce
                self.current_sauce = -1

        if self.current_sauce == 0 : # Algérienne : damages x2
            print("Algerienne")
            self.damagemodifier = 2

        if self.current_sauce == 1 : # Samouraï : knockback x2
            print("Samourai")
            self.knockbackmodifier = 2

        if self.current_sauce == 2 : # Blanche : superarmor
            print("Blanche")
            self.superarmor = -1
            self.sauces[self.current_sauce] -= 2

        if self.current_sauce == 3 : # Moutarde : -5 frames de lag
            print("Moutarde")
            self.changeframe = -5

        if self.current_sauce == 4 : # Américaine : Better Air stats
            print("Americaine")
            self.airspeed = 3
            self.fallspeed = 0.8
            self.fastfallspeed = 1.5
            self.fullhop = 18
            self.shorthop = 14
            self.doublejumpheight = 16

        if self.current_sauce == 5 : # Harissa : Better Ground Speed
            print("Harissa")
            self.speed = 3
            self.dashspeed = 5.5

        if self.current_sauce == 6 : # BBQ : Better Airdodge Speed
            print("BBQ")
            self.airdodgespeed = 11
            self.airdodgetime = 1

        if self.current_sauce == 7 : # Ketchup : Less frictions
            print("Ketchup")
            self.deceleration = 0.9
            self.speed = 1
            self.dashspeed = 2

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            if self.frame < 11 :
                self.vy = self.fallspeed
            if self.frame == 11: # Saute frame 11
                self.attack = None
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
                if self.sauce != self.current_sauce and self.sauces[self.sauce] >= 599:
                    self.current_sauce = self.sauce
            if self.frame > 15: # 10 frames de lag
                self.attack = None

        if attack == "DownB":
            if self.frame == 9 and self.eatleft:
                self.damages = max(self.damages-15.5,0)
                self.eatleft -= 1
            if (self.frame > 20 + self.changeframe and self.eatleft) or self.frame > 25: # 16 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame > 80 + self.changeframe : # 20 frames de lag
                self.attack = None

        if attack == "Jab":

            if self.frame > 22 + self.changeframe: # 10 frames de lag
                self.attack = None

        if attack == "DownTilt":

            if self.frame > 20 + self.changeframe: # 7 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame < 3  + self.changeframe:
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True

            if self.frame > 30 + self.changeframe: # 8 frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame > 25 + self.changeframe: # 11 Frames de lag
                self.attack = None

        if attack == "UpAir":

            if self.frame > 25 + self.changeframe: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 15 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 15+

        if attack == "ForwardAir":

            if self.frame > 50 + self.changeframe: # 29 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 40 :
                    self.lag = self.frame-3 # Auto cancel frame 1-3 et 40+

        if attack == "BackAir":

            if self.frame > 25 + self.changeframe: # 14 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-2 # Auto cancel frame 1-2 et 20+

        if attack == "DownAir":

            if self.frame > 25 + self.changeframe: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 20 :
                    self.lag = self.frame-5 # Auto cancel frame 1-5 et 20+

        if attack == "NeutralAir":

            if self.frame > 40 + self.changeframe: # 17 frames de lag
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
            if self.frame > 45 + self.changeframe: # 30 frames de lag
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

            if self.frame > 40 + self.changeframe: # 23 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
            if self.frame < 26 :
                self.vy = 0
                if self.grounded :
                    self.vx += self.dashspeed*signe(self.direction)
                else :
                    self.vx -= self.dashspeed*signe(self.direction)
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

    def draw(self, window): # Dessine aussi les inputs du konami code et la jauge d'explosifs
        drawing_sprite,size,self.animeframe = get_sprite(self.animation,self.name,self.animeframe,self.look_right)

        drawing_sprite = pygame.transform.scale(drawing_sprite,(round(drawing_sprite.get_size()[0]*4),round(drawing_sprite.get_size()[1]*4))) # Rescale
        size = [size[0]*4,size[1]*4,size[2]*4,size[3]*4] # Rescale
        pos = [self.x + 800 - size[2]/2, self.rect.y-size[3]+self.rect.h + 449] # Position réelle du sprite
        window.blit(drawing_sprite, pos,size) # on dessine le sprite
        #self.rect.y -=  size[3] - self.rect.h # Reste à la surface du stage

        for i,s in enumerate(self.smoke_dash):
                    s.draw(window)
                    if s.life_time < 0:
                        del self.smoke_dash[i]
        
        for i,s in enumerate(self.double_jump):
                    s.draw(window)
                    if s.life_time < 0:
                        del self.double_jump[i]
        
        if self.current_sauce != -1 :
            if self.player == 0 :
                x = 550
            else :
                x = 1100
            window.blit(saucesprites[self.current_sauce],(x,750))
            pygame.draw.rect(window,(0,0,0),(x-1,798,50,5))
            pygame.draw.rect(window,(200,200,100),(x-1,798,self.sauces[self.current_sauce]/12,5))
        if self.attack == "NeutralB":
            for i in range(8):
                if self.sauces[i] >= 599 :
                    if self.sauce == i :
                        pygame.draw.circle(window,(100,250,100),(cos(i*2*pi/8)*75+self.rect.x+800+24,sin(i*2*pi/8)*75+self.rect.y+450+24),30,width=2)
                    window.blit(saucesprites[i],(cos(i*2*pi/8)*75+self.rect.x+800,sin(i*2*pi/8)*75+self.rect.y+450))
###################          
""" Projectiles """
###################

##### Autres skins
