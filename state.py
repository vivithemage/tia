import threading
from log import tlog


class SharedState:
    def __init__(self, initial_value='unset'):
        self._value = initial_value
        self._value_lock = threading.Lock()

    def set(self, value):
        with self._value_lock:
            tlog("setting state to: " + str(value))
            self._value = value

    def get(self):
        with self._value_lock:
            return self._value


class RunningState(SharedState):
    pass


class CurrentTaskState(SharedState):
    pass


class AudioFileNameState(SharedState):
    pass


class DescriptionState(SharedState):
    pass


class ButtonIdState(SharedState):
    pass
