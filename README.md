# Airis: Local Vtuber AI 

**Airis-VtuberAI** is a open source attempt to recreate the populer Vtuber "Neuro Sama". The project utilises no APIs and can run entirely localy without a need for an internet connection or considerable Vram.

the project includes the ability to transcribe the users voice, generate a response, and synthisise a text2speach output with as litle latency as resonable posible while sacraphising as little quality as posible. 

## Features
- **Feature 1: Chat Mode**
  - Allows the Vtuber AI to read and respond to chat messages
  - Interacts with OBS to include Subtitles and updated chat
  - lower VRAM
- **Feature 2: Interview Mode**
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

## Credits

## Contact
