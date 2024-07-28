import keyboard
import pyaudio
import wave
import os

class record_engine:
    def __init__(self):
        self.record = False
    def listener(self, audio_name):
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024
        OUTPUT_FILENAME = str(audio_name)
        if os.path.exists(OUTPUT_FILENAME):
            os.remove(OUTPUT_FILENAME)
        if keyboard.read_key() == "space":
            print("starting audio")
            frames = []
            audio = pyaudio.PyAudio()
            stream = audio.open(format=FORMAT,channels=CHANNELS,rate=RATE, input=True, frames_per_buffer=CHUNK)
        
            while keyboard.is_pressed("space"):
                    data = stream.read(CHUNK)
                    frames.append(data)
            stream.stop_stream()
            stream.close()
            audio.terminate()
            waveFile = wave.open(OUTPUT_FILENAME, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()
            print("ending audio")
        return OUTPUT_FILENAME