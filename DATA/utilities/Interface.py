from typing import Text
import pygame

standard = pygame.image.load("DATA/Images/Menu/Button.png")

def resize(w,h,width,height,basewidth=1600,baseheight=900):
    return (round(w*width/basewidth),round(h*height/baseheight))

def resize_t(s,width,height,basewidth=1600,baseheight=900):
    return (round(s[0]*width/basewidth),round(s[1]*height/baseheight))

class Texte:
    def __init__(self,text,sysfont,color,x,y,show=True,format_ = "center"):
        self.x = x
        self.y = y
        self.show = show

        sysfont = [sysfont[i] for i in range(len(sysfont))]
        sysfont[1] = round(sysfont[1])
        self.font = pygame.font.SysFont(sysfont[0],sysfont[1], bold = sysfont[2], italic = sysfont[3])
        self.text= text
        self.color = color
        self.format = format_
        text = self.font.render(self.text,1,self.color)
        self.width = text.get_size()[0]
    
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
    def __init__(self,text,font,image,x,y,size,show=True) :
        self.x = x
        self.y = y
        w,h = size

        font = ("arial",font[1]*0.8,font[2],font[3])
        self.textobject = Texte(text,font,(0,0,0),self.x,self.y)
        if isinstance(image,str):
            self.image = pygame.image.load(image)
        else :
            self.image = image
        self.width = round(w)
        self.height = round(h)
        self.changeImage(image)
        self.resize(w,h)

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

    def resize(self,sizex,sizey):
        self.image = pygame.transform.scale(self.image,(sizex,sizey))
        self.width = sizex
        self.height = sizey
        self.rect = pygame.Rect(self.x-self.width//2,self.y-self.height//2,self.width,self.height)

    def changeImage(self,image):
        if isinstance(image,str):
            self.image = pygame.image.load(image)
        else :
            self.image = image
        self.image = pygame.transform.scale(self.image,(self.width,self.height))

    def draw(self,win):
        if self.show :
            win.blit(self.image,self.rect)
            self.textobject.draw(win)
