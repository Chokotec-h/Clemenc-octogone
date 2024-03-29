from DATA.utilities.Base_Char import Char, Hitbox, signe
import pygame
from math import pi
from DATA.utilities.functions import *
from DATA.utilities.build import rootDir

exposant_sprite = [
    pygame.transform.scale(pygame.image.load(f"{rootDir()}/Images/Sprites/Projectiles/Balan/Exposants/{i}.png"), resize(36, 36, width, height)) for
    i in range(5)]


##### Balan

class Balan(Char):
    def __init__(self, x, y, player) -> None:
        super().__init__(speed=2, dashspeed=3, airspeed=0.8, deceleration=0.705, fallspeed=0.45, fastfallspeed=1,
                         fullhop=14, shorthop=11,
                         doublejumpheight=15, airdodgespeed=6, airdodgetime=3, dodgeduration=15)

        self.rect = [100, 0, 48, 120]  # Crée le rectangle de perso
        self.name = "Balan"
        self.x = x
        self.rect[1] = y
        self.player = player
        self.resize_rect()

    def __str__(self) -> str:
        return "Balan"

    def special(self, inputs):  # Spécial à Balan, pour son upB
        if self.upB:  # Vitesse de merde après upB
            self.vx *= 0.6
        return False

    def animation_attack(self, attack, inputs, stage, other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs  # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            if self.frame == 11:  # Saute frame 11
                self.can_act = False  # ne peut pas agir après un grounded up B
                self.vy = -19
                self.vx = self.direction/10
                self.attack = None
                self.doublejump = [True for _ in self.doublejump]  # Annule tout les sauts
            elif self.frame > 6:  # Sort frame 7
                self.rect[1] -= 6
            if self.frame < 6:
                if left:  # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right:
                    self.look_right = True
            if self.frame == 6:  # Hitbox frame 6-11
                self.active_hitboxes.append(Hitbox(-1.5, 75, 51, 48, pi+pi / 2.25, 23, 32, 1 / 150, 30, 5, self, False,
                                                   sound="hits/cool hit"))

        if attack == "DownB":
            # self.can_act = False
            if self.frame == 5 :
                self.grab = False
                self.active_hitboxes.append(Hitbox(40, 32, 32, 32, 0, 0, 0, 0, 0, 5, self))
            if 5 < self.frame < 9 and len(self.active_hitboxes) <= 0 :
                self.grab = True
                other.hitstun = 10
                other.vx = 0
            if self.frame > 10 and self.grab and self.frame < 27:
                if 15 < self.frame < 20 :
                    self.vy = 0
                if self.frame < 15 :
                    self.vy -= 35
                if self.frame > 20 :
                    self.vy += 35
                other.hitstun = 10
                other.rect[1] = self.rect[1]
                other.vy = -1
                other.vx = 0
            if self.frame == 30 and self.grab:
                other.rect[1] = self.rect[1] - resize(0,32,width,height)[1]
                other.vy = 0
                other.vx = 0
                self.active_hitboxes.append(Hitbox(40,32,32,32,pi/3,20,16,1/200,18,3,self))
                self.vy = -15
            if self.frame > 35 and self.grab :
                self.attack = None
            if self.frame > 25 and not self.grab :
                self.attack = None
            

        if attack == "NeutralB":
            if self.frame < 5 and special:  # Chargement jusqu'à 200 frames
                self.frame = 0
                self.animeframe -= 1
                self.charge = min(199, self.charge + 1)
                if left:  # peut changer de direction
                    self.look_right = False
                if right:
                    self.look_right = True
            if self.frame == 8:  # 8 frames après relache
                self.active_hitboxes.append(Hitbox(40, 32, 32, 64, 0, 0, 0, 0, 0, 20, self, True))
                self.active_hitboxes[-1].update()
                hitbox = self.active_hitboxes[-1]
                hit = pygame.Rect(hitbox.x, hitbox.y, hitbox.sizex, hitbox.sizey) 
                if hit.colliderect(pygame.Rect(other.rect)):
                    self.projectiles.append(Exposant(other, self, self.charge // 40))
            if self.frame > 20:  # 15 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame < 8:
                if left:  # peut reverse netre les frames 1 et 7
                    self.look_right = False
                if right:
                    self.look_right = True
                if self.grounded and self.frame < 6:  # intangible au sol frame 1-5
                    self.intangibility = True
            if self.frame == 8:
                self.intangibility = False
                self.active_hitboxes.append(Hitbox(16, 30, 32, 32, pi / 4, 28, 10, 0, 12, 3, self, False))
            if self.frame == 10:  # Active on 10-60
                self.active_hitboxes.append(Hitbox(8, 82, 32, 10, pi / 4, 3, 4, 1 / 250, 3, 50, self, False))
            if 12 > self.frame > 10:  # Déplacement
                self.vy = -10
            if 10 < self.frame < 60 :
                self.vx = 20 * signe(self.direction) / (self.frame*0.12)
            if self.frame > 80:  # 20 frames de lag
                self.attack = None

        if attack == "Jab":
            self.animation = "jab"
            if self.frame == 3:  # 1er hit frame 3-6
                self.active_hitboxes.append(Hitbox(40, 36, 48, 24, 3 * pi / 4, 2, 0.6, 0, 10, 4, self, True))
            if self.frame == 9:  # 2e hit frame 9-12
                self.active_hitboxes.append(Hitbox(20, 20, 68, 48, pi / 4, 4.5, 1.4, 1 / 1000, 15, 4, self, False))

            if self.frame > 22:  # 10 frames de lag
                self.attack = None

        if attack == "DownTilt":
            if self.frame == 8:  # Frame 8-13
                self.active_hitboxes.append(Hitbox(35, 100, 48, 20, 2 * pi / 5, 8, 3.8, 1 / 200, 14, 5, self, False))

            if self.frame > 20:  # 7 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame < 3:
                if left:
                    self.look_right = False
                if right:
                    self.look_right = True
            if self.frame == 6:  # 1er hit frame 6-12
                self.active_hitboxes.append(Hitbox(40, 58, 24, 24, pi / 2, 2, 0.6, 0, 9, 6, self, True))
            if self.frame == 14:  # 2e hit frame 14-22
                self.active_hitboxes.append(Hitbox(40, 58, 24, 24, pi / 4, 6, 8, 1 / 150, 15, 6, self, False))

            if self.frame > 30:  # 8 frames de lag
                self.attack = None

        if attack == "UpTilt":
            self.animation = "uptilt"
            if self.frame == 6:  # Frame 6-14
                self.active_hitboxes.append(Hitbox(78, -5, -16, 16, pi / 2, 13, 8.2, 1 / 250, 25, 8, self, False))
                if not self.look_right:
                    self.active_hitboxes[-1].sizex *= -1
                    self.active_hitboxes[-1].relativex -= 16

            # Dessin du cercle
            if self.active_hitboxes:
                x,y = resize(12 * signe(self.direction),10,width,height)
                self.active_hitboxes[-1].y -= y
                if self.frame < 9:  # Frames 7-8
                    self.active_hitboxes[-1].sizey += y
                    self.active_hitboxes[-1].sizex -= x
                if self.frame < 11:  # Frames 9-10
                    self.active_hitboxes[-1].sizex -= x
                if self.frame < 13:  # Frames 11-12
                    self.active_hitboxes[-1].sizey += y
            if self.frame > 25:  # 11 Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame == 5:  # Frame 5-10
                self.active_hitboxes.append(Hitbox(-1, -10, 50, 10, pi / 2, 0, 2.5, 1 / 1000, 8, 5, self, True))
            if self.frame == 10:  # Frame 10-15
                self.active_hitboxes.append(Hitbox(15, -20, 16, 25, pi / 3, 10, 5, 1 / 80, 18, 5, self, True))

            if self.frame > 25:  # 10 frames de lag
                self.attack = None

            if self.grounded:
                self.attack = None
                if 15 > self.frame > 2:
                    self.lag = 8  # Auto cancel frame 1-2 et 15+, 8 frames de landing lag

        if attack == "ForwardAir":
            if self.frame == 15:  # Frame 15-16
                self.active_hitboxes.append(Hitbox(52, 45, 16, 32, -pi / 4, 10, 14, 1 / 150, 22, 6, self, False,
                                                   sound="hits/punch1"))
            if self.frame == 17:  # Frame 17-21
                if not self.look_right:
                    angle = 2 * pi / 3
                else:
                    angle = pi / 3
                if self.active_hitboxes:  # late hitbox
                    self.active_hitboxes[-1].angle = angle
                    self.active_hitboxes[-1].knockback = 3
                    self.active_hitboxes[-1].damages = 10
                    self.active_hitboxes[-1].damage_stacking = 1 / 250
                    self.active_hitboxes[-1].stun = 10

            if self.frame > 50:  # 29 frames de lag
                self.attack = None

            if self.grounded:
                self.attack = None
                if 40 > self.frame > 3:
                    self.lag = 15  # Auto cancel frame 1-3 et 40+, 15 frames de landing lag

        if attack == "BackAir":
            if self.frame == 6:  # Frame 6-8
                self.active_hitboxes.append(Hitbox(-42, 32, 48, 48, 49 * pi / 50, 10, 12, 1 / 150, 20, 6, self, False,
                                                   sound="hits/cool hit"))
            if self.frame == 9:  # Frame 9-11
                if not self.look_right:
                    angle = pi / 25
                else:
                    angle = 24 * pi / 25
                if self.active_hitboxes:  # Late hitbox
                    self.active_hitboxes[-1].angle = angle
                    self.active_hitboxes[-1].knockback = 3
                    self.active_hitboxes[-1].damages = 8
                    self.active_hitboxes[-1].damage_stacking = 1 / 250
                    self.active_hitboxes[-1].stun = 19

            if self.frame > 25:  # 14 frames de lag
                self.attack = None

            if self.grounded:
                self.attack = None
                if 20 > self.frame > 2:
                    self.lag = 6  # Auto cancel frame 1-2 et 20+, 6 frames de landing lag

        if attack == "DownAir":
            if self.frame == 10:  # Frame 10
                self.active_hitboxes.append(
                    Hitbox(16, 90, 24, 32, -2 * pi / 3, 2, 12, 1 / 20, 6, 5, self, False, sound="lasers/laser3"))
            if self.frame == 11:  # Frame 11-15
                if not self.look_right:
                    angle = 4 * pi / 6
                else:
                    angle = 2 * pi / 6
                if self.active_hitboxes:  # late hitbox
                    self.active_hitboxes[-1].angle = angle
                    self.active_hitboxes[-1].knockback = 3
                    self.active_hitboxes[-1].damages = 7
                    self.active_hitboxes[-1].damage_stacking = 1 / 1000
                    self.active_hitboxes[-1].stun = 10

            if self.frame > 25:  # 10 frames de lag
                self.attack = None

            if self.grounded:
                self.attack = None
                if 20 > self.frame > 5:
                    self.lag = 10  # Auto cancel frame 1-5 et 20+, 10 frames de landing lag

        if attack == "NeutralAir":
            self.animation = "nair"
            if self.frame == 3:  # Frame 3-6
                self.active_hitboxes.append(Hitbox(-20, 16, 88, 64, pi, 10, 2, 0, 12, 20, self, True))
                self.active_hitboxes.append(Hitbox(8, 16, 32, 64, pi / 2, 12, 8, 1 / 200, 18, 20, self, False))
            if self.frame == 7:  # Frame 7-23
                if self.active_hitboxes:  # late hitbox
                    if self.active_hitboxes[-1].angle == pi / 2:
                        self.active_hitboxes[-1].knockback = 3
                        self.active_hitboxes[-1].damages = 3
                        self.active_hitboxes[-1].damage_stacking = 1 / 250
                        self.active_hitboxes[-1].stun = 10
            if self.frame < 23 and self.animeframe == 80:
                self.animeframe -= 1
            if self.frame > 40:  # 17 frames de lag
                self.attack = None

            if self.grounded:
                self.attack = None
                if 30 > self.frame > 2:
                    self.lag = 4  # Auto cancel frame 1-2 et 30+, 4 frames de landing lag

        if attack == "ForwardSmash":
            if 6 < self.frame < 9 and smash and self.charge < 200:  # Chargement jusqu'à 200 frames
                self.frame = 7
                self.animeframe -= 1
                self.charge = self.charge + 1
            elif self.frame == 24:  # Active on 24-30
                self.charge = min(self.charge, 100)
                self.active_hitboxes.append(Hitbox(60, 30, 52, 34, pi/2, 2 + 3 * (self.charge / 150), 16, 1 / 120,
                                                   28 + 4 * (self.charge / 100), 6, self, False, True, 1.4,
                                                   sound="lasers/laser3"))
            if self.frame > 42:  # 12 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "UpSmash":

            if self.active_hitboxes:  # Moving hitbox
                self.active_hitboxes[-1].relativex -= 20 * signe(self.direction)
                if self.frame > 11:
                    if self.look_right:  # Reverse angle
                        self.active_hitboxes[-1].angle = 2 * pi / 6
                    else:
                        self.active_hitboxes[-1].angle = 4 * pi / 6
                    self.active_hitboxes[-1].relativey += 10
                else:
                    self.active_hitboxes[-1].relativey -= 10

            if self.frame < 5:
                if left:  # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right:
                    self.look_right = True
            if 5 < self.frame < 8 and smash and self.charge < 200:  # Chargement jusqu'à 200 frames
                self.animeframe -= 1
                self.frame = 6
                self.charge = self.charge + 1
            elif self.frame == 10:  # Active on 10-15
                self.charge = min(self.charge, 100)
                self.active_hitboxes.append(
                    Hitbox(30, 10, 32, 32, 2 * pi / 3, 18 + 10 * (self.charge / 100), 13, 1 / 100,
                           22 + 6 * (self.charge / 100), 6, self, False, sound="hits/mini hit"))

            if self.frame > 40:  # 25 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownSmash":

            if self.frame < 3:
                if left:  # peut reverse netre les frames 1 et 2
                    self.look_right = False
                if right:
                    self.look_right = True
            if 3 < self.frame < 6 and smash and self.charge < 200:  # Chargement jusqu'à 200 frames
                self.animeframe -= 1
                self.frame = 4
                self.charge = self.charge + 1
            elif self.frame == 10:  # Active on 10-13
                self.charge = min(self.charge, 100)
                self.active_hitboxes.append(Hitbox(40, 60, 32, 32, -pi / 6, 7 * (self.charge / 200 + 1), 13, 1 / 250,
                                                   19 + 5 * (self.charge / 100), 3, self, False,
                                                   sound="hits/cool hit"))


            if self.frame > 40:  # 23 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
            if self.frame < 25:
                self.vy = 0
                if self.grounded:
                    self.vx += self.dashspeed * signe(self.direction) * (30-(self.frame+1))/25
                else:
                    self.vx -= self.dashspeed * signe(self.direction) * (30-(self.frame+1))/25

            if self.frame == 25:  # active on 25-28
                self.active_hitboxes.append(Hitbox(40, 38, 48, 48, pi / 4, 15, 9.2, 1 / 200, 11, 3, self, False))
            if self.frame > 40:  # 12 frames de lag
                self.attack = None

        if attack == "UpTaunt":

            if self.frame > 30:  # Durée de 30 frames
                self.attack = None

        if attack == "DownTaunt":

            if self.frame > 30:  # Durée de 30 frames
                self.attack = None

        if attack == "LeftTaunt":

            if self.frame > 30:  # Durée de 30 frames
                self.attack = None

        if attack == "RightTaunt":

            if self.frame > 30:  # Durée de 30 frames
                self.attack = None


###################
""" Projectiles """


###################


class Exposant:
    def __init__(self, opponent, own: Balan, charge) -> None:
        self.opponent = opponent
        self.charge = charge + 1
        self.duration = (charge + 1) * 120
        self.own = own
        self.rect = [-1000,-1000,0,0]

    def update(self):
        if self.opponent.rect[1] > 750 or self.opponent.rect[1] < -750 or self.opponent.rect[0] > 750 or self.opponent.rect[0] < -750:
            self.duration = 0
            self.charge = 0
        if self.duration == 1:
            self.own.active_hitboxes.append(
                Hitbox(20, 20, 20, 20, -pi / 2, 2 ** self.charge, 2.4 ** self.charge, 1 / 250, 8 * self.charge, 5,
                       self.opponent, False))
        self.duration -= 1

    def draw(self, window):
        x = self.opponent.rect[0] + self.opponent.rect[2]
        y = self.opponent.rect[1] - resize(0,50,width,height)[1]
        window.blit(exposant_sprite[self.duration // 120], (x + resize(800,0,width,height)[0], y + resize(0,450,width,height)[1]))


##### Autres skins

class Balan2(Balan):
    def __init__(self, x, y, player) -> None:
        super().__init__(x, y, player)
        self.name = "BalanM"


class Balan3(Balan):
    def __init__(self, x, y, player) -> None:
        super().__init__(x, y, player)
        self.name = "BalanJ"
