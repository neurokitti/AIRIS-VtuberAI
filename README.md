# VtuberAI
this is an AI Vtuber that DOES NOT USE OpenAIs API key. it is designed to run localy and can run ofline.


## instilation
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
