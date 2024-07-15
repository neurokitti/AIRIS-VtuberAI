from openvoice.api import BaseSpeakerTTS, ToneColorConverter
from openvoice import se_extractor
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, AutoModelForSeq2SeqLM, BitsAndBytesConfig
import threading
import time
import torch
from datetime import datetime
import os
from faster_whisper import WhisperModel
from threading import Thread, Lock
import threading
import winsound
import pyaudio
import wave
import keyboard
import time
import re

import winsound
import torch
import time
import os
import pyaudio
import wave
import keyboard
import time
import re
from datetime import datetime
import json


class chat_engine():
    def __init__(self,model_name,name,username="user",mem_length=10, device_map="cuda",torch_dtype=torch.bfloat16,attn_implementation="flash_attention_2",**bnb_kwargs):
        """
        kwargs:
            load_in_4bit=True,
            attn_implementation="flash_attention_2"
        """
        self.summerized_memory = ""
        self.conversation_memory = []
        self.name = name
        self.username = username
        sfg = {'attn_implementation':'flash_attention_2'} if attn_implementation == "flash_attention_2" else {}
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device_map,
            torch_dtype=torch_dtype,
            trust_remote_code=True,
            load_in_4bit=True,
            **sfg
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name,use_fast=True,device_map=device_map)
        self.streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
        self.summerizer_tokenizer = AutoTokenizer.from_pretrained("kabita-choudhary/finetuned-bart-for-conversation-summary",device_map="cpu")
        self.summerizer_model =AutoModelForSeq2SeqLM.from_pretrained("kabita-choudhary/finetuned-bart-for-conversation-summary",)
        self.mem_length = mem_length

    def summerize(self,text,max_new_tokens=200):
        input_ids = self.summerizer_tokenizer(text, return_tensors="pt").input_ids
        output_ids = self.summerizer_model.generate(input_ids, max_new_tokens=max_new_tokens, do_sample=False)
        output = self.summerizer_tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return output
    def summerize_transcript(self,transcription):
        chunk = transcription[:-self.mem_length]
        formated_chunk = self.format_transcription(chunk,special_tokens=False)
        self.summerized_memory = self.summerize(formated_chunk, max_new_tokens=400)
    def send_to_conversation_memory(self, user,name, text, ):
        token_map = {'system': "<|system|>", 'user': "<|user|>", 'assistant': "<|assistant|>"}
        if user in token_map:
            user_token = token_map[user]
        else:
            raise ValueError(f"Invalid user role: {user}")
        chat_entry = {'role': user_token,'name': name, 'text': text}
        self.conversation_memory.append(chat_entry)
    def format_transcription(self,transcript,special_tokens=True):
        formated_memory = ""
        for entry in transcript:
            if special_tokens == True:
                formated_memory += f"{entry['role']}\n{entry['name']}:{entry['text']}<|end|>\n"
            else:
                formated_memory += f"{entry['name']}:{entry['text']}\n"
        return formated_memory
    def format_input(self,system_text,conversation_memory,):
        if self.mem_length != None:
            last_five_items = conversation_memory[-self.mem_length:]
            print(last_five_items)
        transcript = self.format_transcription(last_five_items)
        if self.summerized_memory != "":
            transcript = f"{self.summerized_memory}\n{transcript}"
        formated_input = f"<|system|>\n{system_text} use the conversation transcript to continue the conversation<|end|>\n conversation transcript:\n{transcript}<|assistant|>{self.name}:"
        return formated_input
    def thread_generate(self,input_ids,max_new_tokens=100):
        output_ids = self.model.generate(**input_ids,max_new_tokens=max_new_tokens, do_sample=True, streamer=self.streamer,)
        return output_ids
    def streamer_colector(self,):
        combined_string = ""
        for new_text in self.streamer:
            combined_string += new_text
            yield new_text
    def generate(self, input_text,stream=True,max_new_tokens=100):
        generation_start_time = time.time()
        input_ids = self.tokenizer([input_text], return_tensors="pt").to("cuda")
        generation_thread = Thread(target=self.thread_generate,daemon=True,args=(input_ids,))
        generation_thread.start()
        generation_end_time = time.time()
        generation_time = generation_end_time - generation_start_time

        combined_string= ""
        if stream == True:
            return self.streamer_colector()
        else:
            for new_text in self.streamer:
                combined_string += new_text
            return generation_time, combined_string
    def save_chat_to_file(self,file_name="chatlog",file_dir="chatlogs",json_format=False):
        file_dir_path = f"{file_dir}"
        os.makedirs(file_dir_path, exist_ok=True)

        # Get the current date in YYYYMMDD format
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        if json_format==True:
            file_path = f"{file_dir}/{file_name}_{current_datetime}.json"
            chat = json.dumps(self.conversation_memory, indent=4)
        else:
            file_path = f"{file_dir}/{file_name}_{current_datetime}.txt"
            chat = self.format_transcription(self.conversation_memory)
        # Create the file path with the date appended to the file name
        
        with open(file_path, 'w') as file:
            file.write(chat)
    def get_from_txt(self,file_name): #get information from a txt file.
        with open(file_name, 'r') as file:
            content = file.read()
        return content

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

class speach_engine:
    def __init__(self):
        ckpt_base = 'OpenVoice/checkpoints/base_speakers/EN'
        ckpt_converter = 'OpenVoice/checkpoints/converter'
        device = "cuda:0"
        self.output_dir = 'OpenVoice/outputs'

        self.base_speaker_tts = BaseSpeakerTTS(f'{ckpt_base}/config.json', device=device)
        self.base_speaker_tts.load_ckpt(f'{ckpt_base}/checkpoint.pth')

        self.tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
        self.tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

        os.makedirs(self.output_dir, exist_ok=True)

        self.source_se = torch.load(f'{ckpt_base}/en_default_se.pth').to(device)

        #self.reference_speaker = 'OpenVoice/resources/marcus-voice.mp3' # This is the voice you want to clone
        #self.target_se, self.audio_name = se_extractor.get_se(self.reference_speaker, self.tone_color_converter, target_dir='processed', vad=True)

        self.save_path = f'{self.output_dir}/output_en_default.wav'
    def TTS(self,text,src_path,speaker='default'):
        # choices=['default', 'whispering', 'cheerful', 'terrified', 'angry', 'sad', 'friendly'],
        self.base_speaker_tts.tts(text, src_path, speaker=speaker, language='English', speed=1.0)

"""
class styleTTSv2():
    def __init__(self):
        self.my_tts = tts.StyleTTS2()
    def TTS(self,text,src_path):
        self.my_tts.inference(text, output_wav_file=src_path)
"""
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
engine = chat_engine("microsoft/Phi-3-mini-4k-instruct","Rose")
system_message = engine.get_from_txt("system_message.txt")
OUTPUT_FILENAME="output.wav"
char_list = ['?', '!', '.', ':']
TTS_output = "TTS_output.wav"
record_engine = record_engine()
transcription_engine = transcription_engine()
speach_engine = speach_engine()

engine.send_to_conversation_memory("user","user","hi! how is your day going?")
engine.send_to_conversation_memory("user",engine.name,"my day is going swell! i just got back from my garden where i was planting strawbaries for the summer. I plan on having a party to cellebrate the harvest!")

while True:
    output_file = record_engine.listener(OUTPUT_FILENAME)
    record_finish_time = time.time() #the start time of prossesing (used in time to response calculations)
    transcribed_text = transcription_engine.whisper(output_file)
    if transcribed_text != None and transcribed_text != "": # in case of no response we should attempt to record again
        #print(transcribed_text)
        engine.send_to_conversation_memory("user",engine.username,transcribed_text)
        #print(engine.conversation_memory)
        formated_input = engine.format_input(system_message,engine.conversation_memory)
        print(formated_input)
        combined_string = ""
        final_response = ""
        TTS_finished_time = None
        for new_text in engine.generate(formated_input,max_new_tokens=200):
            combined_string += new_text
            final_response += new_text
            if any(char in char_list for char in new_text):
                TTS_text = combined_string
                combined_string = ""
                speach_engine.TTS(TTS_text,TTS_output)
                if TTS_finished_time == None:
                    TTS_finished_time = time.time() 
                    print("time to output:",TTS_finished_time - record_finish_time)
                winsound.PlaySound(TTS_output,winsound.SND_FILENAME)
        print(final_response)
        engine.send_to_conversation_memory("assistant",engine.name,final_response)
    if len(engine.conversation_memory) > engine.mem_length:
        engine.summerize_transcript(engine.conversation_memory)


# bad_words_ids=bad_words_ids,
