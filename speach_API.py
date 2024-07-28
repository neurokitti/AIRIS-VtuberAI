from openvoice.api import BaseSpeakerTTS, ToneColorConverter
from openvoice import se_extractor
import torch
import os

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