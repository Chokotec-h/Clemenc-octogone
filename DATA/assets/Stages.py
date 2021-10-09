import pygame


class Stage:
    def __init__(self) -> None:
        # Sprite
        self.sprite = pygame.image.load("DATA/Images/Stages/Best Stage Ever.png").convert_alpha()
        # Rectangle
        self.rect = self.sprite.get_rect(center=(0,650))

    def draw(self, window):
        # Position réelle
        pos = [self.rect.x+800, self.rect.y+449]

        # Affichage du stage
        #self.rect.move(self.rect)
        window.blit(self.sprite, pos)
