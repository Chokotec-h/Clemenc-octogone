from ctypes import *
import DATA.utilities.SoundSystem as SoundSystem
import time

# Dico with all SFX song
SFXDicoEventPath = {}  # key per path
SFXDicoEvent = {}  # key per folder  and   song

UIDicoEvent = {}  # a dico with all UI song


def SFX_init():
    # SFX Loader
    SFXnumber = SoundSystem.getEventCount(SoundSystem.BankList[3])
    SFXArray = (c_void_p * SFXnumber)()
    SoundSystem.getAllEventFromBank(SoundSystem.BankList[3], SFXArray, SFXnumber)
    for SFX in SFXArray:
        desc_p = c_void_p(SFX)

        event = SoundSystem.instance(eventDesc=desc_p)
        keys = event.getPath()

        SFXDicoEventPath[str(keys[11:])] = event  # constructe dicoPath

        # split the path
        truc = str(keys).split("/")
        truc[3] = truc[3][:-1]  # NE PAS CHANGER
        folder = truc[2]  # NE  PAS  CHANGER
        song = truc[3]  # NE PAS CHANGER
        print("Loading SFX:", song)

        # builde de dico
        if folder not in SFXDicoEvent.keys():
            SFXDicoEvent[folder] = {}

        SFXDicoEvent[folder][song] = event

    # UI Loader
    UInumber = SoundSystem.getEventCount(SoundSystem.BankList[4])
    UIArray = (c_void_p * UInumber)()
    SoundSystem.getAllEventFromBank(SoundSystem.BankList[4], UIArray, UInumber)

    for UI in UIArray:
        desc_p = c_void_p(UI)

        event = SoundSystem.instance(eventDesc=desc_p)
        keys = event.getPath()

        SFXDicoEventPath[str(keys[11:])] = event  # constructe dicoPath

        # split the path
        truc = str(keys).split("/")
        truc[2] = truc[2][:-1]  # ne pas changer
        song = truc[2]  # ne pas changer
        print("Loading UI:", song)

        SFXDicoEvent[song] = event

    # Voix Loader
    Voixnumber = SoundSystem.getEventCount(SoundSystem.BankList[6])
    VoixArray = (c_void_p * Voixnumber)()
    SoundSystem.getAllEventFromBank(SoundSystem.BankList[6], VoixArray, Voixnumber)
    SFXDicoEvent["Voix"] = {}
    for Voix in VoixArray:
        desc_p = c_void_p(Voix)

        event = SoundSystem.instance(eventDesc=desc_p)
        keys = event.getPath()

        SFXDicoEventPath[str(keys[11:])] = event  # constructe dicoPath

        # split the path
        truc = str(keys).split("/")
        truc[3] = truc[3][:-1]  # NE PAS CHANGER
        folder = truc[2]  # NE  PAS  CHANGER
        song = truc[3][5:]  # NE PAS CHANGER
        print("Loading Voix:", folder, song)

        # builde de dico
        if folder not in SFXDicoEvent["Voix"].keys():
            SFXDicoEvent["Voix"][folder] = {}

        SFXDicoEvent["Voix"][folder][song] = event
