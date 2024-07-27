from chat_API import chat_engine
from record_API import record_engine
from transcription_API import transcription_engine
from speach_API import speach_engine
from OBS_API import OBS_engine
from Youtube_API import youtube_engine
import winsound
import time
import os
import threading

def main_interview():
    chat_instance = chat_engine("microsoft/Phi-3-mini-4k-instruct","Hannah",load_in_4bit=True,save_model_dir="phi3",mem_length=7, skip_special_tokens=True,)
    speach_instace = speach_engine()
    record_instance = record_engine()
    transcription_instance = transcription_engine()

    path_to_system_messages = "OpenVoice\system_message.txt"
    system_message = chat_instance.get_from_txt("OpenVoice\system_message_interview.txt") if os.path.exists(path_to_system_messages) else  "you are Rose evergreen a AI Vtuber live streaming to her viewers, you like to play video games, you respond to the people in chat, "
    OUTPUT_FILENAME="output.wav"
    char_list = ['?', '!', '.', ':']
    TTS_OUTPUT = "TTS_output.wav"
    chat_instance.username = "Henson"
    responded_messages = 0
    chat_instance.send_to_conversation_memory("assistant",chat_instance.name,f"hello evryone I am {chat_instance.name}! welcome to my stream!")
    while True:
        output_file = record_instance.listener(OUTPUT_FILENAME)
        record_finish_time = time.time()
        transcribed_text = transcription_instance.whisper(output_file)

        if transcribed_text != "":
            chat_instance.send_to_conversation_memory("user",chat_instance.username,transcribed_text)
            formated_input = chat_instance.format_input(system_message,chat_instance.conversation_memory)
            print("FORMATED INPUT",formated_input)

            combined_string = ""
            final_response = ""
            TTS_finished_time = None

            for new_text in chat_instance.generate(formated_input,max_new_tokens=400):
                combined_string += new_text
                final_response += new_text
                if any(char in char_list for char in new_text):
                    TTS_text = combined_string
                    combined_string = ""  
                    speach_instace.TTS(TTS_text,TTS_OUTPUT)
                    if TTS_finished_time == None:
                        TTS_finished_time = time.time() 
                        print("time to output:",TTS_finished_time - record_finish_time)
                    winsound.PlaySound(TTS_OUTPUT,winsound.SND_FILENAME)

            chat_instance.send_to_conversation_memory("assistant",chat_instance.name,final_response)
            responded_messages +=1

            if len(chat_instance.conversation_memory) > chat_instance.mem_length:
                chat_instance.summerize_transcript(chat_instance.conversation_memory)
            


def main_chat():
    OBS_instance = OBS_engine("YOUR_OBS_WEBSOCKET_PASWORD") 
    chat_instance = chat_engine("microsoft/Phi-3-mini-4k-instruct","hannah",load_in_8bit=True,save_model_dir="phi3",mem_length=7, skip_special_tokens=True,)
    speach_instace = speach_engine()
    youtube_instance = youtube_engine(OBS_instance)
    youtube_instance.message_compiler()
    print("connection complete!")
    path_to_system_messages = "OpenVoice\system_message.txt"
    system_message = chat_instance.get_from_txt("OpenVoice\system_message.txt") if os.path.exists(path_to_system_messages) else  "you are Rose evergreen a AI Vtuber live streaming to her viewers, you like to play video games, you respond to the people in chat, "
    chat_instance.name= "hannah"
    char_list = ['?', '!', '.', ':']
    TTS_OUTPUT = "TTS_output.wav"

    responded_messages = 0
    chat_instance.send_to_conversation_memory("assistant",chat_instance.name,f"hello evryone I am {chat_instance.name}! welcome to my stream!")
    while True:
        chat_messages = youtube_instance.get_messages()
        record_finish_time = time.time()

        if len(chat_messages) > responded_messages and chat_messages != []:
            most_recent_message = chat_messages[-1]
            chat_instance.send_to_conversation_memory(most_recent_message['role'],most_recent_message['name'],most_recent_message['text'])
            formated_input = chat_instance.format_input(system_message,chat_instance.conversation_memory)
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
                    combined_string = ""
                    speach_instace.TTS(TTS_text,TTS_OUTPUT)
                    if TTS_finished_time == None:
                        TTS_finished_time = time.time() 
                        print("time to output:",TTS_finished_time - record_finish_time)
                    print("playimg")
                    winsound.PlaySound(TTS_OUTPUT,winsound.SND_FILENAME)

            chat_instance.send_to_conversation_memory("assistant",chat_instance.name,final_response)
            responded_messages +=1
            #OBS_instance.update_text("")
            
            if len(chat_instance.conversation_memory) > chat_instance.mem_length:
                chat_instance.summerize_transcript(chat_instance.conversation_memory)

from Twitch_API import Bot
def main_chat_twitch():
    OBS_instance = OBS_engine("YOUR_OBS_WEBSOCKET_PASWORD")
    chat_instance = chat_engine("microsoft/Phi-3-mini-4k-instruct","hannah",load_in_8bit=True,save_model_dir="phi3",mem_length=7, skip_special_tokens=True,)
    speach_instace = speach_engine()
    twitch_instance = Bot("OAUTH_TOKEN","CHANNAL_NAME")# the Oauth_token can be found here: twitchapps.com/tmi and the chanal name is the name of the twitch chanal you want to read the chat from
    bot_thread = threading.Thread(target=twitch_instance.run)
    bot_thread.start()
    print("connection complete!")
    path_to_system_messages = "OpenVoice\system_message.txt"
    system_message = chat_instance.get_from_txt("OpenVoice\system_message.txt") if os.path.exists(path_to_system_messages) else  "you are Rose evergreen a AI Vtuber live streaming to her viewers, you like to play video games, you respond to the people in chat, "
    chat_instance.name= "hannah"
    char_list = ['?', '!', '.', ':']
    TTS_OUTPUT = "TTS_output.wav"

    responded_messages = 0
    chat_instance.send_to_conversation_memory("assistant",chat_instance.name,f"hello evryone I am {chat_instance.name}! welcome to my stream!")
    while True:
        #print("asdf")
        chat_messages = twitch_instance.get_messages()
        #print(chat_messages)
        record_finish_time = time.time()

        if len(chat_messages) > responded_messages and chat_messages != []:
            most_recent_message = chat_messages[-1]
            chat_instance.send_to_conversation_memory(most_recent_message['role'],most_recent_message['name'],most_recent_message['text'])
            formated_input = chat_instance.format_input(system_message,chat_instance.conversation_memory)
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
                    combined_string = ""
                    speach_instace.TTS(TTS_text,TTS_OUTPUT)
                    if TTS_finished_time == None:
                        TTS_finished_time = time.time() 
                        print("time to output:",TTS_finished_time - record_finish_time)
                    print("playimg")
                    winsound.PlaySound(TTS_OUTPUT,winsound.SND_FILENAME)

            chat_instance.send_to_conversation_memory("assistant",chat_instance.name,final_response)
            responded_messages +=1
            #OBS_instance.update_text("")
            
            if len(chat_instance.conversation_memory) > chat_instance.mem_length:
                chat_instance.summerize_transcript(chat_instance.conversation_memory)
