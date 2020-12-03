# Requires pvporcupine and pyaudio
# pip install pvporcupine
# pipwin install pyaudio

import pvporcupine
import pyaudio
import struct

# First draft to recognise a small set of keywords

porcupine = None
pa = None
audioStream = None

# Match keywords with files
keywords = ["Do a wave", "Finger Guns", "Play guitar"]
keywordPaths = ["./TrainedKeywords/do_a_wave.ppn","./TrainedKeywords/finger_guns.ppn","./TrainedKeywords/play_guitar.ppn"]

try:
    porcupine = pvporcupine.create(keyword_paths = keywordPaths)
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate = porcupine.sample_rate,
        channels = 1,
        format = pyaudio.paInt16,
        input = True,
        frames_per_buffer=porcupine.frame_length)

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print(f"Detected: {keywords[keyword_index]}")
finally:
    if porcupine is not None:
        porcupine.delete()
    if audio_stream is not None:
        audio_stream.close()
    if pa is not None:
        pa.terminate()

