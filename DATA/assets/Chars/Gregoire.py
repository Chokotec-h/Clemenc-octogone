from random import randint, choice
from DATA.utilities.Base_Char import Char, Hitbox, signe, SFXDicoEvent
import pygame
from math import pi, cos, sin, asin, sqrt
import DATA.utilities.Animations as Animations
from DATA.utilities.functions import *


def incertitude(x):
    return x + randint(round(-x / (2 * sqrt(3))) * 10, round(x / (2 * sqrt(3))) * 10) / 10


##### Grégoire

class Gregoire(Char):
    def __init__(self, x, y, player) -> None:
        super().__init__(speed=0.9, dashspeed=1.9, airspeed=1.3, deceleration=0.9, fallspeed=0.7, fastfallspeed=1.4,
                         fullhop=15, shorthop=13,
                         doublejumpheight=16, airdodgespeed=6, airdodgetime=3, dodgeduration=15)

        self.rect = [100, 0, 60, 144]  # Crée le rectangle de perso

        self.name = "Gregoire"
        self.x = x
        self.rect[1] = y
        self.player = player
        self.angle_rayon = -pi / 300000
        self.rapidjab = False
        self.strongfair = False
        self.resize_rect()

    def __str__(self) -> str:
        return "Gregoire"

    def special(self, inputs):
        if self.attack is None:
            self.angle_rayon = -pi / 300000
            self.strongfair = False
        if self.strongfair:
            self.superarmor = -1
        else:
            self.superarmor = 14
        return False

    def animation_attack(self, attack, inputs, stage, other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs  # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up

        if attack == "UpB":
            if self.frame < 12:
                if left:  # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right:
                    self.look_right = True
            if self.frame == 12:
                self.projectiles.append(Quantique(self))
            if self.frame > 12 and self.frame < 25:  # Saute frame 12
                self.can_act = False  # ne peut pas agir après un grounded up B
                self.vx = (right - left) * 20
                self.vy = (down - up) * 20
                self.airdodge = True
                self.doublejump = [True for _ in self.doublejump]  # Annule tout les sauts
            if self.frame > 40:
                self.airdodge = False
                self.vy = 0
                self.vx = 0
            if self.frame > 45:  # 5 frames de lag
                self.attack = None

        if attack == "NeutralB":
            if self.frame < 5:
                if left:
                    self.look_right = False
                if right:
                    self.look_right = True
            if self.frame == 8:
                self.animation = "neutralB"
                self.animeframe = 0
            if self.frame < 25:
                if up:
                    self.angle_rayon = pi / 4
                if down:
                    self.angle_rayon = -pi / 6
                if left:
                    self.look_right = False
                if right:
                    self.look_right = True
            if 25 < self.frame < 45:
                if self.frame == 26:
                    SFXDicoEvent['lasers']["laser2"].play()
                self.vy = 0
                self.projectiles.append(
                    Rayon(stage, self.x, self.rect[1] + 24, -self.angle_rayon * signe(self.direction),
                          self))  # l'angle est chelou parce que j'ai géré la vitesse du rayon de façon merdique  # Mais on s'en fout ça marche
            if self.frame > 50:  # 25 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownB":
            if self.frame == 10:
                self.animation = "downb_charge"
                self.animeframe = 0
            if self.frame < 10:
                if left:
                    self.look_right = False
                if right:
                    self.look_right = True
            if self.frame == 70:
                self.animation = "downb_release"
                self.animeframe = 0
            if self.frame == 70:
                self.active_hitboxes.append(
                    Hitbox(32, 32, 64, 64, pi / 4, 23, 68.29, 1 / 100, 9, 5, self, False, sound="explosions/Cannon"))
            if self.frame > 120:  # 15 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame == 8:
                self.animation = "sideB"
                self.animeframe = 0
            if self.frame < 8:
                if left:  # peut reverse netre les frames 1 et 7
                    self.look_right = False
                if right:
                    self.look_right = True
            if 23 < self.frame < 48:
                self.projectiles.append(Thunder(self.x + resize(24 * signe(self.direction) - 48,0,width,height)[0], self.rect[1] + resize(0,24,width,height)[1], self))
            if self.frame == 49:
                self.active_hitboxes.append(
                    Hitbox(32, 32, 32, 64, pi / 4, 14, incertitude(7), 1 / 150, 15, 3, self, False))
            if 50 < self.frame < 90:
                if self.active_hitboxes:
                    self.active_hitboxes[-1].duration += 1
                    self.active_hitboxes[-1].relativex += 24 * signe(self.direction)
            if self.frame > 92:  # 44 frames de lag
                self.attack = None

        if attack == "Jab":
            if self.frame == 8:
                self.animation = "jab"
                self.animeframe = 0
            if attack_button and self.frame < 2:
                self.rapidjab = True
            if self.frame > 10 and self.rapidjab:
                if self.look_right:
                    x = 24
                    angle = 3 * pi / 4
                else:
                    x = -29
                    angle = pi / 4
                self.projectiles.append(Sinusoide(self.x + resize(x,0,width,height)[0], self.rect[1] + resize(0,50 + 20 * cos(self.frame / 2),width,height)[1], angle, self))
            if self.rapidjab and not attack_button:
                self.rapidjab = False
                self.frame = 0
            if not self.rapidjab:
                if self.frame == 3:
                    self.active_hitboxes.append(
                        Hitbox(32, 32, 64, 64, pi / 4, 10, incertitude(2.5), 1 / 200, 8, 3, self, False))
                if self.frame > 30:  # 24 frames de lag
                    self.attack = None

        if attack == "DownTilt":
            if self.frame == 0:
                self.animation = "dtilt"
                self.animeframe = 0
            if self.frame == 16:
                self.active_hitboxes.append(
                    Hitbox(32, 64, 48, 48, -2 * pi / 5, 22, incertitude(9), 1 / 200, 13, 3, self, False,
                           sound="hits/punch2"))
            if self.frame > 35:  # 19 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame == 0:
                self.animation = "ftilt"
                self.animeframe = 0
            if self.frame < 3:
                if left:
                    self.look_right = False
                if right:
                    self.look_right = True
            if self.frame == 10:
                self.active_hitboxes.append(
                    Hitbox(48, 52, 32, 32, pi / 4, 19, incertitude(8), 1 / 225, 10, 3, self, False,
                           sound="hits/punch"))
            if self.frame > 33:  # 27 frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame == 0:
                self.animation = "utilt"
                self.animeframe = 0
            if self.frame == 8:
                self.vy = -6
                angle = pi / 2
                self.active_hitboxes.append(
                    Hitbox(-5, -12, 58, 58, angle, 15, incertitude(10), 1 / 300, 13, 3, self, False,
                           sound="hits/punch2"))
            if self.frame > 25:  # Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame == 0:
                self.animation = "uair"
                self.animeframe = 0
            if self.frame < 25:
                self.vy = 0
                self.vx *= 0.8
            if self.frame == 15:  # 15-23
                self.active_hitboxes.append(
                    Hitbox(40, 10, 32, 32, pi / 2, 20, incertitude(12), 1 / 90, 12, 8, self, False,
                           sound="hits/cool hit"))

            if self.frame > 45:  # 22 frames de lag
                self.attack = None

            if self.grounded:
                self.attack = None
                if 30 > self.frame > 2:
                    self.lag = 6  # Auto cancel frame 1-2 et 30+, 6 frames de landing lag

        if attack == "ForwardAir":
            if self.frame == 0:
                self.animation = "fair"
                self.animeframe = 0
            if self.frame == 7:
                if shield:
                    self.strongfair = True
                    self.animation = "fair2"
                    self.animeframe = 7
                else:
                    self.strongfair = False
                    self.active_hitboxes.append(Hitbox(48, 32, 36, 16, pi / 4, 12, 9, 1 / 200, 13, 3, self,
                                                       sound="hits/8bit hit reverse"))
            if self.frame < 10 and self.active_hitboxes:
                self.active_hitboxes[-1].sizey += 16
            if self.frame == 45:
                self.active_hitboxes.append(
                    Hitbox(48, 45, 16, 16, pi / 2, 3, 95.45, 1 / 1000, 25, 3, self, False, boum=30,
                           sound="hits/slap"))
            if self.frame > 69 or (self.frame > 40 and not self.strongfair):  # 24 frames de lag
                self.attack = None

            # Pas d'auto cancel. Agit même après avoir atterri

        if attack == "BackAir":
            if self.frame == 0:
                self.animation = "bair"
                self.animeframe = 0
            if self.frame == 13:
                self.active_hitboxes.append(
                    Hitbox(-48, 64, 32, 32, pi / 6, 25, incertitude(13), 1 / 200, 14, 5, self, False,
                           sound="wooshs/other woosh"))
            if self.frame > 27:  # 11 frames de lag
                self.attack = None

            if self.grounded:
                self.attack = None
                if self.frame < 22 and self.frame > 2:
                    self.lag = 5  # Auto cancel frame 1-2 et 22+, 5 frames de landing lag

        if attack == "DownAir":
            if self.frame == 0:
                self.animation = "dair_dive"
                self.animeframe = 0
            self.vx = min(self.frame / 10, 15) * signe(self.direction)
            if self.frame < 14:
                self.vy = 0
            self.vy *= 1.1
            if self.frame == 17:
                self.active_hitboxes.append(
                    Hitbox(0, 0, 48, 128, -pi / 2, 19, incertitude(10), 1 / 200, 15, 4096, self, False,
                           sound="hits/cool hit"))
            if self.frame > 19:
                if self.active_hitboxes:
                    self.active_hitboxes[-1].knockback = 8
                    self.active_hitboxes[-1].damages = incertitude(7)
                    self.active_hitboxes[-1].damages_stacking = 1 / 500
                    self.active_hitboxes[-1].hitstun = 5
                    if self.frame % 2 == 0:
                        self.active_hitboxes[-1].angle = 0 if self.look_right else pi
                    else:
                        self.active_hitboxes[-1].angle = pi if self.look_right else 0

            if self.frame == 50:
                self.animation = "dair_fall"
                self.animeframe = 0
            if self.grounded:
                self.animation = "dair_ground"
                self.animeframe = 0
            if self.grounded or self.frame > 60 :
                if self.active_hitboxes:
                    self.active_hitboxes = list()
                self.attack = None
                self.lag = 15  # Ne se termine que lorsqu'il touche le sol ou au bout de 60 frames

        if attack == "NeutralAir":
            if self.frame == 0:
                self.animation = "nair"
                self.animeframe = 0
            if self.frame == 12:
                self.active_hitboxes.append(Hitbox(48, 48, 32, 32, pi / 2, 2, incertitude(6), 0, 20, 3, self, False,
                                                   sound="hits/punch2"))
            if self.frame == 18:
                self.active_hitboxes.append(
                    Hitbox(48, 48, 48, 48, 2 * pi / 5, 20, incertitude(10), 1 / 250, 12, 3, self, False,
                           sound="hits/punch1"))

            if self.frame > 40:  # 26 frames de lag
                self.attack = None

            if self.grounded:
                self.attack = None
                if self.frame < 28 and self.frame > 3:
                    self.lag = 12  # Auto cancel frame 1-3 et 28+, 12 frames de landing lag

        if attack == "ForwardSmash":
            if self.frame == 0:
                self.animation = "fsmash"
                self.animeframe = 0
            if self.frame > 3 and self.frame < 6 and smash and self.charge < 200:  # Chargement jusqu'à 200 frames
                self.frame = 4
                self.charge = self.charge + 1
                self.animeframe -= 1

            elif self.frame == 24:  # Active on 24-27
                self.vx = 10 * signe(self.direction)
                self.charge = min(self.charge, 100)
                self.active_hitboxes.append(
                    Hitbox(48, 16, 48, 48, pi / 4, 22 + 12 * (self.charge / 200), incertitude(20), 1 / 250,
                           9 + 8 * (self.charge / 100), 5, self, True, sound="hits/punch1"))
            elif self.frame == 24:  # Late hitbox
                if self.active_hitboxes:
                    self.active_hitboxes[-1].knockback *= 0.5
            if self.frame > 69:  # 42 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "UpSmash":
            if self.frame == 0:
                self.animation = "usmash"
                self.animeframe = 0

            if self.active_hitboxes:  # Moving hitbox
                self.active_hitboxes[-1].relativey -= 20

            if self.frame < 5:
                if left:  # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right:
                    self.look_right = True
            if self.frame > 4 and self.frame < 8 and smash and self.charge < 200:  # Chargement jusqu'à 200 frames
                self.frame = 5
                self.charge = self.charge + 1
                self.animeframe -= 1

            elif self.frame == 11:  # Active on 11-16
                self.charge = min(self.charge, 100)
                self.active_hitboxes.append(Hitbox(50, 40, 48, 48, pi / 2, 19 + 10 * (self.charge / 200), 18, 1 / 90,
                                                   10 + 7 * (self.charge / 100), 5, self, False,
                                                   sound="hits/punch1"))

            if self.frame > 57:  # 44 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownSmash":
            if self.frame == 0:
                self.animation = "dsmash"
                self.animeframe = 0

            if self.frame < 2:
                if left:  # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right:
                    self.look_right = True
            if self.frame > 4 and self.frame < 6 and smash and self.charge < 200:  # Chargement jusqu'à 200 frames
                self.frame = 4
                self.charge = self.charge + 1
                self.animeframe -= 1
            elif self.frame == 10:  # Active on 10-16
                self.charge = min(self.charge, 100)
                self.active_hitboxes.append(
                    Hitbox(30, 60, 60, 32, pi / 2, 20 + 10 * (self.charge / 200), incertitude(13), 1 / 250,
                           9 + 5 * (self.charge / 150), 6, self, False, sound="hits/punch"))

            if self.frame > 35:  # 19 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
            if self.frame == 0:
                self.animation = "dashattack"
                self.animeframe = 0
            if self.frame == 9:
                self.active_hitboxes.append(
                    Hitbox(0, 64, 64, 48, pi / 5, 9, incertitude(9), 1 / 250, 8, 20, self, False))
            if self.frame == 30:
                self.active_hitboxes.append(
                    Hitbox(48, 64, 48, 48, -2 * pi / 5, 12, incertitude(12), 1 / 150, 12, 2, self, False,
                           sound="hits/cool hit"))
            if self.frame < 30:
                self.vy = 0
                if self.grounded:
                    self.vx += self.dashspeed * signe(self.direction) / 2
                else:
                    self.vx -= self.dashspeed * signe(self.direction) / 2

            if self.frame > 55:  # 27 frames de lag
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

class Rayon():
    def __init__(self, stage, x, y, angle_fwd, own: Gregoire) -> None:
        self.sound = 'lasers/cool lazer'
        self.stage = stage
        self.x = x
        self.y = y
        self.angle_fwd = angle_fwd
        self.v = 9 * signe(own.direction)
        self.rect = [x, y] + list(resize(25, 25,width,height))
        self.damages_stacking = 1 / 300
        if own.look_right:
            self.angle = pi / 4
        else:
            self.angle = 3 * pi / 4
        self.knockback = 3
        self.damages = incertitude(0.2)
        self.stun = 4
        self.duration = 10
        self.g = -6.74 / 4
        nextx = self.x + resize(cos(self.angle_fwd) * self.v,0,width,height)[0]
        nexty = self.y + resize(0,sin(self.angle_fwd) * self.v + self.g,width,height)[1]
        self.g += 0.0981
        self.x = nextx
        self.y = nexty

    def touch_stage(self, stage, rect):
        if rect.colliderect(stage.mainplat.rect):
            return True
        for p in stage.plats:
            if rect.colliderect(p.rect) and rect.y + rect.h - 4 < p.rect.y + self.v * sin(self.angle_fwd) + 4:
                return True
        return False

    def update(self):
        nexty = self.y + resize(0,sin(self.angle_fwd) * self.v + self.g,width,height)[1]
        if self.touch_stage(self.stage, pygame.Rect(self.x, nexty, 5, 5)):
            self.g = -6.74 / 4
            if self.rect[1] < self.stage.mainplat.rect.y - self.g + abs(self.v) + 5:
                self.angle_fwd = -self.angle_fwd
            else:
                self.angle_fwd = pi - self.angle_fwd

        nextx = self.x + resize(cos(self.angle_fwd) * self.v,0,width,height)[0]
        self.g += 0.0981 * 2
        self.x = nextx
        self.y = nexty
        self.rect = [self.x, self.y, 5, 5]
        if self.x < -1000 or self.x > 1000 or self.y > 1000:
            self.duration = 0

    def draw(self, window):
        pygame.draw.rect(window, (250, 0, 0), (self.x + resize(800,0,width,height)[0], self.y + resize(0,450,width,height)[1], resize(10,0,width,height)[0], resize(0,10,width,height)[1]))

    def deflect(self, modifier):
        self.v *= -modifier


thundersprite = pygame.transform.scale(
    pygame.image.load(f"DATA/Images/Sprites/Projectiles/Millet_Gregoire/Thunder.png"), resize(48, 48,width,height))


class Thunder():
    def __init__(self, x, y, own: Gregoire) -> None:
        self.id = 0
        self.size = 2
        self.x = x
        self.y = y + 8
        self.vx = 24 * signe(own.direction)
        self.duration = 50
        self.knockback = 1
        self.damages = incertitude(0.2)
        self.stun = 12
        self.damages_stacking = 0
        if own.look_right:
            self.angle = pi / 4
        else:
            self.angle = 3 * pi / 4
        self.rect = [x, y, 2, 2]
        if not own.look_right:
            self.x += 32

    def update(self):
        rect = thundersprite.get_rect(topleft=(self.x, self.y))
        self.rect = [rect.x,rect.y,rect.w,rect.h]
        self.x += resize(self.vx,0,width,height)[0]
        self.duration -= 1

    def draw(self, window):
        window.blit(thundersprite, (self.x + resize(800,0,width,height)[0], self.y + resize(0,450,width,height)[1]))

    def deflect(self, modifier):
        self.vx = -self.vx
        self.damages *= modifier
        self.angle = -self.angle


class Sinusoide():
    def __init__(self, x, y, angle, own: Gregoire) -> None:
        self.id = 0
        self.sound = 'hits/hit'
        self.rect = [x, y] + list(resize(5, 5,width,height))
        self.angle = angle
        self.v = 5 * signe(own.direction)
        self.duration = 15
        self.knockback = 0.5
        self.damages = incertitude(0.05)
        self.stun = 3
        self.damages_stacking = 1 / 550

    def update(self):
        self.rect[0] += resize(self.v,0,width,height)[0]
        self.duration -= 1

    def draw(self, window):
        pygame.draw.rect(window, (220, 200, 120), (self.rect[0] + resize(800,0,width,height)[0], self.rect[1] + resize(0,450,width,height)[1], self.rect[2], self.rect[3]))

    def deflect(self, modifier):
        self.duration = 0


class Quantique():
    def __init__(self, own: Gregoire) -> None:
        self.id = 0
        self.rect = own.rect
        self.x,self.y = own.x,own.rect[1]
        self.own = own
        self.animeframe = self.own.animeframe
        self.duration = 120
        self.angle = pi / 2
        self.knockback = 7
        self.damages = incertitude(3)
        self.stun = 15
        self.damages_stacking = 1 / 250
        self.vy = 0
        self.g = False

    def update(self):
        self.duration -= 1
        if self.g:
            self.vy += 1
        self.y = self.y + resize(0,self.vy,width,height)[1]

    def deflect(self, modifier):
        self.vy = modifier * 10
        self.g = True

    def draw(self, window):
        sizescalex,sizescaley = resize(self.own.sizescale,self.own.sizescale,width,height)
        drawing_sprite,size,self.animeframe = Animations.get_sprite(self.own.animation,self.own.name,self.animeframe+1,self.own.look_right)
        drawing_sprite = pygame.transform.flip(drawing_sprite.subsurface(size[0], size[1], size[2], size[3]),
                                               not self.own.look_right, False)
        drawing_sprite = pygame.transform.scale(drawing_sprite, (round(drawing_sprite.get_size()[0] * sizescalex),
                                                                 round(drawing_sprite.get_size()[1] * sizescaley)))  # Rescale
        size = [size[0] * sizescalex, size[1] * sizescaley, size[2] * sizescalex,
                size[3] * sizescaley]  # Rescale

        pos = [self.x + resize(800,0,width,height)[0] - size[2] / 2, self.rect[1] - size[3] + self.rect[3] + resize(0,450,width,height)[1] - 1]  # Position réelle du sprite

        window.blit(drawing_sprite, pos)
