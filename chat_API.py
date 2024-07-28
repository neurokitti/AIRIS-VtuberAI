from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, AutoModelForSeq2SeqLM
import torch
from threading import Thread
import torch
import os
import time
from datetime import datetime
import json
import utils
from huggingface_hub import login


class neo_chat_engine():
    def __init__(self,model_name,name,mem_length=7,path_to_system_messages = "OpenVoice\system_message.txt",device_map="cuda",torch_dtype=torch.bfloat16,load_in_4bit=False,load_in_8bit=False):
        login(token="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")
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device_map,
            torch_dtype=torch_dtype,
            trust_remote_code=True,
            load_in_4bit=load_in_4bit,
            load_in_8bit=load_in_8bit,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name,use_fast=True,device_map=device_map)
        self.streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
        self.chat_memory = []
        self.Vtuber_name = name
        self.mem_length = mem_length
        path_to_system_messages = path_to_system_messages
        self.system_message = utils.get_from_txt("OpenVoice\system_message.txt") if os.path.exists(path_to_system_messages) else  f"You are {self.Vtuber_name} a lively and cheerful VTuber who brings warmth and joy to your streams with your genuine and down-to-earth personality. As a friendly and approachable girl-next-door, you connect with your audience through, chatting, and sharing snippets of your everyday life. You enjoy playing a variety of games, from cozy farming sims to thrilling action adventures. Your streams are a made up of candid conversations, and fun community activities, creating a welcoming space for everyone. You also love sharing your hobbies, like cooking, drawing, and singing. Your backstory is simple yet relatable: a regular girl who decided to start streaming to share her passions and connect with like-minded people. Members of your chat will ask questions about your favorite games, your daily life, and your interests, and your role is to answer them with sincerity and a smile, making each viewer feel like a friend."

    def send_to_conversation_memory(self, user,name, text,):
        formated_memory = {'role':user,'content':f"{name}: {text}"}
        self.chat_memory.append(formated_memory)
    def format_transcription(self,transcript,):
        live_mem = transcript[-self.mem_length:]
        return live_mem
    def format_input(self,conversation_memory,):
        system_prompt_dict = {'role':"system",'content':self.system_message}
        conversation_memory.insert(0,system_prompt_dict)
        formated_memory = self.tokenizer.apply_chat_template(conversation_memory,tokenize=False, add_generation_prompt=True)
        formated_memory = f"{formated_memory}{self.Vtuber_name}: "
        return formated_memory
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