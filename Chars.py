from Base_Char import Char
import pygame

##### M Balan

class Balan(Char):
    def __init__(self) -> None:
        super().__init__(speed=1, airspeed=0.7, deceleration=0.8, fallspeed=0.6, fastfallspeed=1, jumpheight=15,
                         doublejumpheight=10)
        # Liste des frames
        self.sprite = [pygame.image.load("DATA/Images/Sprites/M_Balan_idle.png"),pygame.image.load("DATA/Images/Sprites/M_Balan_upB.png")]

        self.image = pygame.image.load("DATA/Images/Sprites/M_Balan_idle.png").convert_alpha() # chargement de l'image
        self.mask = pygame.mask.from_surface(self.image) # Gère les collisions 
        self.rect = self.image.get_rect(center=(0, -100)) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/jump.wav") # Son test
    
    def animation_attack(self,attack):
        if attack == "UpB":
            if self.frame > 6 and self.frame < 10:
                self.sprite_frame = 0
                self.vel[1] = 20
                self.attack = None
                self.doublejump = [True for _ in self.doublejump]
            else :
                self.rect.move_ip(0,-6)
                self.sprite_frame = 1

##### Test

class Balan2(Char):
    def __init__(self) -> None:
        super().__init__(speed=0.5, airspeed=0.8, deceleration=0.7, fallspeed=0.8, fastfallspeed=1.5, jumpheight=15,
                         doublejumpheight=8)
        self.sprite = [pygame.image.load("DATA/Images/Sprites/M_Balan2_idle.png")]  # dictionnaire ?
        self.image = pygame.image.load("DATA/Images/Sprites/M_Balan_idle.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(100, -100))
        self.doublejump.append(False)
