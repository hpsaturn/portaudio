import pyaudio
import wave

CHUNK = 128
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 16000
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "test01.wav"

p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    print p.get_device_info_by_index(i)

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input_device_index=2,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

try:
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
except IOError as ex:
    if ex[1] != pyaudio.paInputOverflowed:
        raise
    print("exception: ")
    data = '\x00' * chunk  # or however you choose to handle it, e.g. return None

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

