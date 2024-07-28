from threading import Thread
import pytchat
import re


class youtube_engine:
    def __init__(self,):
        self.ID = None
        self.messages = []
        while True:
            self.url = input("Live Stream LINK: ")
            self.ID = self.extract_youtube_id(self.url)
            if self.ID != "":
                break
            else:
                print("Extraction failed! please try again! consider just providing the stream ID!")
        print("ID:", self.ID)
        self.chat = pytchat.create(video_id=str(self.ID))
        #OBS_engine.update_browser_source(self.ID)
    def extract_youtube_id(self, url):
        pattern = re.compile(r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/|v/|shorts/|live/|video/)|youtu\.be/|youtube\.com/shorts/|youtube\.com/live/|youtube\.com/clip/)([a-zA-Z0-9_-]{11})')
        match = pattern.search(url)
        if match:
            return match.group(1)
        else:
            return ""
    def chat_streamer_thread(self):
        while self.chat.is_alive():
            for c in self.chat.get().sync_items():
                #print(f"{c.author.name}: {c.message}")
                dict_messge = {'role':'user', 'name':c.author.name, 'text':c.message}
                self.messages.append(dict_messge)
    def message_compiler(self,):
        print("first conntact")
        yt_thread = Thread(target=self.chat_streamer_thread)
        print("second conntact")
        yt_thread.start()
        print("third conntact")

    def get_messages(self,):
        return self.messages