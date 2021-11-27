import RPi.GPIO as gpio

from speech import TextToSpeech
from verbal_log import VerbalLog
from log import tlog
from tracking import Tracking
# from state import RunningState, CurrentTaskState, StartTimeState, EndTimeTaskState, DescriptionState

# Ignore warning for now
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

# Map to gpio, follows board format (1 - ...)
# Run 'pinout' on shell in rpi to get mappings.
pin_out = {
    'email': 3,     # GPIO2
    'call': 13,     # GPIO27
    'meeting': 11,   # GPIO2
    'admin': 5,     # GPIO3
    'stop': 7,     # GPIO17
}

timecamp_task_id = {
    'email': 90658387,
    'call': 96440757,
    'meeting': 96440756,
    'admin': 96440755,
}

bounce_ms = 100


class Tia:
    def __init__(self):
        self.recorder = VerbalLog()
        self.speech = TextToSpeech()
        self.tracking = Tracking()

    def rising(self, button_id, task_id):

        tlog("released - button id: " + str(button_id))

        # Reset button so that it can be pressed again.
        gpio.remove_event_detect(button_id)
        gpio.add_event_detect(button_id, gpio.FALLING, callback=lambda x: self.falling(button_id, task_id), bouncetime=bounce_ms)

        # Convert audio to text
        audio_filename = self.recorder.stop_recording()
        converted_text = self.speech.convert(audio_filename)

        tlog('converted text: ' + converted_text)

        # Start timer for job with speech conversion in description
        self.tracking.start(converted_text, task_id)

    def falling(self, button_id, task_id):
        tlog("pressed - button id: " + str(button_id))
        gpio.remove_event_detect(button_id)
        gpio.add_event_detect(button_id, gpio.RISING, callback=lambda x: self.rising(button_id, task_id), bouncetime=bounce_ms)
        self.recorder.start_recording()

    def stop(self):
        self.tracking.stop()

    def run(self):
        gpio.setup(pin_out['email'], gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(pin_out['call'], gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(pin_out['meeting'], gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(pin_out['admin'], gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(pin_out['stop'], gpio.IN, pull_up_down=gpio.PUD_UP)

        gpio.add_event_detect(pin_out['email'], gpio.FALLING,
                              callback=lambda x: self.falling(pin_out['email'], timecamp_task_id['email']),
                              bouncetime=bounce_ms)

        gpio.add_event_detect(pin_out['call'], gpio.FALLING, callback=lambda x: self.falling(pin_out['call'], timecamp_task_id['call']),
                              bouncetime=bounce_ms)

        gpio.add_event_detect(pin_out['meeting'], gpio.FALLING, callback=lambda x: self.falling(pin_out['meeting'], timecamp_task_id['meeting']),
                              bouncetime=bounce_ms)

        gpio.add_event_detect(pin_out['admin'], gpio.FALLING, callback=lambda x: self.falling(pin_out['admin'], timecamp_task_id['admin']),
                              bouncetime=bounce_ms)

        gpio.add_event_detect(pin_out['stop'], gpio.RISING, callback=lambda x: self.stop(), bouncetime=bounce_ms)

        self.recorder.clear_recordings()
        message = input("<< Tia is ready. Press enter to quit >>\n\n")  # Run until someone presses enter

        gpio.cleanup()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tia = Tia()
    tia.run()
