from lib.Lib_Settings import Get_Mod_Speaker, Set_Rele
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
        prio = 1
        if "priority" in msg:
            prio = msg["priority"]
        for i in range(int(prio)):
            Set_Rele('Access granted-E')
            time.sleep(1)
        # Set_File(self.Salida_COM_RELE,'Access granted-E')


ws = WSSpeaker()
next_reconection_time = time.time() + int(CONFIG_SPEAKER["Tiempo_Reset_WS"])
ws.create_connection()
while True:
    ws.send_message("check_connection", {})
    time.sleep(1)
    if ws.connection and ws.subscription:
        time_now = time.time()
        if time_now > next_reconection_time:
            ws.close_connection()
            next_reconection_time = time_now + \
                int(CONFIG_SPEAKER["Tiempo_Reset_WS"])
    else:
        ws.create_connection()
