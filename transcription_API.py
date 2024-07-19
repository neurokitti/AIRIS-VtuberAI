from faster_whisper import WhisperModel
import time
import os


class transcription_engine:
    def __init__(self, model_size="distil-large-v3",):
        self.comput_tipe = "int8_float16"
        self.model_name = model_size
        self.sound_file = "out1.wav"
        self.model = WhisperModel(self.model_name, device="cuda", compute_type=self.comput_tipe, flash_attention=True) #flash_attention=True
        self.transcribed_text = ''
    def whisper(self, file):
        if os.path.exists(file):
            print("File exists")
            out = ''
            start_t = time.time()
            segments, info = self.model.transcribe(file, beam_size=1)
            
            for segment in segments:
                #print("segments:",segment.text) #  13 for the period # 30 is question mark # 0 is exclemation mark
                out += segment.text
            final_t = time.time()
            elapsed_time = final_t - start_t 
            print(out)
            print(self.comput_tipe,"compute time:",elapsed_time)
            return out
        else:
            print("no file found")
            return None