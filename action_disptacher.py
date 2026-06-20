import time
import pyautogui
import comtypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
import config
from gesture_classifier import (
    GESTURE_NONE,
    GESTURE_POINT,
    GESTURE_CLICK,
    GESTURE_DOUBLE_CLICK,
    GESTURE_VOLUME_UP,
    GESTURE_VOLUME_DOWN,
    GESTURE_SCROLL_UP,
    GESTURE_SCROLL_DOWN,
    GESTURE_PAUSE,
    GESTURE_PLAY,
    GESTURE_DISABLE,
)

comtypes.CoInitialize()
_speakers = AudioUtilities.GetSpeakers()
_interface = _speakers.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
_volume = cast(_interface, POINTER(IAudioEndpointVolume))

_screen_w, _screen_h = pyautogui.size()
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

_last_click_time = 0
_last_scroll_time = 0
_last_volume_time = 0
_last_media_time = 0
_disable_counter = 0
_control_enabled = True
_smooth_x = 0
_smooth_y = 0


def dispatch(gesture, index_tip_norm):
    global _last_click_time, _last_scroll_time, _last_volume_time, _last_media_time, _disable_counter, _control_enabled, _smooth_x, _smooth_y

    if gesture == GESTURE_DISABLE:
        _disable_counter += 1
        if _disable_counter >= config.DISABLE_FRAMES:
            _control_enabled = False
            _disable_counter = 0
        return _control_enabled

    if gesture != GESTURE_DISABLE:
        _disable_counter = 0

    if not _control_enabled:
        return _control_enabled

    if gesture == GESTURE_POINT and index_tip_norm is not None:
        margin = (1 - config.FRAME_REDUCTION) / 2
        raw_x = (index_tip_norm[0] - margin) / config.FRAME_REDUCTION * _screen_w
        raw_y = (index_tip_norm[1] - margin) / config.FRAME_REDUCTION * _screen_h
        _smooth_x = _smooth_x + (raw_x - _smooth_x) / config.SMOOTHING
        _smooth_y = _smooth_y + (raw_y - _smooth_y) / config.SMOOTHING
        pyautogui.moveTo(int(_smooth_x), int(_smooth_y), duration=0)

    elif gesture == GESTURE_CLICK:
        current_time = time.time()
        if current_time - _last_click_time > config.CLICK_COOLDOWN:
            pyautogui.click()
            _last_click_time = current_time

    elif gesture == GESTURE_DOUBLE_CLICK:
        current_time = time.time()
        if current_time - _last_click_time > config.CLICK_COOLDOWN:
            pyautogui.doubleClick()
            _last_click_time = current_time

    elif gesture == GESTURE_VOLUME_UP:
        current_time = time.time()
        if current_time - _last_volume_time > 0.3:
            current_vol = _volume.GetMasterVolumeLevelScalar()
            new_vol = min(current_vol + 0.02, 1.0)
            _volume.SetMasterVolumeLevelScalar(new_vol, None)
            _last_volume_time = current_time

    elif gesture == GESTURE_VOLUME_DOWN:
        current_time = time.time()
        if current_time - _last_volume_time > 0.3:
            current_vol = _volume.GetMasterVolumeLevelScalar()
            new_vol = max(current_vol - 0.02, 0.0)
            _volume.SetMasterVolumeLevelScalar(new_vol, None)
            _last_volume_time = current_time

    elif gesture == GESTURE_SCROLL_UP:
        current_time = time.time()
        if current_time - _last_scroll_time > config.SCROLL_COOLDOWN:
            pyautogui.press('pageup')
            _last_scroll_time = current_time

    elif gesture == GESTURE_SCROLL_DOWN:
        current_time = time.time()
        if current_time - _last_scroll_time > config.SCROLL_COOLDOWN:
            pyautogui.press('pagedown')
            _last_scroll_time = current_time

    elif gesture == GESTURE_PAUSE:
        current_time = time.time()
        if current_time - _last_media_time > 1.0:
            pyautogui.press('playpause')
            _last_media_time = current_time

    elif gesture == GESTURE_PLAY:
        current_time = time.time()
        if current_time - _last_media_time > 1.0:
            pyautogui.press('playpause')
            _last_media_time = current_time

    return _control_enabled


def enable_control():
    global _control_enabled
    _control_enabled = True
