import pvporcupine
import pyaudio
import struct


porcupine = None
pa = None
audio_stream = None
print(pvporcupine.KEYWORDS)
keywords = ["Do a wave", "Finger Guns", "Play guitar"]
patharray = ["C:/Users/lizzy/PycharmProjects/HRI/do_a_wave.ppn","C:/Users/lizzy/PycharmProjects/HRI/finger_guns.ppn","C:/Users/lizzy/PycharmProjects/HRI/play_guitar_windows_1_2_2021_v1.9.0.ppn"]
try:
    porcupine = pvporcupine.create(keyword_paths=patharray)  # ['blueberry', 'computer', "alexa"])
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
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

