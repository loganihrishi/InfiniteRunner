import cv2
from cvzone.HandTrackingModule import HandDetector

class PalmDetector:
    def __init__(self, detectionCon=0.8, maxHands=1):
        self.detector = HandDetector(detectionCon=detectionCon, maxHands=maxHands)

    def is_palm_extended(self, frame):
        # ret, frame = cap.read()
        hands, img = self.detector.findHands(frame)
        if hands:
            lmlist = hands[0]
            fingerUp = self.detector.fingersUp(lmlist)
            return all(fingerUp)
        return False

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    finger_detector = PalmDetector()

    while True:
        ret, frame = cap.read()
        fingers_are_up = finger_detector.is_palm_extended(frame)
        print(fingers_are_up)
        cv2.imshow("Frame", frame)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
