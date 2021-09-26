import pygame

# Forme : (sheet,((posx,posy,sizex,sizey),(posx...),...),time between frames,looped)
Balan = {
    "idle":("./DATA/Images/Sprites/Balan/Default/balan_idle.png",((10,2,12,30),(42,2,12,30),(74,4,12,28),(106,3,12,29)),5,True),
    "walk":("./DATA/Images/Sprites/Balan/Default/balan_walk.png",((7,2,15,30),(40,3,14,29),(70,3,16,29)),5,True),
    "run":("./DATA/Images/Sprites/Balan/Default/balan_run.png",((2,3,21,29),(34,3,22,29),(34,4,22,28),(99,4,20,28)),5,True)
}

animations = {
    "Balan":Balan
}

def get_sprite(animation,char,newframe,right):
    image = animations[char][animation]
    positions = image[1]
    time = image[2]
    looped = image[3]
    image = image[0]
    if not right :
        image = image[0:-4]+"_l.png"
    image = pygame.image.load(image).convert_alpha()
    
    frame = newframe // time
    if frame >= len(positions):
        if looped :
            newframe = 0
            frame = 0
        else :
            frame = -1
    positions = positions[frame]
    return image,positions,newframe