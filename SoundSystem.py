from ctypes import *

# initialisation value
PLATFORM_SUFFIX = "64" if sizeof(c_void_p) == 8 else ""
VERSION = 0x00020114
BANK_FILES = ["Master.bank", "Master.strings.bank", "BGM.bank", "SFX.bank", "UI.bank"]

BANK_PATH = "DATA/FMOD/Desktop/"  # the path from game files

# api value
core_dll = WinDLL("DATA/FMOD/api/core/lib/x64/fmodL.dll")
studio_dll = WinDLL("DATA/FMOD/api/studio/lib/x64/fmodstudioL.dll")
studio_sys = c_void_p()

BankList = []  # a list of all bank
string_buffer = create_string_buffer(100)
bufferSize = 50


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
        BankList.append(bank)


def play_event(eventPath: str) -> c_void_p:
    """
    @param eventPath: the path of the event
    @return: an instance of the event
    """
    print("Playing sound: " + eventPath)
    event_desc = c_void_p()
    check_result(studio_dll.FMOD_Studio_System_GetEvent(studio_sys, eventPath.encode('ascii'), byref(event_desc)))

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
    check_result(studio_dll.FMOD_Studio_EventInstance_Start(event_inst))


def tick_update():
    """
    update FMOD states
    """
    check_result(studio_dll.FMOD_Studio_System_Update(studio_sys))


class instance:
    def __init__(self, name: str = None, evenID=None, eventDesc: c_void_p = None):
        """
        init an instance of an event
        @param name: if specified the instance will be load and put in the instance variable
        if None, the user will specify the instance later
        """

        self.event_desc = c_void_p()
        self.instance = c_void_p()

        if name is not None:  # if a name is passed
            check_result(
                studio_dll.FMOD_Studio_System_GetEvent(studio_sys, name.encode('ascii'), byref(self.event_desc)))
            check_result(studio_dll.FMOD_Studio_EventDescription_CreateInstance(self.event_desc, byref(self.instance)))

        elif evenID is not None:  # if an ID is passed
            check_result(
                studio_dll.FMOD_Studio_System_GetEventByID(studio_sys, evenID, byref(self.event_desc)))
            check_result(studio_dll.FMOD_Studio_EventDescription_CreateInstance(self.event_desc, byref(self.instance)))

        elif eventDesc is not None:  # if and event description is passed
            self.event_desc = eventDesc
            check_result(studio_dll.FMOD_Studio_EventDescription_CreateInstance(eventDesc, byref(self.instance)))

    def play(self):
        """
        start Instance
        """
        start_inst(self.instance)

    def changeParameter(self, name, value):
        """
        take a parameter and change its value  (may not work...)
        @param name: the name of the parameter
        @param value: the new value
        """
        check_result(studio_dll.FMOD_Studio_EventInstance_SetParameterByName(self.instance, name.encode("ascii"),
                                                                             value * 1065353216, True))

    def getPath(self):
        tempBuffer = (c_char * bufferSize).from_address(addressof(string_buffer))
        check_result(
            studio_dll.FMOD_Studio_EventDescription_GetPath(self.event_desc, byref(tempBuffer), bufferSize - 1))
        return tempBuffer.value


def getEventCount(bank):
    """
    @param bank: the bank with event
    @return: the number of event
    """
    eventNumber = c_int()
    check_result(studio_dll.FMOD_Studio_Bank_GetEventCount(bank, byref(eventNumber)))
    return eventNumber.value


def getAllEventFromBank(bank, Array, eventNumber):
    """
    @param bank: a bank to get all his event
    @param Array : an Array to stack all event
    @param eventNumber : the number of event
    @return: a cArray with all events
    """
    check_result(studio_dll.FMOD_Studio_Bank_GetEventList(bank, byref(Array), eventNumber))
