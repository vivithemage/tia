import threading
from log import tlog


class SharedState:
    def __init__(self, initial_value='unset'):
        self._value = initial_value
        self._value_lock = threading.Lock()
        self._note = 'unknown'

    def set_note(self):
        self._note = 'unknown'

    def set(self, value):
        with self._value_lock:
            tlog("setting state (" + self._note + ") to: " + str(value))
            self._value = value

    def get(self):
        with self._value_lock:
            return self._value


class RunningState(SharedState):
    def set_note(self):
        self._note = 'RunningState'
    pass


class CurrentTaskState(SharedState):
    def set_note(self):
        self._note = 'CurrentTaskState'
    pass


class AudioFileNameState(SharedState):
    def set_note(self):
        self._note = 'AudioFileNameState'
    pass


class DescriptionState(SharedState):
    def set_note(self):
        self._note = 'DescriptionState'
    pass


class ButtonIdState(SharedState):
    def set_note(self):
        self._note = 'ButtonIdState'
    pass
