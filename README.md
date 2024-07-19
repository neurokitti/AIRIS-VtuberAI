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

## Installation

## Usage

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
- All right, put that away sonny.
- you're still here? it's over, go home, go.
## Contact
