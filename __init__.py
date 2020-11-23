from mycroft import MycroftSkill, intent_file_handler


class LedController(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('controller.led.intent')
    def handle_controller_led(self, message):
        self.speak_dialog('controller.led')


def create_skill():
    return LedController()

