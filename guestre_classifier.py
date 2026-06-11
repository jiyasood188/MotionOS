import math
from  hand_tracker import handtracker as ht
import config

GESTURE_NONE        = "none"         
GESTURE_POINT       = "point"       
GESTURE_CLICK       = "click"        
GESTURE_VOLUME_UP   = "volume_up"    
GESTURE_VOLUME_DOWN = "volume_down"  
GESTURE_SCROLL_UP   = "scroll_up"    
GESTURE_SCROLL_DOWN = "scroll_down"  
GESTURE_PAUSE       = "pause"        
GESTURE_PLAY        = "play"         
GESTURE_DISABLE     = "disable"


def _dist(a,b):
    return math.hypot(a[0] - b[0], a[1] - b[1])
def _finger_up(lm_norm, tip_idx, pip_idx):
    return lm_norm[tip_idx][1] < lm_norm[pip_idx][1]
def _is_horizontal_hand(lm_norm):
    fingertip_ys = [
        lm_norm[ht.INDEX_TIP][1],    
        lm_norm[ht.MIDDLE_TIP][1], 
        lm_norm[ht.RING_TIP][1],    
        lm_norm[ht.PINKY_TIP][1],   
    ]
    spread = max(fingertip_ys) - min(fingertip_ys)
    return spread < 0.06
  

def classify(lm_norm, lm_px, prev_index_y=None):
    if lm_norm is None:
        return GESTURE_NONE, None
    hand_size = _dist(lm_norm[ht.WRIST], lm_norm[ht.MIDDLE_TIP])
    if hand_size < config.MIN_HAND_SIZE:
        return GESTURE_NONE, None
    index_up  = _finger_up(lm_norm, ht.INDEX_TIP,  ht.INDEX_PIP)
    middle_up = _finger_up(lm_norm, ht.MIDDLE_TIP, ht.MIDDLE_PIP)
    ring_up   = _finger_up(lm_norm, ht.RING_TIP,   ht.RING_PIP)
    pinky_up  = _finger_up(lm_norm, ht.PINKY_TIP,  ht.PINKY_PIP)
    index_tip_norm = lm_norm[ht.INDEX_TIP][:2]
    thumb_y = lm_norm[ht.THUMB_TIP][1]   
    wrist_y = lm_norm[ht.WRIST][1]  

    if not index_up and not middle_up and not ring_up and not pinky_up:
        return GESTURE_PLAY, index_tip_norm
    if not index_up and not middle_up and not ring_up and not pinky_up:
        return GESTURE_PLAY, index_tip_norm
    if thumb_y > wrist_y - 0.05:
            return GESTURE_DISABLE, index_tip_norm
    if index_up and middle_up and ring_up and pinky_up:
        return GESTURE_PAUSE, index_tip_norm
    if index_up and middle_up and ring_up and pinky_up:
        return GESTURE_PAUSE, index_tip_norm
    if not index_up and not middle_up and not ring_up and not pinky_up:
        if thumb_y > wrist_y + 0.08:   # thumb tip is clearly LOWER than wrist = thumbs down
            return GESTURE_VOLUME_DOWN, index_tip_norm
    if _is_horizontal_hand(lm_norm):
        if prev_index_y is not None:
                  
         dy = index_tip_norm[1] - prev_index_y
        if dy < -0.01:    
                return GESTURE_SCROLL_UP, index_tip_norm
        elif dy > 0.01:   
                return GESTURE_SCROLL_DOWN, index_tip_norm
        if index_up and middle_up and ring_up and not pinky_up:
          return GESTURE_CLICK, index_tip_norm 
        if index_up and not middle_up and not ring_up and not pinky_up:
         return GESTURE_POINT, index_tip_norm
        return GESTURE_NONE, index_tip_norm


