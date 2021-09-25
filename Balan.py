from Base_Char import Char, Hitbox, signe
import pygame
from math import pi

##### M Balan

class Balan(Char):
    def __init__(self) -> None:
        super().__init__(speed=2, airspeed=1.2, deceleration=0.7, fallspeed=0.8, fastfallspeed=1.3, jumpheight=15,
                         doublejumpheight=10)
        # Liste des frames
        self.sprite = [pygame.image.load("DATA/Images/Sprites/M_Balan_idle.png"),pygame.image.load("DATA/Images/Sprites/M_Balan_upB.png")]

        self.rect = self.sprite[0].get_rect(center=(0, -100)) # Crée le rectangle de perso
        self.rect.w *= 1.5 # Rescale
        self.rect.h *= 1.5 # Rescale
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav") # Son test
        self.charge = 0


    def act(self, inputs,stage): # Spécial à Balan, pour son upB et son neutral B
        self.last_hit = max(self.last_hit-1,0)
        self.get_inputs(inputs,stage)
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
            self.vx *= 0.1
        if self.hitstun: # Arrête la charge du neutral B en hitstun
            self.charge = 0
    def animation_attack(self,attack,inputs,stage):
        left, right, up, down,jump, attack_button, special, shield = inputs # dissociation des inputs
        if attack == "UpB":
            if self.frame > 10 and self.frame < 12: # Saute frame 11
                self.sprite_frame = 0
                self.can_act = False
                self.vy = -25
                self.attack = None
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts
            elif self.frame > 6 : # Sort frame 7
                if left : # peut reverse netre les frames 7 et 10
                    self.direction = -90
                if right :
                    self.direction = 90
                self.rect.move_ip(0,-6)
                self.sprite_frame = 1
            if self.frame == 6: # Hitbox frame 6-11
                if self.direction < 0 :
                    angle = pi/3
                else:
                    angle = 2*pi/3
                self.active_hitboxes.append(Hitbox(-1.5,88.5,51,48,angle,18,32,1/150,40,5,self))

        if attack == "NeutralB":
            #self.can_act = False
            if self.frame < 5 and special : # Chargement jusqu'à 100 frames
                self.frame = 0
                self.charge = min(100,self.charge+1)
                if left : # peut changer de direction
                    self.direction = -90
                if right :
                    self.direction = 90
            elif self.frame == 5 : # 5 frames après relache
                    for i in range(0,(self.charge-1)//20+1):
                        self.projectiles.append(Projo_Craie(i,self,stage))
            if self.frame > 15: # 10 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "Jab":
            if self.frame == 5 : # 1er hit frame 5-10
                if self.direction < 0:
                    angle = pi/4
                else:
                    angle = 3*pi/4
                self.active_hitboxes.append(Hitbox(40*signe(self.direction)+12,64,24,10,angle,2,0.6,0,5,5,self))
            if self.frame == 10 : # 2e hit frame 10-15
                if self.direction < 0:
                    angle = 3*pi/4
                else:
                    angle = pi/4
                self.active_hitboxes.append(Hitbox(40*signe(self.direction)+19,52,10,24,angle,4.5,1.4,1/1000,8,5,self))

            if self.frame > 25: # 10 frames de lag
                self.attack = None

        if attack == "DownTilt":
            if self.frame == 8 : # Frame 8-13
                if self.direction < 0:
                    angle = 2*pi/3
                else:
                    angle = pi/3
                self.active_hitboxes.append(Hitbox(35*signe(self.direction)+11,90,24,10,angle,3,3.8,1/500,10,5,self))

            if self.frame > 20: # 7 frames de lag
                self.attack = None

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
        self.duration = 10
        self.stage = stage
        self.damages_stacking=0
        if own.direction < 0 :
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
        self.x += round(self.vx)
        self.y += self.vy
        self.vy += 0.3
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
        self.rect.w *= 1.5 # Rescale
        self.rect.h *= 1.5 # Rescale
        if self.y > 800 :
            self.duration = 0
    
    def draw(self,window):
        window.blit(self.sprite, (self.x+800,self.y+450)) # on dessine le sprite
        

##### Autres skins

class Balan2(Balan):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = [pygame.image.load("DATA/Images/Sprites/M_Balan2_idle.png"),pygame.image.load("DATA/Images/Sprites/M_Balan2_upB.png")]  # dictionnaire ?
        self.image = pygame.image.load("DATA/Images/Sprites/M_Balan2_idle.png").convert_alpha()
