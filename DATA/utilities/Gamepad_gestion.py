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
        get.append(("Joy",joystick,j,axis))

    buttons = joystick.get_numbuttons() # Récupération des boutons
    for j in range(buttons):
        button = joystick.get_button(j)
        if button :
            get.append(("Button",joystick,j))

    hats = joystick.get_numhats() # Récupération de la/des croix directionnelle(s)
    for i in range(hats):
        hat = joystick.get_hat(i)
        if hat[1] == 1 :
            get.append(("D-Pad",joystick,i,1,1))
        if hat[1] == -1 :
            get.append(("D-Pad",joystick,i,1,-1))
        if hat[0] == 1 :
            get.append(("D-Pad",joystick,i,0,1))
        if hat[0] == -1 :
            get.append(("D-Pad",joystick,i,0,-1))
    return list(get)

def convert_inputs(controls,joystick,number):
    bool_list = list()
    keys = pygame.key.get_pressed()
    for i in range(len(controls)):
        if controls[i][0] != "Keyboard":
            controls[i].insert(1,joystick[number])
    for c in controls:
        if c[0] == "Keyboard":
            bool_list.append(keys[c[1]])
        if c[0] == "Joy":
            if abs(c[1].get_axis(c[2])) > 0.6 and signe(c[1].get_axis(c[2])) == signe(c[-1]):
                bool_list.append(abs(c[1].get_axis(c[2])))
            else :
                bool_list.append(False)
        if c[0] == "Button":
            bool_list.append(c[1].get_button(c[2]))
        if c[0] == "D-Pad":
            if c[1].get_hat(c[2])[c[3]] == c[-1]:
                bool_list.append(True)
            else :
                bool_list.append(False)
    return bool_list