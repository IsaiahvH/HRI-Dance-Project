# sketch
This folder contains shorts scripts that were used for testing purposes.

## MediaPipeTest:
- [Source](https://google.github.io/mediapipe/solutions/pose)
- Instructions:
	- Download the imports (easy through PyCharm)
	  - If this does not work:
	  - Open CMD anywhere where you can use the pip command
	    - (Or in your Venv if you use one.)
	  - "pip install pipwin"
	  - "pipwin install mediapipe" (or any other package)
  - Ensure your camera is connected if it is not built in
	- Set Python interpreter on one that works (works for Python 3.8 64).
	- Right mouse click on this file --> Run (in PyCharm)
	- Run!
- Close the MediaPipe window by pressing Esc.
- [Tips for classifying poses from MediaPipe (no ML)](https://developers.google.com/ml-kit/vision/pose-detection/classifying-poses)

## PoseRecorder:
- Built around the same code as MediaPipeTest.
- Used for storing poses.
- Instuctions can be found at the top of the script.
- Installation instructions the same as for MediaPipeTest.
- Example of how to sit (i.e. in the middle, space above head, hips and a bit lower visible):
<img src="https://github.com/IsaiahvH/HRI-Dance-Project/blob/main/KeypointCollectorExample.jpg" width="350" />


## VoiceRecognitionPorcupine:
- Voice Recogniser used from: https://github.com/Picovoice/porcupine.
- Use the preprogrammed free words like "Blueberry" or "Hi Alexa" to test if voice recognition with Porcupine works.
