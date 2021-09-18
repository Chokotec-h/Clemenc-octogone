import pygame

class Char(pygame.sprite.Sprite): # Personnage de base, possédant les caractéristiques communes à tous les persos
    def __init__(self,speed,airspeed,deceleration,fallspeed,fastfallspeed,jumpheight,doublejumpheight):
        pygame.sprite.Sprite.__init__( self )
        self.direction = 90
        self.vel = [0,0] # velocity
        self.grounded = False
        self.fastfall = False
        self.doublejump = [False]
        self.sprite = []

        self.speed = speed
        self.airspeed = airspeed
        self.deceleration = deceleration
        self.fallspeed = fallspeed
        self.fastfallspeed = fastfallspeed
        self.jumpheight = jumpheight
        self.doublejumpheight = doublejumpheight

        self.collidegroup = pygame.sprite.GroupSingle()
        self.collidegroup.add(self)
        



    def move(self,inputs,stage):
        right,left,up,down = inputs

        if right: # Right Movement
            if self.grounded : # Grounded
                self.direction = 90
                self.vel[0] += self.speed
            else : # Aerial
                self.vel[0] += self.airspeed

        if left:
            if self.grounded :
                self.direction = -90
                self.vel[0] -= self.speed
            else :
                self.vel[0] -= self.airspeed

        if up:
            if self.grounded:
                self.vel[1] = self.jumpheight
            else : # Multiple jumps
                self.fastfall = False
                if not self.doublejump[-1]:
                    self.vel[1] = self.doublejumpheight
                    i = 0
                    while self.doublejump[i]:
                        i += 1
                    self.doublejump[i] = True
        if down and not self.grounded and self.vel[1] < 5:
            if not self.fastfall :
                self.vel[1] = self.vel[1]-self.fastfallspeed*5
            self.fastfall = True

        self.rect = self.rect.move(self.vel[0],-self.vel[1])
        self.vel[0] *= self.deceleration

        # Grounded
        if ( pygame.sprite.spritecollide( stage, self.collidegroup, False, collided=pygame.sprite.collide_mask ) ):
            while self.rect.y + self.rect.h > stage.rect.y + 1:
                self.rect.move_ip(0,-1)
            self.vel[1] = 0
            self.grounded = True
            self.fastfall = False
            for dj in range(len(self.doublejump)):
                self.doublejump[dj] = False
        # Fall
        else :
            self.vel[1] -= self.fastfallspeed if self.fastfall else self.fallspeed
            self.grounded = False


    def draw(self,window,camera,frame):

        ### à supprimer
        if self.direction < 0:
            sprite = pygame.transform.flip(self.sprite[frame],True,False)
        else :
            sprite = self.sprite[frame]
        ####

        pos = [self.rect.x - camera[0]+400,self.rect.y - camera[1]+300]
        window.blit(sprite,pos)

    def collide(self,other):
        if self.rect.colliderect(other.rect):
            if self.rect.x < other.rect.x :
                self.vel[0] = -1
            if self.rect.x > other.rect.x :
                self.vel[0] = 1
            if self.rect.y < (other.rect.y-2*other.rect.h//3):
                self.vel[1] = self.doublejumpheight


##### M Balan

class Balan(Char):
    def __init__(self) -> None:
        super().__init__(speed=1,airspeed=0.7,deceleration=0.8,fallspeed=0.5,fastfallspeed=0.8,jumpheight=15,doublejumpheight=10)
        self.sprite = [pygame.image.load("./Sprites/M_Balan_idle.png")] # dictionnaire ?
        self.image = pygame.image.load("./Sprites/M_Balan_idle.png").convert_alpha()
        self.mask  = pygame.mask.from_surface( self.image )
        self.rect  = self.image.get_rect( center=( 0, 0 ) )

##### Test

class Balan2(Char):
    def __init__(self) -> None:
        super().__init__(speed=0.5,airspeed=0.8,deceleration=0.7,fallspeed=0.8,fastfallspeed=1.5,jumpheight=15,doublejumpheight=8)
        self.sprite = [pygame.image.load("./Sprites/M_Balan2_idle.png")] # dictionnaire ?
        self.image = pygame.image.load("./Sprites/M_Balan_idle.png").convert_alpha()
        self.mask  = pygame.mask.from_surface( self.image )
        self.rect  = self.image.get_rect( center=( 100, 0 ) )
        self.doublejump.append(False)


