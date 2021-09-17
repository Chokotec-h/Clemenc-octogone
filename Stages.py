import pygame

class Stage():
    def __init__(self) -> None:
        self.sprite = pygame.image.load("./Stages/Best Stage Ever.png")
        
    def draw(self,window,cam):
        pos = [400,850]
        pos[0] = pos[0] - cam[0] - self.sprite.get_size()[0]//2
        pos[1] = pos[1] - cam[1]
        window.blit(self.sprite,pos)
