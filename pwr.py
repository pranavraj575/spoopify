import ctypes
from ctypes import wintypes
def __reset():
    class info(ctypes.Structure):
        _fields_ = [
            ('charging', wintypes.BYTE),
            ('BatteryFlag', wintypes.BYTE),
            ('battery', wintypes.BYTE),
            #('Reserved1', wintypes.BYTE),
            ('lifetime', wintypes.DWORD),
            ('fullLife', wintypes.DWORD),
        ]
    global status
    status=info()
    #SYSTEM_POWER_STATUS_P = ctypes.POINTER(battery)
    GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
    #GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
    #GetSystemPowerStatus.restype = wintypes.BOOL
    if not GetSystemPowerStatus(ctypes.pointer(status)):
        raise ctypes.WinError()
def charging():
    __reset()
    return bool(status.charging)
def battry():
    __reset()
    return int(status.battery)
def life():
    __reset()
    return status.lifetime

