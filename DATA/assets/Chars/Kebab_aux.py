import pygame

def replacewhite(image,colorcoef):
    """ Applique un coefficient à toutes les couleurs 
    NE PAS UTILISER EN COURS D'EXECUTION, PRENDS BEAUCOUP DE TEMPS
    Priviliégier une exécution avant le lancement
    
    Entrées : image ; coefficients (3 ou 4 floats)
    Sorties : image modifiée (modification de l'image entrée aussi)"""
    for x in range(image.get_size()[0]):
        for y in range(image.get_size()[1]):
            newcolor = list(image.get_at((x,y)))
            for i,c in enumerate(colorcoef):
                newcolor[i]*=c
            image.set_at((x,y),newcolor)
    return image


### Recoloring smashes sprites
Attacks = {
    "fsmash0":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2.png"),(0.9,0.7,0.6)),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),
    "fsmash1":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2.png"),(1,0.7,0.05)),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),
    "fsmash2":(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2.png"),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),
    "fsmash3":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2.png"),(0.6,0.6,0.3)),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),
    "fsmash4":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2.png"),(0.5,0.3,0)),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),
    "fsmash5":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2.png"),(0.5,0.3,0.3)),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),
    "fsmash6":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2.png"),(0.4,0,0)),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),
    "fsmash7":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2.png"),(0.8,0.3,0.3)),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),
    "fsmash-1":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2.png"),(0.2,0.2,0.2)),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),

    "fsmash0l":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2_l.png"),(0.9,0.7,0.6)),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),
    "fsmash1l":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2_l.png"),(1,0.7,0.05)),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),
    "fsmash2l":(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2_l.png"),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),
    "fsmash3l":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2_l.png"),(0.6,0.6,0.3)),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),
    "fsmash4l":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2_l.png"),(0.5,0.3,0)),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),
    "fsmash5l":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2_l.png"),(0.5,0.3,0.3)),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),
    "fsmash6l":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2_l.png"),(0.4,0,0)),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),
    "fsmash7l":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2_l.png"),(0.8,0.3,0.3)),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),
    "fsmash-1l":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Fsmash2_l.png"),(0.2,0.2,0.2)),((3,2,8,13),(12,2,12,13),(25,2,16,13),(42,3,21,13)),10,False),


    "usmash0":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2.png"),(0.9,0.7,0.6)),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
    "usmash1":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2.png"),(1,0.7,0.05)),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
    "usmash2":(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2.png"),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
    "usmash3":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2.png"),(0.6,0.6,0.3)),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
    "usmash4":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2.png"),(0.5,0.3,0)),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
    "usmash5":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2.png"),(0.5,0.3,0.3)),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
    "usmash6":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2.png"),(0.4,0,0)),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
    "usmash7":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2.png"),(0.8,0.3,0.3)),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
    "usmash-1":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2.png"),(0.2,0.2,0.2)),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),

    "usmash0l":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2_l.png"),(0.9,0.7,0.6)),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
    "usmash1l":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2_l.png"),(1,0.7,0.05)),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
    "usmash2l":(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2_l.png"),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
    "usmash3l":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2_l.png"),(0.6,0.6,0.3)),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
    "usmash4l":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2_l.png"),(0.5,0.3,0)),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
    "usmash5l":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2_l.png"),(0.5,0.3,0.3)),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
    "usmash6l":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2_l.png"),(0.4,0,0)),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
    "usmash7l":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2_l.png"),(0.8,0.3,0.3)),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
    "usmash-1l":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Chars/Kebab/Usmash2_l.png"),(0.2,0.2,0.2)),((0,13,13,8),(14,9,13,12),(29,5,13,16),(45,1,13,21)),10,False),
}
Sauce = {
    "0":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_air.png"),(0.9,0.7,0.6))),
    "1":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_air.png"),(1,0.7,0.05))),
    "2":(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_air.png")),
    "3":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_air.png"),(0.6,0.6,0.3))),
    "4":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_air.png"),(0.5,0.3,0))),
    "5":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_air.png"),(0.5,0.3,0.3))),
    "6":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_air.png"),(0.4,0,0))),
    "7":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_air.png"),(0.8,0.3,0.3))),
    "-1":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_air.png"),(0.2,0.2,0.2))),

    "0f":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_onfloor.png"),(0.9,0.7,0.6))),
    "1f":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_onfloor.png"),(1,0.7,0.05))),
    "2f":(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_onfloor.png")),
    "3f":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_onfloor.png"),(0.6,0.6,0.3))),
    "4f":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_onfloor.png"),(0.5,0.3,0))),
    "5f":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_onfloor.png"),(0.5,0.3,0.3))),
    "6f":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_onfloor.png"),(0.4,0,0))),
    "7f":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_onfloor.png"),(0.8,0.3,0.3))),
    "-1f":(replacewhite(pygame.image.load("./DATA/Images/Sprites/Projectiles/Kebab/Sauce_onfloor.png"),(0.2,0.2,0.2))),
}