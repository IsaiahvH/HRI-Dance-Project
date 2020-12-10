"""By Emma Vriezen (s1010487), 2020-12-08

Instructions:
1. Run this script (Python 3.8), so you see your webcam feed.
2. (optional) change the text colour if you cannot read it.
3. Check if your webcam works like a mirror.
    If not, change flip_image from False to True.
3. Position yourself in the middle of the video image (= vertical line).
    Leave some empty space above your head.
    Your hips should be visible, but not your legs (or only the very top).
4. Do the poses as instructed. Poses can be found in [file on github]
5. Recording takes place only during 'Hold Pose: X', where X is a pose.
    Recording ends at 'End pose'. You can move then.
6. 'No pose' is the default position. Here you place your hands on your
    lap/down your body; you can move a bit to diversify the recordings.
    IMPORTANT: Avoid making ANY gestures during 'Hold pose: No pose'.
7. Results are stored in TestResults.txt, with .csv layout. It has commas
    as separators, an integer index starting at 0 and a header.
    File will be overwritten if you make a new recording.
8. Do not forget to move the results file to HRI-Dance-Project/TrainingData.
    Change the file name according to the other files there.
"""

# Imports:
import cv2  # For displaying your webcam stream and the keypoints
import mediapipe as mp  # For keypoint recognition
import pandas as pd  # For its dataframes
import threading  # For making threads
import time  # For timer and sleep

# Options (you can change this for accessibility):
text_colour = (100, 255, 0)  # Pick a colour for the font
line_colour = (0, 255, 0)  # Pick a colour for the vertical line
cap = cv2.VideoCapture(0)  # Default webcam == 0, other cams => 1
flip_image = False  # Set to False if your webcam works like a mirror
file_name = "TestResults.txt"  # You can edit this to prevent overwriting

# These are the messages to guide the user through the keypoint logging:
_messages = {
    0: "POSE KEYPOINT LOGGER [press space]",
    1: "Instructions are in script [space...]",
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

# Label for negative samples:
_negative_label = "No pose"
_current_pose = [None]


def pose_logging():
    """Counts down during logging task and regulates the state
    of the program.
    """
    while _k_dic['m'] < 5:  # Wait until the user is ready.
        time.sleep(0.02)

    poses = ["Disco", "Hips", "Box", "Roof", "Kiss", "Guitar", "Clap",
             _negative_label]

    for pose in poses:  # Go through all stages for each of the poses
        for stage in range(5, 11):
            sleep_time = 1  # On-screen count down
            if stage == 5 or stage == 9:  # Announcing or holding pose
                sleep_time = 3  # Longer reading time for user
                if stage == 5:
                    _messages[stage] = "Next pose: " + str(pose)
                else:
                    _current_pose[0] = pose
                    _messages[stage] = "Hold pose: " + str(pose)
            elif stage == 10:  # Reset the pose label
                _current_pose[0] = None
            _k_dic['m'] = stage
            time.sleep(sleep_time)  # Wait before next stage


# Specify the text font, displayed over webcam feed:
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialise the MediaPipe pose detector:
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose_recogniser = mp_pose.Pose(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Make the column names for the dataframe:
column_names = ["Label"]
# There are 24 keypoints, each with an x, y and visibility score
for keypoint_nr in range(0, 24):
    str_nr = str(keypoint_nr)
    column_names.append(str_nr+"_x")
    column_names.append(str_nr+"_y")
    column_names.append(str_nr + "_v")

# Make the dataframe to store the keypoints in:
key_df = pd.DataFrame(columns=column_names)

# Store the pressed keys:
_k_dic = {'k': 0, 'm': 0}

# Start thread that regulates the state of the program:
logger = threading.Thread(target=pose_logging, daemon=True)
logger.start()

# Index used for the initial stage progression, controlled by the user:
user_stage = 0

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Image could not be read from webcam.")
        break

    # Convert the BGR image to RGB.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # To improve performance, mark the image as not writeable:
    image.flags.writeable = False
    if flip_image:  # Flip so that the video looks like a mirror.
        image = cv2.flip(image, 1)
    results = pose_recogniser.process(image)  # Obtain the user pose

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Draw vertical line on image for positioning:
    image = cv2.line(image, (320, 0), (320, 480), line_colour, 1)

    # Write text on the image:
    if _k_dic['m'] < 4:  # Initially at the top of the screen
        cv2.putText(image, _messages.get(_k_dic['m'], "ERROR"),
                    (0, 60), font,
                    1, text_colour,
                    1, cv2.LINE_AA)
    elif _k_dic['m'] >= 4:  # Centre of screen during the recording
        cv2.putText(image, _messages.get(_k_dic['m'], "ERROR"),
                    (260, 250), font,
                    1, text_colour,
                    1, cv2.LINE_AA)

    # Display the new image:
    cv2.imshow('MediaPipe Pose', image)

    # Add the keypoints to the dataframe if a pose is active:
    if _current_pose[0]:
        new_row = {"Label": _current_pose[0]}
        for key_i, point in enumerate(results.pose_landmarks.landmark):
            key_i_x = str(key_i) + "_x"
            key_i_y = str(key_i) + "_y"
            key_i_v = str(key_i) + "_v"
            new_row[key_i_x] = "%.5f" % point.x
            new_row[key_i_y] = "%.5f" % point.y
            new_row[key_i_v] = "%.5f" % point.visibility
        key_df = key_df.append(new_row, ignore_index=True)

    # Read the keyboard input:
    k = cv2.waitKey(5)
    _k_dic['k'] = k
    # When ESC is pressed or the logger thread is dead, stop this loop:
    if k & 0xFF == 27 or not logger.is_alive():
        print("Pressed ESC --> end video capture.")
        key_df.to_csv(file_name)
        break
    # During initial stages, go to next stage if user presses space:
    elif _k_dic['m'] < 5 and k & 0xFF == 32:
        user_stage += 1
        _k_dic['m'] = user_stage

# Clean everything up before ending this script:
pose_recogniser.close()
cap.release()
