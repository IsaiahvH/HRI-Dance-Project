from joblib import load


class GestureClassifier:
    def __init__(self, path='SVM_six_gestures.joblib'):
        self.clf = path
        self.labels = []

    @property
    def clf(self):
        return self.__clf

    @clf.setter
    def clf(self, path):
        if len(path) > 0:
            self.__clf = load(path)
        else:
            self.__clf = None

    @property
    def labels(self):
        return self.__labels

    @labels.setter
    def labels(self, labels):
        if len(labels) > 0:
            self.__labels = labels
        else:
            self.__labels = ['Disco',
                             'Hips',
                             'Box',
                             'Roof',
                             'Guitar',
                             'Clap',
                             'No pose']

    def classify(self, key_points):
        prediction = self.clf.predict(key_points)[0]
        return self.labels[prediction]
