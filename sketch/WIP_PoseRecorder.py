# File by: Emma Vriezen
# See README for comments.

import cv2  # For displaying your webcam stream and the keypoints
import mediapipe as mp  # For keypoint recognition
import pandas as pd  # For its dataframes
import threading  # For making threads
import time  # For timer and sleep

# These are the messages to guide the user through the keypoint logging:
_messages = {
    0: "POSE KEYPOINT LOGGER [press space]",
    1: "Instructions in README [space...]",
    2: "To exit, press ESC [space...]",
    3: "To start, press the spacebar.",
    4: "Sit ready... [space...]",
    5: "Next pose:",
    6: "3",
    7: "2",
    8: "1",
    9: "Hold pose: ",
    10: "End pose"
}


def pose_logging():
    """Counts down during logging task and does the logging itself."""
    while _k_dic['m'] < 5:
        time.sleep(0.02)
    stage = _k_dic['m']

    poses = ["Disco", "Hips", "Box"]

    for pose in poses:
        for stage in range(5, 11):
            if stage == 5 or stage == 9:
                sleep_time = 3
                _messages[stage] = "Next pose: " + str(pose)
            else:
                sleep_time = 1
            _k_dic['m'] = stage
            time.sleep(sleep_time)


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(1)  # Change this number to use another webcam!

_key_df = pd.DataFrame()
font = cv2.FONT_HERSHEY_SIMPLEX
# Store the pressed keys for access by other thread:
_k_dic = {'k': 0, 'm': 0}
logger = threading.Thread(target=pose_logging, daemon=True)
logger.start()
i = 0

while cap.isOpened():
    success, _image = cap.read()
    if not success:
        break

    # Flip the _image horizontally for a later selfie-view display, and convert
    # the BGR _image to RGB.
    _image = cv2.cvtColor(cv2.flip(_image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the _image as not writeable to
    # pass by reference.
    _image.flags.writeable = False
    results = pose.process(_image)

    # Draw the pose annotation on the _image.
    _image.flags.writeable = True
    _image = cv2.cvtColor(_image, cv2.COLOR_RGB2BGR)
    # print(results.pose_landmarks)  # This is all the landmarks
    # print(results.pose_landmarks.landmark[11])
    # print(results.pose_landmarks.landmark[11].x)  # This is a specific one
    mp_drawing.draw_landmarks(
        _image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Write text on the _image:
    if _k_dic['m'] < 4:
            cv2.putText(_image, _messages.get(_k_dic['m'], "ERROR"),
                        (0, 60), font,
                        1, (0, 102, 255),
                        1, cv2.LINE_AA)
    elif _k_dic['m'] >= 4:
        cv2.putText(_image, _messages.get(_k_dic['m'], "ERROR"),
                    (260, 250), font,
                    1, (0, 102, 255),
                    1, cv2.LINE_AA)

    # Display the new image:
    cv2.imshow('MediaPipe Pose', _image)

    # Read the keyboard input:
    k = cv2.waitKey(5)
    _k_dic['k'] = k
    if k & 0xFF == 27:  # When ESC is pressed, stop the loop:
        print("Pressed ESC --> end video capture.")
        break
    elif _k_dic['m'] < 5 and k & 0xFF == 32:
        i += 1
        _k_dic['m'] = i
pose.close()
cap.release()
