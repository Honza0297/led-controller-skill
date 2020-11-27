from mycroft import MycroftSkill, intent_handler
import paho.mqtt.client as paho
from adapt.intent import IntentBuilder

class LedController(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.broker = "192.168.0.105"
        self.port = 1883
        self.client = paho.Client("LEDController")
        self.client.username_pw_set("jaberan", "temderku5j")

#        self.client.on_publish = on_publish  # assign function to callback
        self.client.connect(self.broker, self.port)  # establish connection
    
#    @intent_file_handler('controller.led.intent')
#    def handle_controller_led(self, message):
#        self.speak_dialog('controller.led')

    @intent_handler(IntentBuilder("").require("StateKeyword").require("LEDKeyword"))	
    def handle_turning_on_off(self, message):
        led = message.data.get("LEDKeyword")
        value = message.data.get("StateKeyword") 
        if led  == "room":
            if value == "on":
                value = 100
            else:
                value = 0
        self.client.reconnect()
        led_topic = "dimmer" if led == "room" else "rgbled"
        self.client.publish("home/livingroom/{}".format(led_topic),value)
        self.speak_dialog("success", {"LED":led, "state":value})
     
    @intent_handler(IntentBuilder("").require("LEDKeyword").require("ColorKeyword"))
    def handle_color_change(self, message):
        led = message.data.get("LEDKeyword")
        if led == "room":
            return # TODO ohlasit, ze tahle nema barvicky
        color = message.data.get("ColorKeyword")
        self.client.reconnect()
        self.client.publish("home/livingroom/rgbled", color)
        self.speak_dialog("success", {"LED": led, "state":color})

    def shutdowm(self):
        self.client.disconnect()

def create_skill():
    return LedController()

