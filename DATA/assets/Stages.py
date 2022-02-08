import pygame

# Nom des stages
stages = ["Cour d'honneur", "K201", "Chapelle", "Salle d'info", "Salle de TP","Table de self"]
# Ajouter les musiques : (Nom de fichier,durée,stage,True si musique par défaut, sinon nom du personnage qui active la musique)
musics = [("event:/BGM/let's_fight_!", "K201", True),
          ("event:/BGM/Panda_Ball", "Pandadrome", True),
          ("event:/BGM/chapelle", "Chapelle", True), ("event:/BGM/BIG-SHOT", "Chapelle", "Spamton"),
          ("event:/BGM/Honor winds", "Cour d'honneur", True),
          ("event:/BGM/digital_autority", "Salle d'info", True),
          ("event:/BGM/Lunch_time", "Table de self", True),
          ("event:/BGM/optic'mind", "Salle de TP", True)]


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
        self.x = x
        self.y = y
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite,
                                             (self.sprite.get_size()[0] * 4, self.sprite.get_size()[1] * 4))
        # Rectangle
        self.rect = self.sprite.get_rect(midtop=(x, y))
        self.rect.height += 250

    def draw(self, window):
        # Position réelle
        pos = [self.rect.x + 800, self.rect.y + 449]

        # Affichage du stage
        # self.rect.move(self.rect)
        window.blit(self.sprite, pos)


class Platform():
    def __init__(self, x, y, l, h, color) -> None:
        # Rectangle
        self.rect = pygame.Rect(x - l // 2, y - h // 2, l, h)
        self.color = color

    def draw(self, window):
        # Position réelle
        pos = [self.rect.x + 800, self.rect.y + 449]
        pygame.draw.rect(window, self.color, (pos[0], pos[1], self.rect.w, self.rect.h))


def create_stage(stage):
    if stage == "K201":
        return (Stage(stage,f"{stage}/K201_plateforme", 0, 191 * 1.65),
                [(-350, 0), (350, 0)])  # Coordonnées de départ
    if stage == "Pandadrome":
        return (Stage(stage,f"{stage}/Pandadrome_plateforme", 0, 186 * 1.6),
                [(-350, 0), (0, 0)])  # Coordonnées de départ
    if stage == "Cour d'honneur":
        return (Stage(stage,f"{stage}/Cour d'honneur_plateforme", -6, 220 * 1.65,
                      [(2, 186 * 1.7 + 8, 436, 4, (97, 87, 77)), (2, 186 * 1.7 - 226, 332, 4, (97, 87, 77))]),
                [(-200, 0), (200, 0)])
    if stage == "Chapelle":
        return (Stage(stage,f"{stage}/Chapelle_plateforme", 0, 235 * 1.65,
                      [(-202, 376 - 49 * 4 + 21, 45 * 4, 12, (67, 14, 6)),
                       (206, 376 - 49 * 4 + 21, 45 * 4, 12, (67, 14, 6)), (0, 60, 72 * 4, 12, (67, 14, 6))]),
                [(-200, -50), (200, -50)])
    if stage == "Salle d'info":
        return (Stage(stage,f"{stage}/Salle d'info_plateforme", 0, 308,
                      [(-276, 68, 192, 4, (0, 0, 0)),
                       (276, 68, 192, 4, (0, 0, 0))]),
                [(-200, -50), (200, -50)])
    if stage == "Salle de TP":
        return (Stage(stage,f"{stage}/Salle_de_TP_plateforme", 0, 308,
                      [(-398, 164, 268, 4, (200, 200, 200)),(398, 164, 268, 4, (200, 200, 200)),
                      (-530, 5, 268, 4, (200, 200, 200)),(530, 5, 268, 4, (200, 200, 200))]),
                [(-200, -50), (200, -50)])
    if stage == "Table de self":
        return (Stage(stage,f"{stage}/Table de self_plateforme", 0, 190,
                      [(-620, 293, 200, 4, (24, 47, 73)),
                      (620, 293, 200, 4, (24, 47, 73))]),
                [(-200, -50), (200, -50)])
