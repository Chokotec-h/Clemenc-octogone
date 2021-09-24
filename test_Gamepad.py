import pygame


# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

buttonpos = [((140,44,14,14),"circle"),((152,33,14,14),"circle"),((128,33,14,14),"circle"),((140,20,14,14),"circle"),((37,3,38,16),"rect"),((125,3,38,16),"rect"),((83,34,8,8),"circle"),((109,34,8,8),"circle"),((52,35,4,4),"circle"),((122,63,4,4),"circle")]
joypos = [buttonpos[8][0],buttonpos[9][0]]
buttonposswitch = [((128,33,14,14),"circle"),((140,44,14,14),"circle"),((152,33,14,14),"circle"),((140,20,14,14),"circle"),((37,10,38,9),"rect"),((125,10,38,9),"rect"),((37,0,38,9),"rect"),((125,0,38,9),"rect"),((83,34,8,8),"circle"),((109,34,8,8),"circle"),((52,35,4,4),"circle"),((122,63,4,4),"circle"),((102,44,8,8),"circle"),((90,44,8,8),"rect")]


pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((1000, 141))

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

gamepad = pygame.image.load("C:/Users/Nicolas/Pictures/Things/Gamepad.jpg")

def getaxis(x,y,njoystick) :


    buttpos = []
    xy=[x,y]
    for k in range (len(joypos[njoystick])) :
        val = joypos[njoystick][k]
        if k < 2 :
            val = val + pos[k] + xy[k]*11
        buttpos.append(val)

    pygame.draw.ellipse(screen,(255,0,0),buttpos)

# -------- Main Program Loop -----------
while not done:
    #
    # EVENT PROCESSING STEP
    #
    # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
    for event in pygame.event.get(): # User did something.
        if event.type == pygame.QUIT: # If user clicked close.
            done = True # Flag that we are done so we exit this loop.
        elif event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    #
    # DRAWING STEP
    #
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)


    # Get count of joysticks.
    joystick_count = pygame.joystick.get_count()



    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        pos = (i*250,0)
        screen.blit(gamepad,pos)


        # Get the name from the OS for the controller/joystick.
        name = joystick.get_name()

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()

        for j in range(axes):
            axis = joystick.get_axis(j)



        buttons = joystick.get_numbuttons()

        #if buttons == 10 :
        buttpos = getaxis(joystick.get_axis(0),joystick.get_axis(1),0)
        buttpos = getaxis(joystick.get_axis(4),joystick.get_axis(3),1)

        if joystick.get_axis(2) < -0.001 :
                    pygame.draw.rect(screen,(0,250,0),(125,0,38,joystick.get_axis(2)*-5))
        if joystick.get_axis(2) > 0.001 :
                    pygame.draw.rect(screen,(0,250,0),(37,0,38,joystick.get_axis(2)*5))

        for j in range(buttons):
            button = joystick.get_button(j)
            if button :
#                    print(j)
                buttpos = []
                for k in range(len(buttonpos[j][0])):
                    val = buttonpos[j][0][k]
                    if k < 2 :
                        val = val + pos[k]
                    buttpos.append(val)

                if buttonpos[j][1] == "circle" :
                    pygame.draw.ellipse(screen,(0,0,0),buttpos)

                if buttonpos[j][1] == "rect" :
                    pygame.draw.rect(screen,(0,0,0),buttpos)

#         elif buttons == 14 :
#             buttpos = getaxis(joystick.get_axis(0),joystick.get_axis(1),0)
#             buttpos = getaxis(joystick.get_axis(2),joystick.get_axis(3),1)

#             for j in range(buttons):
#                 button = joystick.get_button(j)
#                 if button :
# #                    print(j)
#                     buttpos = []
#                     for k in range(len(buttonposswitch[j][0])):
#                         val = buttonposswitch[j][0][k]
#                         if k < 2 :
#                             val = val + pos[k]
#                         buttpos.append(val)

#                     if buttonposswitch[j][1] == "circle" :
#                         pygame.draw.ellipse(screen,(0,0,0),buttpos)

#                     if buttonposswitch[j][1] == "rect" :
#                         pygame.draw.rect(screen,(0,0,0),buttpos)


        hats = joystick.get_numhats()

        # Hat position. All or nothing for direction, not a float like
        # get_axis(). Position is a tuple of int values (x, y).
        for i in range(hats):
            hat = joystick.get_hat(i)
            if hat[1] == 1 :
                pygame.draw.rect(screen,(0,0,255),(71+pos[0],53,9,11))
            if hat[1] == -1 :
                pygame.draw.rect(screen,(0,0,255),(71+pos[0],72,9,11))
            if hat[0] == 1 :
                pygame.draw.rect(screen,(0,0,255),(80+pos[0],62,9,11))
            if hat[0] == -1 :
                pygame.draw.rect(screen,(0,0,255),(62+pos[0],63,9,11))



    #
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    #

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second.
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()