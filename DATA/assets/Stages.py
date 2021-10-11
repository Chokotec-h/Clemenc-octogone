import pygame

class Stage():
    def __init__(self,platforms=[]) -> None:
        self.mainplat = MainPlat("DATA/Images/Stages/Best Stage Ever.png")
        # Platforms : [(x,y,l,h,color),...]
        self.plats = []
        for p in platforms:
            self.plats.append(Platform(p[0],p[1],p[2],p[3],p[4]))
    
    def draw(self,window):
        self.mainplat.draw(window)
        for p in self.plats :
            p.draw(window)

class MainPlat:
    def __init__(self,sprite) -> None:
        # Sprite
        self.sprite = pygame.image.load(sprite).convert_alpha()
        # Rectangle
        self.rect = self.sprite.get_rect(center=(0,650))

    def draw(self, window):
        # Position réelle
        pos = [self.rect.x+800, self.rect.y+449]

        # Affichage du stage
        #self.rect.move(self.rect)
        window.blit(self.sprite, pos)

class Platform():
    def __init__(self,x,y,l,h,color) -> None:
        # Rectangle
        self.rect = pygame.Rect(x,y,l,h)
        self.color = color

    def draw(self, window):
        # Position réelle
        pos = [self.rect.x+800, self.rect.y+449]
        pygame.draw.rect(window,self.color,(pos[0],pos[1],self.rect.w,self.rect.h))