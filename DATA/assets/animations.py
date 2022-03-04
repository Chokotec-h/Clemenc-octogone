import pygame



icons ={
    "Balan":pygame.image.load("./DATA/Images/Sprites/Chars/Balan/icon.png"),
    "Joueur de air-president":pygame.image.load("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/icon.png"), "Spamton":pygame.image.load("./DATA/Images/Sprites/Chars/Joueur_de_Air_President/icon_S.png"),
    "Millet":pygame.image.load("./DATA/Images/Sprites/Chars/None/icon.png"),
    "Gregoire":pygame.image.load("./DATA/Images/Sprites/Chars/Gregoire/icon.png"),
    "Reignaud":pygame.image.load("./DATA/Images/Sprites/Chars/None/icon.png"),
    "Rey":pygame.image.load("./DATA/Images/Sprites/Chars/None/icon.png"),
    "Pyro-Aubin":pygame.image.load("./DATA/Images/Sprites/Chars/Pyro_Aubin/icon.png"),
    "Kebab":pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/icon.png"),
    "Poissonnier":pygame.image.load("./DATA/Images/Sprites/Chars/None/icon.png"),
    "Renault":pygame.image.load("./DATA/Images/Sprites/Chars/Renault/icon.png"),
    "Isaac":pygame.image.load("./DATA/Images/Sprites/Chars/None/icon.png"),
}
icons64 ={
    "Balan":pygame.transform.scale(icons["Balan"],(64,64)),
    "Joueur de air-president":pygame.transform.scale(icons["Joueur de air-president"],(64,64)), "Spamton":pygame.transform.scale(icons["Spamton"],(64,64)),
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

Nonesprite = {
    "idle":("./DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),
    "walk":("./DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),
    "run":("./DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),
    "jump":("./DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),
    "fall":("./DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),
    "airdodge":("./DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),

}

Renault = {
    "idle":("./DATA/Images/Sprites/Chars/Renault/Default/idle.png",((2,1,16,35),),1,True),
    "walk":("./DATA/Images/Sprites/Chars/Renault/Default/idle.png",((2,1,16,35),),1,True),
    "run":("./DATA/Images/Sprites/Chars/Renault/Default/idle.png",((2,1,16,35),),1,True),
    "jump":("./DATA/Images/Sprites/Chars/Renault/Default/idle.png",((2,1,16,35),),1,True),
    "fall":("./DATA/Images/Sprites/Chars/Renault/Default/idle.png",((2,1,16,35),),1,True),
    "airdodge":("./DATA/Images/Sprites/Chars/Renault/Default/idle.png",((2,1,16,35),),1,True),

}

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

Gregoire = {
    "idle":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_idle.png",((1,0,17,36),(18,1,18,35),(36,0,17,36),(55,1,16,35)),8,True),
    "walk":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_walk.png",((1,0,16,36),(18,0,16,36),(34,0,20,36),(54,0,18,36),(72,0,16,36),(88,0,16,36),(106,0,16,36)),8,True),
    "run":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_run.png",((1,0,16,36),(21,0,20,36),(50,0,18,36),(73,0,20,36),(96,0,24,36),(128,0,18,36)),12,True),
    "jump":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_jump.png",((3,2,17,34),(25,1,15,35),(46,0,16,37),(63,1,21,36)),12,False),
    "fall":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_jump.png",((63,1,21,36),),8,True),
    "airdodge":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_parry_airdodge.png",((1,0,15,36),(20,0,17,36),(39,0,17,36)),8,False),
    "jab":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_jab.png",((1,0,17,36),(19,0,19,36),(38,0,19,36),(60,0,19,35),(79,0,17,36),(97,0,18,36),(120,0,16,36),(136,0,18,36)),20,True),
    "nair":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_nair.png",((0,0,19,36),(20,0,14,36),(37,0,15,36),(53,0,15,35),(70,0,21,36),(91,0,18,36)),12,False),
    "dashattack":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_dashattack.png",((1,2,18,36),(21,4,18,34),(42,9,25,29),(69,20,18,18),(89,20,18,18),(110,20,18,18),(130,20,18,18),(150,20,18,18),(170,20,18,18),(191,20,18,18),(211,13,29,25)),20,False),
    "downb_charge":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_downBCharge.png",((1,0,29,36),(30,0,32,36),(63,0,26,36)),10,False),
    "downb_release":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_downBRelease.png",((0,0,34,36),(37,0,32,36),(69,0,36,36),(106,0,34,36),(146,0,34,36)),10,False),
    "dsmash":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_dsmash.png",((3,0,20,36),(28,0,17,36),(48,0,17,36),(65,0,18,36),(83,0,18,36)),9,False),
    "dtilt":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_dtilt.png",((2,1,21,35),(26,3,17,33),(43,3,16,33),(60,6,17,30),(80,3,14,33)),10,False),
    "fair":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_fair.png",((2,0,14,36),(21,0,14,36),(40,0,14,36),(62,0,14,36),(79,0,22,36),(106,0,30,36),(136,0,24,36),(160,0,16,36),(180,0,14,36)),20,False),
    "fair2":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_fair2.png",((0,0,14,36),(15,0,37,36)),0.75,False),
    "fsmash":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_fsmash.png",((2,0,21,36),(27,0,20,36),(50,0,17,36),(75,0,16,36),(101,0,23,36),(126,0,23,36),(153,0,23,36),(179,0,23,36),(209,0,23,36),(232,0,17,36)),10,False),
    "ftilt":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_ftilt.png",((2,0,21,36),(31,0,14,36),(57,0,19,36),(84,0,19,36)),10,False),
    "sideB":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_la_mort.png",((1,0,20,36),(24,0,28,36),(54,0,28,36),(85,0,28,36),(117,0,21,36)),10,False),
    "neutralB":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_neutralB.png",((4,0,16,36),(23,0,17,36),(44,0,18,36),(64,0,17,36),(82,0,16,36)),10,False),
    "uair":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_uair.png",((2,0,21,36),(27,0,16,36),(44,0,15,36),(60,0,15,36)),10,False),
    "usmash":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_usmash.png",((1,2,18,36),(21,4,18,34),(39,4,21,34),(60,4,18,34),(78,1,14,37)),10,False),
    "utilt":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_utilt.png",((1,6,27,30),(29,0,17,36),(54,5,25,31),(83,0,14,36)),10,False),
    "dair_dive":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_dair_dive.png",((4,6,25,31),(31,8,25,29),(63,12,29,25),(97,0,14,37)),10,False),
    "dair_fall":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_dair_fall.png",((6,0,14,37),(25,12,30,25),(61,7,25,29),(93,9,29,25),(125,2,21,36)),15,False),
    "dair_ground":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_dair_ground.png",((6,0,14,37),(25,12,29,25),(61,8,25,29),(94,4,18,34)),10,False),
    "bair":("./DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_bair.png",((2,0,21,36),(25,0,22,36),(48,0,23,36),(78,0,14,36),(99,0,21,36),(122,0,26,36),(148,0,16,36)),10,False),
}

Pyro_Aubin = {
    "idle":("./DATA/Images/Sprites/Chars/Pyro_Aubin/Aubin_idle.png",((14,1,22,46),(62,2,26,46),(108,4,29,44),(158,2,26,46)),8,True),
    "walk":("./DATA/Images/Sprites/Chars/Pyro_Aubin/Aubin_idle.png",((14,1,22,47),(62,2,26,46),(108,4,29,44),(158,2,26,46)),8,True),
    "run":("./DATA/Images/Sprites/Chars/Pyro_Aubin/Aubin_idle.png",((14,1,22,47),(62,2,26,46),(108,4,29,44),(158,2,26,46)),8,True),
    "jump":("./DATA/Images/Sprites/Chars/Pyro_Aubin/Aubin_jump.png",((7,4,31,44),(55,2,30,46),(101,1,38,46)),8,False),
    "fall":("./DATA/Images/Sprites/Chars/Pyro_Aubin/Aubin_jump.png",((101,1,38,46),),8,False),
    "airdodge":("./DATA/Images/Sprites/Chars/Pyro_Aubin/Aubin_idle.png",((14,1,22,47),(62,2,26,46),(108,4,29,44),(158,2,26,46)),8,True),

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
    "downb":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_DownB.png",((1,2,17,12),(19,2,17,12),(37,2,16,12),(54,2,15,12),(70,2,15,12),(86,2,14,12),(101,2,14,12),(116,2,12,12),(129,2,12,12)),20,False),
    "downb_no":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_DownB_echec.png",((1,2,13,12),(15,2,13,12),(29,2,13,12),(42,2,12,12)),20,False),
    "upb":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_UpB.png",((2,2,12,12),(16,2,12,12),(29,2,12,12),(42,2,11,12),(54,2,12,12),(67,2,12,12),(80,2,12,12),(93,2,12,12)),18,False),
    "jab":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Jab.png",((2,2,12,12),(16,2,12,12),(29,2,12,12),(42,2,13,12),(55,2,12,12)),20,False),
    "jab2":("./DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Jab2.png",((1,2,13,12),(15,2,14,12),(30,2,15,12),(46,2,13,12),(59,2,12,12)),20,False),

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
    "Gregoire":Gregoire,
    "Reignaud":Nonesprite,
    "Rey":Nonesprite,
    "Pyro-Aubin":Pyro_Aubin,
    "Kebab":Kebab,
    "Poissonnier":Nonesprite,
    "Renault":Renault,
    "Isaac":Nonesprite,
    "Training":Training
}