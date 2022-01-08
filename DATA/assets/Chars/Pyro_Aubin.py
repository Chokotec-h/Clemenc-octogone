from DATA.utilities.Animations import get_sprite
from DATA.utilities.Base_Char import Char, Hitbox, change_left, signe
import pygame
from math import atan, degrees, floor, pi, sqrt, sin, cos
from DATA.utilities.Sound_manager import playsound

from DATA.utilities.Interface import Texte


##### Aubin

class Pyro_Aubin(Char):
    def __init__(self,x,y,player) -> None:
        super().__init__(speed=2, dashspeed=3, airspeed=1.2, deceleration=0.8, fallspeed=0.6, fastfallspeed=1.2, fullhop=13, shorthop=10,
                         doublejumpheight=15,airdodgespeed=6,airdodgetime=3,dodgeduration=15)

        self.rect = pygame.Rect(100,0,48,120) # Crée le rectangle de perso
        self.jumpsound = pygame.mixer.Sound("DATA/Musics/SE/jump.wav") # Son test
        self.name = "Pyro-Aubin"
        self.konamiadd = False
        self.x = x
        self.rect.y = y
        self.konami = []
        self.backspecial = []
        self.player = player
        self.explosifs = 25
        self.angle_fusee = 0
        self.hold = 0
        self.turnaround = 0
    
    def __str__(self) -> str:
        return "Pyro-Aubin"

    def special(self,inputs):
        if self.attack == "DashAttack":
            self.deceleration = 0.9
        else :
            self.deceleration = 0.8
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs
        special = inputs[7]

        # Annule backspecial si input trop long ou si d'autres inputs
        if self.backspecial :
            self.backspecial[-1] -= 1
            if self.backspecial [-1] < 0:
                self.backspecial = []
        if up or fullhop or shorthop or attack_button or shield or C_Left or C_Down or C_Right or C_Up or D_Down or D_Left or D_Right or D_Up :
            self.backspecial = []

        if down :
            self.backspecial = [8]
        if left :
            if self.look_right :
                if len(self.backspecial) == 1 :
                    self.backspecial.append(8)
                    inputs[0] = False
                elif len(self.backspecial) > 1 :
                    self.look_right = True
                    inputs[0] = False
            else :
                self.backspecial = []
        if right:
            if not self.look_right :
                if len(self.backspecial) == 1 :
                    self.backspecial.append(8)
                    inputs[1] = False
                elif len(self.backspecial) > 1 :
                    self.look_right = False
                    inputs[1] = False
            else :
                self.backspecial = []
        if special :
            if len(self.backspecial) == 2 :
                self.backspecial = []
                self.inputattack("BackSpecial")
            else :
                self.backspecial = []

        if self.konami == ["Up","Up","Down","Down","Left","Right","Left","Right","B","A"]:
            self.inputattack("Superspecial")
        self.explosifs = min(self.explosifs+0.5/60,50)

    def animation_attack(self,attack,inputs,stage,other):
        left, right, up, down, fullhop, shorthop, attack_button, special, shield, C_Left, C_Right, C_Up, C_Down, D_Left, D_Right, D_Up, D_Down = inputs # dissociation des inputs
        smash = C_Down or C_Left or C_Right or C_Up
        if attack == "UpB":
            if self.frame == 2 :
                self.angle_fusee = pi/2
            if self.angle_fusee > -1 and self.frame > 5: # Saute frame 11
                if special :
                    self.frame -= 1
                    if self. explosifs > 0.1 :
                        self.explosifs -= 0.1
                    else :
                        self.frame = 20
                    if left :
                        self.angle_fusee += 0.05
                        if self.angle_fusee < 0 :
                            self.angle_fusee = 2*pi
                    if right :
                        self.angle_fusee -= 0.05
                        if self.angle_fusee > 2*pi :
                            self.angle_fusee = 0
                self.vx = cos(self.angle_fusee) * 10
                self.vy = -sin(self.angle_fusee) * 10
            if self.frame > 18 :
                self.can_act = False # ne peut pas agir après un grounded up B
                self.attack = None
                self.doublejump = [True for _ in self.doublejump] # Annule tout les sauts

        if attack == "NeutralB":
            if self.frame < 5 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.konami == ["Up","Up","Down","Down","Left","Right","Left","Right"] and not self.konamiadd:
                self.konamiadd = True
                print("B")
                self.konami.append("B")
            #elif not self.konamiadd :
            #    self.konami = []
            if self.frame == 5 :
                launch = False
                for p in self.projectiles :
                    if isinstance(p,Fusee) and not p.done:
                        launch = True
                if launch :
                    for p in self.projectiles:
                        if isinstance(p,Fusee) and not p.done and self.explosifs > 5 and not p.homing :
                            self.explosifs -= 5
                            p.homing = True
                elif self.explosifs > 1:
                    self.explosifs -= 1
                    self.projectiles.append(Fusee(stage,self,other))

            if self.frame > 15: # 10 frames de lag
                self.attack = None
                self.konamiadd = False
                self.charge = 0

        if attack == "DownB":
            if self.frame == 10:
                if self.explosifs > 6 :
                    if left :
                        if self.look_right :
                            v = 0.5
                        else :
                            v = -10
                    elif right :
                        if self.look_right :
                            v = 10
                        else :
                            v = -0.5
                    else :
                        v = 5*signe(self.direction)
                    self.projectiles.append(Grenade(self,other,v,stage))
                    playsound("DATA/Musics/SE/wooshs/mini woosh.wav")
                    self.explosifs -= 6
            if self.frame > 20 : # 15 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "SideB":
            if self.frame < 5:
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 10 :
                self.hold = 0
                self.turnaround = 0
            if self.frame > 14 and self.frame < 17 :
                self.vy = -self.fallspeed
                self.fastfall = False
                if self.explosifs > 0.5 :
                    if special :
                        self.frame = 14
                        self.explosifs -= 0.1
                        self.hold += 1
                    if self.hold % 5 == 0:
                        self.active_hitboxes.append(Hitbox(-10,100,100,20,3*pi/4,abs(self.vx),10,1/200,7,5,self))

                    if ((left and self.look_right) or (right and not self.look_right)) and self.turnaround == 0:
                        self.turnaround = 1
                    self.vx += signe(self.direction)*4
                else :
                    self.frame = 18
                    self.hold = -1

            if self.turnaround > 0 :
                if self.explosifs > 0.5 :
                    self.explosifs -= 0.1
                    
                    self.vx *= 0.65
                    self.turnaround += 1
                    self.hold = 1
                    if self.turnaround == 5 :
                        self.active_hitboxes.append(Hitbox(36,80,46,46,pi/4,4,7,1/500,8,15,self))
                    if self.turnaround > 25 :
                        self.turnaround = 0
                        self.look_right = not self.look_right
                        self.vx = 0
                else :
                    self.look_right = not self.look_right
                    self.hold = -1

            
            if self.hold == -1 :
                if self.frame > 20 and self.frame < 25 :
                    self.vx *= 0.8
                if self.frame > 80 :
                    self.attack = None
            else :
                if self.frame == 22 and special:
                    if self.explosifs > 4 :
                        self.explosifs -= 4
                        self.active_hitboxes.append(Hitbox(-31,5,110,110,pi/2,20,18,1/100,19,2,self,boum=5))
                        self.vy = -20
                        self.can_act = False
                if self.frame > 30 :
                    self.attack = None


            if self.frame > 80 : # 20 frames de lag
                self.attack = None

        if attack == "Jab":
            if self.konami == ["Up","Up","Down","Down","Left","Right","Left","Right","B"] and not self.konamiadd:
                self.konamiadd = True
                print("A")
                self.konami.append("A")
                self.attack = None
            #elif not self.konamiadd :
            #    self.konami = []

            if self.frame == 5 :
                self.active_hitboxes.append(Hitbox(50,85,30,30,pi/6,7,9,1/200,10,4,self))

            if self.frame > 20: # 11 frames de lag
                self.attack = None

        if attack == "DownTilt":
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(48,80,48,48,-pi/3,10,6,1/200,8,17,self,sound="hits and slap/cool hit.wav"))
            if self.frame > 8 and self.active_hitboxes:
                self.active_hitboxes[-1].relativey += self.frame

            if self.frame > 33: # 10 frames de lag
                self.attack = None

        if attack == "ForwardTilt":
            if self.frame < 3 :
                if left :
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame == 8 :
                if self.explosifs > 5 :
                    self.explosifs -= 5
                    playsound("DATA/Musics/SE/other/gun shot.wav")
                    self.vx = -signe(self.direction)*10
                    self.active_hitboxes.append(Hitbox(48,60,60,60,pi/6,15,13,1/150,17,2,self,boum=2))
                else :
                    self.active_hitboxes.append(Hitbox(48,60,32,32,pi/5,10,3,1/220,8,3,self))

            if self.frame > 30: # 8 frames de lag
                self.attack = None

        if attack == "UpTilt":
            if self.frame == 8 :
                self.active_hitboxes.append(Hitbox(50,60,30,30,pi/2,15,4,1/300,12,4,self,deflect=True,modifier=0.5,sound="hits and slap/punch2.mp3"))
            if self.frame == 10 and self.active_hitboxes :
                self.active_hitboxes[-1].relativey -= 20
            if self.frame > 25: # 11 Frames de lag
                self.attack = None

        if attack == "UpAir":
            if self.frame == 6 :
                self.active_hitboxes.append(Hitbox(45,-30,60,60,pi/3,9,9,1/200,16,4,self))
            if self.frame > 6 and self.active_hitboxes:
                self.active_hitboxes[-1].relativex -= 30*signe(self.direction)
                if self.frame == 8 :
                    if self.look_right :
                        self.active_hitboxes[-1].angle = 2*pi/3
                    else :
                        self.active_hitboxes[-1].angle = pi/3

            if self.frame > 25: # 10 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 22 and self.frame > 2 :
                    self.lag = 8 # Auto cancel frame 1-2 et 22+, 8 frames de landing lag

        if attack == "ForwardAir":
            if self.frame == 8 :
                if self.explosifs > 5:
                    self.explosifs -= 5
                    playsound("DATA/Musics/SE/other/gun shot.wav")
                    self.active_hitboxes.append(Hitbox(50,30,64,64,-pi/6,15,15,1/180,15,2,self))
                    self.vy -= 8
                else :
                    self.active_hitboxes.append(Hitbox(50,30,32,32,0,7,5,1/220,6,4,self))

            if self.frame > 35: # 29 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 30 and self.frame > 5 :
                    self.lag = 16 # Auto cancel frame 1-5 et 22+, 16 frames de landing lag

        if attack == "BackAir":
            if self.frame == 12 :
                if self.explosifs > 4 :
                    self.explosifs -= 4
                    playsound("DATA/Musics/SE/other/gun shot.wav")
                    self.active_hitboxes.append(Hitbox(-60,30,60,60,pi-0.01,13,15,1/130,12,2,self,boum=2))
                    self.vx += signe(self.direction)*15

            if self.frame > 25: # 14 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 19 and self.frame > 3 :
                    self.lag = 10 # Auto cancel frame 1-3 et 19+, 10 frames de landing lag

        if attack == "DownAir":
            if self.frame == 13 :
                self.active_hitboxes.append(Hitbox(-1,100,50,50,-pi/2,12,14,1/190,15,3,self))

            if self.frame > 40: # 25 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 32 and self.frame > 5 :
                    self.lag = 19 # Auto cancel frame 1-5 et 32+, 19 frames de landing lag

        if attack == "NeutralAir":
            if self.konami == ["Up","Up","Down","Down","Left","Right","Left","Right","B"] and not self.konamiadd:
                self.konamiadd = True
                print("A")
                self.konami.append("A")
                self.attack = None
            #elif not self.konamiadd :
            #    self.konami = []
            if self.frame == 4 :
                if self.explosifs > 0.5 :
                    self.explosifs -= 0.5
                    playsound("DATA/Musics/SE/other/gun shot.wav")
                    self.active_hitboxes.append(Hitbox(48,30,60,60,pi/2,12,11,1/100,20,2,self))
                else :
                    self.active_hitboxes.append(Hitbox(48,48,32,32,pi/2,10,9,1/250,10,2,self))
            if self.frame == 8 :
                if self.explosifs > 0.5 :
                    self.explosifs -= 0.5
                    playsound("DATA/Musics/SE/other/gun shot.wav")
                    self.active_hitboxes.append(Hitbox(12,130,60,60,pi/2,12,11,1/100,20,2,self))
            if self.frame == 12 :
                if self.explosifs > 0.5 :
                    self.explosifs -= 0.5
                    playsound("DATA/Musics/SE/other/gun shot.wav")
                    self.active_hitboxes.append(Hitbox(-72,130,60,60,pi/2,12,11,1/100,20,2,self))
            if self.frame == 16 :
                if self.explosifs > 0.5 :
                    self.explosifs -= 0.5
                    playsound("DATA/Musics/SE/other/gun shot.wav")
                    self.active_hitboxes.append(Hitbox(change_left(48,60),30,60,60,pi/2,12,11,1/100,20,2,self))
            if self.frame == 20 :
                if self.explosifs > 0.5 :
                    self.explosifs -= 0.5
                    playsound("DATA/Musics/SE/other/gun shot.wav")
                    self.active_hitboxes.append(Hitbox(-72,-70,60,60,pi/2,12,11,1/100,20,2,self))
            if self.frame == 24 :
                if self.explosifs > 0.5 :
                    self.explosifs -= 0.5
                    playsound("DATA/Musics/SE/other/gun shot.wav")
                    self.active_hitboxes.append(Hitbox(12,-70,60,60,pi/2,12,11,1/100,20,2,self))

            if self.frame > 40: # 17 frames de lag
                self.attack = None

            if self.grounded :
                self.attack = None
                if self.frame < 33 and self.frame > 2 :
                    self.lag = 6 # Auto cancel frame 1-2 et 33+, 6 frames de landing lag

        if attack == "ForwardSmash":
            if self.frame > 6 and self.frame < 9 and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.frame = 7
                self.animeframe -= 1
                self.charge = self.charge+1
            if self.frame == 40 :
                self.charge = min(100,self.charge,self.explosifs*12)
                if self.explosifs > 5:
                    self.explosifs -= max(self.charge/12,3)
                    playsound("DATA/Musics/SE/BOOM !!!/Cannon.wav")
                    self.projectiles.append(Boulet(self.charge,stage,self))
                self.vx = -signe(self.direction)*self.charge*0.5
                self.active_hitboxes.append(Hitbox(-10,0,24,120,5*pi/6,8,3,1/200,8,self.charge/10,self))
            if self.frame > 45: # 30 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "UpSmash":

            if self.frame < 5 :
                if left : # peut reverse netre les frames 1 et 5
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 5 and self.frame < 8  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.animeframe -= 1
                self.frame = 6
                self.charge = self.charge+1

            if self.frame == 11 :
                self.charge = min(self.charge,100)
                if self.explosifs > 7 :
                    self.explosifs -= 7
                    self.active_hitboxes.append(Hitbox(-15,-30,78,48,pi/2,20+8*(self.charge/100),25,1/200,20+8*(self.charge/100),2,self))
                else :
                    self.active_hitboxes.append(Hitbox(4,-30,32,32,pi/2,14+3*(self.charge/100),12,1/200,12+3*(self.charge/100),4,self))

            if self.frame > 40: # 25 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DownSmash":

            if self.frame < 3 :
                if left : # peut reverse netre les frames 1 et 2
                    self.look_right = False
                if right :
                    self.look_right = True
            if self.frame > 3 and self.frame < 6  and smash and self.charge < 200 : # Chargement jusqu'à 200 frames
                self.animeframe -= 1
                self.frame = 4
                self.charge = self.charge+1
            if self.frame == 14 :
                self.charge = min(self.charge,100)
                if self.explosifs > 7 :
                    self.explosifs -= 7
                    playsound("DATA/Musics/SE/other/gun shot.wav")
                    self.vy = -10
                    self.active_hitboxes.append(Hitbox(-32,80,110,42,pi/6,15+9*(self.charge/100),18,1/150,19+9*(self.charge/100),2,self,position_relative=True,boum=3))
                else :
                    self.active_hitboxes.append(Hitbox(-32,80,32,32,5*pi/6,7+3*(self.charge/100),6,1/150,8+3*(self.charge/100),4,self))
                    self.active_hitboxes.append(Hitbox(48,80,32,32,pi/6,7+3*(self.charge/100),6,1/150,8+3*(self.charge/100),4,self))

            if self.frame > 40: # 23 frames de lag
                self.attack = None
                self.charge = 0

        if attack == "DashAttack":
            if self.frame == 2 :
                self.hold = 0
            if self.frame > 10 and self.frame < 14 :
                if attack_button and self.explosifs > 1 :
                    self.explosifs -= 0.1
                    if self.hold%8 == 0:
                        playsound("DATA/Musics/SE/other/gun shot.wav")
                        self.vx += 10*self.dashspeed*signe(self.direction)
                        self.active_hitboxes.append(Hitbox(-10,0,40,100,3*pi/4,12,7,1/200,14,8,self))
                    self.hold += 1
                    self.frame = 11
            if self.frame > 50: # 24 frames de lag
                self.attack = None
        
        if attack == "UpTaunt":
            if (self.konami == [] or self.konami == ["Up"]) and not self.konamiadd:
                print("Up")
                self.konamiadd = True
                self.konami.append("Up")
                self.attack = None
            #elif not self.konamiadd :
            #    self.konami = []
            
            if self.frame > 30: # Durée de 30 frames
                self.attack = None
                self.konamiadd = False

        if attack == "DownTaunt":
            if (self.konami == ["Up","Up"] or self.konami == ["Up","Up","Down"]) and not self.konamiadd:
                self.konamiadd = True
                print("Down")
                self.konami.append("Down")
            #elif not self.konamiadd :
            #    self.konami = []
            
            if self.frame > 30: # Durée de 30 frames
                self.attack = None
                self.konamiadd = False

        if attack == "LeftTaunt":
            if (self.konami == ["Up","Up","Down","Down"] or self.konami == ["Up","Up","Down","Down","Left","Right"]) and not self.konamiadd:
                self.konamiadd = True
                print("Left")
                self.konami.append("Left")
            #elif not self.konamiadd :
            #    self.konami = []
            
            if self.frame > 30: # Durée de 30 frames
                self.attack = None
                self.konamiadd = False

        if attack == "RightTaunt":
            if (self.konami == ["Up","Up","Down","Down","Left"] or self.konami == ["Up","Up","Down","Down","Left","Right","Left"]) and not self.konamiadd:
                self.konamiadd = True
                print("Right")
                self.konami.append("Right")
            #elif not self.konamiadd :
            #    self.konami = []
            
            if self.frame > 30: # Durée de 30 frames
                self.attack = None
                self.konamiadd = False

        if (not (D_Up or D_Down or D_Left or D_Right) and self.attack in ("RightTaunt","LeftTaunt","UpTaunt","DownTaunt")
            or (self.attack == "NeutralB" and attack_button)):
                self.frame = 150

        if attack == "BackSpecial":
            if self.frame > 4 and self.frame < 7 :
                if special :
                    self.frame = 5
                    self.explosifs += 3/60
            if self.frame > 10 :
                self.attack = None

        if attack == "Superspecial":
            if self.frame == 8 :
                if self.explosifs > 49.5 :
                    self.explosifs = 0
                    print("boum")
                    self.konami = []
                    self.konamiadd = False
                    playsound("DATA/Musics/SE/BOOM !!!/Explosion.wav")
                    self.active_hitboxes.append(Hitbox(-140,-100,328,320,pi/4,35,120,1/100,40,10,self,True,sound="other/gun shot.wav"))
                else :
                    self.konami = []
                    self.konamiadd = False
                    self.active_hitboxes.append(Hitbox(-40,-4,128,128,pi/4,2,2,0,2,2,self,True))
            if self.frame > 30: # Durée de 30 frames
                self.attack = None

    def draw(self, window): # Dessine aussi les inputs du konami code et la jauge d'explosifs
            drawing_sprite,size,self.animeframe = get_sprite(self.animation,self.name,self.animeframe,self.look_right)

            drawing_sprite = pygame.transform.scale(drawing_sprite,(round(drawing_sprite.get_size()[0]*4),round(drawing_sprite.get_size()[1]*4))) # Rescale
            size = [size[0]*4,size[1]*4,size[2]*4,size[3]*4] # Rescale
            pos = [self.x + 800 - size[2]/2, self.rect.y-size[3]+self.rect.h + 449] # Position réelle du sprite
            window.blit(drawing_sprite, pos,size) # on dessine le sprite
            #self.rect.y -=  size[3] - self.rect.h # Reste à la surface du stage

            for p in self.projectiles :
                p.draw(window)

            for i,s in enumerate(self.smoke_dash):
                        s.draw(window)
                        if s.life_time < 0:
                            del self.smoke_dash[i]
            
            for i,s in enumerate(self.double_jump):
                        s.draw(window)
                        if s.life_time < 0:
                            del self.double_jump[i]
            if self.player == 0 :
                x = 533
            else :
                x = 1066
            
            for i,key in enumerate(self.konami) :
                window.blit(pygame.image.load(f"./DATA/Images/Sprites/Misc/Konami_Code/{key}.png"),(i*20+x,800))
            pygame.draw.rect(window,(0,0,0),(x,770,100,20))
            pygame.draw.rect(window,(100,100,0),(x,770,self.explosifs*2,20))
            Texte(str(floor(self.explosifs))+"/50",("Arial",12,True,False),(200,200,200),x+50,780).draw(window)
###################          
""" Projectiles """
###################

boulet = pygame.image.load("./DATA/Images/Sprites/Projectiles/Aubin/Boulet.png")

class Boulet():
    def __init__(self,charge,stage,own:Pyro_Aubin) -> None:
        self.x = own.x + 48*signe(own.direction)
        self.y = own.rect.y + 48
        self.charge = charge
        self.vx = (10+charge)*signe(own.direction)*0.2
        self.vy = -5-charge*0.1
        self.damages = 28
        self.stun = 19+8*(self.charge/100)
        self.knockback = sqrt(abs(self.vy)+abs(self.vx))/2
        self.damages_stacking = 1/200
        if not own.look_right :
            self.angle = 3*pi/4
        else :
            self.angle = pi/4
        self.rect = pygame.Rect((0,0,0,0))
        self.stage = stage
        self.duration = 80

    def update(self):
        self.knockback = (abs(self.vy)+abs(self.vx))/2
        self.x += self.vx
        self.y += self.vy
        self.rect = boulet.get_rect(topleft=(self.x,self.y))
        if self.rect.colliderect(self.stage.mainplat.rect) :
            self.vy = -1
            self.vx *= 0.9
        else :
            self.vy += 3
        self.duration -= 1

    def deflect(self,modifier):
        self.vx = -self.vx*modifier
        self.damages = self.damages * modifier
        self.angle = pi-self.angle

    def draw(self,window):
        window.blit(boulet, (self.x+800,self.y+450)) # on dessine le sprite

fusee = pygame.image.load("./DATA/Images/Sprites/Projectiles/Aubin/Fusee.png")

class Fusee():
    def __init__(self,stage,own:Pyro_Aubin,other:Char) -> None:
        self.x = own.x + signe(own.direction)*48
        self.y = own.rect.y + 86
        self.vx = 0.5*signe(own.direction)
        self.vy = -10
        self.damages = 5
        self.stun = 12
        self.knockback = 6
        self.damages_stacking = 1/200
        self.angle = pi/2
        self.rect = pygame.Rect((0,0,0,0))
        self.stage = stage
        self.duration = 9
        self.frame = 1
        self.homing = False
        self.own = own
        self.other = other
        self.done = False
    
    def touch_stage(self,stage,rect):
        if rect.colliderect(stage.mainplat.rect):
            return True
        for p in stage.plats:
            if rect.colliderect(p.rect) and rect.y + rect.h-4 < p.rect.y+self.vy+4:
                return True
        return False
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.frame += 1
        if not self.done :
            if not self.homing :
                self.vy += 0.005*self.frame
            else :
                dx = (self.x - self.other.x)
                dy = (self.y - self.other.rect.y)
                if dx == 0 :
                    dx = 0.001
                angle = atan(dy/dx)
                self.angle = angle
                self.vx = -abs(cos(angle))*5*signe(dx) - 0.005*self.frame*signe(dx)
                self.vy = -abs(sin(angle))*5*signe(dy) - 0.005*self.frame*signe(dy)
                self.duration -= 0.01
        else:
            self.frame += 1
            self.vy += 0.005*self.frame
            self.duration -= 1
        if self.touch_stage(self.stage,self.rect) or abs(self.y) > 1000 or abs(self.x) > 1000:
            self.done = True
            self.vy = 0
        if self.rect.colliderect(self.other.rect):
            self.done = True
            self.frame = 0
            self.homing = False
        if round(self.duration) == 2 :
            self.own.projectiles.append(Explosion(self.x,self.y,9,12,self.angle,14,1/150,48))
    
    def draw(self,window):
        if self.vy == 0 :
            self.vx = 0.000001
        if self.vx < 0 :
            sprite = pygame.transform.rotate(fusee,degrees(pi-atan(self.vy/self.vx)))
        else :
            sprite = pygame.transform.rotate(fusee,degrees(pi-atan(self.vy/self.vx))+180)
        self.rect = sprite.get_rect(topleft=(self.x,self.y))
        if self.rect.colliderect(self.stage.mainplat.rect):
            sprite = fusee
        window.blit(sprite, (self.x+800,self.y+450)) # on dessine le sprite

    def deflect(self,modifier):
        self.vx = -self.vx*modifier
        self.vy = -self.vy*modifier
        self.damages = self.damages * modifier
        self.angle = pi-self.angle
        self.homing = False
        self.done = True
        self.frame = 0

grenade = pygame.image.load("./DATA/Images/Sprites/Projectiles/Aubin/Grenade.png")

class Grenade():
    def __init__(self,own:Pyro_Aubin,other,speed,stage) -> None:
        self.vx = speed
        self.vy = -15
        self.basevy = self.vy
        self.x = own.x
        self.y = own.rect.y + 48
        self.own = own
        self.other = other
        self.duration = 80
        self.stage = stage
        self.rect = pygame.Rect((0,0,0,0))
        self.rotate = 0
        self.angle = 0
        self.damages = 2
        self.stun = 3
        self.knockback = 2
        self.damages_stacking = 1/200
    
    def touch_stage(self,stage,rect):
        if rect.colliderect(stage.mainplat.rect):
            return True
        for p in stage.plats:
            if rect.colliderect(p.rect) and rect.y + rect.h-4 < p.rect.y+self.vy+4:
                return True
        return False

    def touch_stage(self,stage,rect):
        if rect.colliderect(stage.mainplat.rect):
            return True
        for p in stage.plats:
            if rect.colliderect(p.rect) and rect.y + rect.h < p.rect.y+self.vy+3:
                return True
        return False
    
    def update(self):
        dx = (self.x - self.other.x)
        dy = (self.y - self.other.rect.y)
        if dx == 0 :
            dx = 0.001
        self.angle = atan(dy/dx)
        self.rect = grenade.get_rect(topleft=(self.x,self.y))
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.8
        if self.touch_stage(self.stage,self.rect):
            self.basevy *= 0.8
            self.vy = self.basevy
        self.duration -= 1
        if self.duration == 1 :
            self.own.projectiles.append(Explosion(self.x,self.y,19,16,self.angle,20,1/100,75))
    
    def draw(self,window):
        self.rotate += self.vx
        sprite = pygame.transform.rotate(grenade,degrees(self.rotate))
        window.blit(sprite, (self.x+800,self.y+450)) # on dessine le sprite

class Explosion():
    def __init__(self,x,y,damages,knockback,angle,stun,damages_stacking,size) -> None:
        playsound("DATA/Musics/SE/other/gun shot.wav")
        self.x = x
        self.y = y
        self.damages = damages
        self.knockback = knockback
        self.angle = angle
        self.stun = stun
        self.damages_stacking = damages_stacking
        self.size = size
        self.sprite = pygame.transform.scale(pygame.image.load("./DATA/Images/Sprites/Projectiles/Fire/1.png"),(size,size))
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
        self.duration = 10

    def deflect(self,modifier):
        self.damages = 0
        self.knockback = 0
        self.stun = 0

    def update(self):
        spritenumber = (self.duration-6) if self.duration > 6 else (6-self.duration)
        print(spritenumber)
        self.sprite = pygame.transform.scale(pygame.image.load(f"./DATA/Images/Sprites/Projectiles/Fire/{spritenumber}.png"),(self.size,self.size))
        self.duration -= 1
        self.rect = self.sprite.get_rect(topleft=(self.x,self.y))
        
    def draw(self,window):
        window.blit(self.sprite,(self.x+800,self.y+450))


##### Autres skins
