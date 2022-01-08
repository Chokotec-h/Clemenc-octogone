import pygame



icons ={
    "Balan":pygame.image.load("./DATA/Images/Sprites/Chars/Balan/icon.png"),
    "Joueur de air-president":pygame.image.load("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/icon.png"),
    "Millet":pygame.image.load("./DATA/Images/Sprites/Chars/None/icon.png"),
    "Gregoire":pygame.image.load("./DATA/Images/Sprites/Chars/None/icon.png"),
    "Reignaud":pygame.image.load("./DATA/Images/Sprites/Chars/None/icon.png"),
    "Rey":pygame.image.load("./DATA/Images/Sprites/Chars/None/icon.png"),
    "Pyro-Aubin":pygame.image.load("./DATA/Images/Sprites/Chars/None/icon.png"),
    "Kebab":pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/icon.png"),
    "Poissonnier":pygame.image.load("./DATA/Images/Sprites/Chars/None/icon.png"),
    "Renault":pygame.image.load("./DATA/Images/Sprites/Chars/None/icon.png"),
    "Isaac":pygame.image.load("./DATA/Images/Sprites/Chars/None/icon.png"),
}
icons64 ={
    "Balan":pygame.transform.scale(icons["Balan"],(64,64)),
    "Joueur de air-president":pygame.transform.scale(icons["Joueur de air-president"],(64,64)),
    "Millet":pygame.transform.scale(icons["Millet"],(64,64)),
    "Gregoire":pygame.transform.scale(icons["Gregoire"],(64,64)),
    "Reignaud":pygame.transform.scale(icons["Reignaud"],(64,64)),
    "Rey":pygame.transform.scale(icons["Rey"],(64,64)),
    "Pyro-Aubin":pygame.transform.scale(icons["Pyro-Aubin"],(64,64)),
    "Kebab":pygame.transform.scale(icons["Kebab"],(64,64)),
    "Poissonnier":pygame.transform.scale(icons["Poissonnier"],(64,64)),
    "Renault":pygame.transform.scale(icons["Renault"],(64,64)),
    "Isaac":pygame.transform.scale(icons["Isaac"],(64,64)),
}

# Forme : (sheet,((posx,posy,sizex,sizey),(posx...),...),time between frames,looped)
Balan = {
    "idle":("./DATA/Images/Sprites/Chars/Balan/Default/balan_idle.png",((10,2,12,30),(42,2,12,30),(74,4,12,28),(106,3,12,29)),5,True),
    "walk":("./DATA/Images/Sprites/Chars/Balan/Default/balan_walk.png",((7,2,15,30),(40,3,14,29),(70,3,16,29)),6,True),
    "run":("./DATA/Images/Sprites/Chars/Balan/Default/balan_run.png",((2,3,21,29),(34,3,22,29),(65,4,22,28),(99,4,20,28)),6,True),
    "jab":("./DATA/Images/Sprites/Chars/Balan/Default/balan_jab.png",((4,2,16,30),(36,2,20,30),(66,2,24,30),(99,2,22,30),(131,2,22,30),(164,4,21,28),(196,2,21,30),(228,2,21,30),(260,3,21,29),(292,2,21,30)),20,False),
    "uptilt":("./DATA/Images/Sprites/Chars/Balan/Default/balan_uptilt.png",((9,19,20,29),(36,21,26,27),(68,17,25,31),(99,17,20,31),(132,20,19,28),(169,18,14,30)),10,False),
    "jump":("./DATA/Images/Sprites/Chars/Balan/Default/balan_jumping.png",((5,6,20,26),(40,2,13,30),(63,1,14,29)),5,False),
    "fall":("./DATA/Images/Sprites/Chars/Balan/Default/balan_fall.png",((8,2,14,27),),1,False),
    "airdodge":("./DATA/Images/Sprites/Chars/Balan/Default/balan_idle.png",((10,2,12,30),(42,2,12,30),(74,4,12,28),(106,3,12,29)),5,True),
    "nair":("./DATA/Images/Sprites/Chars/Balan/Default/balan_nair.png",((8,1,14,29),(36,2,22,28),(68,2,22,27),(100,2,22,27),(139,2,12,27)),10,False),
}

BalanM = dict()
for s in Balan:
    BalanM[s] = (Balan[s][0].replace("Default","Masked"),Balan[s][1],Balan[s][2],Balan[s][3])

BalanJ = dict()
for s in Balan:
    BalanJ[s] = (Balan[s][0].replace("Default","Jedi"),Balan[s][1],Balan[s][2],Balan[s][3])

Air_President = {
    "idle":("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/Default/joueur_air_president_idle.png",((3,0,11,32),(19,2,11,30)),3,True),
    "walk":("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/Default/joueur_air_president_idle.png",((3,0,11,32),(19,2,11,30)),3,True),
    "run":("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/Default/joueur_air_president_idle.png",((3,0,11,32),(19,2,11,30)),3,True),
    "jump":("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/Default/joueur_air_president_idle.png",((3,0,11,32),(19,2,11,30)),3,True),
    "fall":("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/Default/joueur_air_president_idle.png",((3,0,11,32),(19,2,11,30)),3,True),
    "airdodge":("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/Default/joueur_air_president_idle.png",((3,0,11,32),(19,2,11,30)),3,True),

}

Nonesprite = {
    "idle":("./DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),
    "walk":("./DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),
    "run":("./DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),
    "jump":("./DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),
    "fall":("./DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),
    "airdodge":("./DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),

}

Kebab = {
    "idle":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_idle.png",((2,2,12,12),(16,1,12,13),(30,2,12,12),(44,3,12,11),(58,2,12,12),),6,True),
    "walk":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Walk.png",((2,2,12,12),(16,2,12,12),(30,2,12,12),(43,2,12,12),(57,2,12,12),(70,2,12,12)),8,True),
    "run":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Walk.png",((2,2,12,12),(16,2,12,12),(43,2,12,12),(57,2,12,12)),10,True),
    "jump":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Jump.png",((2,3,12,11),(16,1,12,14),(30,1,12,14),(44,1,12,11),(57,3,12,11)),10,False),
    "fall":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Jump.png",((57,3,12,11),),1,False),
    "airdodge":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Airdodge.png",((2,3,12,11),(16,1,12,14),(29,1,12,14),(43,1,9,14),(54,1,12,14),(67,1,12,14),(80,1,12,14),(93,1,9,14),(104,1,12,14),(117,1,12,14)),20,False),
    "dashattack":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_DashAttack.png",((2,2,12,12),(16,1,12,14),(29,1,12,14),(42,2,14,12),(57,2,14,12),(72,2,14,12),(89,1,12,14),(102,1,12,14),(116,2,14,12),(131,2,12,12)),12,True),

}


Training = {
    "idle":("./DATA/Images/Sprites/Misc/Training/Training.png",((0,0,12,30),),1,True),
    "walk":("./DATA/Images/Sprites/Misc/Training/Training.png",((0,0,12,30),),1,True),
    "run":("./DATA/Images/Sprites/Misc/Training/Training.png",((0,0,12,30),),1,True),
    "jump":("./DATA/Images/Sprites/Misc/Training/Training.png",((0,0,12,30),),1,True),
    "fall":("./DATA/Images/Sprites/Misc/Training/Training.png",((0,0,12,30),),1,True),
    "airdodge":("./DATA/Images/Sprites/Misc/Training/Training.png",((0,0,12,30),),1,True),

}
### Lien Nom/animation

animations = {
    "Balan":Balan,
    "BalanM":BalanM,
    "BalanJ":BalanJ,
    "Joueur de air-president":Air_President,
    "Millet":Nonesprite,
    "Gregoire":Nonesprite,
    "Reignaud":Nonesprite,
    "Rey":Nonesprite,
    "Pyro-Aubin":Nonesprite,
    "Kebab":Kebab,
    "Poissonnier":Nonesprite,
    "Renault":Nonesprite,
    "Isaac":Nonesprite,
    "Training":Training
}