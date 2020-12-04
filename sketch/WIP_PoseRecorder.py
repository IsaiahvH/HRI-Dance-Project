# File by: Emma Vriezen
# See README for comments.

import cv2  # For displaying your webcam stream and the keypoints
import mediapipe as mp  # For keypoint recognition
import pandas as pd  # For its dataframes

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(1)  # Change this number to use another webcam!

key_df = pd.DataFrame()

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
    # print(results.pose_landmarks)  # This is all the landmarks
    print(results.pose_landmarks.landmark[11])
    print(results.pose_landmarks.landmark[11].x)  # This is a specific one

    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imshow('MediaPipe Pose', image)

    if cv2.waitKey(5) & 0xFF == 27:  # When ESC is pressed, stop the loop:
        print("Pressed ESC --> end video capture.")
        break
pose.close()
cap.release()
