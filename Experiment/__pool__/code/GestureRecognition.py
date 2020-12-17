import time
import cv2
import sklearn
from joblib import load
import mediapipe as mp
import numpy as np


class GestureRecognizer:

    def __init__(self, flip_image = False):
        self.__engine = None
        self.__videoStream = None
        self.__clf = None
        self.__flip_image = flip_image
        self.__trainedKeywordOrder = ["do the disco",
                                      "hands on hips",
                                      "give a box",
                                      "raise the roof",
                                      "air guitar",
                                      "clap your hands"]
        self.__keywords = None

    def startEngine(self, clf_path, keywords):
        """Start GR engine.
        - clf_path: path to gesture classifier.
        - keywords: an array of strings; names of the gestures.
            Must be subset of self.__trainedKeywordOrder!
        """
        try:
            self.__clf = load(clf_path)
            assert all(keyword in self.__trainedKeywordOrder for keyword in
                       keywords), "Provided keywords must be subset " \
                                  "of pretrained keyword list"
            self.__keywords = keywords

            self.__engine = mp.solutions.pose.Pose(
                min_detection_confidence=0.5,
                min_tracking_confidence=-0.5)
            assert self.__openVideoStream(), "Could not open video stream " \
                                             "in gesture recognition"
        except Exception as e:
            print("GestureRecognizer engine start encountered an exception", e)
            self.shutDownEngine()
        else:
            print("GestureRecognizer engine started")

    def restartEngine(self, clf_path, keywords=None):
        """Restart GestureRecognition engine.
        - clf_path: path to the classifier.
        - keywords: (optional) an array of strings; names of gestures.
                    May be omitted only if engine is already running,
                    in which case those keywords will be reused.
        """
        if keywords is None:
            assert self.__keywords is not None, "Cannot restart engine as no" \
                " keywords provided and none stored in GestureRecognizer."
            keywords = self.__keywords

        self.shutDownEngine()
        self.startEngine(clf_path, keywords)

    def shutDownEngine(self):
        """Shut down gesture recognition engine."""
        self.__keywords = None
        self.__clf = None
        if self.__engine is not None:
            self.__engine.close()
            self.__engine = None
        if self.__videoStream is not None:
            self.__closeVideoStream()
            self.__videoStream = None
        print("GestureRecognizer engine shut down")

    def getEngineStatus(self):
        """ Get GR engine status
        Returns: True if engine is running normally, False otherwise
        """
        return (self.__engine is not None) and (self.__videoStream is not None)

    def __openVideoStream(self):
        """(Private) Open video stream
        Returns: True if video stream was successfully opened, False otherwise
        """
        try:
            self.__videoStream = cv2.VideoCapture(0)  # = cap
        except Exception as e:
            print("GestureRecogniser video stream opening encountered" +
                  " an exception",
                  e)
            self.__closeVideoStream()
            return False
        else:
            return True

    def __closeVideoStream(self):
        """(Private) Close video stream"""
        if self.__videoStream is not None:
            self.__videoStream.release()
            self.__videoStream = None

    def recognize(self, timeout):
        """Recognize gestures.
        - timeout: the amount of seconds before classifying gestures stops.
        Precondition: GR engine must be running successfully.
        Returns: an Int being the index of the first keyword detected, or
                None if the timeout expired before a keyword was detected.
        """
        assert self.getEngineStatus(), "Could not start listening because" \
                                       " of invalid video engine status"
        deadline = time.time() + timeout

        try:
            predictions = []
            while time.time() < deadline:
                _, image = self.__videoStream.read()
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                if self.__flip_image:
                    image = cv2.flip(image, 1)
                image.flags.writeable = False
                results = self.__engine.process(image)

                if results.pose_landmarks is None:  # No pose detected
                    continue

                # Extract the key-points from the pose and predict:
                key_points = []
                for i in range(25):
                    key_points.append(results.pose_landmarks.landmark[i].x)
                    key_points.append(results.pose_landmarks.landmark[i].y)

                key_points = np.array(key_points).reshape(1, -1)
                prediction = self.__clf.predict(key_points)[0]

                if len(predictions) > 0 and prediction != predictions[-1]:
                    predictions.clear()
                elif prediction != 6:
                    predictions.append(prediction)

                # If the same pose is seen 15 frames in a row, stop
                # and return transformed prediction:
                if len(predictions) > 15:
                    return self.__keywords.index(
                        self.__trainedKeywordOrder[prediction])
                cv2.waitKey(33)  # 30 fps
            return None
        except Exception as e:
            print("GestureRecognizer encountered an error while watching the"
                  " video stream for gestures", e)
