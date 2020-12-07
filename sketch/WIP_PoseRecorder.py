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

# Make the label to name negative samples:
_negative_label = "No pose"
_current_pose = [_negative_label]


def pose_logging():
    """Counts down during logging task and does the logging itself."""
    while _k_dic['m'] < 5:
        time.sleep(0.02)

    poses = ["Disco", "Hips", "Box", "Roof", "Kiss", "Guitar", "Clap"]

    for pose in poses:
        for stage in range(5, 11):
            if stage == 5 or stage == 9:
                sleep_time = 3
                if stage == 5:
                    _messages[stage] = "Next pose: " + str(pose)
                else:
                    _current_pose[0] = pose
                    _messages[stage] = "Hold pose: " + str(pose)
            elif stage == 10:
                _current_pose[0] = _negative_label
            else:
                sleep_time = 1
            _k_dic['m'] = stage
            time.sleep(sleep_time)


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose_recogniser = mp_pose.Pose(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)
# TODO: Change back to 0
cap = cv2.VideoCapture(0)  # Change this number to use another webcam!

# Make the column names for the dataframe:
column_names = ["Label"]
for keypoint_nr in range(0, 24):
    str_nr = str(keypoint_nr)
    column_names.append(str_nr+"_x")
    column_names.append(str_nr+"_y")
    column_names.append(str_nr + "_v")

# Make the dataframe to store the keypoints in:
key_df = pd.DataFrame(columns=column_names)

# Specify the text font and colour, displayed over webcam feed:
font = cv2.FONT_HERSHEY_SIMPLEX
text_colour = (0, 0, 0)  # Change if you cannot read the text well!

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
    results = pose_recogniser.process(_image)

    # Draw the pose annotation on the _image.
    _image.flags.writeable = True
    _image = cv2.cvtColor(_image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        _image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Write text on the _image:
    if _k_dic['m'] < 4:
            cv2.putText(_image, _messages.get(_k_dic['m'], "ERROR"),
                        (0, 60), font,
                        1, text_colour,
                        1, cv2.LINE_AA)
    elif _k_dic['m'] >= 4:
        cv2.putText(_image, _messages.get(_k_dic['m'], "ERROR"),
                    (260, 250), font,
                    1, text_colour,
                    1, cv2.LINE_AA)

    # Display the new image:
    cv2.imshow('MediaPipe Pose', _image)

    # Add the keypoints to the dataframe if a pose is active:
    if _current_pose[0] != _negative_label:
        new_row = {"Label": _current_pose[0]}
        for key_i, point in enumerate(results.pose_landmarks.landmark):
            key_i_x = str(key_i) + "_x"
            key_i_y = str(key_i) + "_y"
            key_i_v = str(key_i) + "_v"
            new_row[key_i_x] = point.x
            new_row[key_i_y] = point.y
            new_row[key_i_v] = point.visibility
        key_df = key_df.append(new_row, ignore_index=True)

    # Read the keyboard input:
    k = cv2.waitKey(5)
    _k_dic['k'] = k
    if k & 0xFF == 27 or not logger.is_alive():  # When ESC is pressed, stop the loop:
        print("Pressed ESC --> end video capture.")
        key_df.to_csv("TestResults.txt")
        break
    elif _k_dic['m'] < 5 and k & 0xFF == 32:
        i += 1
        _k_dic['m'] = i

pose_recogniser.close()
cap.release()
