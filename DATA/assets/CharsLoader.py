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
from DATA.assets.Chars.Training_Mob import *

pygame.mixer.init()

charobjects = {
    "Balan":Balan,
    "Joueur de air-president":Air_President,
    "Millet":Millet,
    "Gregoire":Gregoire,
    "Reignaud":Reignaud,
    "Rey":Rey,
    "Pyro-Aubin":Pyro_Aubin,
    "Kebab":Kebab,
    "Poissonnier":Poissonnier,
    "Renault":Renault,
}

airspeeds = {
    "Balan":Balan(0,0,0).airspeed,
    "Joueur de air-president":Air_President(0,0,0).airspeed,
    "Millet":Millet(0,0,0).airspeed,
    "Gregoire":Gregoire(0,0,0).airspeed,
    "Reignaud":Reignaud(0,0,0).airspeed,
    "Rey":Rey(0,0,0).airspeed,
    "Pyro-Aubin":Pyro_Aubin(0,0,0).airspeed,
    "Kebab":Kebab(0,0,0).airspeed,
    "Poissonnier":Poissonnier(0,0,0).airspeed,
    "Renault":Renault(0,0,0).airspeed,
}

decelerations = {
    "Balan":Balan(0,0,0).deceleration,
    "Joueur de air-president":Air_President(0,0,0).deceleration,
    "Millet":Millet(0,0,0).deceleration,
    "Gregoire":Gregoire(0,0,0).deceleration,
    "Reignaud":Reignaud(0,0,0).deceleration,
    "Rey":Rey(0,0,0).deceleration,
    "Pyro-Aubin":Pyro_Aubin(0,0,0).deceleration,
    "Kebab":Kebab(0,0,0).deceleration,
    "Poissonnier":Poissonnier(0,0,0).deceleration,
    "Renault":Renault(0,0,0).deceleration,
}

fallspeeds = {
    "Balan":Balan(0,0,0).fallspeed,
    "Joueur de air-president":Air_President(0,0,0).fallspeed,
    "Millet":Millet(0,0,0).fallspeed,
    "Gregoire":Gregoire(0,0,0).fallspeed,
    "Reignaud":Reignaud(0,0,0).fallspeed,
    "Rey":Rey(0,0,0).fallspeed,
    "Pyro-Aubin":Pyro_Aubin(0,0,0).fallspeed,
    "Kebab":Kebab(0,0,0).fallspeed,
    "Poissonnier":Poissonnier(0,0,0).fallspeed,
    "Renault":Renault(0,0,0).deceleration,
}

fastfallspeeds = {
    "Balan":Balan(0,0,0).fastfallspeed,
    "Joueur de air-president":Air_President(0,0,0).fastfallspeed,
    "Millet":Millet(0,0,0).fastfallspeed,
    "Gregoire":Gregoire(0,0,0).fastfallspeed,
    "Reignaud":Reignaud(0,0,0).fastfallspeed,
    "Rey":Rey(0,0,0).fastfallspeed,
    "Pyro-Aubin":Pyro_Aubin(0,0,0).fastfallspeed,
    "Kebab":Kebab(0,0,0).fastfallspeed,
    "Poissonnier":Poissonnier(0,0,0).fastfallspeed,
    "Renault":Renault(0,0,0).deceleration,
}