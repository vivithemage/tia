import speech_recognition as sr
from log import tlog


class TextToSpeech:
    def __init__(self):
        # initialize the recognizer
        self.recognizer = sr.Recognizer()

    def convert(self, filename):
        tlog("converting")
        try:
            with sr.AudioFile(filename) as source:
                # listen for the data (load audio to memory)
                audio_data = self.recognizer.record(source)

                # recognize (convert from speech to text)
                text = self.recognizer.recognize_google(audio_data)

                return text
        # Sometimes occurs, I think it's if the speech is bad quality and there is difficulty converting.
        # see: https://stackoverflow.com/questions/56359106/speech-recognition-unknownvalueerror
        except:
            return 'error running voice to text'
