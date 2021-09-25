import pygame

smokesprite = [pygame.image.load(f"./DATA/Images/Sprites/Smoke/{i}.png") for i in range(1,6)]

class Smoke():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.duration = 20

    def draw(self,window):
        window.blit(smokesprite[self.duration//4-1],(self.x+800,self.y+450))
        self.duration -= 1