# VtuberAI
this is an AI Vtuber that DOES NOT USE OpenAIs API key. it is designed to run localy and can run ofline.

## Updates
None lol

## instilation
i dont know how to make a requirements.txt so for now just do this.
first install pytorch using the following. this is what I used for my nvidia GPU but you can use other instilations [here](https://pytorch.org/get-started/locally/)
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```
```
pip install git+https://github.com/huggingface/parler-tts.git
pip install styletts2
pip install git+https://github.com/suno-ai/bark.git
pip install faster-whisper
pip install PyAudio
pip install transformers -U
pip install optimum
```
you also need to install AutoGPTQ. it must me installed from source and this is the only way that worked for me. if this does not you can find alternative instructions [here](https://github.com/AutoGPTQ/AutoGPTQ)
```
git clone https://github.com/PanQiWei/AutoGPTQ.git
cd AutoGPTQ
pip install numpy gekko pandas
python setup.py install
```

## usage
after instilation you can literaly just run the main.py file to test it but there are many features you should impliment yourself when making your own Vtuber or assistant AI.  

you will need a virtual audio cable to have the mouth of the vtuber model move which you can get [here](https://vb-audio.com/Cable/)

set the output of python to the virtual audio cable:

![Screenshot 2024-05-01 164304](https://github.com/neurokitti/VtuberAI/assets/168581144/aaf8f4b9-663c-4cca-9972-12fbf7b75341)


then set the virtual audio cable as input in Vtube studio. make sure the preview microphone feedback is on so you can hear the voice. make sure your lip sync type is advanced and that you have pressed the setup in model button.

![image](https://github.com/neurokitti/VtuberAI/assets/168581144/1415e2c2-f3b7-4382-b1f5-de525821ca0e)

at this point the voice should be audable but the mouth wont move unleass the mouth open is set to VoiceVolumePlusMouthOpen

![image](https://github.com/neurokitti/VtuberAI/assets/168581144/d98a794d-c9cf-47d0-91fd-ad7a65414812)



finaly

## Future Plans
- add Twitch API and Youtube Live Stream API
- impliment PiperTTS for the voice
- impliment openvoice v2
- add LLaVa for vision capabilitys
