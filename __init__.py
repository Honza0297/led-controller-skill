from mycroft import MycroftSkill, intent_file_handler
import paho.mqtt.client as paho
from adapt.intent import IntentBuilder

class LedController(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.broker = "192.168.0.105"
        self.port = 1883
        self.client = paho.Client("LEDController")
        self.client.username_pw_set("jaberan", "temderku5j")

        self.client.on_publish = on_publish  # assign function to callback
        self.client.connect(self.broker, self.port)  # establish connection
    
    @intent_file_handler('controller.led.intent')
    def handle_controller_led(self, message):
        self.speak_dialog('controller.led')

    @intent_handler(IntentBuilder("").require("StateKeyword").require("LEDKeyword"))	
    def handle_turning_on_off(self, message):
        self.client.reconnect()
        self.client.publish("home/livingroom/dimmer", "on")

    def shutdowm(self):
        self.client.disconnect()

def create_skill():
    return LedController()

