import ctypes
from ctypes import *

PLATFORM_SUFFIX = "64" if sizeof(c_void_p) == 8 else ""
VERSION = 0x00020114
BANK_FILES = ["Master.bank", "Master.strings.bank", "BGM.bank", "SE.bank"]

BANK_PATH = "DATA/FMOD/Desktop/"

core_dll = WinDLL("DATA/FMOD/api/core/lib/x64/fmodL.dll")
studio_dll = WinDLL("DATA/FMOD/api/studio/lib/x64/fmodstudioL.dll")
studio_sys = c_void_p()


def check_result(r):
    if r != 0:
        print("ERROR: Got FMOD_RESULT {0}".format(r))


def studio_init():
    print("Initializing FMOD Studio")
    # Write debug log to file
    check_result(studio_dll.FMOD_Studio_System_Create(byref(studio_sys), VERSION))
    # Call System init
    check_result(studio_dll.FMOD_Studio_System_Initialize(studio_sys, 256, 0x00000001, 0, c_void_p()))
    # Load banks
    for bankname in BANK_FILES:
        print("Loading bank: " + bankname)
        bank = c_void_p()
        temp = BANK_PATH + bankname
        check_result(studio_dll.FMOD_Studio_System_LoadBankFile(studio_sys, temp.encode('ascii'), 0, byref(bank)))


def play_event(soundname: str) -> c_void_p:
    print("Playing sound: " + soundname)
    event_desc = c_void_p()
    check_result(studio_dll.FMOD_Studio_System_GetEvent(studio_sys, soundname.encode('ascii'), byref(event_desc)))
    event_inst = c_void_p()
    check_result(studio_dll.FMOD_Studio_EventDescription_CreateInstance(event_desc, byref(event_inst)))
    check_result(studio_dll.FMOD_Studio_EventInstance_Start(event_inst))
    return event_inst


def init_inst(eventname: str) -> c_void_p:
    # print("Creating: " + eventname)   #a garder pour les logs
    event_desc = c_void_p()
    check_result(studio_dll.FMOD_Studio_System_GetEvent(studio_sys, eventname.encode('ascii'), byref(event_desc)))
    event_inst = c_void_p()
    check_result(studio_dll.FMOD_Studio_EventDescription_CreateInstance(event_desc, byref(event_inst)))
    return event_inst


def stop_inst(event_inst: c_void_p):
    check_result(studio_dll.FMOD_Studio_EventInstance_Stop(event_inst))


def start_inst(event_inst: c_void_p):
    check_result(studio_dll.FMOD_Studio_EventInstance_Start(byref(event_inst)))


def tick_update():
    check_result(studio_dll.FMOD_Studio_System_Update(studio_sys))


class instance:
    def __init__(self, event: str = None):
        """
        init an instance of an event
        @param event: if specifed the instance will be load and put in the instance variable
        if None, the user will specify the instance later
        """

        self.event_desc = c_void_p()
        self.instance = c_void_p()

        if event is not None:
            check_result(
                studio_dll.FMOD_Studio_System_GetEvent(studio_sys, event.encode('ascii'), byref(self.event_desc)))
            check_result(studio_dll.FMOD_Studio_EventDescription_CreateInstance(self.event_desc, byref(self.instance)))

    def play(self):
        start_inst(self.instance)

    def changeParameter(self, name, value):
        """
        take a parameter and change its value  (may not work...)
        @param name: the name of the parameter
        @param value: the new value
        """
        val = c_void_p()
        val1 = c_void_p()
        check_result(
            studio_dll.FMOD_Studio_EventInstance_GetParameterByName(self.instance, name.encode("ascii"), byref(val), byref(val1)))

        print(val.value, val1.value)

        check_result(studio_dll.FMOD_Studio_EventInstance_SetParameterByName(self.instance, name.encode("ascii"), value*1065353216, True))
