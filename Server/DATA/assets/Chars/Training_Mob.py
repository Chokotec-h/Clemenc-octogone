from DATA.utilities.Base_Char import Char
import pygame

##### Training Mob

class Training(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=2, dashspeed=3, airspeed=0.9, deceleration=0.5, fallspeed=0.5, fastfallspeed=1, fullhop=13, shorthop=10,
                         doublejumpheight=15,airdodgespeed=6,airdodgetime=3,dodgeduration=15)

        self.rect = [100,0,48,120] # Crée le rectangle de perso
        self.name = "Training"
        self.x = x
        self.rect[1] = y
        self.player = player
        self.basedamages = 0
        self.resize_rect()

    def __str__(self) -> str:
        return ""

    def special(self,inputs): 
        if self.die :
            self.damages = self.basedamages
        pass

    def animation_attack(self,attack,inputs,stage,other):
        self.attack = None