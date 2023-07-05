from lib.Lib_WS import WebSocketFuseaccess
from gtts import gTTS
import subprocess
import time
import os

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class WSSpeaker(WebSocketFuseaccess):
    def on_message(self, msg):
        print(msg)
        mytext = msg['message']
        language = 'es'
        tld = 'com.mx'
        myobj = gTTS(text=mytext, lang=language, tld=tld, slow=False)
        tmp_path = CURRENT_DIR_PATH+"/tmp"
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)
        file_name = tmp_path+"/voz_"+str(int(time.time()*1000))+".mp3"
        myobj.save(file_name)
        subprocess.run(["cvlc","--play-and-exit",file_name])
        os.remove(file_name)


ws = WSSpeaker()

while True:
    ws.create_connection()
    time.sleep(1*1)
    ws.send_message(
        "recive_data", {"uuid": "a0c58953859a", "message": "ayyy migue e e el"})
    time.sleep(1*60)
    ws.close_connection()
