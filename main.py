from startup_scripts import main_interview_non_legacy, main_chat_twitch_non_legacy, main_chat_youtube_non_legacy
#_______SETUP_______#
CHAT_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct" # the model you want to use to find models go to https://huggingface.co/models
CHAT_VTUBER_NAME = "The_Vtuber_name" #the name for your Vtuber
TWITCH_OAUTH = "oauth:zaco5qix5486kmjvswipun1wauq483"# the Oauth_token can be found here: twitchapps.com/tmi
TWITCH_CHANEL = "Your_channel_name" # this is the name of your twitch channel
YOUR_NAME = "your_name" # this is the name you want to be called by the AI (only used in interview mode)
HUGGING_FACE_TOKEN = "" # this is only nessisary if you are downloading gated models on hugging face


def run_option(option):

    if option == 1:
        print("Starting YouTube Chat mode...")
        main_chat_youtube_non_legacy(CHAT_MODEL, CHAT_VTUBER_NAME,)
    elif option == 2:
        print("Starting Twitch Chat mode...")
        main_chat_twitch_non_legacy(CHAT_MODEL, CHAT_VTUBER_NAME,TWITCH_OAUTH,TWITCH_CHANEL)
    elif option == 3:
        print("Starting Interview mode...")
        main_interview_non_legacy(CHAT_MODEL, CHAT_VTUBER_NAME, YOUR_NAME)
    else:
        print("Invalid option selected!")

def main():
    print("Choose an option to run:")
    print("1. YouTube Chat")
    print("2. Twitch Chat")
    print("3. Interview")

    try:
        option = int(input("Enter the number of your choice: "))
        run_option(option)
    except ValueError:
        print("Invalid input! Please enter a number.")

if __name__ == "__main__":
    main()
