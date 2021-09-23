from Base_Char import Char, Hitbox, signe
import pygame
from math import pi

##### M Balan

class Balan(Char):
    def __init__(self) -> None:
        super().__init__(speed=2, airspeed=1.4, deceleration=0.7, fallspeed=0.8, fastfallspeed=1.3, jumpheight=15,
                         doublejumpheight=10)
        # Liste des frames
        self.sprite = [pygame.image.load("DATA/Images/Sprites/M_Balan_idle.png"),pygame.image.load("DATA/Images/Sprites/M_Balan_upB.png")]

        self.rect = self.sprite[0].get_rect(center=(0, -100)) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav") # Son test
        self.charge = 0

    def animation_attack(self,attack,inputs,stage):
        right, left, up, down, attack_button, special, shield = inputs # dissociation des inputs
        if attack == "UpB":
            if self.frame > 10 and self.frame < 12: # Saute frame 11
                self.sprite_frame = 0
                self.can_act = False
                self.vy = -20
                self.attack = None
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts
            elif self.frame > 6 : # Sort frame 6
                self.rect.move_ip(0,-6)
                self.sprite_frame = 1
                if self.direction < 0 :
                    angle = pi/3
                else:
                    angle = 2*pi/3
                self.active_hitboxes.append(Hitbox(-1,59,34,32,angle,18,40,1/100,40,4,self))
        if attack == "NeutralB":
            #self.can_act = False
            if self.frame < 5 and special and self.charge < 100:
                self.frame = 0
                self.charge += 1
            elif self.frame == 5 :
                    for i in range(0,(self.charge-1)//20+1):
                        self.projectiles.append(Projo_Craie(i,self,stage))
            if self.frame > 15:
                self.attack = None
                self.charge = 0

class Projo_Craie():
    def __init__(self,id,own,stage):
        self.id = id+1
        self.sprite = pygame.image.load("./DATA/Images/Sprites/Craies/Craie_"+["blanche","rouge","bleue","verte","jaune"][id]+".png")
        self.rect = self.sprite.get_rect()
        self.x = own.rect.x
        self.y = own.rect.y + own.rect.h//2
        self.vx = 15*signe(own.direction)+self.id
        self.vy = -3*(self.id)
        self.duration = 10
        self.stage = stage
        self.damages_stacking=0
        if own.direction < 0 :
            self.angle = 3*pi/4
        else :
            self.angle = pi/4
        self.knockback = 3
        self.damages = 3
        self.stun = 4

    def update(self):
        if self.rect.colliderect(self.stage.rect) :
            self.sprite = pygame.image.load("./DATA/Images/Sprites/Craies/Explosion_"+["blanche","rouge","bleue","verte","jaune"][self.id-1]+".png")
            self.y -= 3
            self.duration -= 1
            self.vx = 0
            self.vy = 0
        self.x += round(self.vx)
        self.y += self.vy
        self.vy += 0.5
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
        if self.y > 800 :
            self.duration = 0
    
    def draw(self,window):
        window.blit(self.sprite, (self.x+800,self.y+450)) # on dessine le sprite
        

##### Test

class Balan2(Char):
    def __init__(self) -> None:
        super().__init__(speed=1, airspeed=1.5, deceleration=0.7, fallspeed=0.8, fastfallspeed=1.5, jumpheight=15,
                         doublejumpheight=8)
        self.sprite = [pygame.image.load("DATA/Images/Sprites/M_Balan2_idle.png")]  # dictionnaire ?
        self.image = pygame.image.load("DATA/Images/Sprites/M_Balan_idle.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(100, -100))
        self.doublejump.append(False)
