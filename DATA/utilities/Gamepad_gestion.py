import pygame

def signe(val):
    if val == 0:
        return 0
    else :
        return val/abs(val)

def get_inputs(joystick):
    get = []
    axes = joystick.get_numaxes() # Récupération des joysticks et des gâchettes
    for j in range(axes):
        axis = joystick.get_axis(j)
        get.append(["Joy",joystick,j,axis])

    buttons = joystick.get_numbuttons() # Récupération des boutons
    for j in range(buttons):
        button = joystick.get_button(j)
        if button :
            get.append(["Button",joystick,j])

    hats = joystick.get_numhats() # Récupération de la/des croix directionnelle(s)
    for i in range(hats):
        hat = joystick.get_hat(i)
        if hat[1] == 1 :
            get.append(["D-Pad",joystick,i,1,1])
        if hat[1] == -1 :
            get.append(["D-Pad",joystick,i,1,-1])
        if hat[0] == 1 :
            get.append(["D-Pad",joystick,i,0,1])
        if hat[0] == -1 :
            get.append(["D-Pad",joystick,i,0,-1])
    return list(get)

def convert_inputs(controls,joystick,number):
    bool_list = list()
    keys = pygame.key.get_pressed()
    for c in controls:
        returning = True
        if not c :
            returning = False
        else :
            for i in c :
                if i[0] == "Keyboard":
                    if not keys[i[1]] :
                        returning = False
                if i[0] == "Joy":
                    if abs(joystick[number].get_axis(i[1])) > 0.6 and signe(joystick[number].get_axis(i[1])) == signe(i[-1]) and returning:
                        returning = abs(joystick[number].get_axis(i[1]))
                    else :
                        returning = False
                if i[0] == "Button":
                    if not joystick[number].get_button(i[1]):
                        returning = False
                if i[0] == "D-Pad":
                    if not joystick[number].get_hat(i[1])[i[2]] == i[-1]:
                        returning = False
        bool_list.append(returning)
    return bool_list