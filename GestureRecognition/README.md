# Gesture Recognition
Support vector machine (SVM) that can recognise six poses.

<img src="https://github.com/IsaiahvH/HRI-Dance-Project/blob/main/GestureRecognition/AllPoses.png" height="500">

Folders:
* GestureExamples: Images that show the poses that the SVM is trained on.
* TrainingData: Training data for the SVM

Files:
* AllPoses.png: the image shown above
* GestureSVMTraining.py: Cleans up the training data and generates an SVM
* SVM_final.joblib: Final SVM as used in the experiment
* SVM_final_scikit0_22_1.joblib: Same SVM, but for scikit 0.22.1
* TrainingTest.py: Loads in an SVM and you can see the webcam feed plus the predicted pose
