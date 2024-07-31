import time
import csv
import json
from better_profanity import profanity
import re

def Elapsed_Time_Wrapper(function): 
        #this wraps the OBS functions to automaticly handle when OBS is not open.
        def wrapper(*args, **kwargs):
            start_time = time.time()
            function(*args, **kwargs)
            end_time = time.time()
            print("Time Elapsed: ",end_time-start_time)
        return wrapper

def get_from_txt(file_path):
        #returns a string from a text file.
        with open(file_path, 'r') as file:
            content = file.read()
        return content

def get_dict_from_txt(file_path):
    words = []
    with open(file_path, 'r') as file:
        for line in file:
            words.append(line.strip())
    return words

def censor(text,custom_badwords=[],extend_profanity_list=False):
    text = text.replace('"', '')
    
    pattern = r'\*[^*]*\*'
    text = re.sub(pattern, '', text)

    modified_list = []
    for word in custom_badwords:
        # Original word
        modified_list.append(word)
        # Word with a space at the beginning
        modified_list.append(' ' + word)
        # Capitalized word
        modified_list.append(word.capitalize())
        # Capitalized word with a space at the beginning
        modified_list.append(' ' + word.capitalize())
        # Uppercase word
        modified_list.append(word.upper())
        # Uppercase word with a space at the beginning
        modified_list.append(' ' + word.upper())
    print(modified_list)
    if extend_profanity_list == True:
        print("AAAAAAAAAAAA")
        profanity.add_censor_words(modified_list)
    else:
        print("FALSEsssss")
        profanity.load_censor_words(modified_list)

    filtered_text = profanity.censor(text, "~")
    
    pattern = r'~{1,}'
    filltered_text = re.sub(pattern, "[Censored]", filtered_text)
    return filltered_text
