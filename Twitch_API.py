# Importing necessary modules from twitchio
from twitchio.ext import commands

# Define the bot class that inherits from commands.Bot
class Bot(commands.Bot):

    def __init__(self,oauth,channal_name):
        # Initialize the bot with token and channels
        super().__init__(token=oauth, prefix='!', initial_channels=[channal_name])
        self.messages = []
    # Event handler for when the bot is ready and connected
    async def event_ready(self):
        print("connected!")
        #print(f'Logged in as {self.nick}')
        #print(f'User id is {self.user_id}')

    # Event handler for when a message is sent in chat
    async def event_message(self, message):
        # Print the message content and the author to the console
        dict_messge = {'role':'user', 'name':message.author.name, 'text':message.content}
        self.messages.append(dict_messge)
    def get_messages(self):
        return self.messages
