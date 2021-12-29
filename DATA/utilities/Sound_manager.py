from pygame.mixer import Sound

musicvolume = 1
soundvolume = 0.7

def playsound(sound):
    play = Sound(sound)
    play.set_volume(soundvolume)
    play.play()