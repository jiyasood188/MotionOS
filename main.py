# main.py
import cv2
import config
from hand_tracker import HandTracker
from guestre_classifier import classify
from action_disptacher import dispatch


def main():
    tracker = HandTracker()
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    prev_index_y = None

    while True:
        success, frame = cap.read()
        if not success:
            print("Camera not found or disconnected.")
            break

        frame = cv2.flip(frame, 1)
        lm_norm, _, annotated = tracker.process(frame)
        gesture, index_tip_norm = classify(lm_norm, prev_index_y)

        if index_tip_norm is not None:
            prev_index_y = index_tip_norm[1]
        else:
            prev_index_y = None

        control_enabled = dispatch(gesture, index_tip_norm)

        margin = (1 - config.FRAME_REDUCTION) / 2
        rect_x1 = int(margin * annotated.shape[1])
        rect_y1 = int(margin * annotated.shape[0])
        rect_x2 = int((1 - margin) * annotated.shape[1])
        rect_y2 = int((1 - margin) * annotated.shape[0])

        cv2.rectangle(annotated, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 255, 0), 2)
        cv2.putText(annotated, f"Gesture: {gesture}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        status_text = "ACTIVE" if control_enabled else "DISABLED"
        status_color = (0, 255, 0) if control_enabled else (0, 0, 255)
        cv2.putText(annotated, status_text, (annotated.shape[1] - 120, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)

        cv2.imshow("MotionOS", annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    tracker.close()  
    cap.release()
    cv2.destroyAllWindows()  


if __name__ == "__main__":
    main()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       