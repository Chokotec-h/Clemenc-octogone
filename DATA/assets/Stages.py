import pygame
from DATA.utilities.functions import *

# Nom des stages
stages = ["Cour d'honneur", "K201", "Chapelle", "Salle d'info", "Salle de TP","Table de self","BDE","I211","H010"]
# Ajouter les musiques : (Nom de fichier,durée,stage,True si musique par défaut, sinon nom du personnage qui active la musique)
musics = [
    ("event:/BGM/let's_fight_!", "K201", True),("event:/BGM/Industrial class", "K201", "Renault"),("event:/BGM/THE WORLD of Mathematics", "K201", "Balan"),
    ("event:/BGM/Panda_Ball", "Pandadrome", True),
    ("event:/BGM/chapelle", "Chapelle", True), ("event:/BGM/BIGSHOT", "Chapelle", "Spamton"),
    ("event:/BGM/Honor winds", "Cour d'honneur", True),
    ("event:/BGM/Cyber Class", "Salle d'info", True),
    ("event:/BGM/Lunch time !", "Table de self", True),
    ("event:/BGM/City night", "BDE", True),
    ("event:/BGM/optic'mind", "Salle de TP", True),
    ("event:/BGM/within_octogone", "I211", True), ("event:/BGM/Beijing de zhuren", "I211", "Gourmelen"),
    ("event:/BGM/let's_fight_!", "H010", True), ("event:/BGM/Logic_game", "H010", "Journault"),    
]

class Rect():
    def __init__ (self,x,y,w,h):
        self.rect = [x,y,w,h]
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def colliderect(self,other):
        return pygame.Rect(self.rect).colliderect(other)

class Stage:
    def __init__(self,name , sprite, mainx, mainy, platforms=[]) -> None:
        self.name = name
        self.mainplat = MainPlat(f"DATA/Images/Stages/{sprite}.png", mainx, mainy)
        # Platforms : [(x,y,l,h,color),...]
        self.plats = []
        for p in platforms:
            self.plats.append(Platform(p[0], p[1], p[2], p[3], p[4]))

    def draw(self, window):
        self.mainplat.draw(window)
        for p in self.plats:
            p.draw(window)


class MainPlat:
    def __init__(self, sprite, x, y) -> None:
        # Sprite
        self.x, self.y = x,y
        self.sprite = sprite
        sprite = pygame.image.load(self.sprite).convert_alpha()
        sprite = pygame.transform.scale(sprite,
                                             (sprite.get_size()[0] * 4,sprite.get_size()[1] * 4))
        
        # Recalcul de l'ordonnée
        self.y = self.y + height - sprite.get_size()[1]

        # Rectangle
        rect = sprite.get_rect(midtop=(x, self.y))
        self.rect = Rect(rect.x,rect.y,rect.w,rect.h)
        self.rect.h += 250

    def draw(self, window):
        # Position réelle

        sprite = pygame.image.load(self.sprite).convert_alpha()
        sprite = pygame.transform.scale(sprite,
                                             (resize(sprite.get_size()[0] * 4,sprite.get_size()[1] * 4,width,height)))
        pos = [resize(self.rect.x + 800,0,width,height)[0] ,resize(0,self.rect.y + 450,width,height)[1]]
        # Affichage du stage
        # self.rect.move(self.rect)
        window.blit(sprite, pos)


class Platform():
    def __init__(self, x, y, l, h, color) -> None:
        # Rectangle
        self.rect = Rect(x - l // 2, y - h // 2, l, h)
        self.color = color

    def draw(self, window):
        # Position réelle
        pos = [resize(self.rect.x + 800,0,width,height)[0], resize(0,self.rect.y + 450,width,height)[1]-1]
        pygame.draw.rect(window, self.color, (pos[0], pos[1], resize(self.rect.w,0,width,height)[0], resize(0,self.rect.h,width,height)[1]))


def create_stage(stage):
    if stage == "K201":
        return (Stage(stage,f"{stage}/K201_plateforme", 0, 0,
                    [(-500, 220, 150, 12, (100, 70, 0)),
                    (500, 220, 150, 12, (100, 70, 0))]),
                [(-350,0), (350,0)])  # Coordonnées de départ
    if stage == "Pandadrome":
        return (Stage(stage,f"{stage}/Pandadrome_plateforme", 0, 0),
                [(-350,0), (0, 0)])  # Coordonnées de départ
    if stage == "Cour d'honneur":
        return (Stage(stage,f"{stage}/Cour d'honneur_plateforme", 0, 0,
                      [(2, 186 * 1.7 + 8, 436, 4, (97, 87, 77)), (2, 87, 332, 4, (97, 87, 77))]),
                [(-200,0), (200,0)])
    if stage == "Chapelle":
        return (Stage(stage,f"{stage}/Chapelle_plateforme", 0, 0,
                      [(-202, 376 - 49 * 4 + 21, 45 * 4, 12, (67, 14, 6)),
                       (206, 376 - 49 * 4 + 21, 45 * 4, 12, (67, 14, 6)), (0, 60, 72 * 4, 12, (67, 14, 6))]),
                [(-200,-50), (200,-50)])
    if stage == "Salle d'info":
        return (Stage(stage,f"{stage}/Salle d'info_plateforme", 0, 0,
                      [(-276, 68, 192, 4, (0, 0, 0)),
                       (276, 68, 192, 4, (0, 0, 0))]),
                [(-230,-65), (230,-65)])
    if stage == "Salle de TP":
        return (Stage(stage,f"{stage}/Salle_de_TP_plateforme", 0, 0,
                      [(-398, 164, 268, 4, (200, 200, 200)),(398, 164, 268, 4, (200, 200, 200)),
                      (-530, 5, 268, 4, (200, 200, 200)),(530, 5, 268, 4, (200, 200, 200))]),
                [(-200,-50), (200,-50)])
    if stage == "Table de self":
        return (Stage(stage,f"{stage}/Table de self_plateforme", 6, 0),
                [(-200,-50), (200,-50)])
    if stage == "BDE":
        return (Stage(stage,f"{stage}/BDE_platform", 0, 0,
                [(0, 156, 640, 4, (0, 0, 0))]),
                [(-200,-50), (200,-50)])
    if stage == "H010":
        return (Stage(stage,f"{stage}/H010_platform", 0, 0,
                    []),
                [(-150,10), (150,10)])
    if stage == "I211":
        return (Stage(stage,f"{stage}/I211_plateforme", 0, 0,
                    []),
                [(-350,0), (350,0)])
