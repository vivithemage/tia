import uuid

import RPi.GPIO as gpio

from speech import TextToSpeech
from verbal_log import Recorder
from log import tlog
from tracking import Tracking
from state import RunningState, CurrentTaskState, DescriptionState, ButtonIdState
import time

import glob
import os

# Ignore warning for now
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

# Map to gpio, follows board format (1 - ...)
# Run 'pinout' on shell in rpi to get mappings.
pin_out = {
    'email': 3,  # GPIO2
    'call': 13,  # GPIO27
    'meeting': 11,  # GPIO2
    'admin': 5,  # GPIO3
    'stop': 7,  # GPIO17
    'tracking_led': 23
}

timecamp_task_id = {
    'email': 90658387,
    'call': 96440757,
    'meeting': 96440756,
    'admin': 96440755,
}

bounce_ms = 100


class GlobalState:
    def __init__(self):
        self.running = RunningState()
        self.task = CurrentTaskState()
        self.description = DescriptionState()
        self.button = ButtonIdState()


global_state = GlobalState()


class InputHandler:
    def __init__(self):
        self.recorder = Recorder(channels=1)
        self.speech = TextToSpeech()
        self.tracking = Tracking()
        self.audio_filename = "recordings/recording-" + str(uuid.uuid4()) + ".wav"
        self.recording_file = None
        self.record_time_sec = 5.0

    def init(self):
        tlog('Starting InputHandler thread.')

        # Idle is the state where this loop does nothing so after each action, set it to idle
        while True:
            if global_state.running.get() == 'pressed':
                tlog("pressed task button")

                # Stop existing task if active
                if self.tracking.is_active():
                    self.tracking.stop()

                with self.recorder.open(self.audio_filename, 'wb') as self.recording_file:

                    tlog("start recording")
                    global_state.running.set('recording')
                    self.recording_file = self.recording_file.start_recording()
                    '''
                    TODO - There's a timer placed here because using the stop_recording method outside this method
                    does not work for some reason. For the sake of getting this working, it uses a preset time which
                    blocks the system. Also the buttons I have seem really bad, so this is probably a better 
                    way for now.
                    '''
                    time.sleep(self.record_time_sec)
                    self.recording_file.stop_recording()

                    # Convert audio to text
                    converted_text = self.speech.convert(self.audio_filename)
                    tlog('converted text: ' + converted_text)

                    # Start timer for job with speech conversion in description
                    self.tracking.start(converted_text, global_state.task.get())

            elif global_state.running.get() == 'stop':
                tlog("stopping")
                self.tracking.stop()
                global_state.running.set('idle')


class Tia:
    def __init__(self):
        pass

    # Clear out recordings
    def clear(self):
        # Initializing the Folder Path
        recordings_directory = "recordings"

        # Getting List of All the Files in the Folder
        file_list = glob.glob(recordings_directory + "/*")

        for file in file_list:
            print("Removing {}".format(file))
            os.remove(file)

    def falling(self, button_id, task_id):
        tlog("pressed - button id: " + str(button_id))

        # Set state for monitor to pick up on
        global_state.running.set('pressed')
        global_state.task.set(task_id)
        global_state.button.set(button_id)

    def stop(self):
        tlog("stopping")
        global_state.running.set('stop')

    def run(self):
        # TODO put this in a loop...
        gpio.setup(pin_out['email'], gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(pin_out['call'], gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(pin_out['meeting'], gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(pin_out['admin'], gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(pin_out['stop'], gpio.IN, pull_up_down=gpio.PUD_UP)

        gpio.setup(pin_out['tracking_led'], gpio.OUT)

        gpio.add_event_detect(pin_out['email'], gpio.FALLING,
                              callback=lambda x: self.falling(pin_out['email'], timecamp_task_id['email']),
                              bouncetime=bounce_ms)

        gpio.add_event_detect(pin_out['call'], gpio.FALLING,
                              callback=lambda x: self.falling(pin_out['call'], timecamp_task_id['call']),
                              bouncetime=bounce_ms)

        gpio.add_event_detect(pin_out['meeting'], gpio.FALLING,
                              callback=lambda x: self.falling(pin_out['meeting'], timecamp_task_id['meeting']),
                              bouncetime=bounce_ms)

        gpio.add_event_detect(pin_out['admin'], gpio.FALLING,
                              callback=lambda x: self.falling(pin_out['admin'], timecamp_task_id['admin']),
                              bouncetime=bounce_ms)

        gpio.add_event_detect(pin_out['stop'], gpio.RISING, callback=lambda x: self.stop(), bouncetime=bounce_ms)

        # start monitoring and acting on button state changes
        tlog("Tia is starting up.")
        self.clear()
        # If execution lasts longer than the button press bounce value, it seems to crash.
        # This is the reason for a seperate thread (InputHandler) being used to monitor and act on button/state changes.
        handler = InputHandler()
        handler.init()

        gpio.cleanup()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tia = Tia()
    tia.run()
