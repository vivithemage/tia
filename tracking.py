from timecamp import TimecampApi
from log import tlog
from indicators import tracking_led_on, tracking_led_off


class Tracking:
    def __init__(self):
        self.timecamp = TimecampApi()

    def stop(self):
        tlog("Stop request (either button or start)")
        tracking_led_off()
        self.timecamp.stop_timer()

    def start(self, description, task_id):
        tlog("starting to track job id: " + str(task_id))
        tracking_led_on()
        entry_id = self.timecamp.start_timer(task_id)
        self.timecamp.set_description(entry_id, description)
        tlog('Entry id: ' + str(entry_id))
