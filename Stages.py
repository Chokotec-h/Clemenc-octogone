import pygame


class Stage:
    def __init__(self) -> None:
        # Sprite
        self.sprite = pygame.image.load("DATA/Images/Stages/Best Stage Ever.png").convert_alpha()
        # Masque, permet de détecter le sprite pour les collisions
        self.mask = pygame.mask.from_surface(self.sprite)
        # Rectangle
        self.rect = self.sprite.get_rect(topleft=(-100,0))

    def draw(self, window, cam):
        # Position réelle
        pos = [300, 300]
        pos[0] = pos[0] - cam[0]
        pos[1] = pos[1] - cam[1]
        # Affichage du stage
        self.rect.move(self.rect.x - pos[0], self.rect.y - pos[1])
        window.blit(self.sprite, pos)
