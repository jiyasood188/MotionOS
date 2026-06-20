import math
from hand_tracker import HandTracker as HT
import config

GESTURE_NONE         = "none"
GESTURE_POINT        = "point"
GESTURE_CLICK        = "click"
GESTURE_DOUBLE_CLICK = "double_click"
GESTURE_VOLUME_UP    = "volume_up"
GESTURE_VOLUME_DOWN  = "volume_down"
GESTURE_SCROLL_UP    = "scroll_up"
GESTURE_SCROLL_DOWN  = "scroll_down"
GESTURE_PAUSE        = "pause"
GESTURE_PLAY         = "play"
GESTURE_DISABLE      = "disable"


def _dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _finger_up(lm_norm, tip_idx, pip_idx):
    return lm_norm[tip_idx][1] < lm_norm[pip_idx][1]


def _thumb_out(lm_norm):
    thumb_x = lm_norm[HT.THUMB_TIP][0]
    wrist_x = lm_norm[HT.WRIST][0]
    return abs(thumb_x - wrist_x) > 0.1


def classify(lm_norm, prev_index_y=None):
    if lm_norm is None:
        return GESTURE_NONE, None

    hand_size = _dist(lm_norm[HT.WRIST], lm_norm[HT.MIDDLE_TIP])
    if hand_size < config.MIN_HAND_SIZE:
        return GESTURE_NONE, None

    index_up  = _finger_up(lm_norm, HT.INDEX_TIP,  HT.INDEX_PIP)
    middle_up = _finger_up(lm_norm, HT.MIDDLE_TIP, HT.MIDDLE_PIP)
    ring_up   = _finger_up(lm_norm, HT.RING_TIP,   HT.RING_PIP)
    pinky_up  = _finger_up(lm_norm, HT.PINKY_TIP,  HT.PINKY_PIP)
    thumb_out = _thumb_out(lm_norm)

    index_tip_norm = lm_norm[HT.INDEX_TIP][:2]
    thumb_y = lm_norm[HT.THUMB_TIP][1]
    wrist_y = lm_norm[HT.WRIST][1]

    if not index_up and not middle_up and not ring_up and not pinky_up:
        if thumb_y < wrist_y - 0.05:
            return GESTURE_VOLUME_UP, index_tip_norm

    if not index_up and not middle_up and not ring_up and not pinky_up:
        if thumb_y > wrist_y + 0.05:
            return GESTURE_VOLUME_DOWN, index_tip_norm

    if not index_up and not middle_up and not ring_up and not pinky_up:
        return GESTURE_PLAY, index_tip_norm

    if index_up and middle_up and not ring_up and not pinky_up and thumb_out:
        return GESTURE_SCROLL_UP, index_tip_norm

    if index_up and middle_up and not ring_up and not pinky_up and not thumb_out:
        if thumb_y > wrist_y + 0.02:
            return GESTURE_DISABLE, index_tip_norm

    if index_up and not middle_up and not ring_up and not pinky_up and thumb_out:
        return GESTURE_SCROLL_DOWN, index_tip_norm

    if index_up and not middle_up and not ring_up and not pinky_up and not thumb_out:
        return GESTURE_POINT, index_tip_norm

    if index_up and middle_up and ring_up and pinky_up and thumb_out:
        return GESTURE_PAUSE, index_tip_norm

    if index_up and middle_up and ring_up and pinky_up and not thumb_out:
        return GESTURE_DOUBLE_CLICK, index_tip_norm

    if index_up and middle_up and ring_up and not pinky_up and not thumb_out:
        return GESTURE_CLICK, index_tip_norm

    return GESTURE_NONE, index_tip_norm
