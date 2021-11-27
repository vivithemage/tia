import RPi.GPIO as gpio

from speech import TextToSpeech
from verbal_log import VerbalLog
from log import tlog
from tracking import Tracking
# from state import RunningState, CurrentTaskState, StartTimeState, EndTimeTaskState, DescriptionState

# Ignore warning for now
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)


class Tia:
    def __init__(self):
        self.recorder = VerbalLog()
        self.speech = TextToSpeech()
        self.tracking = Tracking()

    def rising(self, button_id):

        tlog("released - button id: " + str(button_id))

        # Reset button so that it can be pressed again.
        gpio.remove_event_detect(button_id)
        gpio.add_event_detect(button_id, gpio.FALLING, callback=lambda x: self.falling(button_id), bouncetime=100)

        # Convert audio to text
        audio_filename = self.recorder.stop_recording()
        converted_text = self.speech.convert(audio_filename)

        tlog('converted text: ' + converted_text)
        # Start timer for job with speech conversion in description
        task_category_id = 0
        self.tracking.start(converted_text, task_category_id)

    def falling(self, button_id):
        tlog("pressed - button id: " + str(button_id))
        gpio.remove_event_detect(button_id)
        gpio.add_event_detect(button_id, gpio.RISING, callback=lambda x: self.rising(button_id), bouncetime=100)
        self.recorder.start_recording()

    def run(self):
        gpio.setup(3, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.add_event_detect(3, gpio.FALLING, callback=lambda x: self.falling(3), bouncetime=100)

        self.recorder.clear_recordings()
        message = input("<< Tia is ready. Press enter to quit >>\n\n")  # Run until someone presses enter

        gpio.cleanup()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tia = Tia()
    tia.run()
