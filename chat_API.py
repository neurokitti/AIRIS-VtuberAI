from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, AutoModelForSeq2SeqLM
import torch
from threading import Thread
import torch
import os
import time
from datetime import datetime
import json
import utils
class chat_engine():
    def __init__(self,model_name,name,load_in_8bit=False,load_in_4bit=False,save_model_dir=None,skip_special_tokens=True,username="user",mem_length=10, device_map="cuda",torch_dtype=torch.bfloat16,**kwargs):
        """
        kwargs:
            load_in_4bit=True,
            attn_implementation="flash_attention_2"
        """
        self.summerized_memory = ""
        self.conversation_memory = []
        self.name = name
        self.username = username
        self.save_model_dir = save_model_dir
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device_map,
            torch_dtype=torch_dtype,
            trust_remote_code=True,
            load_in_4bit=load_in_4bit,
            load_in_8bit=load_in_8bit,
            **kwargs
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name,use_fast=True,device_map=device_map)
        if self.save_model_dir != None:
            self.model.save_pretrained(self.save_model_dir)
            self.tokenizer.save_pretrained(self.save_model_dir)


        self.streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=skip_special_tokens)
        self.summerizer_tokenizer = AutoTokenizer.from_pretrained("kabita-choudhary/finetuned-bart-for-conversation-summary",device_map="cpu")
        self.summerizer_model =AutoModelForSeq2SeqLM.from_pretrained("kabita-choudhary/finetuned-bart-for-conversation-summary",)
        self.mem_length = mem_length
    @utils.Elapsed_Time_Wrapper
    def summerize(self,text,max_new_tokens=200):
        # this uses a chat sumerisation model to sumerize the entire transcript that is no longer included in the active conversation memory
        input_ids = self.summerizer_tokenizer(text, return_tensors="pt").input_ids
        output_ids = self.summerizer_model.generate(input_ids, max_new_tokens=max_new_tokens, do_sample=False)
        output = self.summerizer_tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return output
    def summerize_transcript(self,transcription):
        # sumerizes the transcript.
        chunk = transcription[:-self.mem_length]
        formated_chunk = self.format_transcription(chunk,special_tokens=False)
        self.summerized_memory = self.summerize(formated_chunk, max_new_tokens=400)
    def send_to_conversation_memory(self, user,name, text,):
        # this will append a message to the conversation memory.
        token_map = {'system': "<|system|>", 'user': "<|user|>", 'assistant': "<|assistant|>"}
        if user in token_map:
            user_token = token_map[user]
        else:
            raise ValueError(f"Invalid user role: {user}")
        chat_entry = {'role': user_token,'name': name, 'text': text}
        self.conversation_memory.append(chat_entry)
    def format_transcription(self,transcript,special_tokens=True):
        # properly formats the transcription with the proper tokens and role with content
        formated_memory = ""
        for entry in transcript:
            if special_tokens == True:
                formated_memory += f"{entry['role']}\n{entry['name']}:{entry['text']}<|end|>\n"
            else:
                formated_memory += f"{entry['name']}:{entry['text']}\n"
        return formated_memory
    def format_input(self,system_text,conversation_memory,):
        # formats the input to the model to include system prompt and a properly formated transcript
        if self.mem_length != None:
            last_five_items = conversation_memory[-self.mem_length:]
            print(last_five_items)
        transcript = self.format_transcription(last_five_items)
        if self.summerized_memory != "":
            transcript = f"{self.summerized_memory}\n{transcript}"
        formated_input = f"<|system|>\n{system_text}<|end|>\n livestream chatlog transcript:\n{transcript}<|assistant|>{self.name} Response:"
        return formated_input
    def thread_generate(self,input_ids,max_new_tokens):
        # a thread for the generation prosses
        output_ids = self.model.generate(**input_ids,max_new_tokens=max_new_tokens, do_sample=True, streamer=self.streamer,)
        return output_ids
    def streamer_colector(self,):
        # streams tokens from the generation thread
        combined_string = ""
        for new_text in self.streamer:
            combined_string += new_text
            yield new_text
            
    def generate(self, input_text,stream=True,max_new_tokens=100):
        # spawns a thread to generate a response
        generation_start_time = time.time()
        input_ids = self.tokenizer([input_text], return_tensors="pt").to("cuda")
        generation_thread = Thread(target=self.thread_generate,daemon=True,args=(input_ids,max_new_tokens))
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
        #saves the Chat Engine memory to eather a Json or Text file.

        file_dir_path = f"{file_dir}"
        os.makedirs(file_dir_path, exist_ok=True)

        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        if json_format==True:
            file_path = f"{file_dir}/{file_name}_{current_datetime}.json"
            chat = json.dumps(self.conversation_memory, indent=4)
        else:
            file_path = f"{file_dir}/{file_name}_{current_datetime}.txt"
            chat = self.format_transcription(self.conversation_memory)
  
        
        with open(file_path, 'w') as file:
            file.write(chat)

    def get_from_txt(self,file_name):
        #returns a string from a text file.
        with open(file_name, 'r') as file:
            content = file.read()
        return content
