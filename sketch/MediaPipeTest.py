# Source: https://google.github.io/mediapipe/solutions/pose
# File by: Emma Vriezen
# Instructions:
#   Download the imports (easy through PyCharm)
#   Ensure your camera is connected if it is not built in
#   Set Python interpreter on one that works, I used Python 3.8 64.
#   Right mouse click on this file --> Run (in PyCharm)
#   Should work then.
# Close the MediaPipe window by pressing Esc.

import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# For webcam input:
pose = mp_pose.Pose(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)  # Change this number to use another webcam!
while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = pose.process(image)

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    print(results.pose_landmarks)
    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
pose.close()
cap.release()
