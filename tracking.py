from timecamp import TimecampApi
from log import tlog


class Tracking:
    def __init__(self):
        self.timecamp = TimecampApi()

    def stop(self):
        tlog("Stop request (either button or start)")
        self.timecamp.stop_timer()

    def start(self, description, task_category_id):
        tlog("starting to track job id: " + str(task_category_id))
        entry_id = self.timecamp.start_timer(task_category_id)
        print(entry_id)
