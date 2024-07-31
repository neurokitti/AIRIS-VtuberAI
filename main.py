from startup_scripts import main_interview_non_legacy, main_chat_twitch_non_legacy, main_chat_youtube_non_legacy
import utils
#_______SETUP_______#
CHAT_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct" # the model you want to use to find models go to https://huggingface.co/models
CHAT_VTUBER_NAME = "Hannah" #the name for your Vtuber REMMEBER TO ALSO UPDATE THE SYSTEM_MESSAGE.TXT FILE AS WELL!
TWITCH_OAUTH = "Your_twitch_Oauth_token"# the Oauth_token can be found here: twitchapps.com/tmi
TWITCH_CHANEL = "neuro_kitti" # this is the name of your twitch channel
YOUR_NAME = "Bill Lumbergh" # this is the name you want to be called by the AI (only used in interview mode)
HUGGING_FACE_TOKEN = "your_hugging_face_token" # this is only nessisary if you are downloading gated models on hugging face. (find it in the hugging face settings)
BANNED_WORDS = utils.get_dict_from_txt('OpenVoice/test.txt')
print(BANNED_WORDS)
USE_DEFAULT_PROFANITY_LIST = True # there are default profanity words as part of the filter if you set this to true it will just add your blacklist to its own but if set to False the censor list will just include your words
def main():
    print("Choose an option to run:")
    print("1. YouTube Chat")
    print("2. Twitch Chat")
    print("3. Interview")
    option = int(input("Enter the number of your choice: "))

    if option == 1:
        print("Starting YouTube Chat mode...")
        main_chat_youtube_non_legacy(CHAT_MODEL, CHAT_VTUBER_NAME,BANNED_WORDS,USE_DEFAULT_PROFANITY_LIST,HUGGING_FACE_TOKEN)
    elif option == 2:
        print("Starting Twitch Chat mode...")
        main_chat_twitch_non_legacy(CHAT_MODEL, CHAT_VTUBER_NAME,TWITCH_OAUTH,TWITCH_CHANEL,BANNED_WORDS,USE_DEFAULT_PROFANITY_LIST,HUGGING_FACE_TOKEN)
    elif option == 3:
        print("Starting Interview mode...")
        main_interview_non_legacy(CHAT_MODEL, CHAT_VTUBER_NAME,YOUR_NAME,BANNED_WORDS,USE_DEFAULT_PROFANITY_LIST,HUGGING_FACE_TOKEN)
    else:
        print("Invalid option selected!")

if __name__ == "__main__":
    main()
