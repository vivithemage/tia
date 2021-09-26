import datetime
import time

from log import tlog
from timecamp import TimecampApi

# import thread

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

global_state = {
    'running': False,
    'current_task': 'unknown',
    'start_time': None,
    'end_time': None
}


class Tasks:
    def pull(self):
        tlog("pulling all tasks")
        api = TimecampApi()
        tasks = api.get_tasks()

    def populate(self):
        tlog("populating tasks")

    def get_id(self, name):
        tlog("getting id based on name")


class Buttons:
    def setup(self):
        tlog("running Button Setup...")
        # Map to gpio, follows board format (1 - ...)
        # Run 'pinout' on shell in rpi to get mappings.
        pin_out = {
            'email': 3,
            'call': 13,
            'meeting': 11,
            'admin': 5,
            'stop': 7,
        }

        # Set pins for each button
        for pin in pin_out:
            GPIO.setup(pin_out[pin], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Setup event for each button on rising pin
        GPIO.add_event_detect(pin_out['email'], GPIO.RISING, callback=start_email, bouncetime=3000)
        GPIO.add_event_detect(pin_out['call'], GPIO.RISING, callback=start_call, bouncetime=3000)
        GPIO.add_event_detect(pin_out['meeting'], GPIO.RISING, callback=start_meeting, bouncetime=3000)
        GPIO.add_event_detect(pin_out['admin'], GPIO.RISING, callback=start_admin, bouncetime=3000)
        GPIO.add_event_detect(pin_out['stop'], GPIO.RISING, callback=stop_tracking, bouncetime=3000)


# TODO: Initialize led's for notifications
class Indicators:
    def setup(self):
        GPIO.setup(23, GPIO.OUT)
        GPIO.output(23, GPIO.LOW)

    def running(self):
        tlog("Led 2 (red) on indicating task running")
        GPIO.setup(23, GPIO.OUT)
        GPIO.output(23, GPIO.HIGH)

    def not_running(self):
        tlog("Led 2 (red) off indicating no task is active")
        GPIO.setup(23, GPIO.OUT)
        GPIO.output(23, GPIO.LOW)

    def ready(self):
        tlog("Led 1 (green) on indicating ready for input")

    def booting(self):
        tlog("Led 1 (green) is off")


class Tracking:
    def __init__(self):
        self.timecamp = TimecampApi()
        self.indicators = Indicators()

    def _task_running(self):
        if global_state['running'] is True:
            tlog("a task is running")
            return True

    def _get_current_time(self):
        today = datetime.datetime.now()
        time_string = today.strftime("%H:%M:%S")
        tlog(time_string)

        return time_string

    def stop(self):
        tlog("Stop request (either button or start)")

        self.indicators.not_running()
        self.timecamp.stop_timer()

    def start(self, task_name):
        tlog(task_name + " button was pushed.")

        indicators = Indicators()
        indicators.running()

        tlog("starting to track " + task_name)
        global_state['running'] = True
        global_state['current_task'] = task_name
        global_state['start_time'] = self._get_current_time()

        tlog("startinggg")
        self.timecamp.start_timer()


# Start Triggers TODO - change this to a single function by padding argument 
# in event trigger
def start_email(channel):
    t = Tracking()
    t.start('email')


def start_admin(channel):
    t = Tracking()
    t.start('admin')


def start_call(channel):
    tlog("call running base")
    # time.sleep(2)
    t = Tracking()
    t.start('call')


def start_meeting(channel):
    t = Tracking()
    t.start('meeting')


# Stop tracking and save to timecamp
def stop_tracking(channel):
    t = Tracking()
    t.stop()


def tia():
    tlog("starting tia...")

    buttons = Buttons()
    indicators = Indicators()
    # tasks = Tasks()

    tlog("Initializing buttons...")
    buttons.setup()

    tlog("Initializing notification LED's...")
    indicators.setup()

    # tlog("Populating tasks...")
    # # tasks.populate()
    #
    # tlog("Ready!")
    # led.ready()

    message = input("Press enter to quit\n\n")  # Run until someone presses enter

    GPIO.cleanup()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tia()
