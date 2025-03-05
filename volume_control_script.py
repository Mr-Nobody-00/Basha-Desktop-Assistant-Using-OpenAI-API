import pycaw.pycaw as pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import sys

def change_volume(action):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    if action == "up":
        volume.SetMasterVolumeLevelScalar(min(volume.GetMasterVolumeLevelScalar() + 0.1, 1.0), None)
    elif action == "down":
        volume.SetMasterVolumeLevelScalar(max(volume.GetMasterVolumeLevelScalar() - 0.1, 0.0), None)
    elif action == "mute":
        volume.SetMute(1, None)
    elif action == "unmute":
        volume.SetMute(0, None)
    
    print(f"Volume {action} executed.")

change_volume(sys.argv[1])  # Pass argument (up/down/mute/unmute)
