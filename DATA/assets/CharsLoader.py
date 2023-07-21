from DATA.assets.Chars.Balan import *
from DATA.assets.Chars.JoueurDeCartes import *
from DATA.assets.Chars.Millet import *
from DATA.assets.Chars.Gregoire import *
from DATA.assets.Chars.Reignaud import *
from DATA.assets.Chars.Pyro_Aubin import *
from DATA.assets.Chars.Rey import *
from DATA.assets.Chars.Kebab import *
from DATA.assets.Chars.Poissonnier import *
from DATA.assets.Chars.Renault import *
from DATA.assets.Chars.Gourmelen import *
from DATA.assets.Chars.Journault import *
from DATA.assets.Chars.Le_Berre import *
from DATA.assets.Chars.EnglishTeacher import *
from DATA.assets.Chars.Thevenet import *
from DATA.assets.Chars.Training_Mob import *

# Nom des personnages
chars = [["Balan","BalanM"],
         ["Millet", "Bowser"],
         ["Gregoire"],
         ["Poissonnier"],
         ["Renault"],
         ["Reignaud"],
         ["Rey"],
         ["Joueur de air-president", "Spamton"],
         ["Pyro-Aubin"],
         ["Kebab"],
         ["Gourmelen"],
         ["Journault"],
         ["Le Berre"],
         ["EnglishTeacher"],
         ["Thevenet"]]


charobjects = {
    "Balan": Balan, "BalanM": Balan2,
    "Joueur de air-president": Air_President, "Spamton": Spamton,
    "Millet": Millet, "Bowser": Bowser,
    "Gregoire": Gregoire,
    "Reignaud": Reignaud,
    "Rey": Rey,
    "Pyro-Aubin": Pyro_Aubin,
    "Kebab": Kebab,
    "Poissonnier": Poissonnier,
    "Renault": Renault,
    "Gourmelen": Gourmelen,
    "Journault": Journault,
    "Le Berre": LeBerre,
    "EnglishTeacher": EnglishTeacher,
    "Thevenet": Thevenet,
}

airspeeds = {
    "Balan": Balan(0, 0, 0).airspeed,
    "Joueur de air-president": Air_President(0, 0, 0).airspeed,
    "Millet": Millet(0, 0, 0).airspeed,
    "Gregoire": Gregoire(0, 0, 0).airspeed,
    "Reignaud": Reignaud(0, 0, 0).airspeed,
    "Rey": Rey(0, 0, 0).airspeed,
    "Pyro-Aubin": Pyro_Aubin(0, 0, 0).airspeed,
    "Kebab": Kebab(0, 0, 0).airspeed,
    "Poissonnier": Poissonnier(0, 0, 0).airspeed,
    "Renault": Renault(0, 0, 0).airspeed,
    "Gourmelen": Gourmelen(0, 0, 0).airspeed,
    "Journault": Journault(0, 0, 0).airspeed,
    "Le Berre": LeBerre(0, 0, 0).airspeed,
    "EnglishTeacher": EnglishTeacher(0, 0, 0).airspeed,
    "Thevenet": Thevenet(0, 0, 0).airspeed,
}

decelerations = {
    "Balan": Balan(0, 0, 0).deceleration,
    "Joueur de air-president": Air_President(0, 0, 0).deceleration,
    "Millet": Millet(0, 0, 0).deceleration,
    "Gregoire": Gregoire(0, 0, 0).deceleration,
    "Reignaud": Reignaud(0, 0, 0).deceleration,
    "Rey": Rey(0, 0, 0).deceleration,
    "Pyro-Aubin": Pyro_Aubin(0, 0, 0).deceleration,
    "Kebab": Kebab(0, 0, 0).deceleration,
    "Poissonnier": Poissonnier(0, 0, 0).deceleration,
    "Renault": Renault(0, 0, 0).deceleration,
    "Gourmelen": Gourmelen(0, 0, 0).deceleration,
    "Journault": Journault(0, 0, 0).deceleration,
    "Le Berre": LeBerre(0, 0, 0).deceleration,
    "EnglishTeacher": EnglishTeacher(0, 0, 0).deceleration,
    "Thevenet": Thevenet(0, 0, 0).deceleration,
}

fallspeeds = {
    "Balan": Balan(0, 0, 0).fallspeed,
    "Joueur de air-president": Air_President(0, 0, 0).fallspeed,
    "Millet": Millet(0, 0, 0).fallspeed,
    "Gregoire": Gregoire(0, 0, 0).fallspeed,
    "Reignaud": Reignaud(0, 0, 0).fallspeed,
    "Rey": Rey(0, 0, 0).fallspeed,
    "Pyro-Aubin": Pyro_Aubin(0, 0, 0).fallspeed,
    "Kebab": Kebab(0, 0, 0).fallspeed,
    "Poissonnier": Poissonnier(0, 0, 0).fallspeed,
    "Renault": Renault(0, 0, 0).fallspeed,
    "Gourmelen": Gourmelen(0, 0, 0).fallspeed,
    "Journault": Journault(0, 0, 0).fallspeed,
    "Le Berre": LeBerre(0, 0, 0).fallspeed,
    "EnglishTeacher": EnglishTeacher(0, 0, 0).fallspeed,
    "Thevenet": Thevenet(0, 0, 0).fallspeed,
}

fastfallspeeds = {
    "Balan": Balan(0, 0, 0).fastfallspeed,
    "Joueur de air-president": Air_President(0, 0, 0).fastfallspeed,
    "Millet": Millet(0, 0, 0).fastfallspeed,
    "Gregoire": Gregoire(0, 0, 0).fastfallspeed,
    "Reignaud": Reignaud(0, 0, 0).fastfallspeed,
    "Rey": Rey(0, 0, 0).fastfallspeed,
    "Pyro-Aubin": Pyro_Aubin(0, 0, 0).fastfallspeed,
    "Kebab": Kebab(0, 0, 0).fastfallspeed,
    "Poissonnier": Poissonnier(0, 0, 0).fastfallspeed,
    "Renault": Renault(0, 0, 0).fastfallspeed,
    "Gourmelen": Gourmelen(0, 0, 0).fastfallspeed,
    "Journault": Journault(0, 0, 0).fastfallspeed,
    "Le Berre": LeBerre(0, 0, 0).fastfallspeed,
    "EnglishTeacher": EnglishTeacher(0, 0, 0).fastfallspeed,
    "Thevenet": Thevenet(0, 0, 0).fastfallspeed,
}
