import pygame



icons ={
    "Balan":pygame.image.load("./DATA/Images/Sprites/Chars/Balan/icon.png"),
    "Joueur de air-president":pygame.image.load("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/icon.png"), "Spamton":pygame.image.load("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/Spamton/icon.png"),
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
    "Joueur de air-president":pygame.transform.scale(icons["Joueur de air-president"],(64,64)), "Spamton":pygame.image.load("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/Spamton/icon.png"),
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

Spamton = {
    "idle":("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/Spamton/spamton_idle.png",((1,1,16,31),(17,2,16,30)),2,True),
    "walk":("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/Spamton/spamton_idle.png",((1,1,16,31),(17,2,16,30)),2,True),
    "run":("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/Spamton/spamton_idle.png",((1,1,16,31),(17,2,16,30)),2,True),
    "jump":("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/Spamton/spamton_idle.png",((1,1,16,31),(17,2,16,30)),2,True),
    "fall":("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/Spamton/spamton_idle.png",((1,1,16,31),(17,2,16,30)),2,True),
    "airdodge":("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/Spamton/spamton_idle.png",((1,1,16,31),(17,2,16,30)),2,True),

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
    "nair":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Jump.png",((57,3,12,11),),1,False),
    "fair":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Fair.png",((2,3,12,12),(15,2,12,12),(28,2,12,12),(41,2,12,12),(54,2,13,12),(68,2,13,12),(82,2,13,12),(96,2,13,12),(110,2,12,12)),20,False),
    "dair":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Dair.png",((2,3,12,12),(15,1,12,12),(28,1,12,13),(41,1,12,12),(54,1,12,12),(67,1,12,13),(80,1,12,12),(93,1,12,12),(106,1,12,13),(119,1,12,14),(132,1,12,14),(145,1,12,12),(158,1,12,11)),30,False),
    "bair":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Bair.png",((2,3,12,9),(17,3,12,9),(31,3,12,12),(44,2,12,13),(57,2,14,13),(72,6,19,9),(92,6,18,9),(112,6,16,9),(129,6,14,9),(146,6,12,9),(159,6,12,9),(172,6,12,9)),30,False),
    "uair":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Uair.png",((3,20,12,9),(17,18,12,11),(30,16,12,13),(43,12,12,17),(56,4,12,25),(69,1,12,28),(82,7,12,22),(95,12,12,17),(108,19,12,10),(121,20,12,9)),30,False),
    "utilt":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Utilt.png",((2,17,12,12),(16,16,12,13),(30,12,12,17),(44,8,12,21),(57,2,12,27),(70,2,12,27),(83,8,12,21),(97,12,12,17),(111,16,12,13),(125,17,12,12)),30,False),
    "dtilt":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Dtilt.png",((2,3,12,11),(15,3,12,11),(28,3,12,11),(41,3,12,10),(54,3,12,10),(67,3,12,10),(80,3,12,10),(93,3,12,10),(106,3,12,11)),30,False),
    "ftilt":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Ftilt.png",((2,3,12,11),(16,3,15,11),(33,3,16,11),(50,3,18,11),(69,3,16,11),(86,3,15,11),(103,3,12,11)),20,False),

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
    "Joueur de air-president":Air_President,"Spamton":Spamton,
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