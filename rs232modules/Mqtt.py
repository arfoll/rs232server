import jsonpickle
import paho.mqtt.client as mqtt
from threading import Thread
from typing import Callable, Dict

class comm:
    def __init__(self, broker_address):
        self.client = mqtt.Client("rs232server")
        self.client.on_message = self.on_message
        self.callbacks = dict()
        self.client.connect(broker_address)
        Thread(target=self.__run, daemon=True).start()

    def __run(self):
        self.client.loop_forever()

    def on_message(self, client, userdata, msg):
        self.callbacks[msg.topic](msg.topic, msg.payload)

    def on_connect(self, client, userdata, flags, rc):
        for topic in self.callbacks:
            self.client.subscribe(topic)

    def register_handler(self, topic: str, service: str, handler: Callable[[Dict], None]):
        self.callbacks[topic] = handler
        self.client.subscribe(topic)
