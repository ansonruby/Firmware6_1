from actioncable.connection import Connection
from actioncable.subscription import Subscription
from actioncable.message import Message
from lib.Lib_Settings import Get_Rout_server
from lib.Fun_Dispositivo import Get_ID_Dispositivo


class WebSocketFuseaccess():

    def __init__(self):
        url = Get_Rout_server()
        ws_url = url.replace("http", "ws", 1) + "/cable"
        self.ws_url = ws_url
        self.uuid = Get_ID_Dispositivo()

    def create_connection(self):
        connection = Connection(url=self.ws_url)
        connection.connect()

        subscription = Subscription(connection,
                                    identifier={
                                        'channel': 'SpeakerNotificationsChannel', 'uuid': self.uuid}
                                    )

        subscription.on_receive(callback=self.on_message)
        subscription.create()
        self.connection = connection
        self.subscription = subscription

    def close_connection(self):
        if self.connection and self.subscription:
            self.subscription.remove()
            self.connection.disconnect()
            self.subscription = None
            self.connection = None

    def send_message(self, action, data):
        if self.connection.connected and self.subscription:
            message = Message(action=action, data=data)
            self.subscription.send(message)
            return True

    def on_message(self, msg):
        pass
