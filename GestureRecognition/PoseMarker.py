import cv2
import mediapipe as mp


class PoseMarker:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose(min_detection_confidence=0.5,
                                           min_tracking_confidence=-0.5)
        self.drawing = mp.solutions.drawing_utils
        self.key_points = []

    @property
    def pose(self):
        return self.__pose

    @pose.setter
    def pose(self, pose):
        if not self.__pose:
            self.__pose = pose

    @property
    def drawing(self):
        return self.__drawing

    @drawing.setter
    def drawing(self, drawing):
        if not self.__drawing:
            self.__drawing = drawing

    @property
    def key_points(self):
        return self.__key_points

    @key_points.setter
    def key_points(self, results):
        self.__key_points = []
        if results:
            landmarks = results.pose_landmarks.landmark
            if len(landmarks) > 0:
                for key_point in landmarks:
                    self.__key_points.append(key_point.x)
                    self.__key_points.append(key_point.y)

    def process_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.pose.process(image)
        self.key_points = results
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        self.drawing.draw_landmarks(
            image, results.pose_landmarks, self.pose.POSE_CONNECTIONS)
        return image, self.key_points


