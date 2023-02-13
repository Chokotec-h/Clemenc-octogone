import pygame
from math import atan, cos, sin, pi
from copy import deepcopy
import DATA.utilities.SoundSystem as SoundSystem
import DATA.utilities.SoundEventsLibs as SFXEvents
from DATA.utilities.functions import *

from DATA.utilities.Animations import get_sprite

from DATA.assets.Misc import Dash_Smoke, Double_Jump

# À FAIRE QUE UNE FOIS
SoundSystem.studio_init()
SFXEvents.SFX_init()
print("[LOG] SFX inited")

SFXDicoEvent = SFXEvents.SFXDicoEvent


def signe(val):
    if val == 0:
        return 0
    else:
        return val / abs(val)


def change_left(x, size, w=48):
    return resize(-x -size,0,width,height)[0]+w


class Hitbox():
    def __init__(self, x, y, sizex, sizey, angle, knockback, damages, damage_stacking, stun, duration, own,
                 position_relative=False, deflect=False, modifier=1, boum=0,
                 sound="hits/8bit hit",linked=False) -> None:
        self.relativex,self.relativey = resize(x,y,width,height)
        self.sizex,self.sizey = resize(sizex,sizey,width,height)
        self.angle = angle
        self.knockback = knockback
        self.damages = damages
        self.damages_stacking = damage_stacking
        self.stun = stun
        self.duration = duration + 1  # Because duration is reduced on init (line 26)
        self.own = own
        self.position_relative = position_relative  # Est-ce que l'ange d'éjection dépend de la position de l'adversaire par rapport à la hitbox ?
        self.deflect = deflect
        self.modifier = modifier
        self.boum = boum
        self.linked = linked
        self.sound = sound.split("/")


        if not own.look_right:
            self.relativex = change_left(x, sizex,own.rect[2])
            self.angle = pi - angle
        self.update()

    def update(self):
        self.x = self.relativex + self.own.rect[0]
        self.y = self.relativey + self.own.rect[1]
        self.duration -= 1

    def draw(self, window):  # debug
        x = self.x
        sizex = self.sizex
        if sizex < 0:
            x = self.x + self.sizex
            sizex = abs(self.sizex)
        pygame.draw.rect(window, (255, 0, 0), (x + resize(800,0,width,height)[0], self.y + resize(0,450,width,height)[1], sizex, self.sizey))


class Char(pygame.sprite.Sprite):  # Personnage de base, possédant les caractéristiques communes à tous les persos
    def __init__(self, speed, dashspeed, airspeed, deceleration, fallspeed, fastfallspeed, fullhop, shorthop,
                 doublejumpheight, airdodgespeed, airdodgetime, dodgeduration):
        pygame.sprite.Sprite.__init__(self)


        self.x = 0
        self.damages = 0.0
        self.direction = 90
        self.vx = 0  # vitesse (x,y)
        self.vy = 0
        self.grounded = False  # Le personnage touche-t-il le sol ?
        self.fastfall = False  # Le personnage fastfall-t-il ?
        self.doublejump = [False]  # Liste des double sauts, ainsi que de leur utilisation

        self.speed = speed  # vitesse au sol
        self.dashspeed = dashspeed  # vitesse de dash
        self.airspeed = airspeed  # vitesse aérienne
        self.deceleration = deceleration  # vitesse de décélération (peut permettre de faire un perso qui glisse ;) )
        self.fallspeed = fallspeed  # vitesse de chute
        self.fastfallspeed = fastfallspeed  # vitesse de fastfall
        self.fullhop = fullhop  # Hauteur de saut (full hop)
        self.shorthop = shorthop  # Hauteur de saut (short hop)
        self.doublejumpheight = doublejumpheight  # Hauteur des double sauts

        self.collidegroup = pygame.sprite.GroupSingle()  # Groupe de collision (spécial à pygame)
        self.collidegroup.add(self)

        self.frame = 0  # Frames écoulées depuis le début de la précédente action
        self.attack = None  # Attaque en cours
        self.can_act = True  # Le personnage peut-il agir ?
        self.upB = False  # Le personnage peut-il agir ?
        self.look_right = True

        self.hitstun = 0  # Frames de hitstun
        self.totalhitstun = 0
        self.active_hitboxes = list()  # Liste des hitbox actives
        self.projectiles = list()
        self.lag = 0
        self.charge = 0
        self.parry = False
        self.lenght_parry = 0
        self.tumble = False
        self.parried = False

        self.jumping = False
        self.dash = False  # Unused

        self.animeframe = 0
        self.show = True
        self.animation = "idle"
        self.name = "Name"

        self.airdodgespeed = airdodgespeed
        self.airdodgetime = airdodgetime
        self.airdodgeduration = dodgeduration
        self.airdodge = False
        self.can_airdodge = True

        self.tech = 0

        self.intangibility = False
        self.dodgex = 0
        self.dodgey = 0

        self.BOUM = 0
        self.superarmor = 0

        self.smoke_dash = list()
        self.double_jump = list()

        self.combo = 0
        self.combodamages = 0
        self.truecombo = 0

        self.immune_to_projectiles = []
        self.die = 0

        self.crouch = 0

        self.sizescale = 4

        self.basecoords = (0,-200)

        self.hasbeenhit = False

        self.projectileid = 0
        self.addeprojectiles = []

    def resize_rect(self):
        self.rect[2], self.rect[3] = resize(self.rect[2], self.rect[3],width,height)

    def inputattack(self, attack):
        if self.attack != attack:
            self.animeframe = 0
            self.tumble = False
            if self.can_act:
                self.frame = 0  # on démarre à la frame 0
                self.attack = attack  # on update l'action en cours
                if attack == "UpB":
                    self.fastfall = False
                    self.can_act = False  # Ne peut pas attaquer après le up B
                    self.upB = True  # Effets spéciaux après upB (uniquement grounded)

    def animation_attack(self, attack, inputs, stage, other):
        pass  # à modifier pour chaque personnage dans <Personnage>.py

    def special(self, inputs):
        return False  # cancel, pour Reignaud

    def act(self, inputs, stage, other, continuer):
        if self.die > 0 and continuer:
            self.move(stage)
            self.special(inputs)
            for i, projectile in enumerate(self.projectiles):
                self.projectiles[i].update()
                if projectile.duration <= 0:
                    del self.projectiles[i]
            self.attack = None
            self.charge = 0
            self.active_hitboxes = list()
            return
        if continuer:
            for i, projectile in enumerate(self.projectiles):
                if projectile not in self.addeprojectiles :
                    self.addeprojectiles.append(projectile)
                    self.projectileid += 1
                    projectile.id = self.projectileid
            if not (self.lag or self.hitstun):
                self.truecombo = 0
            if self.attack is None:
                self.lag = max(0, self.lag - 1)
            self.hitstun = max(0, self.hitstun - 1)
            self.frame += 1
            self.animeframe += 1
            cancel = self.special(inputs)
            self.get_inputs(inputs, stage, other, cancel)
            self.move(stage)
            delete = False
            for i, hitbox in enumerate(self.active_hitboxes):
                hitbox.update()
                if hitbox.duration <= 0:
                    if self.active_hitboxes[i].linked :
                        delete = True
                    del self.active_hitboxes[i]
            if delete :
                self.active_hitboxes = list()
            for i, projectile in enumerate(self.projectiles):
                self.projectiles[i].update()
                if projectile.duration <= 0:
                    del self.projectiles[i]
            self.damages = min(999., self.damages)
            if self.hitstun:  # Arrête la charge des smashs en hitstun
                self.charge = 0
        else:
            self.BOUM = max(0, self.BOUM - 1)

    def get_inputs(self, inputs, stage, other,
                   cancel):  # Cancel spécial pour reignaud (pour pas avoir à tout copier coller)

        (left, right, up, down, fullhop, shorthop, attack, special, shield,
         C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down) = inputs  # dissociation des inputs
        jump = fullhop or shorthop

        self.direction = 90 if self.look_right else -90

        if self.lenght_parry > 0:
            self.lenght_parry += 1
            if self.lenght_parry > 4 and self.lenght_parry < 10:
                self.parry = True
            else:
                self.parry = False
            if self.lenght_parry > 10:
                self.animation = "idle"
                if not self.parried and self.lenght_parry == 11:
                    self.lag = 10
                if (not shield) or (left or right):
                    self.lenght_parry = 0
            else:
                self.animation = "airdodge"
                self.animeframe = self.lenght_parry

        if self.tech > 0:
            self.tech -= 1
            if self.tech == 0:
                self.tech = -20
        if self.tech < 0:
            self.tech += 1

        if not (left or right) or (left and self.look_right) or (
                right and not self.look_right):  # Cancel le dash au changement de direction
            self.dash = False
        if not self.grounded and self.vy > -3 and down and not (
                attack or special or C_Left or C_Right or C_Up or C_Down) and not self.tumble:  # si le personnage est en fin de saut
            if not self.fastfall:  # fastfall
                self.vy = self.vy + self.fastfallspeed * 5
            self.fastfall = True

        

        if self.hitstun:  # Directional Influence
            if self.totalhitstun - self.hitstun < 10:
                if right:
                    self.vx += self.airspeed / 4
                if left:
                    self.vx -= self.airspeed / 4
                if up:
                    self.vy -= self.fallspeed / 4
                if down:
                    self.vy += self.fallspeed / 4
            else:
                if right:
                    self.vx += self.airspeed / 50
                if left:
                    self.vx -= self.airspeed / 50
                if up:
                    self.vy -= self.fallspeed / 50
                if down:
                    self.vy += self.fallspeed / 50
            if shield and self.tech == 0:
                self.tech = 10
        
        else:

            if self.grounded and self.attack is None and not self.lag and shield and self.lenght_parry < 5:
                if right or left:
                    if not self.dash:
                        self.smoke_dash.append(Dash_Smoke(self.rect[0] + self.rect[2] / 2 - (right - 0.5) * 70,
                                                          self.rect[1] + self.rect[3] / 2, right))
                    self.dash = True
                    self.parry = False
                    self.lenght_parry = 0
                elif not self.dash and self.lenght_parry == 0:
                    self.lenght_parry = 1

            if (shield and (not self.grounded) and (self.can_airdodge)
                    and self.attack is None and self.can_act and not self.jumping):
                self.animation = "airdodge"
                self.can_airdodge = False
                self.airdodge = True
                self.dodgex = (right - left) * self.airdodgespeed
                self.dodgey = (down - up) * self.airdodgespeed
                if not self.tumble:
                    self.vx = 0
                    self.vy = 0
                self.vx += self.dodgex * (self.airdodgeduration - self.airdodgetime) / 2
                self.vy += self.dodgey * (self.airdodgeduration - self.airdodgetime) / 2
                self.frame = 0
            if self.hitstun:
                self.active_hitboxes = list()
            if (self.attack is None or cancel) and not self.lag and not (
                    self.airdodge) and self.lenght_parry < 5:  # Si aucune attaque n'est en cours d'exécution et si on n'est pas dans un lag (ex:landing lag)
                if self.grounded:
                    self.animation = "idle"
                elif self.vy > 0:
                    self.animation = "fall"
                else:
                    self.animation = "jump"

                if self.parry:
                    self.animation = "airdodge"

                if right:  # Si on input à droite
                    if special:
                        self.inputattack("SideB")
                    if attack:
                        if self.grounded:
                            self.inputattack("ForwardTilt")
                        else:
                            if not self.look_right:
                                self.inputattack("BackAir")
                            else:
                                self.inputattack("ForwardAir")
                    if self.grounded and not cancel:  # Si le personnage est au sol
                        self.animation = "run" if self.dash else "walk"
                        self.look_right = True  # tourne à droite et se déplace de la vitesse au sol
                        self.vx += self.dashspeed if self.dash else self.speed
                    else:  # Sinon, se déplace de la vitesse aérienne
                        if not self.tumble:
                            self.vx += self.airspeed

                if left:  # Si on input à gauche
                    if special:
                        self.inputattack("SideB")
                    if attack:
                        if self.grounded:
                            self.inputattack("ForwardTilt")
                        else:
                            if self.look_right:
                                self.inputattack("BackAir")
                            else:
                                self.inputattack("ForwardAir")

                    if self.grounded and not cancel:  # la même, mais vers la gauche
                        self.animation = "run" if self.dash else "walk"
                        self.look_right = False
                        self.vx -= self.dashspeed if self.dash else self.speed
                    else:
                        if not self.tumble:
                            self.vx -= self.airspeed
                if up:  # si on input vers le haut
                    if special and not self.upB:  # si la touche spécial est pressée, et que le up b n'a pas été utilisé
                        self.inputattack("UpB")  # on input un upB
                        jump = False  # On input pas un saut en plus
                    if attack:
                        jump = False
                        if self.grounded:
                            self.inputattack("UpTilt")
                        else:
                            self.inputattack("UpAir")

                if jump and not self.jumping:  # si on input un saut
                    if self.grounded:  # Si le personnage est au sol
                        self.animeframe = 0
                        self.tumble = False
                        self.jumping = True
                        if fullhop:
                            self.vy = -self.fullhop  # il utilise son premier saut
                        else:
                            self.vy = -self.shorthop  # il utilise son premier saut

                    else:  # Si le personnage est en l'air
                        self.fastfall = False  # il cesse de fastfall
                        if not self.doublejump[-1]:  # Si il possède un double saut
                            self.animeframe = 0
                            self.tumble = False
                            self.jumping = True
                            self.vy = -self.doublejumpheight  # il saute
                            self.double_jump.append(
                                Double_Jump(self.rect[0] + self.rect[2] / 2, self.rect[1] + self.rect[3] / 2))

                            i = 0  # il montre qu'il utilise le premier saut disponible dans la liste
                            while self.doublejump[i]:  # cette boucle a une fin, qui est testée ligne 70
                                i += 1
                            self.doublejump[i] = True

                # Traversée des plateformes :
                # self.crouch == 0 : normal
                # self.crouch < 0 : appuie une fois sur bas
                # 0 < self.crouch < 9 : appuie une fois sur bas, puis relâche
                # self.crouch > 9 : appuie deux fois sur bas, traverse les plateformes
                if self.crouch < 0:
                    self.crouch += 1
                else:
                    if self.crouch > 0:
                        self.crouch -= 1
                    if self.crouch == 9:
                        self.crouch = 0
                if down:  # Si on input vers le bas
                    if attack:
                        if self.grounded:
                            self.inputattack("DownTilt")
                        else:
                            self.inputattack("DownAir")
                    elif special:
                        self.inputattack("DownB")
                    if self.crouch == 0:
                        self.crouch = -8
                    if self.crouch > 0:
                        self.crouch = 16
                else:
                    if self.crouch < 0:
                        self.crouch = 8

                if not (left or right or up or down):
                    if special:
                        self.inputattack("NeutralB")
                    if attack:
                        if self.grounded:
                            self.inputattack("Jab")
                        else:
                            self.inputattack("NeutralAir")

                if attack and self.dash and self.grounded and shield:
                    self.inputattack("DashAttack")
                    self.dash = False

                if C_Left:  # C-Stick inputs
                    if self.grounded:  # Smash
                        self.look_right = False
                        self.inputattack("ForwardSmash")
                    else:  # Aerial
                        if not self.look_right:
                            self.inputattack("ForwardAir")
                        else:
                            self.inputattack("BackAir")
                if C_Right:
                    if self.grounded:  # Smash
                        self.look_right = True
                        self.inputattack("ForwardSmash")
                    else:  # Aerial
                        if self.look_right:
                            self.inputattack("ForwardAir")
                        else:
                            self.inputattack("BackAir")
                if C_Down:
                    if self.grounded:  # Smash
                        self.inputattack("DownSmash")
                    else:  # Aerial
                        self.inputattack("DownAir")
                if C_Up:
                    if self.grounded:  # Smash
                        self.inputattack("UpSmash")
                    else:  # Aerial
                        self.inputattack("UpAir")

                if self.grounded:
                    if D_Left:
                        self.inputattack("LeftTaunt")
                    if D_Right:
                        self.inputattack("RightTaunt")
                    if D_Up:
                        self.inputattack("UpTaunt")
                    if D_Down:
                        self.inputattack("DownTaunt")

            if self.attack is not None:  # si une attaque est exécutée, on anime la frame suivante
                self.animation_attack(self.attack, inputs, stage, other)
                if not self.grounded:
                    if right:  # drift en l'air
                        self.vx += self.airspeed / 10
                    if left:
                        self.vx -= self.airspeed / 10
            if self.airdodge:
                if self.frame > self.airdodgetime and self.frame < self.airdodgeduration:
                    self.intangibility = True
                    self.tumble = False
                    # self.vx = self.dodgex*(self.airdodgeduration/self.frame)
                    # self.vy = self.dodgey*(self.airdodgeduration/self.frame)
                elif self.frame > self.airdodgeduration:
                    self.intangibility = False
                    self.airdodge = False
                    self.lag = 10

    def touch_stage(self, stage, rect):
        if rect.colliderect(stage.mainplat.rect):
            return True
        for p in stage.plats:
            if rect.colliderect(p.rect) and rect.y + rect.h < p.rect.y + self.vy + 4 and self.crouch < 9:
                return True
        return False

    def move(self, stage):
        if not self.airdodge:
            if self.hitstun:
                self.vy = self.vy + self.fastfallspeed / 2
            elif self.fastfall:  # gravité
                self.vy = self.vy + self.fastfallspeed
            else:
                self.vy = self.vy + self.fallspeed
        else:
            self.vy *= 0.8

        # détection de collisions à la frame suivante
        rect = pygame.Rect(self.rect)
        nextframe = rect.move(self.vx + signe(self.vx), -signe(self.vy))
        if nextframe.colliderect(stage.mainplat.rect):
            i = 0
            previousrect = deepcopy(rect)
            while (not rect.move(signe(self.vx), -signe(self.vy)).colliderect(stage.mainplat.rect)) and i <= (
                    abs(self.vx) + 1) * 3:
                rect.x += signe(self.vx)
                self.x += signe(self.vx)
                i += 1
            if i > (abs(self.vx) + 1) * 3:
                rect = previousrect
            self.x -= signe(self.vx)
            self.vx = 0
        nextframe = rect.move(signe(self.vx), self.vy)
        if self.touch_stage(stage, nextframe):
            i = 0
            previousrect = deepcopy(rect)
            while (not self.touch_stage(stage, rect.move(0, signe(self.vy)))) and i <= (abs(self.vy) + 1) * 3:
                rect.y += signe(self.vy)
                i += 1
            if i > (abs(self.vy) + 1) * 3:
                rect = previousrect
            if self.hitstun:
                self.vy = -self.vy * 0.5
            else:
                self.vy = 0

        # Déplacement
        vx,vy = resize(round(self.vx),self.vy,width,height)
        self.x += vx
        rect.y += vy

        if self.airdodge:
            self.vx *= 0.8
        elif (not self.hitstun) and (not self.tumble):
            # déceleration et vitesse max
            if self.grounded:
                self.vx *= self.deceleration
            elif self.vx < -3 * self.airspeed:
                self.vx = (2 * self.vx - 3 * self.airspeed) / 3
            elif self.vx > 3 * self.airspeed:
                self.vx = (2 * self.vx + 3 * self.airspeed) / 3
            if abs(self.vx) < 0.01:
                self.vx = 0

        # Tech
        if self.touch_stage(stage, rect.move(0, 3)):
            if self.tumble:
                if self.airdodge:
                    self.vx = self.airdodgespeed
                    self.hitstun = 0
                elif self.tech > 0:
                    self.lag = 2
                    self.vx = self.direction / 45
                    self.vy = 0
                    self.hitstun = 0
                else:
                    self.lag = 20
                self.tumble = False
        # Détection de si le personnage est au sol
        if self.touch_stage(stage, rect.move(0, 1)):
            if self.hitstun:  # diminue la vitesse de hitstun
                self.vx *= 0.8
            if not self.can_act:  # permet de jouer après un upb
                self.can_act = True
            if self.upB:  # reset le upb
                self.upB = False
            self.grounded = True
            self.fastfall = False
            if self.airdodge:
                self.airdodge = False
                self.intangibility = False
            self.can_airdodge = True
            for dj in range(len(self.doublejump)):
                self.doublejump[dj] = False
        else:
            self.grounded = False

        rect.x = self.x - rect.w / 2
        # respawn
        self.die = max(0, self.die - 1)
        if (not (self.name == "Le Berre" and self.attack == "ForwardSmash")) and (rect.y > resize(0,1000,width,height)[1] or rect.y < resize(0,-1000,width,height)[1] or self.x < resize(-1000,0,width,height)[0] or self.x > resize(1000,0,width,height)[0]):
            if self.die < 1:
                self.die = 30
                self.damages = 0.
                SFXDicoEvent['hits']["8bit hit"].play() # Son décès
            if self.die == 1:
                self.x,rect.y = self.basecoords
                self.damages = 0.
                self.vy = 0
                self.vx = 0
                self.hitstun = 0
        self.rect = [rect.x,rect.y,rect.w,rect.h]

    def draw(self, window):
        sizescalex,sizescaley = resize(self.sizescale,self.sizescale,width,height)
        drawing_sprite, size, self.animeframe = get_sprite(self.animation, self.name, self.animeframe, self.look_right)
        drawing_sprite = pygame.transform.flip(drawing_sprite.subsurface(size[0], size[1], size[2], size[3]),
                                               not self.look_right, False)
        drawing_sprite = pygame.transform.scale(drawing_sprite, (round(drawing_sprite.get_size()[0] * sizescalex),
                                                                 round(drawing_sprite.get_size()[1] * sizescaley)))  # Rescale
        size = [size[0] * sizescalex, size[1] * sizescaley, size[2] * sizescalex,
                size[3] * sizescaley]  # Rescale
        pos = [self.x + resize(800,0,width,height)[0] - size[2] / 2, self.rect[1] - size[3] + self.rect[3] + resize(0,450,width,height)[1] - 1]  # Position réelle du sprite
        if self.show:
            window.blit(drawing_sprite, pos)  # on dessine le sprite
        # self.rect.y -=  size[3] - self.rect.h # Reste à la surface du stage

        for i, s in enumerate(self.smoke_dash):
            s.draw(window)
            if s.life_time < 0:
                del self.smoke_dash[i]

        for i, s in enumerate(self.double_jump):
            s.draw(window)
            if s.life_time < 0:
                del self.double_jump[i]

        # debug
        if self.parry:
            pygame.draw.rect(window, (200, 200, 200), (pos[0], pos[1], self.rect[2], self.rect[3]))

        # draw projectiles
        for p in self.projectiles:
            p.draw(window)
        
        for d in self.smoke_dash :
            d.draw(window)

    def collide(self, other, inputs):
        left,right,up,down = inputs[:4]
        if self.intangibility > 0:
            self.intangibility -= 1
            if self.intangibility <= 0:
                self.intangibility = False
        self.hasbeenhit = False
        
        # Détection des hitboxes
        for i, hitbox in enumerate(other.active_hitboxes):  
            hit = pygame.Rect(hitbox.x, hitbox.y, hitbox.sizex, hitbox.sizey) 
            if pygame.Rect(self.rect).colliderect(hit):
                self.hasbeenhit = True
                if (not self.parry) and (not self.intangibility):  # Parry
                    if self.truecombo == 0:
                        self.combo = 0
                        self.combodamages = 0
                    self.combo += 1
                    self.combodamages += hitbox.damages
                    self.truecombo += 1
                    if hitbox.position_relative:  # Reverse hit
                        if self.x > hit.x + hit.w // 2 and hitbox.own.direction < 0:
                            hitbox.angle = pi - hitbox.angle
                        if self.x < hit.x - hit.w // 2 and hitbox.own.direction > 0:
                            hitbox.angle = pi - hitbox.angle
                    knockback = hitbox.knockback * (self.damages * hitbox.damages_stacking + 1)
                    if self.superarmor < knockback and not (self.superarmor == -1):

                        angle = calculate_angle(hitbox.angle,left,right,up,down) # Calcul de DI
                        self.BOUM = hitbox.boum + 4
                        self.vx = (hitbox.knockback) * cos(angle) * (
                                self.damages * hitbox.damages_stacking + 1)  # éjection x
                        self.vy = -(hitbox.knockback) * sin(angle) * (
                                self.damages * hitbox.damages_stacking + 1)  # éjection y
                        self.hitstun = hitbox.stun * (self.damages * hitbox.damages_stacking + 2) - (
                                self.superarmor / 5)  # hitstun
                        self.totalhitstun = self.hitstun
                        self.damages += hitbox.damages  # dommages
                        self.rect[1] -= 1
                        self.attack = None  # cancel l'attaque en cours
                        self.upB = False
                        self.can_act = True
                        self.can_airdodge = True
                        self.fastfall = False
                        if abs(self.vx) + abs(self.vy) > 5:
                            self.tumble = True
                    else:
                        if self.superarmor != -1:
                            self.superarmor = max(self.superarmor - hitbox.damages, 0)
                        self.damages += hitbox.damages
                else:
                    if self.parry:
                        other.BOUM = 8
                        self.parried = True
                        other.attack = None
                        other.lag = min(hitbox.damages * hitbox.knockback / 10, 10)
                path = hitbox.sound
                SFXDicoEvent[path[0]][path[1] + ""].play()
                if other.active_hitboxes[i].linked :
                    other.active_hitboxes = list()
                else :
                    del other.active_hitboxes[i]  # Supprime la hitbox
                return


        # Détection des projectiles
        for i, projectile in enumerate(other.projectiles):  
            self.hasbeenhit = True
            for h in self.active_hitboxes:
                hit = pygame.Rect(h.x, h.y, h.sizex, h.sizey) 
                if h.deflect and hit.colliderect(pygame.Rect(projectile.rect)):
                    self.projectiles.append(projectile)
                    projectile.deflect(h.modifier)
                    del other.projectiles[i]  # Supprime la hitbox
                    return

            if pygame.Rect(self.rect).colliderect(pygame.Rect(projectile.rect)) and projectile.id not in self.immune_to_projectiles:
                if (not self.parry) and (not self.intangibility):  # Parry
                    self.immune_to_projectiles.append(projectile.id)
                    if self.truecombo == 0:
                        self.combo = 0
                        self.combodamages = 0
                    self.combo += 1
                    self.combodamages += projectile.damages
                    self.truecombo += 1
                    knockback = projectile.knockback * (self.damages * projectile.damages_stacking + 1)

                    if self.superarmor < knockback and not (self.superarmor == -1):
                        angle = calculate_angle(projectile.angle,left,right,up,down) # Calcul de DI
                        self.vx = projectile.knockback * cos(angle) * (
                                self.damages * projectile.damages_stacking + 1)  # éjection x
                        self.vy = -projectile.knockback * sin(angle) * (
                                self.damages * projectile.damages_stacking + 1)  # éjection y
                        self.hitstun = projectile.stun * (self.damages * projectile.damages_stacking / 2 + 1)  # hitstun
                        self.totalhitstun = self.hitstun
                        self.damages += projectile.damages  # dommages
                        self.rect[1] -= 1
                        self.attack = None
                        self.upB = False
                        self.can_act = True
                        self.can_airdodge = True
                        self.fastfall = False
                        if abs(self.vx) + abs(self.vy) > 5:
                            self.tumble = True
                    else:
                        if self.superarmor != -1:
                            self.superarmor = max(self.superarmor - projectile.damages, 0)
                        self.damages += projectile.damages
                    try:
                        path = projectile.sound.split("/")
                        SFXDicoEvent[path[0]][path[1] + ""].play()
                    except:
                        SFXDicoEvent['hits']["8bit hit"].play()
                else:
                    if self.parry:
                        other.BOUM = 8
                        self.projectiles.append(projectile)  # Renvoie le projectile
                        projectile.deflect(1)
                        del other.projectiles[i]
                        self.parried = True
                        other.attack = None
                        other.lag = min(projectile.damages * projectile.knockback / 10, 9)
                return

def calculate_angle(base_angle,left,right,up,down):

    lr = right - left
    ud = down - up
    if abs(lr) < 0.1: 
        if abs(ud) < 0.1:
            return base_angle
        stickangle = (pi/2)*signe(ud)
    else :
        if lr < 0 :
            stickangle = pi-atan(ud/lr)
        else :
            stickangle = atan(ud/lr)
    #print(base_angle)
    #print(stickangle)
    #print(base_angle + pi/10*sin(stickangle-base_angle))
    #print()
    return base_angle + pi/10*sin(stickangle-base_angle)
