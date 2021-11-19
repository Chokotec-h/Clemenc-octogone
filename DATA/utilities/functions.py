from DATA.utilities.Gamepad_gestion import *

keyrepeat = [[],[]]
repeat = [[],[]]

def addkeyrepeat(key,p):
    keyrepeat[p].append(key)
    repeat[p].append(10)

def input_but_no_repeat(key,controls,joysticks,player):
    if convert_inputs(controls[player],joysticks,player)[key] and key not in keyrepeat[player]:
        addkeyrepeat(key,player)
        return True
    else :
        return False

def actualize_repeating():
    for p in range(2):
        for k in range(len(keyrepeat[p])):
            try :
                repeat[p][k] = repeat[p][k]-1
                if repeat[p][k] < 0 :
                    keyrepeat[p].pop(k)
                    repeat[p].pop(k)
            except :
                pass


def get_controler_input(events,joysticks):
    controls = []
    for joystick in joysticks:
        inputs = get_inputs(joystick)
        for i in inputs :
            if len(i) > 3 :
                if i[0] == "D-Pad":
                    controls.append(i)
                else :
                    if abs(i[-1]) > 0.3 and abs(i[-1]) != 1:
                        move = list(i[0:3])+[signe(i[-1])]
                        controls.append(move)
            else :
                controls.append(i)
    for e in events:
        # Récupération des inputs claviers
        if e.type == pygame.KEYDOWN:
            controls.append(["Keyboard","",e.key])
    if controls :
        controls[0].pop(1)
        return controls[0]