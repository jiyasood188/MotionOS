
import os
os.environ["MEDIAPIPE_DISABLE_GPU"] = "1"
import cv2

import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
import config
import urllib.request
import os



MODEL_PATH = "hand_landmarker.task"
if not os.path.exists(MODEL_PATH):
    print("Downloading hand landmark model...")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
        MODEL_PATH
    )
    print("Model downloaded.")

class HandTracker:
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
        base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=config.DETECTION_CONFIDENCE,
            min_tracking_confidence=config.TRACKING_CONFIDENCE,
        )

        self._detector = vision.HandLandmarker.create_from_options(options)

        self._draw = mp.solutions.drawing_utils
        self._draw_styles = mp.solutions.drawing_styles
        self._mp_hands = mp.solutions.hands

    def process(self, frame):
        h, w = frame.shape[:2]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        result = self._detector.detect(mp_image)

        annotated = frame.copy()

        if not result.hand_landmarks:
            return None, None, annotated

        hand = result.hand_landmarks[0]

        landmarks_norm = [(lm.x, lm.y, lm.z) for lm in hand]

        landmarks_px = [(int(lm.x * w), int(lm.y * h)) for lm in hand]

        for connection in self._mp_hands.HAND_CONNECTIONS:
            start = landmarks_px[connection[0]]
            end = landmarks_px[connection[1]]
            cv2.line(annotated, start, end, (0, 200, 0), 2)

        for point in landmarks_px:
            cv2.circle(annotated, point, 4, (0, 255, 0), -1)

        return landmarks_norm, landmarks_px, annotated

    def close(self):
        self._detector.close()
