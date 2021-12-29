import pygame
from random import randint

# Nom des stages
stages = ["Cour d'honneur","K201"]
# Ajouter les musiques : (Nom de fichier,durée,stage,True si musique par défaut, sinon nom du personnage qui active la musique)
musics = [("DATA/Musics/BGM/lets_fight.mp3","K201",True),("DATA/Musics/BGM/Panda_Ball.mp3","Pandadrome",True),("DATA/Musics/BGM/chapelle.mp3","Cour d'honneur",True),("DATA/Musics/BGM/digital_autority.mp3","Salle d'info",True)]

class Stage():
    def __init__(self,sprite,mainx,mainy,platforms=[]) -> None:
        self.mainplat = MainPlat(f"DATA/Images/Stages/{sprite}.png",mainx,mainy)
        # Platforms : [(x,y,l,h,color),...]
        self.plats = []
        for p in platforms:
            self.plats.append(Platform(p[0],p[1],p[2],p[3],p[4]))
    
    def draw(self,window):
        self.mainplat.draw(window)
        for p in self.plats :
            p.draw(window)

class MainPlat:
    def __init__(self,sprite,x,y) -> None:
        # Sprite
        self.x = x
        self.y = y
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite,(self.sprite.get_size()[0]*4,self.sprite.get_size()[1]*4))
        # Rectangle
        self.rect = self.sprite.get_rect(midtop=(x,y))
        self.rect.height += 250

    def draw(self, window):
        # Position réelle
        pos = [self.rect.x+800, self.rect.y+449]

        # Affichage du stage
        #self.rect.move(self.rect)
        window.blit(self.sprite, pos)

class Platform():
    def __init__(self,x,y,l,h,color) -> None:
        # Rectangle
        self.rect = pygame.Rect(x-l//2,y-h//2,l,h)
        self.color = color

    def draw(self, window):
        # Position réelle
        pos = [self.rect.x+800, self.rect.y+449]
        pygame.draw.rect(window,self.color,(pos[0],pos[1],self.rect.w,self.rect.h))

def create_stage(stage):
    # Le placement des plateformes, c'est du bidouillage 👍
    if stage == "K201":
        return Stage(f"{stage}/K201_plateforme",0,191*1.65)
    if stage == "Pandadrome":
        return Stage(f"{stage}/Pandadrome_plateforme",0,186*1.6)
    if stage == "Cour d'honneur":
        return Stage(f"{stage}/Cour d'honneur_plateforme",-6,220*1.65,[(2,186*1.7+8,436,4,(97,87,77)),(2,186*1.7-226,332,4,(97,87,77))])