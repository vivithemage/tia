import threading
from threading import Thread
import time
import random

intervals = [1, 2, 3, 4, 5, 6, 7, 8]

class SharedData:
    def __init__(self):
        self._running = False,
        self._current_task_id = 'unknown',
        self._start_time = None,
        self._end_time = None
        self._thread_lock = threading.Lock()

    def set_running(self):
        with self._thread_lock:
            self._running = True

    def set_stopped(self):
        with self._thread_lock:
            self._running = False


    def set_current_task_id(self, task_id):
        with self._thread_lock:
            self._current_task_id = task_id

global_data = SharedData()


def start_state():
    time.sleep(random.choice(intervals))
    print("setting running state to True")
    global_data.set_running()

def stop_state():
    time.sleep(random.choice(intervals))
    print("setting running state to False")
    global_data.set_stopped()


t = Thread(target=start_state)
t2 = Thread(target=stop_state)

t.start()
print (global_data._running)


t2.start()
print (global_data._running)

