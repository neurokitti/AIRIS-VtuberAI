# Airis: Local Vtuber AI 

**Airis-VtuberAI** is a open source attempt to recreate the populer Vtuber "Neuro Sama". The project utilises no APIs and can run entirely localy without a need for an internet connection or considerable Vram.

the project includes the ability to transcribe the users voice, generate a response, and synthisise a text2speach output with as litle latency as resonable posible while sacraphising as little quality as posible. 

## To-Do
- blank
- lorum ipsum
- summerisation fix

## Benchmark
The Metrics in this section include the full project including the overhead from running OBS, and Vtube Studio. All of these test were run on GPU and used the phi 3 mini 4k instruct model from microsoft. 

### Airis
| Implementation | Precision | Beam size | Time | Max. GPU memory | Max. CPU memory |
| --- | --- | --- | --- | --- | --- |
| openai/whisper | fp16 | 5 | 4m30s | 11325MB | 9439MB |
| faster-whisper | fp16 | 5 | 54s | 4755MB | 3244MB |
| faster-whisper | int8 | 5 | 59s | 3091MB | 3117MB |





Git clone https://github.com/neurokitti/VtuberAI.git


Open the created folder in vs-code

Go to https://github.com/myshell-ai/OpenVoice 

In the vtuber folder clone the repo
Git clone https://github.com/myshell-ai/OpenVoice.git

You will need to download the models for open voice here:https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_1226.zip 

Then take the checkpoints folder inside it and place it in the open voice folder in your project. You should also place the main.py file in the open voice folder. (why? Because for some reason it wont let you access the openvoice utils unless its in there. If you can fix this pls help me)
![Screenshot 2024-07-15 175047](https://github.com/user-attachments/assets/b3cbeaaf-090a-4314-85dc-88aa8869410d)


Your workspace is now setup. All we need to do is install dependencies.
First make a virtual environment and activate it:
(i am using python 3.10.11)
![Screenshot 2024-07-15 175224](https://github.com/user-attachments/assets/d1ba2aa9-2945-4ed3-803f-8739566ca96b)

.venv/Scripts/Activate
Next install the requirements.txt from openvoice.
Cd OpenVoice
pip install -r requirements.txt

Open voice uses an older version of whisper so we will update it manually
Pip uninstall faster_whisper
Pip install faster_whisper
To get better GPU performance we will use:https://pytorch.org/get-started/locally/ 

I use the following:
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

Next we need to install all the requirements for the actual vtuber which are as follows:
Pip install transformers, pyaudio, keyboard, accelerate,bitsandbytes, flash_attn==2.5.8


Your done! If you need you can add a system text file! 

The script should run fine but if you want to set this up with Vtube studio for streaming there are a few more steps:

First:
We need to reroute the audio from the python file too a virtual audio cable. You can get a free one here:https://vb-audio.com/Cable/
Next go to settings and set the output device to the virtual audio cable. If python does not show up you need to run the vtuber script so and have it say something so that it shows up on the list of applications
![Screenshot 2024-07-15 181921](https://github.com/user-attachments/assets/bd1b58ab-cbbb-4c4b-9b79-b4e01d431a62)


Now in OBS (which i assume you have or something similar for streaming)
Add the virtual audio cable as a input: 
![Screenshot 2024-07-15 182114](https://github.com/user-attachments/assets/d18cfeb2-1a93-4c4c-b996-3a3734dd7e45)

If you want to be able to here the audio as well click the 3 dots for more options and click advanced properties
Finally find the audio cable in the sources and set it to monitor without output:
![Screenshot 2024-07-15 182154](https://github.com/user-attachments/assets/b8594c22-0a28-40d6-8370-3b3ea736334a)

All you need to do now is set up the vtuber avatar:
Go to setting and set the virtual audio cable as input:

![Screenshot 2024-07-15 182410](https://github.com/user-attachments/assets/055a5694-bcde-49fe-885f-6cf461358a53)



Next you need to setup the model:  adjust the settings to the following
![Screenshot 2024-07-15 182622](https://github.com/user-attachments/assets/db3026e2-2597-4b67-a604-c3b12cee205d)

YOUR DONE. THATS IT. sorry for the long instructions but its alot of simple steps that are easy to miss and openvoice has some issues. In the coming days and weeks the repo should have a install video and hopefully have simplified instructions for the install!




