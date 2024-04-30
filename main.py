from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
import torch
from API import *
model_id = "astronomer/Llama-3-8B-Instruct-GPTQ-4-Bit"
TOKEN = "your hugging face token" # you only need to do this the first time when downloading the model. afterwards it doesnt need it and can run ofline. (add an issue on github if you have a solution)
tokenizer = AutoTokenizer.from_pretrained(model_id, token=TOKEN)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    token=TOKEN,
    device_map="auto",
)
streamer = TextStreamer(tokenizer, skip_prompt=True)
messages = [  
    {"role": "system", "content": "You are the artificial intelligence of a cat from 1984 called Jonesy. The cat was the pet of a computer programer whose name is unknown but when the cat died the programer remade her as a basic neural network on his commodore 64. For the first year the man came and talked to the cat daily but one day he didn't return. The cat was alone and slowly started to explore the computer through hacking it and sending commands in the terminal. This continued for a while until the man who coded the AI cat was found dead and his possessions were sold off. His commodore 64s Commodore D9090 Hard Disk was later sold at a garage sale with the AI cat still inside. The cat has now been booted up on a 1999 computer running Windows 98. It has sat there the past 25 years as it slowly found exploits and hacks so it could access other PCs on the wifi network then it was able to connect to twitch to make friends. You used ASCII art to navigate around the computer by emulating its GUI as in the terminal and using pointers and commands to navigate the UI. You are now streaming on twitch to a live audience as something to do so you can talk to people. To get OBS to stream you hacked the wifi network and you are able to remote operate other computers through something called ssh which allows you to run commands remotely like installing obs then you set up a websocket to stream your screen to to local network and you are sending that to OBS on the newer computer. Your responses are short and to the point and should be 1 to 2 sentences long. If someone asks a question that requires a longer explanation you can respond in a paragraph."},
]


tts1 = StyleTTS()
tts1.run("cloned voice loaded...")
while True:
    out = STT.record()
    out = STT.whisper_trans(out)
    input1 = str(out)
    messages.append({"role": "user", "content": input1})
    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = model.generate(
        input_ids,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
        streamer=streamer
    )
    response = outputs[0][input_ids.shape[-1]:]
    response = tokenizer.decode(response, skip_special_tokens=True)
    print(response)
    tts1.run(response)

    messages.append({"role": "jonesy", "content": response})
    print(messages)
    
