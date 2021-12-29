from pygame.mixer import Sound

with open("DATA/utilities/Settings.txt","r") as settings :
    r = settings.read()
    r = r.split("=")
    musicvolume = float(r[1].split("\n")[0])
    soundvolume = float(r[2].split("\n")[0])

def playsound(sound):
    play = Sound(sound)
    play.set_volume(soundvolume)
    play.play()