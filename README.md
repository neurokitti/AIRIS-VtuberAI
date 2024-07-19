![Screenshot 2024-07-19 002209](https://github.com/user-attachments/assets/ff1739da-5b37-4bb4-8c7b-20c66e8dd193)

## Airis: Local Vtuber AI 
**Airis-VtuberAI** is a open source attempt to recreate the populer Vtuber "Neuro Sama". The project utilises no APIs and can run entirely localy without a need for an internet connection or considerable Vram.

the project includes the ability to transcribe the users voice, generate a response, and synthisise a text2speach output with as litle latency as resonable posible while sacraphising as little quality as posible. 

## Features
- **Chat Mode**
  - Allows the Vtuber AI to read and respond to chat messages
  - Interacts with OBS to include Subtitles and updated chat
  - lower VRAM
- **Interview Mode**
  - Allows the Vtuber AI to convers with the user with low latency
  - Includes fast transcription

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Benchmark](#benchmark)
- [Comming Soon](#license)
- [License](#license)
- [Credits](#credits)
- [Contact](#contact)
- [Join Our Community That Doesnt Exist](#Join-Our-Community-That-Doesnt-Exist)

## Installation
commming in like an hour i got to get some sleep
## Usage
To run this project you can simply run the main file. to run interview mode just uncoment it.
```python
from startup_scripts import main_chat, main_interview


if __name__ == "__main__":
    main_chat() #this will run a chat mode that will interact with the chat but will not respond to you
    #main_interview() # this will not read chat but instead respond to anyone on the stream over mic
```
you may also want to edit the project to better suit your needs. in that case navigate to the startup_scripts.py file.



## Benchmark
The Metrics in this section include the full project including the overhead from running OBS, and Vtube Studio. All of these test were run on GPU and used the phi 3 mini 4k instruct model from microsoft. 

***NOTE: Because I have fully tested response time for reference its between 1 and 2 seconds***

### Time to First token: Interview Mode
| Whisper Model | Precision | Language Model | Quantization | Max. GPU memory | Response Time |
| --- | --- | --- | --- | --- | --- |
| tiny | int8_float16 | Phi-3-mini-4k-instruct | 4-bit | tbd | time tbd |
| tiny | int8_float16 | Phi-3-mini-4k-instruct | 8-bit | tbd | time tbd |
| tiny | int8_float16 | Phi-3-mini-4k-instruct | full | tbd | time tbd |
| distil-large-v3 | int8_float16 | Phi-3-mini-4k-instruct | 4-bit | tbd | time tbd |
| distil-large-v3 | int8_float16 | Phi-3-mini-4k-instruct | 8-bit | tbd | time tbd |
| distil-large-v3 | int8_float16 | Phi-3-mini-4k-instruct | full | tbd | time tbd |

*Executed with CUDA 12.1 on a NVIDIA Laptop RTX 4080 with 12 GB of VRAM.*

### Time to First token: Chat Mode
| Whisper Model | Precision | Language Model | Quantization | Max. GPU memory | Response Time |
| --- | --- | --- | --- | --- | --- |
| tiny | int8_float16 | Phi-3-mini-4k-instruct | 4-bit | tbd | time tbd |
| tiny | int8_float16 | Phi-3-mini-4k-instruct | 8-bit | tbd | time tbd |
| tiny | int8_float16 | Phi-3-mini-4k-instruct | full | tbd | time tbd |
| distil-large-v3 | int8_float16 | Phi-3-mini-4k-instruct | 4-bit | tbd | time tbd |
| distil-large-v3 | int8_float16 | Phi-3-mini-4k-instruct | 8-bit | tbd | time tbd |
| distil-large-v3 | int8_float16 | Phi-3-mini-4k-instruct | full | tbd | time tbd |

*Executed with CUDA 12.1 on a NVIDIA Laptop RTX 4080 with 12 GB of VRAM.*
## Comming Soon

## License
idk how to do A license but all projects used in this use MIT so i think you can do whatver you want cuz i dont care. go nuts
## Credits
- [OpenVoice](https://github.com/myshell-ai/OpenVoice)
- [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)
- All right, put that away sonny.
- you're still here? it's over... go home... go...

## Join Our Community That Doesnt Exist
[Discord](https://discord.gg/gdV6XzNN)
## Contact
