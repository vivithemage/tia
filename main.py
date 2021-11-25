import RPi.GPIO as gpio
import threading
import pyaudio
import wave
import random
import uuid

from speech import TextToSpeech

# Ignore warning for now
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)


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

        print('Recording')
        t = threading.Thread(target=self.record)
        t.start()

    def stop_recording(self):
        self.is_recording = False
        self.filename = "recordings/recording-" + str(uuid.uuid4()) + ".wav"
        print('recording complete')
        print('writing to: ' + self.filename)

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
            print('an error occurred')

    def record(self):
        while self.is_recording:
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            self.frames.append(data)

        print("stopped thread")


class Tia:
    def __init__(self):
        self.recorder = VerbalLog()
        self.speech = TextToSpeech()

    def rising(self, channel):
        print("released")
        gpio.remove_event_detect(3)
        gpio.add_event_detect(3, gpio.FALLING, callback=self.falling, bouncetime=100)
        audio_filename = self.recorder.stop_recording()
        converted_text = self.speech.convert(audio_filename)

        print(converted_text)

    def falling(self, channel):
        print("pressed")
        gpio.remove_event_detect(3)
        gpio.add_event_detect(3, gpio.RISING, callback=self.rising, bouncetime=100)
        self.recorder.start_recording()

    def run(self):
        print("starting tia...")
        gpio.setup(3, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.add_event_detect(3, gpio.FALLING, callback=self.falling, bouncetime=100)

        message = input("Press enter to quit\n\n")  # Run until someone presses enter

        gpio.cleanup()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tia = Tia()
    tia.run()
