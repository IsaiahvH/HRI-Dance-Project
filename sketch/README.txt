sketch: this folder contains shorts scripts that are used for testing purposes

MediaPipeTest:
- Source: https://google.github.io/mediapipe/solutions/pose
	- Contains original code, landmark indices
- Do not use the z-value (depth): model is not trained properly for that.
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
- Tips for classifying poses: https://developers.google.com/ml-kit/vision/pose-detection/classifying-poses

PoseRecorder:
- STILL WIP ++++ DON'T USE IT YET.
- Built around the same code as MediaPipeTest.
- Used for storing poses.
