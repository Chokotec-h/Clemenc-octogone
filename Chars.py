from Base_Char import Char, Hitbox
import pygame
from math import pi

##### M Balan

class Balan(Char):
    def __init__(self) -> None:
        super().__init__(speed=2, airspeed=1.4, deceleration=0.8, fallspeed=0.8, fastfallspeed=1.3, jumpheight=15,
                         doublejumpheight=10)
        # Liste des frames
        self.sprite = [pygame.image.load("DATA/Images/Sprites/M_Balan_idle.png"),pygame.image.load("DATA/Images/Sprites/M_Balan_upB.png")]

        self.rect = self.sprite[0].get_rect(center=(0, -100)) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav") # Son test
    
    def animation_attack(self,attack):
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
                self.active_hitboxes.append(Hitbox(-1,59,34,32,angle,20,40,60,4,self))

class Projo_Craie():
    def __init__(self,id):
        self.sprite = pygame.image.load("./DATA/Sprites/Craie_"+["blanche"][id])         

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
