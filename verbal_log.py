import threading
import pyaudio
import wave
import uuid
import os

from log import tlog


class VerbalLog:
    def __init__(self):
        self.is_recording = False
        self.filename = None
        self.p = None
        self.stream = None
        self.chunk = 8192
        self.sample_format = pyaudio.paInt16
        self.channels = 1
        self.fs = 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.sample_format, channels=self.channels, rate=self.fs,
                                  frames_per_buffer=self.chunk, input=True)

        self.frames = []

    def start_recording(self):
        self.is_recording = True

        tlog('Recording')
        t = threading.Thread(target=self.record)
        t.start()

    def stop_recording(self):
        self.is_recording = False
        self.filename = "recordings/recording-" + str(uuid.uuid4()) + ".wav"
        tlog('recording complete')
        tlog('writing to: ' + self.filename)

        try:
            wf = wave.open(self.filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(self.frames))
            wf.close()

            self.frames = []

            return self.filename

        except():
            tlog('an error occurred in stop_recording method')

    def record(self):
        while self.is_recording:
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            self.frames.append(data)

        tlog("stopped VerbalLog thread")

    def clear_recordings(self):
        directory = 'recordings'

        tlog("Clearing old recordings")
        for f in os.listdir(directory):
            os.remove(os.path.join(directory, f))
