# Last update: 2020-12-15
# Imports:
import numpy as np  # For its arrays
from joblib import load  # To load the classifier
import cv2  # For displaying the webcam feed and the pose keypoints
import mediapipe as mp  # Detects the keypoints on a body

# Import the classifier and make a list of the labels:
clf = load('SVM_final.joblib')
labels = ['Disco', 'Hips', 'Box', 'Roof', 'Guitar', 'Clap', 'No pose']

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
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = pose.process(image)

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Predict the pose:
    key_points = []
    for key_point in results.pose_landmarks.landmark:
        key_points.append(key_point.x)
        key_points.append(key_point.y)
        # key_points.append(key_point.visibility)
    key_points = np.array(key_points).reshape(1, -1)
    prediction = clf.predict(key_points)[0]
    print(labels[prediction])

    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
pose.close()
cap.release()
