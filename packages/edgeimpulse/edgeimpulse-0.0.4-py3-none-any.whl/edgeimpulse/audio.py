
import numpy as np
import pyaudio
import time
from six.moves import queue
from edgeimpulse.runner import ImpulseRunner as ImpulseRunner

CHUNK_SIZE = 1024
OVERLAP = 0.25

def now():
    return round(time.time() * 1000)

class Microphone():
    def __init__(self, rate, chunk_size):
        self.buff = queue.Queue()
        self.chunk_size = chunk_size
        self.data = []
        self.rate = rate
        self.closed = True

    def __enter__(self):
        self.interface = pyaudio.PyAudio()
        self.stream = self.interface.open(
            format = pyaudio.paInt16,
            channels = 1,
            rate = self.rate,
            input = True,
            frames_per_buffer = self.chunk_size,
            stream_callback = self.fill_buffer
        )
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self.stream.stop_stream()
        self.stream.close()
        self.closed = True
        self.interface.terminate()

    def fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self.buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self.buff.get()

            if chunk is None:
                return

            data = [chunk]

            while True:
                try:
                    chunk = self.buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

class AudioImpulseRunner(ImpulseRunner):
    def __init__(self, model_path: str):
        super(AudioImpulseRunner, self).__init__(model_path)
        self.closed = True
        self.sampling_rate = 0
        self.window_size = 0
        self.labels = []


    def init(self):
        model_info = super(AudioImpulseRunner, self).init()
        if model_info['model_parameters']['frequency'] == 0:
            raise Exception('Model file "' + self._model_path + '" is not suitable for audio recognition')

        self.window_size = model_info['model_parameters']['input_features_count']
        self.sampling_rate = model_info['model_parameters']['frequency']
        self.labels = model_info['model_parameters']['labels']

        return model_info

    def __enter__(self):
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self.closed = True

    def classify(self):
        with Microphone(self.sampling_rate, CHUNK_SIZE) as mic:
            generator = mic.generator()
            features = np.array([], dtype=np.uint16)
            for audio in generator:
                if not self.closed:
                    break
                data = np.frombuffer(audio, dtype=np.uint16)
                features = np.concatenate((features, data), axis=0)
                while len(features) >= self.window_size:
                    begin = now()
                    res = super(AudioImpulseRunner, self).classify(features[:self.window_size].tolist())
                    features = features[int(self.window_size * OVERLAP):]
                    yield res
