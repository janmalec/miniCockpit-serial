from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def set_master_volume(volume_level):
    # Get the default audio device
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Calculate the volume level (0.0 to 1.0)
    volume_level = max(0.0, min(1.0, volume_level))  # Ensure volume is within bounds

    # Set the volume
    volume.SetMasterVolumeLevelScalar(volume_level, None)
    print(f"Volume set to {volume_level * 100}%")

# Example usage: Set volume to 50%
set_master_volume(0.1)
