from ctypes import *

PLATFORM_SUFFIX = "64" if sizeof(c_void_p) == 8 else ""
VERSION = 0x00020114
BANK_FILES = ["Master.bank", "Master.strings.bank", "BGM.bank"]

BANK_PATH = "DATA/SoundSystem/"

core_dll = WinDLL("FMOD/api/core/lib/x64/fmodL.dll")
studio_dll = WinDLL("FMOD/api/studio/lib/x64/fmodstudioL.dll")
studio_sys = c_void_p()


def check_result(r):
    if r != 0:
        print("ERROR: Got FMOD_RESULT {0}".format(r))


def studio_init():
    print("Initializing FMOD Studio")
    # Write debug log to file
    check_result(core_dll.FMOD_Debug_Initialize(0x00000002, 1, 0, "log.txt".encode('ascii')))
    check_result(studio_dll.FMOD_Studio_System_Create(byref(studio_sys), VERSION))
    # Call System init
    check_result(studio_dll.FMOD_Studio_System_Initialize(studio_sys, 256, 0x00000001, 0, c_void_p()))
    # Load banks
    for bankname in BANK_FILES:
        print("Loading bank: " + bankname)
        bank = c_void_p()
        temp = BANK_PATH + bankname
        check_result(studio_dll.FMOD_Studio_System_LoadBankFile(studio_sys, temp.encode('ascii'), 0, byref(bank)))


def play_sound(soundname):
    print("Playing sound: " + soundname)
    event_desc = c_void_p()
    check_result(studio_dll.FMOD_Studio_System_GetEvent(studio_sys, soundname.encode('ascii'), byref(event_desc)))
    event_inst = c_void_p()
    check_result(studio_dll.FMOD_Studio_EventDescription_CreateInstance(event_desc, byref(event_inst)))
    check_result(studio_dll.FMOD_Studio_EventInstance_Start(event_inst))
    check_result(studio_dll.FMOD_Studio_EventInstance_Release(event_inst))
    return event_inst


def stop_inst(event_inst):
    check_result(studio_dll.FMOD_Studio_EventInstance_Stop(event_inst))


def tick_update():
    check_result(studio_dll.FMOD_Studio_System_Update(studio_sys))


class instance:
    def __init__(self):
        self.instance = None
