import pygame

from DATA.utilities.Interface import resize
from DATA.utilities.functions import *



icons ={
    "Balan":pygame.image.load("DATA/Images/Sprites/Chars/Balan/icon.png"),"BalanM":pygame.image.load("DATA/Images/Sprites/Chars/Balan/Masked/icon.png"),
    "Joueur de air-president":pygame.image.load("DATA/Images/Sprites/Chars/Joueur_de_Air_President/icon.png"), "Spamton":pygame.image.load("DATA/Images/Sprites/Chars/Joueur_de_Air_President/icon_S.png"),
    "Millet":pygame.image.load("DATA/Images/Sprites/Chars/Millet/icon.png"), "Bowser":pygame.image.load("DATA/Images/Sprites/Chars/Millet/Bowser/icon.png"),
    "Gregoire":pygame.image.load("DATA/Images/Sprites/Chars/Gregoire/icon.png"),
    "Reignaud":pygame.image.load("DATA/Images/Sprites/Chars/Reignaud/icon.png"),
    "Rey":pygame.image.load("DATA/Images/Sprites/Chars/None/icon.png"),
    "Pyro-Aubin":pygame.image.load("DATA/Images/Sprites/Chars/Pyro_Aubin/icon.png"),
    "Kebab":pygame.image.load("DATA/Images/Sprites/Chars/Kebab/icon.png"),
    "Poissonnier":pygame.image.load("DATA/Images/Sprites/Chars/None/icon.png"),
    "Renault":pygame.image.load("DATA/Images/Sprites/Chars/Renault/icon.png"),
    "Gourmelen":pygame.image.load("DATA/Images/Sprites/Chars/None/icon.png"),
    "Journault":pygame.image.load("DATA/Images/Sprites/Chars/None/icon.png"),
    "Le Berre":pygame.image.load("DATA/Images/Sprites/Chars/None/icon.png"),
    "EnglishTeacher":pygame.image.load("DATA/Images/Sprites/Chars/None/icon.png"),
    "Thevenet":pygame.image.load("DATA/Images/Sprites/Chars/None/icon.png"),
    #"Isaac":pygame.image.load("DATA/Images/Sprites/Chars/None/icon.png"),
}
icons64 ={
    "Balan":pygame.transform.scale(icons["Balan"],resize(64,64,width,height)),"BalanM":pygame.transform.scale(icons["BalanM"],resize(64,64,width,height)),
    "Joueur de air-president":pygame.transform.scale(icons["Joueur de air-president"],resize(64,64,width,height)), "Spamton":pygame.transform.scale(icons["Spamton"],resize(64,64,width,height)),
    "Millet":pygame.transform.scale(icons["Millet"],resize(64,64,width,height)), "Bowser":pygame.transform.scale(icons["Bowser"],resize(64,64,width,height)),
    "Gregoire":pygame.transform.scale(icons["Gregoire"],resize(64,64,width,height)),
    "Reignaud":pygame.transform.scale(icons["Reignaud"],resize(64,64,width,height)),
    "Rey":pygame.transform.scale(icons["Rey"],resize(64,64,width,height)),
    "Pyro-Aubin":pygame.transform.scale(icons["Pyro-Aubin"],resize(64,64,width,height)),
    "Kebab":pygame.transform.scale(icons["Kebab"],resize(64,64,width,height)),
    "Poissonnier":pygame.transform.scale(icons["Poissonnier"],resize(64,64,width,height)),
    "Renault":pygame.transform.scale(icons["Renault"],resize(64,64,width,height)),
    "Gourmelen":pygame.transform.scale(icons["Gourmelen"],resize(64,64,width,height)),
    "Journault":pygame.transform.scale(icons["Journault"],resize(64,64,width,height)),
    "Le Berre":pygame.transform.scale(icons["Le Berre"],resize(64,64,width,height)),
    "EnglishTeacher":pygame.transform.scale(icons["EnglishTeacher"],resize(64,64,width,height)),
    "Thevenet":pygame.transform.scale(icons["Thevenet"],resize(64,64,width,height)),
    #"Isaac":pygame.transform.scale(icons["Isaac"],resize(64,64,width,height)),
}

# Forme : (sheet,((posx,posy,sizex,sizey),(posx...),...),time between frames,looped)

Nonesprite = {
    "idle":("DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),
    "walk":("DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),
    "run":("DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),
    "jump":("DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),
    "fall":("DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),
    "airdodge":("DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True),

}

None_Journault = Nonesprite
None_Journault["UpB0"] = ("DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True)
None_Journault["UpB1"] = ("DATA/Images/Sprites/Chars/None/Nameless_sprite90.png",((0,0,30,12),),1,True)
None_Journault["UpB2"] = ("DATA/Images/Sprites/Chars/None/Nameless_sprite.png",((0,0,12,30),),1,True)
None_Journault["UpB3"] = ("DATA/Images/Sprites/Chars/None/Nameless_sprite90.png",((0,0,30,12),),1,True)

Reignaud = {
    "idle":("DATA/Images/Sprites/Chars/Reignaud/Default/Idle.png",((1,1,13,35),(21,2,13,34),(40,1,13,35)),2,True),
    "walk":("DATA/Images/Sprites/Chars/Reignaud/Default/Walk.png",((4,1,15,35),(28,1,17,35),(55,1,19,34),(86,1,13,35),(104,1,14,35),(122,1,16,35)),8,True),
    "run":("DATA/Images/Sprites/Chars/Reignaud/Default/Run.png",((4,1,15,35),(27,1,18,35),(52,1,24,35),(86,1,13,35),(103,1,15,35),(121,1,19,35)),10,True),
    "jump":("DATA/Images/Sprites/Chars/Reignaud/Default/Jump.png",((0,5,15,31),(19,3,17,33),(39,2,13,34)),12,False),
    "fall":("DATA/Images/Sprites/Chars/Reignaud/Default/Jump.png",((57,1,15,35),),1,True),
    "airdodge":("DATA/Images/Sprites/Chars/Reignaud/Default/Idle.png",((1,1,13,35),),1,True),
    "jab":("DATA/Images/Sprites/Chars/Reignaud/Default/Jab.png",((1,1,13,35),(18,1,14,35),(38,1,14,35),(54,1,14,35),(75,1,13,35)),10,False),
    "utilt":("DATA/Images/Sprites/Chars/Reignaud/Default/Utilt.png",((20,1,16,35),(39,1,16,35),(59,1,16,35),(79,1,18,35),(101,1,16,35),(122,1,16,35)),16,True),
    "dtilt":("DATA/Images/Sprites/Chars/Reignaud/Default/DTilt.png",((1,1,13,35),(17,1,13,35),(33,1,15,35),(49,1,17,35),(69,1,13,35),(85,1,13,35)),16,False),
    "ftilt":("DATA/Images/Sprites/Chars/Reignaud/Default/Ftilt.png",((1,1,16,35),(20,1,17,35),(40,1,16,35)),4,False),
    "fsmash":("DATA/Images/Sprites/Chars/Reignaud/Default/FSmash.png",((1,1,13,35),(18,1,15,35),(36,1,23,35)),6,False),
    "usmash":("DATA/Images/Sprites/Chars/Reignaud/Default/USmash.png",((1,1,16,35),(20,1,17,35),(40,1,16,35)),6,False),
    "dsmash":("DATA/Images/Sprites/Chars/Reignaud/Default/DSmash.png",((1,1,13,35),(27,1,17,35),(53,1,19,35),(83,1,28,35),(121,1,44,35),(182,1,19,35)),8,False),
    "dashattack":("DATA/Images/Sprites/Chars/Reignaud/Default/DashAttack.png",((1,1,13,35),(19,1,17,35)),8,False),
    "dair":("DATA/Images/Sprites/Chars/Reignaud/Default/Dair.png",((1,1,13,35),(23,1,17,33),(43,1,15,31),(63,1,15,35),(83,1,14,35)),8,False),
    "bair":("DATA/Images/Sprites/Chars/Reignaud/Default/Bair.png",((1,1,13,35),(21,1,14,35),(42,1,17,35),(64,1,17,35),(83,1,21,35),(108,1,16,35),(131,1,13,35)),12,False),
    "fair":("DATA/Images/Sprites/Chars/Reignaud/Default/Fair.png",((0,1,14,35),(22,1,17,35),(44,1,13,35),(68,1,15,35),(85,1,14,35)),10,False),
    "uair":("DATA/Images/Sprites/Chars/Reignaud/Default/Uair.png",((2,1,12,35),(24,1,13,35),(45,1,14,35),(60,1,13,35)),11,False),
    "nair":("DATA/Images/Sprites/Chars/Reignaud/Default/Nair.png",((5,4,19,36),(27,4,24,36),(52,4,25,36),(105,0,21,44),(137,0,17,44),(161,0,23,44),(190,0,24,44),(218,0,23,44),(242,0,25,44),(295,0,21,44),(321,0,17,44),(346,0,17,44),(372,0,16,44),(389,0,13,44)),25,False),
    "sideB":("DATA/Images/Sprites/Chars/Reignaud/Default/SideB.png",((0,1,15,35),(28,1,16,35),(47,1,19,35),(67,1,25,35)),11,False),
    "UpB0":("DATA/Images/Sprites/Chars/Reignaud/Default/UpB.png",((19,2,17,33),(0,4,16,31),(19,2,17,33),(39,1,13,34)),11,False),
    "UpB1":("DATA/Images/Sprites/Chars/Reignaud/Default/UpB1.png",((19,2,17,37),(0,4,16,35),(19,2,17,37),(39,1,13,34)),11,False),
    "UpB2":("DATA/Images/Sprites/Chars/Reignaud/Default/UpB2.png",((19,2,17,41),(0,4,16,39),(19,2,17,41),(39,1,13,34)),11,False),
    "UpB3":("DATA/Images/Sprites/Chars/Reignaud/Default/UpB3.png",((19,2,17,45),(0,4,16,43),(19,2,17,45),(39,1,13,34)),11,False),
    "UpB4":("DATA/Images/Sprites/Chars/Reignaud/Default/UpB4.png",((19,2,17,49),(0,4,16,47),(19,2,17,49),(39,1,13,34)),11,False),
    "DownB":("DATA/Images/Sprites/Chars/Reignaud/Default/DownB.png",((0,1,12,35),(16,1,12,35)),2,False),
    "NeutralB":("DATA/Images/Sprites/Chars/Reignaud/Default/NeutralB.png",((2,1,30,35),(52,1,30,35),(96,1,30,35),(142,1,32,35),(176,1,35,35),(219,1,12,35)),8,False),
    "Counter":("DATA/Images/Sprites/Chars/Reignaud/Default/Counter.png",((2,1,12,35),(21,1,18,35),(45,1,18,35),(69,1,21,35)),12,False),

}

# Poissonnier = {
#     "idle":("DATA/Images/Sprites/Chars/Poissonnier/Default/Idle.png",((0,2,13,34),),2,True),
#     "walk":("DATA/Images/Sprites/Chars/Poissonnier/Default/Idle.png",((0,2,13,34),),1,True),
#     "run":("DATA/Images/Sprites/Chars/Poissonnier/Default/Idle.png",((0,2,13,34),),1,True),
#     "jump":("DATA/Images/Sprites/Chars/Poissonnier/Default/Idle.png",((0,2,13,34),),1,True),
#     "fall":("DATA/Images/Sprites/Chars/Poissonnier/Default/Idle.png",((0,2,13,34),),1,True),
#     "airdodge":("DATA/Images/Sprites/Chars/Poissonnier/Default/Idle.png",((0,2,13,34),),1,True),

# }

Renault = {
    "idle":("DATA/Images/Sprites/Chars/Renault/Default/Idle.png",((2,1,14,35),(21,1,14,35),(42,3,14,33),(59,2,14,34)),9,True),
    "walk":("DATA/Images/Sprites/Chars/Renault/Default/walk.png",((2,1,16,35),(22,2,16,34),(40,1,14,35),(56,1,14,35),(74,1,14,35),(95,2,18,34),(115,1,14,35)),10,True),
    "run":("DATA/Images/Sprites/Chars/Renault/Default/Run.png",((2,14,18,20),(22,14,18,20),(42,14,18,20),(62,14,18,20),(82,14,18,20),(102,14,18,20)),10,True),
    "jump":("DATA/Images/Sprites/Chars/Renault/Default/Jump.png",((2,1,14,35),(19,1,17,35),(38,1,19,35),(62,1,15,35)),12,False),
    "fall":("DATA/Images/Sprites/Chars/Renault/Default/Fall.png",((1,1,16,35),),1,True),
    "airdodge":("DATA/Images/Sprites/Chars/Renault/Default/Parry_Dodge.png",((2,1,14,35),(21,1,14,35),(37,1,15,35)),12,False),
    "jab":("DATA/Images/Sprites/Chars/Renault/Default/Jab.png",((0,1,27,35),(31,1,27,35)),12,True),
    "downtilt":("DATA/Images/Sprites/Chars/Renault/Default/DownTilt.png",((2,1,14,35),(23,1,14,35),(39,1,24,35),(70,1,21,35),(96,1,24,35),(119,1,24,35),(145,1,24,35),(170,1,21,35),(195,1,16,35),(212,1,14,35)),16,False),
    "forwardtilt":("DATA/Images/Sprites/Chars/Renault/Default/Ftilt.png",((2,2,14,35),(27,2,68,35),(95,2,68,35),(168,2,14,35)),9,False),
    "uptilt":("DATA/Images/Sprites/Chars/Renault/Default/UpTilt.png",((1,1,22,35),(23,1,23,35),(45,1,22,35),(70,1,24,35),(94,1,22,35),(119,1,23,35)),12,False),
    "upsmash":("DATA/Images/Sprites/Chars/Renault/Default/UpSmash.png",((23,1,14,35),(38,1,28,35),(66,1,28,35),(94,1,28,35),(122,1,27,35),(149,1,27,35),(178,1,27,35),(205,1,28,35),(233,1,27,35),(261,1,21,35),(285,1,14,35)),16,False),
    "fsmash_init":("DATA/Images/Sprites/Chars/Renault/Default/Fsmash_init.png",((2,1,15,35),(22,1,14,35),(39,1,25,35)),11,False),
    "fsmash_hold":("DATA/Images/Sprites/Chars/Renault/Default/Fsmash_hold.png",((1,1,24,35),(32,1,23,35)),16,True),
    "fsmash_release":("DATA/Images/Sprites/Chars/Renault/Default/Fsmash_release.png",((2,1,24,35),(30,1,24,35),(56,1,24,35),(80,1,24,35)),12,True),
    "dsmash":("DATA/Images/Sprites/Chars/Renault/Default/DownSmash.png",((2,1,24,35),(24,1,26,35),(62,1,26,35),(95,1,26,35),(124,1,26,35),(156,1,26,35),(190,1,27,35),(225,1,25,35),(256,1,22,35),(285,1,14,35)),12,True),
    "bair":("DATA/Images/Sprites/Chars/Renault/Default/Bair.png",((1,1,14,35),(22,1,14,35),(54,1,14,35),(72,1,23,35),(103,1,23,35),(131,1,23,35),(161,1,14,35),(181,1,14,35)),18,False),
    "uair":("DATA/Images/Sprites/Chars/Renault/Default/Uair.png",((1,4,14,35),(21,4,14,35),(37,4,14,35),(53,3,14,36),(70,2,14,37),(87,1,24,38),(111,4,14,35)),14,False),
    "fair":("DATA/Images/Sprites/Chars/Renault/Default/Fair.png",((5,4,15,35),(29,4,16,35),(49,7,20,32),(74,7,22,32),(101,4,15,34),(124,3,15,35)),14,False),
    "dair":("DATA/Images/Sprites/Chars/Renault/Default/Dair.png",((1,3,14,35),(22,2,14,35),(40,3,20,35),(62,3,27,35),(94,3,22,35),(117,3,16,35),(140,3,14,35)),18,False),
    "nair1":("DATA/Images/Sprites/Chars/Renault/Default/Nair1.png",((2,1,14,35),(25,1,14,35)),10,True),
    "nair2":("DATA/Images/Sprites/Chars/Renault/Default/Nair2.png",((6,11,36,57),(45,11,41,57)),10,True),
    "neutralB":("DATA/Images/Sprites/Chars/Renault/Default/NeutralB.png",((2,1,14,35),(19,1,17,35),(38,1,19,35),(62,1,15,35)),12,False),
    "sideB":("DATA/Images/Sprites/Chars/Renault/Default/SideB.png",((2,1,30,35),),1,False),
    "upB":("DATA/Images/Sprites/Chars/Renault/Default/UpB.png",((3,4,16,42),(23,4,16,42)),12,True),

}

Balan = {
    "idle":("DATA/Images/Sprites/Chars/Balan/Default/balan_idle.png",((10,2,12,30),(42,2,12,30),(74,4,12,28),(106,3,12,29)),5,True),
    "walk":("DATA/Images/Sprites/Chars/Balan/Default/balan_walk.png",((7,2,15,30),(40,3,14,29),(70,3,16,29)),6,True),
    "run":("DATA/Images/Sprites/Chars/Balan/Default/balan_run.png",((2,3,21,29),(34,3,22,29),(65,4,22,28),(99,4,20,28)),6,True),
    "jab":("DATA/Images/Sprites/Chars/Balan/Default/balan_jab.png",((4,2,16,30),(36,2,20,30),(66,2,24,30),(99,2,22,30),(131,2,22,30),(164,4,21,28),(196,2,21,30),(228,2,21,30),(260,3,21,29),(292,2,21,30)),20,False),
    "uptilt":("DATA/Images/Sprites/Chars/Balan/Default/balan_uptilt.png",((9,19,20,29),(36,21,26,27),(68,17,25,31),(99,17,20,31),(132,20,19,28),(169,18,14,30)),10,False),
    "jump":("DATA/Images/Sprites/Chars/Balan/Default/balan_jumping.png",((5,6,20,26),(40,2,13,30),(63,1,14,29)),5,False),
    "fall":("DATA/Images/Sprites/Chars/Balan/Default/balan_fall.png",((8,2,14,27),),1,False),
    "airdodge":("DATA/Images/Sprites/Chars/Balan/Default/balan_idle.png",((10,2,12,30),(42,2,12,30),(74,4,12,28),(106,3,12,29)),5,True),
    "nair":("DATA/Images/Sprites/Chars/Balan/Default/balan_nair.png",((8,1,14,29),(36,2,22,28),(68,2,22,27),(100,2,22,27),(139,2,12,27)),10,False),
}

BalanM = dict()
for s in Balan:
    BalanM[s] = (Balan[s][0].replace("Default","Masked"),Balan[s][1],Balan[s][2],Balan[s][3])

BalanJ = dict()
for s in Balan:
    BalanJ[s] = (Balan[s][0].replace("Default","Jedi"),Balan[s][1],Balan[s][2],Balan[s][3])

Air_President = {
    "idle":("DATA/Images/Sprites/Chars/Joueur_de_Air_President/Default/air_president-idle.png",((4,1,12,31),(20,1,12,31)),1,True),
    "walk":("DATA/Images/Sprites/Chars/Joueur_de_Air_President/Default/air_president-walk.png",((3,1,13,31),(18,0,14,32),(35,0,13,32),(52,0,12,32),(67,1,13,31),(82,0,14,32),(99,0,13,32),(116,0,12,32)),8,True),
    "run":("DATA/Images/Sprites/Chars/Joueur_de_Air_President/Default/air_president-idle.png",((4,1,12,31),(20,1,12,31)),10,True),
    "jump":("DATA/Images/Sprites/Chars/Joueur_de_Air_President/Default/air_president-idle.png",((4,1,12,31),),1,False),
    "fall":("DATA/Images/Sprites/Chars/Joueur_de_Air_President/Default/air_president-idle.png",((4,1,12,31),),1,True),
    "airdodge":("DATA/Images/Sprites/Chars/Joueur_de_Air_President/Default/air_president-idle.png",((4,1,12,31),(20,1,12,31)),1,True),
    "dtilt":("DATA/Images/Sprites/Chars/Joueur_de_Air_President/Default/air_president-dtilt.png",((0,1,12,31),(16,1,13,31),(32,2,13,30),(48,1,13,31)),15,False),

}

Spamton = Air_President
"""{
    "idle":("DATA/Images/Sprites/Chars/Joueur_de_Air_President/Spamton/spamton_idle.png",((1,1,16,31),(17,2,16,30)),2,True),
    "walk":("DATA/Images/Sprites/Chars/Joueur_de_Air_President/Spamton/spamton_idle.png",((1,1,16,31),(17,2,16,30)),2,True),
    "run":("DATA/Images/Sprites/Chars/Joueur_de_Air_President/Spamton/spamton_idle.png",((1,1,16,31),(17,2,16,30)),2,True),
    "jump":("DATA/Images/Sprites/Chars/Joueur_de_Air_President/Spamton/spamton_idle.png",((1,1,16,31),(17,2,16,30)),2,True),
    "fall":("DATA/Images/Sprites/Chars/Joueur_de_Air_President/Spamton/spamton_idle.png",((1,1,16,31),(17,2,16,30)),2,True),
    "airdodge":("DATA/Images/Sprites/Chars/Joueur_de_Air_President/Spamton/spamton_idle.png",((1,1,16,31),(17,2,16,30)),2,True),

}"""

Gregoire = {
    "idle":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_idle.png",((1,0,17,36),(18,1,18,35),(36,0,17,36),(55,1,16,35)),8,True),
    "walk":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_walk.png",((1,0,16,36),(18,0,16,36),(34,0,20,36),(54,0,18,36),(72,0,16,36),(88,0,16,36),(106,0,16,36)),8,True),
    "run":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_run.png",((1,0,16,36),(21,0,20,36),(50,0,18,36),(73,0,20,36),(96,0,24,36),(128,0,18,36)),12,True),
    "jump":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_jump.png",((3,2,17,34),(25,1,15,35),(46,0,16,37),(63,1,21,36)),12,False),
    "fall":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_jump.png",((63,1,21,36),),8,True),
    "airdodge":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_parry_airdodge.png",((1,0,15,36),(20,0,17,36),(39,0,17,36)),8,False),
    "jab":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_jab.png",((1,0,17,36),(19,0,19,36),(38,0,19,36),(60,0,19,35),(79,0,17,36),(97,0,18,36),(120,0,16,36),(136,0,18,36)),20,True),
    "nair":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_nair.png",((0,0,19,36),(20,0,14,36),(37,0,15,36),(53,0,15,35),(70,0,21,36),(91,0,18,36)),12,False),
    "dashattack":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_dashattack.png",((1,2,18,36),(21,4,18,34),(42,9,25,29),(69,20,18,18),(89,20,18,18),(110,20,18,18),(130,20,18,18),(150,20,18,18),(170,20,18,18),(191,20,18,18),(211,13,29,25)),20,False),
    "downb_charge":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_downBCharge.png",((1,0,29,36),(30,0,32,36),(63,0,26,36)),10,False),
    "downb_release":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_downBRelease.png",((0,0,34,36),(37,0,32,36),(69,0,36,36),(106,0,34,36),(146,0,34,36)),10,False),
    "dsmash":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_dsmash.png",((3,0,20,36),(28,0,17,36),(48,0,17,36),(65,0,18,36),(83,0,18,36)),9,False),
    "dtilt":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_dtilt.png",((2,1,21,35),(26,3,17,33),(43,3,16,33),(60,6,17,30),(80,3,14,33)),10,False),
    "fair":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_fair.png",((2,0,14,36),(21,0,14,36),(40,0,14,36),(62,0,14,36),(79,0,22,36),(106,0,30,36),(136,0,24,36),(160,0,16,36),(180,0,14,36)),20,False),
    "fair2":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_fair2.png",((0,0,14,36),(15,0,37,36)),0.75,False),
    "fsmash":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_fsmash.png",((2,0,21,36),(27,0,20,36),(50,0,17,36),(75,0,16,36),(101,0,23,36),(126,0,23,36),(153,0,23,36),(179,0,23,36),(209,0,23,36),(232,0,17,36)),10,False),
    "ftilt":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_ftilt.png",((2,0,21,36),(31,0,14,36),(57,0,19,36),(84,0,19,36)),10,False),
    "sideB":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_la_mort.png",((1,0,20,36),(24,0,28,36),(54,0,28,36),(85,0,28,36),(117,0,21,36)),10,False),
    "neutralB":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_neutralB.png",((4,0,16,36),(23,0,17,36),(44,0,18,36),(64,0,17,36),(82,0,16,36)),10,False),
    "uair":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_uair.png",((2,0,21,36),(27,0,16,36),(44,0,15,36),(60,0,15,36)),10,False),
    "usmash":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_usmash.png",((1,2,18,36),(21,4,18,34),(39,4,21,34),(60,4,18,34),(78,1,14,37)),10,False),
    "utilt":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_utilt.png",((1,6,27,30),(29,0,17,36),(54,5,25,31),(83,0,14,36)),10,False),
    "dair_dive":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_dair_dive.png",((4,6,25,31),(31,8,25,29),(63,12,29,25),(97,0,14,37)),10,False),
    "dair_fall":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_dair_fall.png",((6,0,14,37),(25,12,30,25),(61,7,25,29),(93,9,29,25),(125,2,21,36)),15,False),
    "dair_ground":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_dair_ground.png",((6,0,14,37),(25,12,29,25),(61,8,25,29),(94,4,18,34)),10,False),
    "bair":("DATA/Images/Sprites/Chars/Gregoire/Default/gregoire_bair.png",((2,0,21,36),(25,0,22,36),(48,0,23,36),(78,0,14,36),(99,0,21,36),(122,0,26,36),(148,0,16,36)),10,False),
}

Pyro_Aubin = {
    "idle":("DATA/Images/Sprites/Chars/Pyro_Aubin/Default/aubin_idle.png",((14,1,22,46),(62,2,26,46),(108,4,29,44),(158,2,26,46)),8,True),
    "walk":("DATA/Images/Sprites/Chars/Pyro_Aubin/Default/aubin_idle.png",((14,1,22,47),(62,2,26,46),(108,4,29,44),(158,2,26,46)),8,True),
    "run":("DATA/Images/Sprites/Chars/Pyro_Aubin/Default/aubin_idle.png",((14,1,22,47),(62,2,26,46),(108,4,29,44),(158,2,26,46)),8,True),
    "jump":("DATA/Images/Sprites/Chars/Pyro_Aubin/Default/aubin_jump.png",((7,4,31,44),(55,2,30,46),(101,1,38,46)),8,False),
    "fall":("DATA/Images/Sprites/Chars/Pyro_Aubin/Default/aubin_jump.png",((101,1,38,46),),8,False),
    "airdodge":("DATA/Images/Sprites/Chars/Pyro_Aubin/Default/aubin_idle.png",((14,1,22,47),(62,2,26,46),(108,4,29,44),(158,2,26,46)),8,True),

}

Millet = {
    "idle":("DATA/Images/Sprites/Chars/Millet/Default/Idle.png",((5,2,12,34),(24,3,12,33),(40,3,12,33),(56,3,12,33),(72,2,12,34)),5,True),
    "walk":("DATA/Images/Sprites/Chars/Millet/Default/Idle.png",((5,2,12,34),),1,True),
    "run":("DATA/Images/Sprites/Chars/Millet/Default/Idle.png",((5,2,12,34),),1,True),
    "jump":("DATA/Images/Sprites/Chars/Millet/Default/Idle.png",((5,2,12,34),),1,True),
    "fall":("DATA/Images/Sprites/Chars/Millet/Default/Idle.png",((5,2,12,34),),1,True),
    "airdodge":("DATA/Images/Sprites/Chars/Millet/Default/Idle.png",((5,2,12,34),),1,True),
    #"dair":("DATA/Images/Sprites/Chars/Millet/Default/Idle.png",((5,2,12,34),),1,True),

}

Bowser = {
    "idle":("DATA/Images/Sprites/Chars/Millet/Bowser/Idle.png",((4,1,16,36),(23,2,16,35),(39,2,16,35),(55,2,16,35),(71,1,16,36),),8,True),
    "walk":("DATA/Images/Sprites/Chars/Millet/Bowser/Idle.png",((4,1,16,36),),8,True),
    "run":("DATA/Images/Sprites/Chars/Millet/Bowser/Idle.png",((4,1,16,36),),8,True),
    "jump":("DATA/Images/Sprites/Chars/Millet/Bowser/Idle.png",((4,1,16,36),),8,False),
    "fall":("DATA/Images/Sprites/Chars/Millet/Bowser/Idle.png",((4,1,16,36),),8,False),
    "airdodge":("DATA/Images/Sprites/Chars/Millet/Bowser/Idle.png",((4,1,16,36),),8,True),
    #"dair":("DATA/Images/Sprites/Chars/Millet/Bowser/DownAir.png",((3,0,34,39),),8,False),

}

Kebab = {
    "idle":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Idle.png",((2,2,12,12),(16,1,12,13),(30,2,12,12),(44,3,12,11),(58,2,12,12),),6,True),
    "walk":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Walk.png",((2,2,12,12),(16,2,12,12),(30,2,12,12),(43,2,12,12),(57,2,12,12),(70,2,12,12)),8,True),
    "run":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Walk.png",((2,2,12,12),(16,2,12,12),(43,2,12,12),(57,2,12,12)),10,True),
    "jump":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Jump.png",((2,3,12,11),(16,1,12,14),(30,1,12,14),(44,1,12,11),(57,3,12,11)),10,False),
    "fall":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Jump.png",((57,3,12,11),),1,False),
    "airdodge":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Airdodge.png",((2,3,12,11),(16,1,12,14),(29,1,12,14),(43,1,9,14),(54,1,12,14),(67,1,12,14),(80,1,12,14),(93,1,9,14),(104,1,12,14),(117,1,12,14)),20,False),
    "dashattack":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_DashAttack.png",((2,2,12,12),(16,1,12,14),(29,1,12,14),(42,2,14,12),(57,2,14,12),(72,2,14,12),(89,1,12,14),(102,1,12,14),(116,2,14,12),(131,2,12,12)),12,True),
    "nair":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Jump.png",((57,3,12,11),),1,False),
    "fair":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Fair.png",((2,3,12,12),(15,2,12,12),(28,2,12,12),(41,2,12,12),(54,2,13,12),(68,2,13,12),(82,2,13,12),(96,2,13,12),(110,2,12,12)),20,False),
    "dair":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Dair.png",((2,3,12,12),(15,1,12,12),(28,1,12,13),(41,1,12,12),(54,1,12,12),(67,1,12,13),(80,1,12,12),(93,1,12,12),(106,1,12,13),(119,1,12,14),(132,1,12,14),(145,1,12,12),(158,1,12,11)),30,False),
    "bair":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Bair.png",((2,3,12,9),(17,3,12,9),(31,3,12,12),(44,2,12,13),(57,2,14,13),(72,6,19,9),(92,6,18,9),(112,6,16,9),(129,6,14,9),(146,6,12,9),(159,6,12,9),(172,6,12,9)),30,False),
    "uair":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Uair.png",((3,20,12,9),(17,18,12,11),(30,16,12,13),(43,12,12,17),(56,4,12,25),(69,1,12,28),(82,7,12,22),(95,12,12,17),(108,19,12,10),(121,20,12,9)),30,False),
    "utilt":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Utilt.png",((2,17,12,12),(16,16,12,13),(30,12,12,17),(44,8,12,21),(57,2,12,27),(70,2,12,27),(83,8,12,21),(97,12,12,17),(111,16,12,13),(125,17,12,12)),30,False),
    "dtilt":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Dtilt.png",((2,3,12,11),(15,3,12,11),(28,3,12,11),(41,3,12,10),(54,3,12,10),(67,3,12,10),(80,3,12,10),(93,3,12,10),(106,3,12,11)),30,False),
    "ftilt":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Ftilt.png",((2,3,12,11),(16,3,15,11),(33,3,16,11),(50,3,18,11),(69,3,16,11),(86,3,15,11),(103,3,12,11)),20,False),
    "downb":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_DownB.png",((1,2,17,12),(19,2,17,12),(37,2,16,12),(54,2,15,12),(70,2,15,12),(86,2,14,12),(101,2,14,12),(116,2,12,12),(129,2,12,12)),20,False),
    "downb_no":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_DownB_echec.png",((1,2,13,12),(15,2,13,12),(29,2,13,12),(42,2,12,12)),20,False),
    "upb":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_UpB.png",((2,2,12,12),(16,2,12,12),(29,2,12,12),(42,2,11,12),(54,2,12,12),(67,2,12,12),(80,2,12,12),(93,2,12,12)),18,False),
    "jab":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Jab.png",((2,2,12,12),(16,2,12,12),(29,2,12,12),(42,2,13,12),(55,2,12,12)),20,False),
    "jab2":("DATA/Images/Sprites/Chars/Kebab/Default/Kebab_Jab2.png",((1,2,13,12),(15,2,14,12),(30,2,15,12),(46,2,13,12),(59,2,12,12)),20,False),

}


Training = {
    "idle":("DATA/Images/Sprites/Misc/Training/Training.png",((0,0,12,30),),1,True),
    "walk":("DATA/Images/Sprites/Misc/Training/Training.png",((0,0,12,30),),1,True),
    "run":("DATA/Images/Sprites/Misc/Training/Training.png",((0,0,12,30),),1,True),
    "jump":("DATA/Images/Sprites/Misc/Training/Training.png",((0,0,12,30),),1,True),
    "fall":("DATA/Images/Sprites/Misc/Training/Training.png",((0,0,12,30),),1,True),
    "airdodge":("DATA/Images/Sprites/Misc/Training/Training.png",((0,0,12,30),),1,True),

}
### Lien Nom/animation

animations = {
    "Balan":Balan,"BalanM":BalanM,"BalanJ":BalanJ,
    "Joueur de air-president":Air_President,"Spamton":Spamton,
    "Millet":Millet, "Bowser":Bowser,
    "Gregoire":Gregoire,
    "Reignaud":Reignaud,
    "Rey":Nonesprite,
    "Pyro-Aubin":Pyro_Aubin,
    "Kebab":Kebab,
    "Poissonnier":Nonesprite,
    "Renault":Renault,
    "Gourmelen":Nonesprite,
    "Journault":Nonesprite,
    "Le Berre":Nonesprite,
    "EnglishTeacher":Nonesprite,
    "Thevenet":Nonesprite,
    #"Isaac":Nonesprite,
    "Training":Training
}