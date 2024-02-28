from lib.Lib_Settings import Get_Mod_Speaker
from lib.Lib_WS import WebSocketFuseaccess
from gtts import gTTS
from threading import Thread
import subprocess
import time
import os
import time

CONFIG_SPEAKER = Get_Mod_Speaker()
if not "Tiempo_Reset_WS" in CONFIG_SPEAKER:
    CONFIG_SPEAKER["Tiempo_Reset_WS"] = "120"

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def speak(text):
    language = 'es'
    tld = 'com.mx'
    myobj = gTTS(text=text, lang=language, tld=tld,
                 slow=False, lang_check=False)
    tmp_path = CURRENT_DIR_PATH + "/tmp"
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    file_name = tmp_path + "/voz_" + str(int(time.time() * 1000)) + ".mp3"
    myobj.save(file_name)
    subprocess.call(["cvlc", "--alsa-audio-device", "hw:1,0", "--play-and-exit", file_name],
                    stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
    os.remove(file_name)


class WSSpeaker(WebSocketFuseaccess):
    speak_threads = [Thread(args=("",))]

    def on_message(self, msg):
        text = msg['message']
        speak_thread = self.speak_threads.pop()
        if speak_thread and speak_thread.is_alive() and text != speak_thread._Thread__arg[0]:
            self.speak_threads.append(speak_thread)
            return

        new_speak_thread = Thread(target=speak, args=(text,))
        new_speak_thread.daemon = True
        new_speak_thread.start()
        self.speak_threads.append(new_speak_thread)


ws = WSSpeaker()
next_reconection_time = time.time() + int(CONFIG_SPEAKER["Tiempo_Reset_WS"])
while True:
    try:
        time.sleep(0.5)
        if ws.connection and ws.connection.connected and ws.subscription:
            time_now = time.time()
            if time_now > next_reconection_time:
                ws.close_connection()
                next_reconection_time = time_now + \
                    int(CONFIG_SPEAKER["Tiempo_Reset_WS"])
        else:
            ws.close_connection()
            ws.create_connection()
            time.sleep(15)
    except Exception as e:
        print(e)
