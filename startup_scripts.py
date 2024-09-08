from record_API import record_engine
from transcription_API import transcription_engine
from speach_API import speach_engine
from OBS_API import OBS_engine
from Youtube_API import youtube_engine
import winsound
import time
import os
import threading
from chat_API import neo_chat_engine
from Twitch_API import Bot
import utils


def main_chat_twitch_non_legacy(model, Vtuber_name, oauth_token, channal_name,banned_words, extend_profanity_list,HF_token):
    chat_instance = neo_chat_engine(model,Vtuber_name,mem_length=5,token=HF_token,path_to_system_messages = "OpenVoice\system_message.txt", device_map="cuda",load_in_4bit=True,)
    speach_instace = speach_engine()
    twitch_instance = Bot(oauth_token,channal_name)# the Oauth_token can be found here: twitchapps.com/tmi and the chanal name is the name of the twitch chanal you want to read the chat from
    bot_thread = threading.Thread(target=twitch_instance.run)
    bot_thread.start()
    print("connection complete!")
    char_list = ['?', '!', '.', ':']
    TTS_OUTPUT = "TTS_output.wav"

    responded_messages = 0
    chat_instance.send_to_conversation_memory("assistant",chat_instance.Vtuber_name,f"hello evryone I am {chat_instance.Vtuber_name}! welcome to my stream!")
    while True:
        #print("asdf")
        chat_messages = twitch_instance.get_messages()
        #print(chat_messages)
        record_finish_time = time.time()

        if len(chat_messages) > responded_messages and chat_messages != []:
            most_recent_message = chat_messages[-1]
            chat_instance.send_to_conversation_memory(most_recent_message['role'],most_recent_message['name'],most_recent_message['text'])
            formated_input = chat_instance.format_input(chat_instance.chat_memory)
            print("FORMATED INPUT",formated_input)

            combined_string = ""
            final_response = ""
            TTS_finished_time = None

            for new_text in chat_instance.generate(formated_input,max_new_tokens=400):
                combined_string += new_text
                final_response += new_text
                #OBS_instance.update_text(combined_string)
                if any(char in char_list for char in new_text):
                    TTS_text = combined_string
                    TTS_text = utils.censor(TTS_text, custom_badwords=banned_words,extend_profanity_list=extend_profanity_list)
                    combined_string = ""
                    speach_instace.TTS(TTS_text,TTS_OUTPUT)
                    if TTS_finished_time == None:
                        TTS_finished_time = time.time() 
                        print("time to output:",TTS_finished_time - record_finish_time)
                    print("playimg")
                    winsound.PlaySound(TTS_OUTPUT,winsound.SND_FILENAME)

            chat_instance.send_to_conversation_memory("assistant",chat_instance.Vtuber_name,final_response)
            responded_messages +=1
            #OBS_instance.update_text("")

def main_chat_youtube_non_legacy(model,Vtuber_name,banned_words,extend_profanity_list,HF_token):
    chat_instance = neo_chat_engine(model,Vtuber_name,mem_length=5,token=HF_token,path_to_system_messages = "OpenVoice\system_message.txt",device_map="cuda",load_in_4bit=True,)
    speach_instace = speach_engine()
    youtube_instance = youtube_engine()
    youtube_instance.message_compiler()
    print("connection complete!")
    char_list = ['?', '!', '.', ':']
    TTS_OUTPUT = "TTS_output.wav"

    responded_messages = 0
    chat_instance.send_to_conversation_memory("assistant",chat_instance.Vtuber_name,f"hello evryone I am {chat_instance.Vtuber_name}! welcome to my stream!")
    chat_instance.send_to_conversation_memory("user","henson","Hi! what is your favorite color?")
    chat_instance.send_to_conversation_memory("assistant",chat_instance.Vtuber_name,"my favorite color is orange!")
    
    
    while True:
        chat_messages = youtube_instance.get_messages()
        #print(chat_messages)
        record_finish_time = time.time()

        if len(chat_messages) > responded_messages and chat_messages != []:
            most_recent_message = chat_messages[-1]
            chat_instance.send_to_conversation_memory(most_recent_message['role'],most_recent_message['name'],most_recent_message['text'])
            formated_input = chat_instance.format_input(chat_instance.chat_memory)
            print("FORMATED INPUT",formated_input)

            combined_string = ""
            final_response = ""
            TTS_finished_time = None

            for new_text in chat_instance.generate(formated_input,max_new_tokens=400):
                combined_string += new_text
                final_response += new_text
                #OBS_instance.update_text(combined_string)
                if any(char in char_list for char in new_text):
                    TTS_text = combined_string
                    TTS_text = utils.censor(TTS_text,custom_badwords=banned_words,extend_profanity_list=extend_profanity_list)
                    combined_string = ""
                    speach_instace.TTS(TTS_text,TTS_OUTPUT)
                    if TTS_finished_time == None:
                        TTS_finished_time = time.time() 
                        print("time to output:",TTS_finished_time - record_finish_time)
                    print("playimg")
                    winsound.PlaySound(TTS_OUTPUT,winsound.SND_FILENAME)

            chat_instance.send_to_conversation_memory("assistant",chat_instance.Vtuber_name,final_response)
            responded_messages +=1
            #OBS_instance.update_text("")

def main_interview_non_legacy(model,Vtuber_name,your_name,banned_words,extend_profanity_list,HF_token):
    chat_instance = neo_chat_engine(model,Vtuber_name,mem_length=3,token=HF_token,path_to_system_messages = "OpenVoice\system_message.txt",device_map="cuda",load_in_4bit=True,)
    speach_instace = speach_engine()
    record_instance = record_engine()
    transcription_instance = transcription_engine()

    OUTPUT_FILENAME="output.wav"
    char_list = ['?', '!', '.', ':']
    TTS_OUTPUT = "TTS_output.wav"
    username = your_name
    responded_messages = 0
    chat_instance.send_to_conversation_memory("assistant",chat_instance.Vtuber_name,f"hello evryone I am {chat_instance.Vtuber_name}! welcome to my stream!")
    while True:
        output_file = record_instance.listener(OUTPUT_FILENAME)
        record_finish_time = time.time()
        transcribed_text = transcription_instance.whisper(output_file)

        if transcribed_text != "":
            chat_instance.send_to_conversation_memory("user",username,transcribed_text)
            formated_input = chat_instance.format_input(chat_instance.chat_memory)
            print("FORMATED INPUT",formated_input)

            combined_string = ""
            final_response = ""
            TTS_finished_time = None

            for new_text in chat_instance.generate(formated_input,max_new_tokens=400):
                combined_string += new_text
                
                final_response += new_text
                if any(char in char_list for char in new_text):
                    TTS_text = combined_string
                    print("COMBINED STRING: ",combined_string)
                    f_TTS_text = utils.censor(TTS_text,custom_badwords=banned_words,extend_profanity_list=extend_profanity_list)
                    combined_string = ""  
                    speach_instace.TTS(f_TTS_text,TTS_OUTPUT)
                    if TTS_finished_time == None:
                        TTS_finished_time = time.time() 
                        print("time to output:",TTS_finished_time - record_finish_time)
                    winsound.PlaySound(TTS_OUTPUT,winsound.SND_FILENAME)

            chat_instance.send_to_conversation_memory("assistant",chat_instance.Vtuber_name,final_response)

