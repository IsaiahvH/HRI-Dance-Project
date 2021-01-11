# HRI-Dance-Project
Git repository to host code for the final project of Human-Robot Interaction, 2020 Radboud.

This repository contains the folders and files which were necessary to conduct the experiment for the HRI course. The following will eplxain briefly what the folders and files were used for.

### Administration:
- Consent Letter: the letter the participants read and signed.
- Information Letter: the letter the participants read before the experiment. Is used to inform them of the experiment and familiarise with what is expected from them. 
- Trial Structure: First this was used as possible options for trial. The final trial setup is now in the main text and considered alternatives are indicated in bold.
- Final Movements: The explanation in text of the movements Nao performs in the videos. 

### Experiment:
- Pool Folder: Folder contains the libraries, images, movies, and models which OpenSesame needed to run the experiment. 
- Responses Folder: The responses from the OpenSesame experiment are stored here.
- Experiment instructions.
- Analysis.ipynb: the Jupyter Notebook file which was used to analyse the data from the questionnaire and experiment. 
- HRIDanceExperiment.osexp: The OpenSesame file.
- OpenSesame Instructions.
- Questionnaire results.

### Gesture Recognition:
- .idea Folder
- Gesture Examples Folder: pictures of examples of the gestures meant for instructing researchers how to pose for collecting training data.
- Training Data Folder: Training Data obtained by the researchers.
- AllPoses.png: Image used in the OpenSesame code to show poses which participants needed to do.
- GestureRecognizer.py: Code to recognise gestures
- GestureRecognition.py: Analyses performance of SVM.
- PoseMarker.py: Recognises the poses.
- SVM_final.joblib
- SVM_final_scikit0_22_1.joblib
- TrainingTest.py

### Motions:
- Animations Nao zip file with videos of all the dance moves.

### Sketch:



### Folders (Incl. TODOs)
Here: (delete this line)
- TODO: Briefly describe the experiment at the top of this README.
- TODO: Remove the ...Improvements.md and keep updating this README until all TODOs are done.

Experiment: OpenSesame file and dependencies, the results of the experiment, their statistical analysis.
- TODO: Remove drafts.

GestureRecognition: MediaPipe Pose implementation, pose recognising SVM, its training data.
- TODO: update readme

Motions: Animations of the Nao's dance moves.
- TODO: remove the files that we did not use in the experiment... which is everything except the Animations_nao.zip.

sketch: Python files that implement the libraries used in the experiment, for testing purposes.
- TODO: update readme
