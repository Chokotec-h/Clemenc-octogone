import pygame

def get_sprite(animation,newframe,right):
    positions = animation[1]
    time = animation[2]
    looped = animation[3]
    image = animation[0]
    if not right :
        image = image[0:-4]+"_l.png"
    image = pygame.image.load(image).convert_alpha()

    frame = round(newframe / (60/time))
    if frame >= len(positions):
        if looped :
            newframe = 0
            frame = 0
        else :
            frame = -1
            newframe = -1
    positions = positions[frame]
    return image,positions,newframe





smokesprite = [pygame.image.load(f"./DATA/Images/Sprites/Smoke/{i}.png") for i in range(1,6)]

class Smoke():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.duration = 20

    def draw(self,window):
        window.blit(smokesprite[self.duration//4-1],(self.x+800,self.y+450))
        self.duration -= 1







class Dash_Smoke():
    def __init__(self,x,y,right) -> None:
        self.x = x
        self.y = y
        self.life_time = 0
        self.right = right
        self.animation = ("./DATA/Images/Sprites/Misc/dash_smoke.png", ((0 * 32,0,32,32), (1 * 32,0,32,32), (2 * 32,0,32,32), (3 * 32,0,32,32), (4 * 32,0,32,32), (5 * 32,0,32,32), (6 * 32,0,32,32), (7 * 32,0,32,32), (8 * 32,0,32,32)), 30, False)
    
    def draw(self,window):
        drawing_sprite,size,self.life_time = get_sprite(self.animation,self.life_time,self.right)

        drawing_sprite = pygame.transform.scale(drawing_sprite,(round(drawing_sprite.get_size()[0]*4),round(drawing_sprite.get_size()[1]*4))) # Rescale
        size = [size[0]*4,size[1]*4,size[2]*4,size[3]*4] # Rescale
        pos = [self.x + 800 - size[2]/2, self.y-size[3] + 520] # Position réelle du sprite
        window.blit(drawing_sprite, pos,size) # on dessine le sprite

        if self.life_time >= 0 :
            self.life_time += 1