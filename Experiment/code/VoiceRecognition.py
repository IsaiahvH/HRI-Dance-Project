import pvporcupine
import pyaudio
import struct
import time

class VoiceRecognizer:

    def __init__(self):
        self.__engine = None
        self.__pa = None
        self.__audioStream = None

        # Demo keywords
        self.__keywords = None #["terminator", "grapefruit", "grasshopper", "blueberry"]

    def startEngine(self, keywords):
        ''' Start VR engine
        - keywords: an array of strings of Porcupine predefined keywords to listen for
        '''
        try:
            self.__keywords = keywords
            self.__engine = pvporcupine.create(keywords=self.__keywords)#.create(keyword_paths = keywordPaths)
            self.__pa = pyaudio.PyAudio()
        except Exception as e:
            print("VoiceRecognizer engine start encountered an exception", e)
            self.shutDownEngine()
        else:
            print("VoiceRecognizer engine started")

    def restartEngine(self, keywords = None):
        ''' Restart VR engine 
        - keywords: (optional) an array of strings of Porcupine predefined keywords to listen for.
                    May be omitted only if engine is already running, in which case those keywords will be reused.
        '''
        if keywords is None:
            assert self.__keywords is not None, "Cannot restart engine as no keywords provided and none stored in VoiceRecognizer"
            keywords = self.__keywords

        self.shutDownEngine()
        self.startEngine(keywords)

    def shutDownEngine(self):
        ''' Shut down VR engine
        '''
        self.__keywords = None
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
        assert self.getEngineStatus(), "Could not open audio stream because of invalid audio engine status"
        try:
            self.__audioStream = self.__pa.open(
                rate = self.__engine.sample_rate,
                channels = 1,
                format = pyaudio.paInt16,
                input = True,
                frames_per_buffer = self.__engine.frame_length)
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

    def listen(self, timeout):
        ''' Listen for keywords.
        - timeout: the amount of seconds before listening stops

        Precondition: VR engine must be running successfully

        Returns: an Int being the index of the first keyword detected, or
                None if the timeout expired before a keyword was detected 
        '''
        assert self.getEngineStatus(), "Could not start listening because of invalid audio engine status"
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

