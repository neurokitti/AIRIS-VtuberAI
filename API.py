import torch
import winsound
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import os
import logging
from styletts2 import tts
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
from transformers import pipeline
from faster_whisper import WhisperModel
import pyaudio
import wave
import keyboard
import time
import re


class VtubeAI:
    def __init__(self,debug_messages=False):
        self.debug_messages = debug_messages
    def debug_log(self, message):
        if self.debug_messages:
            print("Debug:", message)  
            logging.debug(message)


class TTS(VtubeAI):
    def __init__(self):
        super().__init__()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.debug_log(f"process sent to: {self.device}")
        self.TTS_voice_file_path = None
        self.TTS_output_path = "out.wav"

class LLM(VtubeAI):
    def find_words_in_brackets_and_remove(text):
        # Regex pattern to find words within brackets
        pattern = r'\[([^\]]+)\]'
        
        # Finding all occurrences of bracketed words
        words_in_brackets = re.findall(pattern, text)
        
        # Removing all bracketed words from the text
        text_without_brackets = re.sub(r'\[[^\]]+\]', '', text)
        
        # Return both the words found and the modified text
        return words_in_brackets, text_without_brackets









class ParlerTTS(TTS):
    def __init__(self):
        super().__init__()
        self.model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler_tts_mini_v0.1").to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler_tts_mini_v0.1",use_fast=True)
        self.output_path = self.TTS_output_path

    def run(self, prompt, auto_delete=False, file_path= "auto", description="A female speaker with a slightly low-pitched voice delivers her words quite expressively, in a very confined sounding environment with clear audio quality. She speaks very fast."):
        if file_path == "auto":
            output_path = self.output_path
        device = self.device  # Define device here

        if device == "auto":
            device = self.device

        model = self.model
        tokenizer = self.tokenizer
        
        self.debug_log("model and tokenizer loaded...")

        input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
        prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
        self.debug_log("prompt tokenized...")
        generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
        self.debug_log("finished generation...")
        audio_arr = generation.cpu().numpy().squeeze()
        sf.write(output_path, audio_arr, model.config.sampling_rate)
        winsound.PlaySound(output_path, winsound.SND_ALIAS)
        self.debug_log("file played...")

        if auto_delete:
            os.remove(output_path)
            return None
        else:
            return output_path


class StyleTTS(TTS):
    def __init__(self):
        super().__init__()
        self.syletts = tts.StyleTTS2()
        self.file_path = self.TTS_voice_file_path
        self.output_path = self.TTS_output_path

    def run(self, prompt, auto_delete=False, target_voice_path = "auto", output_path= "auto", alpha=0.1, beta=0.9,diffusion_steps=5, embedding_scale=1):
        if target_voice_path == "auto":
            target_voice_path = self.file_path
        if output_path == "auto":
            output_path = self.output_path

        device = self.device
        out = self.syletts.inference(prompt,target_voice_path=target_voice_path, output_wav_file=output_path, alpha=alpha,beta=beta, diffusion_steps=diffusion_steps, embedding_scale=embedding_scale)
        winsound.PlaySound(output_path, winsound.SND_ALIAS)
    
        """
        Text-to-speech function
        :param text: Input text to turn into speech.
        :param target_voice_path: Path to audio file of target voice to clone.
        :param output_wav_file: Name of output audio file (if output WAV file is desired).
        :param output_sample_rate: Output sample rate (default 24000).
        :param alpha: Determines timbre of speech, higher means style is more suitable to text than to the target voice.
        :param beta: Determines prosody of speech, higher means style is more suitable to text than to the target voice.
        :param diffusion_steps: The more the steps, the more diverse the samples are, with the cost of speed.
        :param embedding_scale: Higher scale means style is more conditional to the input text and hence more emotional.
        :param ref_s: Pre-computed style vector to pass directly.
        :param phonemize: Phonemize text. Defaults to True.
        :return: audio data as a Numpy array (will also create the WAV file if output_wav_file was set).
        """
        if auto_delete:
            os.remove(output_path)
            return None
        else:
            return output_path
        
class BarkTTS(TTS):
    def __init__(self):
        super().__init__()
        self.output_path = self.TTS_output_path
        preload_models()

    def run(self, prompt,voice="v2/en_speaker_6", auto_delete=False, output_path= "auto"):
        if output_path == "auto":
            output_path = self.output_path
        # generate audio from text
        
        audio_array = generate_audio(prompt, history_prompt=voice)

        write_wav(output_path, SAMPLE_RATE, audio_array)
        winsound.PlaySound(output_path, winsound.SND_ALIAS)

        if auto_delete:
            os.remove(output_path)
            return None
        else:
            return output_path





#tiny.en, tiny, base.en, base, small.en, small, medium.en, medium, large-v1, large-v2, large-v3, large, distil-large-v2, distil-medium.en, distil-small.en
model_size = "base.en" 

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")
class STT(VtubeAI):
    def whisper_trans(file):
        out = ''
        print("transcribing...")
        segments, info = model.transcribe(file, beam_size=5)
        for segment in segments:
            out = out.join(segment.text)
        return out


    def record(filename="out.wav"):
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE =44100
        CHUNK =1024
        OUTPUT_FILENAME = filename
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT,channels=CHANNELS,rate=RATE, input=True, frames_per_buffer=CHUNK)
        frames = []
        print("space to start")
        keyboard.wait('space')
        print("listening...")
        time.sleep(0.2)

        while True:
            try:
                data = stream.read(CHUNK)
                frames.append(data)
            except KeyboardInterrupt:
                break
            if keyboard.is_pressed('space'):
                time.sleep(0.2)
                break
        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        return OUTPUT_FILENAME
