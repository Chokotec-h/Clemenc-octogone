from DATA.utilities.Game import Game
from DATA.utilities.Interface import Texte


# Themes de victoire
Victorythemes = {
    "Balan":"Balan",
    "Joueur de Air-President":"Spamton 1", "Spamton":"Spamton 2", 
    "Millet":"Science", "Bowser":"Science",
    "Gregoire":"Science",
    "Reignaud":"Classical",
    "Rey":"Normal",
    "Pyro-Aubin":"Lunch",
    "Kebab du dimanche soir":"BDE",
    "Poissonnier":"Poissonier",
    "Renault":"SI",
    -1:"Bonus"
}



class Results():
    def __init__(self,game:Game,width,height,names1,names2) -> None:
        self.frame = 0
        self.game = game
        self.x = 0
        self.y = 80
        self.vel = 60
        self.names = (names1,names2)
        self.winner = -1
    
    def check_winner(self):
        """Calcul du gagnant"""
        # Celui qui a le plus de vie
        if self.game.stock[0] > self.game.stock[1] :
            self.winner = 0
        elif self.game.stock[1] > self.game.stock[0] :
            self.winner = 1
        # En cas d'égalité, celui qui a le moins de dégâts
        elif self.game.Char_P1.damages > self.game.Char_P2.damages :
            self.winner = 1
        elif self.game.Char_P2.damages > self.game.Char_P1.damages :
            self.winner = 0
        else :
            # Egalité parfaite
            self.winner = -1

    def draw(self,win,width,height):
        # Actualisation
        self.frame += 1
        if self.frame < 30 :
            self.x += self.vel
            self.vel -= 2
            Texte("LE GAGNANT EST",("consolas",90,True,False),(0,0,0),self.x,self.y).draw(win)
        elif self.frame < 60 :
            Texte("LE GAGNANT EST",("consolas",90,True,False),(0,0,0),self.x,self.y).draw(win)
        else :
            if self.winner == -1 :
                Texte("EGALITE",("consolas",90,True,False),(0,0,0),width/2,height/2).draw(win)
            else :
                Texte("LE GAGNANT EST",("consolas",90,True,False),(0,0,0),self.x,self.y).draw(win)

                # Affichage du nom du joueur et du personnage
                if self.winner == 0 :
                    # Spécial
                    if self.names[0] == "Default" :
                        self.names = ("Joueur 1",self.names[1])
                    #if str(self.game.Char_P1) == "Spamton" :
                    #    self.game.Char_P1 = "[[SPAMTON G. SPAMTON]]"

                    Texte(f"{self.names[0].upper()}",("consolas",90,True,False),(0,0,0),width/2,250).draw(win)
                    Texte(f"avec",("consolas",70,False,True),(0,0,0),width/2,310).draw(win)
                    Texte(f"{str(self.game.Char_P1).upper()}",("consolas",90,True,False),(0,0,0),width/2,370).draw(win)
                if self.winner == 1 :
                    # Spécial
                    if self.names[1] == "Default" :
                        self.names = (self.names[0],"Joueur 2")
                    #if str(self.game.Char_P2) == "Spamton" :
                    #    self.game.Char_P2 = "[[SPAMTON G. SPAMTON]]"

                    Texte(f"{self.names[1].upper()}",("consolas",90,True,False),(0,0,0),width/2,250).draw(win)
                    Texte(f"avec",("consolas",70,False,True),(0,0,0),width/2,310).draw(win)
                    Texte(f"{str(self.game.Char_P2).upper()}",("consolas",90,True,False),(0,0,0),width/2,370).draw(win)

        # Affichage de texte de retour
        if self.frame > 300 :
            Texte(f"Appuyer sur attaque pour continuer",("arial",40,False,False),(0,0,0),width/5,9*height/10,format_="left").draw(win)
