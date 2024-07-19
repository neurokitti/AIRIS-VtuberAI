from obswebsocket import obsws, requests
import obswebsocket

class OBS_engine:
    # the OBS Engine handles passing information between the Vtuber AI and the OBS Websocket
    def __init__(self,password,port=4444,host="localhost"):
        # connects to the OBS Websocket
        print("Connecting to OBS Websocket...")
        self.ws = obsws(host, port, password)
        try:
            self.ws.connect()
            print("connected!")
        except:
            print("Failed to connect to OBS! prosseading without OBS Module.")
    def OBS_Wrapper(function): 
        #this wraps the OBS functions to automaticly handle when OBS is not open.
        def wrapper(*args, **kwargs):
            try:
                function(*args, **kwargs)
            except:
                print("OBS was unable to connect! check that OBS is open and has the websocket extention!")
        return wrapper
    @OBS_Wrapper
    def update_browser_source(self,id,source_name="chat"):
        # this function updates a browser source titled "chat" by default, it updates it with the youtube chat from the link provided by the user from instantiating the youtube Engine
        source_name=source_name
        settings = {
            "url": f"https://studio.youtube.com/live_chat?is_popout=1&v={id}"
        }
        self.ws.call(requests.SetSourceSettings(sourceName=source_name, sourceSettings=settings))
    @OBS_Wrapper
    def update_text(self,text,source_name="TextSource"):
        #this will update the captions, this requires you to have a text source titled "TextSource" by default
        self.ws.call(requests.SetTextGDIPlusProperties(source=source_name, text=text))