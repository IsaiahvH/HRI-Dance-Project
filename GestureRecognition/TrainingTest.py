# Last update: 2020-12-10
# Imports:
import glob  # To loop through files
import os  # To find the current working directory
import pandas as pd  # For DataFrame
import numpy as np  # For its arrays
from sklearn import svm, metrics  # To train a simple SVM for testing
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from joblib import dump

# For testing whether the fault is due to joblib:
import cv2
import mediapipe as mp

# Read in data and convert labels to vector:
path = os.path.join(os.getcwd(), "TrainingData")
all_files = glob.glob(os.path.join(path, "*.txt"))
df = pd.concat((pd.read_csv(f, index_col=0) for f in all_files))
df.reset_index(drop=True, inplace=True)
# df = pd.read_csv(r"TrainingData/TestResults_Emma2.txt", index_col=0)
print(df.head())
print("Input data shape:", df.shape)

# Swap the bad cols:
cols = list(df)
cols[75], cols[73], cols[74] = cols[73], cols[74], cols[75]
df = df.loc[:, cols]

print(df.head())

# Extract all labels:
labels = df['Label'].unique()
print("All labels:", labels)

# Factorise the categories:
df["label_int"] = pd.factorize(df.Label)[0]
print(df.tail())

# Split in training and testing data:
train_share = 0.8
msk = np.random.rand(len(df)) < train_share
train = df[msk]
test = df[~msk]

# Convert into binary array, that can be used as target array:
one_target = np.array((labels[:] == "Clap")).astype(int)
print("Example of target vector:", one_target)

# Get the binary array for the entire training set (to be used later):
train_target = pd.get_dummies(train.Label).to_numpy()
print(train_target)

# Confirm the split:
print("Total nr. of samples:", len(df))
print("Training sampels:", len(train))
print("Testing samples:", len(test))

# Test a simple SVM:
y_train = train.label_int.to_numpy()
X_train = train.loc[:, "0_x":"24_v"].to_numpy()
y_test = test.label_int.to_numpy()
X_test = test.loc[:, "0_x":"24_v"].to_numpy()

clf = make_pipeline(StandardScaler(), svm.SVC())
# clf = svm.SVC()
clf.fit(X_train, y_train)

predictions = clf.predict(X_test)
print(predictions)
print(y_test)
accuracy = metrics.accuracy_score(y_test, predictions)
print(accuracy)
print(labels)


# Training model is finished, continue with testing it:
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
        key_points.append(key_point.visibility)
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
