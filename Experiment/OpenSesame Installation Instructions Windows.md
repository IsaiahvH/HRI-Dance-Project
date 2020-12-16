## Disclaimer
OpenSesame is used on many (Windows) computers so it should work fine. However, we also hack the flip out of it by using Python, recognisers, etc. OpenSesame uses its own (python) virtual environment, which is not really obvious or clear how it works.

We will therefore need to install the dependencies inside OpenSesame. We did not manage to make this work for PyAudio / PortAudio, so these are included manually (in `__pool__` > `code` > `libraries`).

After following the steps below, take a look through the code and that inside the experiment (through OpenSesame) to discover its structure.

----

## Version 2
1. Download OpenSesame from here: https://osdoc.cogsci.nl/3.3/download/#windows notice, please download the megapack
1. When installed open the opensesame file from the experiment folder
1. Type '!pip install pvporcupine' and '!pip install mediapipe' (if [Errno 13], add '--user') in its console
1. Try running it with the blue arrows button at the top
1. It should work now, if not, call/whatsapp me (Lizzy)



## Version 1
1. Download OpenSesame from here: https://osdoc.cogsci.nl/
1. When installed open the opensesame file from the experiment folder
1. Rename the folder in setup to the folder where you python code is
1. Test if PyAudio is installed by typing "import pyaudio" in the OpenSesame console
1. If no pyaudio errors nice. Continue at step 12
1. Else: 
1. Go to the the Folder of OpenSesame (probably in your program files). Go to the share folder
1. Create 2 folders. One named "PyAudio" and one "PortAudio"
1. Look for a file named pyaudio.py on your pc and copy this file to the PyAudio folder you just created
1. Do the same for portaudio but copy it to the PortAudio folder. For me the file was named this "_portaudio.cp37-win_amd64"
1. Test if PyAudio works by typing "import pyaudio" into the OpenSesame console 
1. Try running it with the blue arrows button at the top
1. If pvporcupine is not installed go to the opensesame console and type !pip install pvporcupine
1. It should work now, if not, call/whatsapp me (Lizzy)
