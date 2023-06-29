from lib.Lib_WS import WebSocketFuseaccess
from gtts import gTTS
import time

wsf = WebSocketFuseaccess()

while True:
    connection, subscription = wsf.create_connection()
    time.sleep(1*60)
    wsf.close_connection(connection, subscription)
