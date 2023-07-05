from lib.Lib_Settings import Get_Mod_Speaker
from lib.Lib_WS import WebSocketFuseaccess
from gtts import gTTS
import subprocess
import time
import os

CONFIG_SPEAKER = Get_Mod_Speaker()
if not "Tiempo_Reset_WS" in CONFIG_SPEAKER:
    CONFIG_SPEAKER["Tiempo_Reset_WS"] = "120"

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
        subprocess.run(["cvlc", "--play-and-exit", file_name])
        os.remove(file_name)


ws = WSSpeaker()

while True:
    ws.create_connection()
    time.sleep(int(CONFIG_SPEAKER["Tiempo_Reset_WS"]))
    ws.close_connection()
