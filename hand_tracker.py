import cv2
import mediapipe as mp
import config


class hand_tracker:
    WRIST      = 0
    THUMB_TIP  = 4
    INDEX_TIP  = 8
    INDEX_PIP  = 6
    MIDDLE_TIP = 12
    MIDDLE_PIP = 10
    RING_TIP   = 16
    RING_PIP   = 14
    PINKY_TIP  = 20
    PINKY_PIP  = 18

    def __init__(self):
        self._mp_hands=mp.solutions.hands
        self._hands=self._mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=config.detection_confidence,
            min_tracking_confidence=config.tracking_confidence
        )
        self._draw = mp.solutions.drawing_utils
        self._draw_styles = mp.solutions.drawing_styles

    def processing(self, frame):
        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        results = self._hands.process(rgb)
        rgb.flags.writeable = True
        annotated = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        if not results.multi_hand_landmarks:
            return None, None, annotated
        hand = results.multi_hand_landmarks[0]


        self._draw.draw_landmarks(
            annotated,
            hand,
            self._mp_hands.HAND_CONNECTIONS,
            self._draw_styles.get_default_hand_landmarks_style(),
            self._draw_styles.get_default_hand_connections_style()
        )
        landmarks_norm = [(lm.x, lm.y, lm.z) for lm in hand.landmark]
        landmarks_px = [(int(lm.x * w), int(lm.y * h)) for lm in hand.landmark]
        return landmarks_norm, landmarks_px, annotated

    def close(self):
        self._hands.close()

