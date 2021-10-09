import pygame
class Texte:
    def __init__(self,text,sysfont,color,x,y,l,show=True,format_ = "center"):
        self.x = x
        self.y = y
        self.show = show
        ratio = l/800

        sysfont = [sysfont[i] for i in range(len(sysfont))]
        sysfont[1] = round(sysfont[1] * ratio)
        self.font = pygame.font.SysFont(sysfont[0],sysfont[1], bold = sysfont[2], italic = sysfont[3])
        self.text= text
        self.color = color
        self.format = format_
    
    def draw(self,win):
        text = self.font.render(self.text,1,self.color)
        self.width = text.get_size()[0]
        self.height = text.get_size()[1]
        if self.format == "center":
            win.blit(text,(self.x - self.width//2 , self.y - self.height//2))
        elif self.format == "left":
            win.blit(text,(self.x , self.y - self.height//2))
        elif self.format == "right":
            win.blit(text,(self.x - self.width , self.y - self.height//2))
        else :
            win.blit(text,(self.x , self.y))

class Button :
    def __init__(self,image,x,y,l,show=True) :
        self.x = x
        self.y = y
        self.ratio = l/800

        self.changeImage(image)

        self.show = show
        
    def is_focused(self):
        mouse = pygame.mouse.get_pos()
        if mouse[0] >= self.rect.left and mouse[0] <= self.rect.left + self.width :
            if mouse[1] >= self.rect.top and mouse[1] <= self.rect.top + self.height :
                return True
        return False

    def is_clicked(self,mousedown) :
        if self.is_focused():
            if mousedown :   
                return True
        return False
        
    def changeImage(self,image):
        self.image = image
        self.width = round(self.image.get_size()[0] * self.ratio)
        self.height = round(self.image.get_size()[1] * self.ratio)
        self.rect = pygame.Rect(self.x-self.width//2,self.y-self.height//2,self.width,self.height)
    
    def draw(self,win):
        if self.show :
            win.blit(self.image,self.rect)
