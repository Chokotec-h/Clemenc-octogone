from ctypes import *
import DATA.utilities.SoundSystem as SoundSystem
import time

# Dico with all SFX song
SFXDicoEventPath = {}  # key per path
SFXDicoEvent = {}  # key per folder  and   song

UIDicoEvent = {}  # a dico with all UI song


def SFX_init():
    # SFX Loader
    SFXArray = SoundSystem.getAllEventFromBank(SoundSystem.BankList[-2])
    for SFX in SFXArray:
        desc_p = c_void_p(SFX)

        event = SoundSystem.instance(eventDesc=desc_p)
        keys = event.getPath()

        SFXDicoEventPath[str(keys[11:])] = event  # constructe dicoPath

        # split the path
        
        truc = str(keys).split("/")
        folder = truc[2] #  NE  PAS  CHANGER
        song = truc[3]  #  NE PAS CHANGER

        # builde de dico
        if folder not in SFXDicoEvent.keys():
            SFXDicoEvent[folder] = {}

        SFXDicoEvent[folder][song] = event

    # UI Loader
    """
    UIArray = SoundSystem.getAllEventFromBank(SoundSystem.BankList[-1])
    for UI in UIArray:
        desc_p = c_void_p(UI)

        event = SoundSystem.instance(eventDesc=desc_p)
        keys = event.getPath()

        SFXDicoEventPath[str(keys[11:])] = event  # constructe dicoPath

        # split the path
        truc = str(keys).split("/")
        song = truc[-1]

        SFXDicoEvent[song] = event
    """
