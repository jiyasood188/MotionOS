import time
import pyautogui 
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER 
import config  
from guestre_classifier import (     
    GESTURE_NONE,
    GESTURE_POINT,
    GESTURE_CLICK,
    GESTURE_VOLUME_UP,
    GESTURE_VOLUME_DOWN,
    GESTURE_SCROLL_UP,
    GESTURE_SCROLL_DOWN,
    GESTURE_PAUSE,
    GESTURE_PLAY,
    GESTURE_DISABLE,
)
_speakers = AudioUtilities.GetSpeakers()
_interface = _speakers.Activate(IAudioEndpointVolume._iid_, 1, None)
_volume = cast(_interface, POINTER(IAudioEndpointVolume))
_vol_min,_vol_max=_volume.get_volumerange()
_screen_w,_screen_h=pyautogui.size()
pyautogui.FAILSAFE = True #emergency stop
pyautogui.PAUSE = 0
_last_click_time = 0    
_control_enabled = True    
_smooth_x = 0              
_smooth_y = 0 
def dispatch(guestre, index_tip_norm,frame_w,frame_h):
    global _last_click_time,_control_enabled,_smooth_x,_smooth_y
    if guestre==GESTURE_DISABLE:
        _control_enabled=False
        return _control_enabled


    if not _control_enabled:   
        return _control_enabled
    if guestre==GESTURE_POINT and index_tip_norm is not None:
        margin = (1 - config.FRAME_REDUCTION) / 2
        raw_x = (index_tip_norm[0] - margin) / config.FRAME_REDUCTION * _screen_w
        raw_y = (index_tip_norm[1] - margin) / config.FRAME_REDUCTION * _screen_h
        _smooth_x = _smooth_x + (raw_x - _smooth_x) / config.SMOOTHING
        _smooth_y = _smooth_y + (raw_y - _smooth_y) / config.SMOOTHING
        pyautogui.moveTo(int(_smooth_x), int(_smooth_y), duration=0)
    elif guestre==GESTURE_CLICK:
        current_time=time.time()
        if current_time- _last_click_time>config.CLICK_COOLDOWN:
            pyautogui.click() 
            _last_click_time=current_time
    elif guestre == GESTURE_VOLUME_UP:
        current_volume=_volume.GetMasterVolumeLevel()
        new_vol = current_volume - (config.VOLUME_STEP / 100) * (_vol_max - _vol_min)
        new_vol = max(new_vol, _vol_min)
        _volume.SetMasterVolumeLevel(new_vol, None)
    elif guestre == GESTURE_VOLUME_DOWN:
        current_volume=_volume.GetMasterVolumeLevel()
        new_vol=current_volume +(config.VOLUME_STEP/100)*(_vol_max-_vol_min)
        new_vol = min(new_vol, _vol_max)
        _volume.SetMasterVolumeLevel(new_vol, None)
    elif guestre==GESTURE_SCROLL_UP:
        pyautogui.press('pageup')
    elif guestre==GESTURE_SCROLL_DOWN:
        pyautogui.press('pagedown')

    elif guestre==GESTURE_PAUSE:
        pyautogui.press('space')
    elif guestre==GESTURE_PLAY:
        pyautogui.press('space')
    return _control_enabled

def enable_control():
    
    global _control_enabled
    _control_enabled = True




    
       

