from ctypes import *
import SoundSystem
import time

dicoEventPath = {}
dicoEvent = {}
eventList = []


def SFX_init():
    SFXArray = SoundSystem.getAllEventFromBank(SoundSystem.BankList[-2])
    for SFX in SFXArray:
        desc_p = c_void_p(SFX)
        eventList.append(SoundSystem.instance(eventDesc=desc_p))

        """
        event = SoundSystem.instance(eventDesc=desc_p)
        keys = event.getPath()

        dicoEventPath[str(keys[11:])] = event  # constructe dicoPath

        # split the path
        truc = str(keys).split("/")
        folder = truc[2]
        song = truc[3]

        # builde de dico
        if folder not in dicoEvent.keys():
            dicoEvent[folder] = {}

        dicoEvent[folder][song] = event

    print(dicoEventPath)
    print(dicoEvent)
    """