FMOD_OK = 0
FMOD_ERR_BADCOMMAND = 1
FMOD_ERR_CHANNEL_ALLOC = 2
FMOD_ERR_CHANNEL_STOLEN = 3
FMOD_ERR_DMA = 4
FMOD_ERR_DSP_CONNECTION = 5
FMOD_ERR_DSP_DONTPROCESS = 6
FMOD_ERR_DSP_FORMAT = 7
FMOD_ERR_DSP_INUSE = 8
FMOD_ERR_DSP_NOTFOUND = 9
FMOD_ERR_DSP_RESERVED = 10
FMOD_ERR_DSP_SILENCE = 11
FMOD_ERR_DSP_TYPE = 12
FMOD_ERR_FILE_BAD = 13
FMOD_ERR_FILE_COULDNOTSEEK = 14
FMOD_ERR_FILE_DISKEJECTED = 15
FMOD_ERR_FILE_EOF = 16
FMOD_ERR_FILE_ENDOFDATA = 17
FMOD_ERR_FILE_NOTFOUND = 18
FMOD_ERR_FORMAT = 19
FMOD_ERR_HEADER_MISMATCH = 20
FMOD_ERR_HTTP = 21
FMOD_ERR_HTTP_ACCESS = 22
FMOD_ERR_HTTP_PROXY_AUTH = 23
FMOD_ERR_HTTP_SERVER_ERROR = 24
FMOD_ERR_HTTP_TIMEOUT = 25
FMOD_ERR_INITIALIZATION = 26
FMOD_ERR_INITIALIZED = 27
FMOD_ERR_INTERNAL = 28
FMOD_ERR_INVALID_FLOAT = 29
FMOD_ERR_INVALID_HANDLE = 30
FMOD_ERR_INVALID_PARAM = 31
FMOD_ERR_INVALID_POSITION = 32
FMOD_ERR_INVALID_SPEAKER = 33
FMOD_ERR_INVALID_SYNCPOINT = 34
FMOD_ERR_INVALID_THREAD = 35
FMOD_ERR_INVALID_VECTOR = 36
FMOD_ERR_MAXAUDIBLE = 37
FMOD_ERR_MEMORY = 38
FMOD_ERR_MEMORY_CANTPOINT = 39
FMOD_ERR_NEEDS3D = 40
FMOD_ERR_NEEDSHARDWARE = 41
FMOD_ERR_NET_CONNECT = 42
FMOD_ERR_NET_SOCKET_ERROR = 43
FMOD_ERR_NET_URL = 44
FMOD_ERR_NET_WOULD_BLOCK = 45
FMOD_ERR_NOTREADY = 46
FMOD_ERR_OUTPUT_ALLOCATED = 47
FMOD_ERR_OUTPUT_CREATEBUFFER = 48
FMOD_ERR_OUTPUT_DRIVERCALL = 49
FMOD_ERR_OUTPUT_FORMAT = 50
FMOD_ERR_OUTPUT_INIT = 51
FMOD_ERR_OUTPUT_NODRIVERS = 52
FMOD_ERR_PLUGIN = 53
FMOD_ERR_PLUGIN_MISSING = 54
FMOD_ERR_PLUGIN_RESOURCE = 55
FMOD_ERR_PLUGIN_VERSION = 56
FMOD_ERR_RECORD = 57
FMOD_ERR_REVERB_CHANNELGROUP = 58
FMOD_ERR_REVERB_INSTANCE = 59
FMOD_ERR_SUBSOUNDS = 60
FMOD_ERR_SUBSOUND_ALLOCATED = 61
FMOD_ERR_SUBSOUND_CANTMOVE = 62
FMOD_ERR_TAGNOTFOUND = 63
FMOD_ERR_TOOMANYCHANNELS = 64
FMOD_ERR_TRUNCATED = 65
FMOD_ERR_UNIMPLEMENTED = 66
FMOD_ERR_UNINITIALIZED = 67
FMOD_ERR_UNSUPPORTED = 68
FMOD_ERR_VERSION = 69
FMOD_ERR_EVENT_ALREADY_LOADED = 70
FMOD_ERR_EVENT_LIVEUPDATE_BUSY = 71
FMOD_ERR_EVENT_LIVEUPDATE_MISMATCH = 72
FMOD_ERR_EVENT_LIVEUPDATE_TIMEOUT = 73
FMOD_ERR_EVENT_NOTFOUND = 74
FMOD_ERR_STUDIO_UNINITIALIZED = 75
FMOD_ERR_STUDIO_NOT_LOADED = 76
FMOD_ERR_INVALID_STRING = 77
FMOD_ERR_ALREADY_LOCKED = 78
FMOD_ERR_NOT_LOCKED = 79
FMOD_ERR_RECORD_DISCONNECTED = 80
FMOD_ERR_TOOMANYSAMPLES = 81

def get_error_msg(errCode : int) :
    if errCode == FMOD_OK:
        return "No errors."
    elif errCode == FMOD_ERR_BADCOMMAND:
        return "Tried to call a function on a data type that does not allow this type of functionality (ie calling Sound::lock on a streaming sound)."
    elif errCode == FMOD_ERR_CHANNEL_ALLOC:
        return "Error trying to allocate a channel."
    elif errCode == FMOD_ERR_CHANNEL_STOLEN:
        return "The specelified channel has been reused to play another sound."
    elif errCode == FMOD_ERR_DMA:
        return "DMA Failure.  See debug output for more information."
    elif errCode == FMOD_ERR_DSP_CONNECTION:
        return "DSP connection error.  Connection possibly caused a cyclic dependency or connected dsps with incompatible buffer counts."
    elif errCode == FMOD_ERR_DSP_DONTPROCESS:
        return "DSP return code from a DSP process query callback.  Tells mixer not to call the process callback and therefore not consume CPU.  Use this to optimize the DSP graph."
    elif errCode == FMOD_ERR_DSP_FORMAT:
        return "DSP Format error.  A DSP unit may have attempted to connect to this network with the wrong format, or a matrix may have been set with the wrong size elif the target unit has a specelified channel map."
    elif errCode == FMOD_ERR_DSP_INUSE:
        return "DSP is already in the mixer's DSP network. It must be removed before being reinserted or released."
    elif errCode == FMOD_ERR_DSP_NOTFOUND:
        return "DSP connection error.  Couldn't find the DSP unit specelified."
    elif errCode == FMOD_ERR_DSP_RESERVED:
        return "DSP operation error.  Cannot perform operation on this DSP as it is reserved by the system."
    elif errCode == FMOD_ERR_DSP_SILENCE:
        return "DSP return code from a DSP process query callback.  Tells mixer silence would be produced from read, so go idle and not consume CPU.  Use this to optimize the DSP graph."
    elif errCode == FMOD_ERR_DSP_TYPE:
        return "DSP operation cannot be performed on a DSP of this type."
    elif errCode == FMOD_ERR_FILE_BAD:
        return "Error loading file."
    elif errCode == FMOD_ERR_FILE_COULDNOTSEEK:
        return "Couldn't perform seek operation.  This is a limitation of the medium (ie netstreams) or the file format."
    elif errCode == FMOD_ERR_FILE_DISKEJECTED:
        return "Media was ejected while reading."
    elif errCode == FMOD_ERR_FILE_EOF:
        return "End of file unexpectedly reached while trying to read essential data (truncated?)."
    elif errCode == FMOD_ERR_FILE_ENDOFDATA:
        return "End of current chunk reached while trying to read data."
    elif errCode == FMOD_ERR_FILE_NOTFOUND:
        return "File not found."
    elif errCode == FMOD_ERR_FORMAT:
        return "Unsupported file or audio format."
    elif errCode == FMOD_ERR_HEADER_MISMATCH:
        return "There is a version mismatch between the FMOD header and either the FMOD Studio library or the FMOD Low Level library."
    elif errCode == FMOD_ERR_HTTP:
        return "A HTTP error occurred. This is a catch-all for HTTP errors not listed elsewhere."
    elif errCode == FMOD_ERR_HTTP_ACCESS:
        return "The specelified resource requires authentication or is forbidden."
    elif errCode == FMOD_ERR_HTTP_PROXY_AUTH:
        return "Proxy authentication is required to access the specelified resource."
    elif errCode == FMOD_ERR_HTTP_SERVER_ERROR:
        return "A HTTP server error occurred."
    elif errCode == FMOD_ERR_HTTP_TIMEOUT:
        return "The HTTP request timed out."
    elif errCode == FMOD_ERR_INITIALIZATION:
        return "FMOD was not initialized correctly to support this function."
    elif errCode == FMOD_ERR_INITIALIZED:
        return "Cannot call this command after System::init."
    elif errCode == FMOD_ERR_INTERNAL:
        return "An error occurred that wasn't supposed to.  Contact support."
    elif errCode == FMOD_ERR_INVALID_FLOAT:
        return "Value passed in was a NaN, Inf or denormalized float."
    elif errCode == FMOD_ERR_INVALID_HANDLE:
        return "An invalid object handle was used."
    elif errCode == FMOD_ERR_INVALID_PARAM:
        return "An invalid parameter was passed to this function."
    elif errCode == FMOD_ERR_INVALID_POSITION:
        return "An invalid seek position was passed to this function."
    elif errCode == FMOD_ERR_INVALID_SPEAKER:
        return "An invalid speaker was passed to this function based on the current speaker mode."
    elif errCode == FMOD_ERR_INVALID_SYNCPOINT:
        return "The syncpoint did not come from this sound handle."
    elif errCode == FMOD_ERR_INVALID_THREAD:
        return "Tried to call a function on a thread that is not supported."
    elif errCode == FMOD_ERR_INVALID_VECTOR:
        return "The vectors passed in are not unit length, or perpendicular."
    elif errCode == FMOD_ERR_MAXAUDIBLE:
        return "Reached maximum audible playback count for this sound's soundgroup."
    elif errCode == FMOD_ERR_MEMORY:
        return "Not enough memory or resources."
    elif errCode == FMOD_ERR_MEMORY_CANTPOINT:
        return "Can't use FMOD_OPENMEMORY_POINT on non PCM source data, or non mp3/xma/adpcm data elif FMOD_CREATECOMPRESSEDSAMPLE was used."
    elif errCode == FMOD_ERR_NEEDS3D:
        return "Tried to call a command on a 2d sound when the command was meant for 3d sound."
    elif errCode == FMOD_ERR_NEEDSHARDWARE:
        return "Tried to use a feature that requires hardware support."
    elif errCode == FMOD_ERR_NET_CONNECT:
        return "Couldn't connect to the specelified host."
    elif errCode == FMOD_ERR_NET_SOCKET_ERROR:
        return "A socket error occurred.  This is a catch-all for socket-related errors not listed elsewhere."
    elif errCode == FMOD_ERR_NET_URL:
        return "The specelified URL couldn't be resolved."
    elif errCode == FMOD_ERR_NET_WOULD_BLOCK:
        return "Operation on a non-blocking socket could not complete immediately."
    elif errCode == FMOD_ERR_NOTREADY:
        return "Operation could not be performed because specelified sound/DSP connection is not ready."
    elif errCode == FMOD_ERR_OUTPUT_ALLOCATED:
        return "Error initializing output device, but more specelifically, the output device is already in use and cannot be reused."
    elif errCode == FMOD_ERR_OUTPUT_CREATEBUFFER:
        return "Error creating hardware sound buffer."
    elif errCode == FMOD_ERR_OUTPUT_DRIVERCALL:
        return "A call to a standard soundcard driver failed, which could possibly mean a bug in the driver or resources were missing or exhausted."
    elif errCode == FMOD_ERR_OUTPUT_FORMAT:
        return "Soundcard does not support the specelified format."
    elif errCode == FMOD_ERR_OUTPUT_INIT:
        return "Error initializing output device."
    elif errCode == FMOD_ERR_OUTPUT_NODRIVERS:
        return "The output device has no drivers installed.  elif pre-init, FMOD_OUTPUT_NOSOUND is selected as the output mode.  elif post-init, the function just fails."
    elif errCode == FMOD_ERR_PLUGIN:
        return "An unspecelified error has been returned from a plugin."
    elif errCode == FMOD_ERR_PLUGIN_MISSING:
        return "A requested output, dsp unit type or codec was not available."
    elif errCode == FMOD_ERR_PLUGIN_RESOURCE:
        return "A resource that the plugin requires cannot be allocated or found. (ie the DLS file for MIDI playback)"
    elif errCode == FMOD_ERR_PLUGIN_VERSION:
        return "A plugin was built with an unsupported SDK version."
    elif errCode == FMOD_ERR_RECORD:
        return "An error occurred trying to initialize the recording device."
    elif errCode == FMOD_ERR_REVERB_CHANNELGROUP:
        return "Reverb properties cannot be set on this channel because a parent channelgroup owns the reverb connection."
    elif errCode == FMOD_ERR_REVERB_INSTANCE:
        return "Specelified instance in FMOD_REVERB_PROPERTIES couldn't be set. Most likely because it is an invalid instance number or the reverb doesn't exist."
    elif errCode == FMOD_ERR_SUBSOUNDS:
        return "The error occurred because the sound referenced contains subsounds when it shouldn't have, or it doesn't contain subsounds when it should have.  The operation may also not be able to be performed on a parent sound."
    elif errCode == FMOD_ERR_SUBSOUND_ALLOCATED:
        return "This subsound is already being used by another sound, you cannot have more than one parent to a sound.  Null out the other parent's entry first."
    elif errCode == FMOD_ERR_SUBSOUND_CANTMOVE:
        return "Shared subsounds cannot be replaced or moved from their parent stream, such as when the parent stream is an FSB file."
    elif errCode == FMOD_ERR_TAGNOTFOUND:
        return "The specelified tag could not be found or there are no tags."
    elif errCode == FMOD_ERR_TOOMANYCHANNELS:
        return "The sound created exceeds the allowable input channel count.  This can be increased using the 'maxinputchannels' parameter in System::setSoftwareFormat."
    elif errCode == FMOD_ERR_TRUNCATED:
        return "The retrieved string is too long to fit in the supplied buffer and has been truncated."
    elif errCode == FMOD_ERR_UNIMPLEMENTED:
        return "Something in FMOD hasn't been implemented when it should be! contact support!"
    elif errCode == FMOD_ERR_UNINITIALIZED:
        return "This command failed because System::init or System::setDriver was not called."
    elif errCode == FMOD_ERR_UNSUPPORTED:
        return "A command issued was not supported by this object.  Possibly a plugin without certain callbacks specelified."
    elif errCode == FMOD_ERR_VERSION:
        return "The version number of this file format is not supported."
    elif errCode == FMOD_ERR_EVENT_ALREADY_LOADED:
        return "The specelified bank has already been loaded."
    elif errCode == FMOD_ERR_EVENT_LIVEUPDATE_BUSY:
        return "The live update connection failed due to the game already being connected."
    elif errCode == FMOD_ERR_EVENT_LIVEUPDATE_MISMATCH:
        return "The live update connection failed due to the game data being out of sync with the tool."
    elif errCode == FMOD_ERR_EVENT_LIVEUPDATE_TIMEOUT:
        return "The live update connection timed out."
    elif errCode == FMOD_ERR_EVENT_NOTFOUND:
        return "The requested event, parameter, bus or vca could not be found."
    elif errCode == FMOD_ERR_STUDIO_UNINITIALIZED:
        return "The Studio::System object is not yet initialized."
    elif errCode == FMOD_ERR_STUDIO_NOT_LOADED:
        return "The specelified resource is not loaded, so it can't be unloaded."
    elif errCode == FMOD_ERR_INVALID_STRING:
        return "An invalid string was passed to this function."
    elif errCode == FMOD_ERR_ALREADY_LOCKED:
        return "The specelified resource is already locked."
    elif errCode == FMOD_ERR_NOT_LOCKED:
        return "The specelified resource is not locked, so it can't be unlocked."
    elif errCode == FMOD_ERR_RECORD_DISCONNECTED:
        return "The specelified recording driver has been disconnected."
    elif errCode == FMOD_ERR_TOOMANYSAMPLES:
        return "The length provided exceeds the allowable limit."
    else :
        return "Unknown error."