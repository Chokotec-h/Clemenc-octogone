import pygame

# Forme : (sheet,((posx,posy,sizex,sizey),(posx...),...),time between frames,looped)
Balan = {
    "idle":("./DATA/Images/Sprites/Balan/Default/balan_idle.png",((10,2,12,30),(42,2,12,30),(74,4,12,28),(106,3,12,29)),5,True),
    "walk":("./DATA/Images/Sprites/Balan/Default/balan_walk.png",((7,2,15,30),(40,3,14,29),(70,3,16,29)),6,True),
    "run":("./DATA/Images/Sprites/Balan/Default/balan_run.png",((2,3,21,29),(34,3,22,29),(65,4,22,28),(99,4,20,28)),6,True),
    "jab":("./DATA/Images/Sprites/Balan/Default/balan_jab.png",((4,2,16,30),(36,2,20,30),(66,2,24,30),(99,2,22,30),(131,2,22,30),(164,4,21,28),(196,2,21,30),(228,2,21,30),(260,3,21,29),(292,2,21,30)),20,False),
    "uptilt":("./DATA/Images/Sprites/Balan/Default/balan_uptilt.png",((9,19,20,29),(36,21,26,27),(68,17,25,31),(99,17,20,31),(132,20,19,28),(169,18,14,30)),10,False),
    "jump":("./DATA/Images/Sprites/Balan/Default/balan_jumping.png",((5,6,20,26),(40,2,13,30),(63,1,14,29)),5,False),
    "fall":("./DATA/Images/Sprites/Balan/Default/balan_fall.png",((8,2,14,27),),1,False),
    "airdodge":("./DATA/Images/Sprites/Balan/Default/balan_idle.png",((10,2,12,30),(42,2,12,30),(74,4,12,28),(106,3,12,29)),5,True),
}

BalanM = dict()
for s in Balan:
    BalanM[s] = (Balan[s][0].replace("Default","Masked"),Balan[s][1],Balan[s][2],Balan[s][3])

BalanJ = dict()
for s in Balan:
    BalanJ[s] = (Balan[s][0].replace("Default","Jedi"),Balan[s][1],Balan[s][2],Balan[s][3])

AirPresident = {
    "idle":("./DATA/Images/Sprites/Ca_ressemble_a_rien_mais_faut_que_jaie_un_truc_pour_coder_vite_fait.png",((0,0,12,30),),1,True),
    "walk":("./DATA/Images/Sprites/Ca_ressemble_a_rien_mais_faut_que_jaie_un_truc_pour_coder_vite_fait.png",((0,0,12,30),),1,True),
    "run":("./DATA/Images/Sprites/Ca_ressemble_a_rien_mais_faut_que_jaie_un_truc_pour_coder_vite_fait.png",((0,0,12,30),),1,True),
    "jump":("./DATA/Images/Sprites/Ca_ressemble_a_rien_mais_faut_que_jaie_un_truc_pour_coder_vite_fait.png",((0,0,12,30),),1,True),
    "fall":("./DATA/Images/Sprites/Ca_ressemble_a_rien_mais_faut_que_jaie_un_truc_pour_coder_vite_fait.png",((0,0,12,30),),1,True),
    "airdodge":("./DATA/Images/Sprites/Ca_ressemble_a_rien_mais_faut_que_jaie_un_truc_pour_coder_vite_fait.png",((0,0,12,30),),1,True),
}

Nonesprite = {
    "idle":("./DATA/Images/Sprites/Nameless_sprite",((0,0,12,30),),1,True),
    "walk":("./DATA/Images/Sprites/Nameless_sprite",((0,0,12,30),),1,True),
    "run":("./DATA/Images/Sprites/Nameless_sprite",((0,0,12,30),),1,True),
    "jump":("./DATA/Images/Sprites/Nameless_sprite",((0,0,12,30),),1,True),
    "fall":("./DATA/Images/Sprites/Nameless_sprite",((0,0,12,30),),1,True),
    "airdodge":("./DATA/Images/Sprites/Nameless_sprite",((0,0,12,30),),1,True),

}

animations = {
    "Balan":Balan,
    "BalanM":BalanM,
    "BalanJ":BalanJ,
    "Air President":AirPresident,
    "Millet":Nonesprite,
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
    
    frame = round(newframe / (60/time))
    if frame >= len(positions):
        if looped :
            newframe = 0
            frame = 0
        else :
            frame = -1
    positions = positions[frame]
    return image,positions,newframe