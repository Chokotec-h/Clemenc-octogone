import pygame
from DATA.assets.animations import animations

def get_sprite(animation,char,newframe,right):
    image = animations[char][animation]
    positions = image[1]
    time = image[2]
    looped = image[3]
    image = image[0]
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
    positions = positions[frame]
    return image,positions,newframe