import pygame

class Stage():
    def __init__(self) -> None:
        self.sprite = pygame.image.load("./Best Stage Ever.png").convert_alpha()
        self.mask  = pygame.mask.from_surface(self.sprite)
        self.rect = self.sprite.get_rect()
        
    def draw(self,window,cam):
        pos = [400,300]
        pos[0] = pos[0] - cam[0]
        pos[1] = pos[1] - cam[1]
        self.rect.move(self.rect.x-pos[0],self.rect.y-pos[1])
        window.blit(self.sprite,pos)
