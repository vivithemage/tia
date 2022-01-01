from timecamp import TimecampApi
from log import tlog
from indicators import tracking_led_on, tracking_led_off


class Tracking:
    def __init__(self):
        self.timecamp = TimecampApi()
        self._active = False
        self._entry_id = None

    def is_active(self):
        return self._active

    def stop(self):
        tlog("Stop request (either button or start)")
        tracking_led_off()
        self.timecamp.stop_timer()
        self._active = False

    def start(self, description, task_id):
        self._active = True
        tlog("starting to track job id: " + str(task_id))
        tracking_led_on()
        self._entry_id = self.timecamp.start_timer(task_id)
        self.timecamp.set_description(self._entry_id, description)
        tlog('Entry id: ' + str(self._entry_id))
