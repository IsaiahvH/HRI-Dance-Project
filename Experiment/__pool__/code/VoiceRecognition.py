import time
import struct
import pyaudio
import pvporcupine


class VoiceRecognizer:

    def __init__(self):
        self.__engine = None
        self.__pa = None
        self.__audioStream = None
        self.__keywordPaths = None

    def startEngine(self, keywordPaths):
        ''' Start VR engine
        - keywordPaths: an array of strings of the path keywords PPN files to use
        '''
        try:
            self.__keywordPaths = keywordPaths
            self.__engine = pvporcupine.create(keyword_paths=self.__keywordPaths)
            self.__pa = pyaudio.PyAudio()
        except Exception as e:
            print("VoiceRecognizer engine start encountered an exception", e)
            self.shutDownEngine()
        else:
            print("VoiceRecognizer engine started")

    def restartEngine(self, keywordPaths=None):
        ''' Restart VR engine
        - keywordPaths: (optional) an array of strings of Porcupine predefined keyword paths to listen for.
                    May be omitted only if engine is already running, in which case those keyword paths will be reused.
        '''
        if keywordPaths is None:
            assert self.__keywordPaths is not None, "Cannot restart engine as no keyword paths provided and none stored in VoiceRecognizer"
            keywordPaths = self.__keywordPaths

        self.shutDownEngine()
        self.startEngine(keywordPaths)

    def shutDownEngine(self):
        ''' Shut down VR engine
        '''
        self.__keywordPaths = None
        if self.__engine is not None:
            self.__engine.delete()
            self.__engine = None
        if self.__pa is not None:
            self.__pa.terminate()
            self.__pa = None
        if self.__audioStream is not None:
            self.__closeAudioStream()
        print("VoiceRecognizer engine shut down")

    def getEngineStatus(self):
        ''' Get VR engine status
        Returns: True if engine is running normally, False otherwise
        '''
        return (self.__engine is not None) and (self.__pa is not None)

    def __openAudioStream(self):
        ''' (Private) Open audio stream
        Returns: True if audio stream was successfully opened, False otherwise
        '''
        assert self.getEngineStatus(
        ), "Could not open audio stream because of invalid audio engine status"
        try:
            self.__audioStream = self.__pa.open(
                rate=self.__engine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.__engine.frame_length)
        except Exception as e:
            print("VoiceRecognizer audio stream opening encountered an exception", e)
            self.__closeAudioStream()
            return False
        else:
            return True

    def __closeAudioStream(self):
        ''' (Private) Close audio stream
        '''
        if self.__audioStream is not None:
            self.__audioStream.close()
            self.__audioStream = None

    def recognize(self, timeout):
        ''' Listen for keywords.
        - timeout: the amount of seconds before listening stops

        Precondition: VR engine must be running successfully

        Returns: an Int being the index of the first keyword detected, or
                None if the timeout expired before a keyword was detected
        '''
        assert self.getEngineStatus(
        ), "Could not start listening because of invalid audio engine status"
        if not self.__openAudioStream():
            return None

        deadline = time.time() + timeout

        try:
            while time.time() < deadline:
                pcm = self.__audioStream.read(self.__engine.frame_length)
                pcm = struct.unpack_from("h" * self.__engine.frame_length, pcm)
                keywordIndex = self.__engine.process(pcm)
                if keywordIndex >= 0:
                    return keywordIndex
            return None
        except Exception as e:
            print("VoiceRecognizer encountered an error upon listening")
        finally:
            self.__closeAudioStream()
