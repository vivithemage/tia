"""
python3 -m sounddevice

{'index': 1, 'structVersion': 2, 'name': 'USB Audio Device: - (hw:1,0)', 'hostApi': 0, 'maxInputChannels': 1, 'maxOutputChannels': 2, 'defaultLowInputLatency': 0.008684807256235827, 'defaultLowOutputLatency': 0.008707482993197279, 'defaultHighInputLatency': 0.034829931972789115, 'defaultHighOutputLatency': 0.034829931972789115, 'defaultSampleRate': 44100.0}


https://python-sounddevice.readthedocs.io/en/0.3.14/examples.html#recording-with-arbitrary-duration
"""


import pyaudio
import wave

# Record in chunks of 1024 samples
chunk = 256

# 16 bits per sample
sample_format = pyaudio.paInt16
chanels = 1

# Record at 44400 samples per second
smpl_rt = 44100
seconds = 4
filename = "path_of_file.wav"

# Create an interface to PortAudio
pa = pyaudio.PyAudio()

stream = pa.open(format=sample_format, channels=chanels,
                 rate=smpl_rt, input=True,
                 frames_per_buffer=chunk)

print('Recording...')

# Initialize array taht be used for storing frames
frames = []

# Store data in chunks for 8 seconds

for i in range(0, int(smpl_rt / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

# Stop and close the stream
stream.stop_stream()
stream.close()

# Terminate - PortAudio interface
pa.terminate()

print('Done !!! ')

# Save the recorded data in a .wav format
sf = wave.open(filename, 'wb')
sf.setnchannels(chanels)
sf.setsampwidth(pa.get_sample_size(sample_format))
sf.setframerate(smpl_rt)
sf.writeframes(b''.join(frames))
sf.close()
