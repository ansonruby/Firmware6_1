from actioncable.connection import Connection
from actioncable.subscription import Subscription
from actioncable.message import Message

import time
import os


class WebSocketFuseaccess():
    
    ws_url='ws://192.168.0.30:3000/cable'
    uuid="1234"

    def create_connection(url,uuid,receiver):
        connection = Connection(url=url)
        connection.connect()

        subscription = Subscription(connection, 
            identifier={'channel':'SpeakerNotificationsChannel','uuid':uuid}
        )

        subscription.on_receive(callback=receiver)
        subscription.create()
        return connection,subscription

    def close_connection(connection,subscription):
        subscription.remove()
        connection.disconnect()

    def on_msg(msg):
        print(msg)
        mytext =  msg['message']
        language = 'es'
        tld='com.mx'
        myobj = gTTS(text=mytext, lang=language,tld=tld, slow=False)
        file_name="tmp/voz_"+str(int(time.time()))+".mp3"
        myobj.save(file_name)
        os.system("cvlc --play-and-exit "+file_name )
        os.remove(file_name)

