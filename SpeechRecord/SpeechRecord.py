import pyaudio
import math
import struct
import wave
import time
import os
import requests
from enum import Enum
import GoodreadsService

Threshold = 50           #optimal val = 50, set to 500 for debug

speechToTexEndpoint = 'http://localhost:5000/getText'
SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2
serv = GoodreadsService.GoodreadsService()

TIMEOUT_LENGTH = 5

class Command(Enum):
    AddBook = 1
    RemoveBook = 2
    AddComment = 3

dir_path = os.path.dirname(os.path.realpath(__file__))
f_name_directory = dir_path + r'\records'
print(f_name_directory)
class Recorder:

    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)

    def record(self):
        print('Noise detected, recording beginning')
        rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH

        while current <= end:

            data = self.stream.read(chunk)
            if self.rms(data) >= Threshold: end = time.time() + TIMEOUT_LENGTH

            current = time.time()
            rec.append(data)
        self.write(b''.join(rec))

    def postToTransformService(self, filepath):
        #self.playAudio(filepath);
        sppechFile = open(filepath, 'rb');
        data = {'file': sppechFile};
        r = requests.post(url=speechToTexEndpoint, files=data);

        response = r.text;
        print(response);
        if response == Command.AddBook.name :
            userInput = input('Please print the name of the book: ').split(" ")
            serv.addBook(userInput)
        elif response == Command.AddComment.name : 
            bookName = input('Please print the name of the book: ').split(" ")
            bookId = serv.getBookId(bookName)
            review = input('Please print the review of the book: ')
            serv.addReview(bookName, bookId, review)
        elif response == Command.RemoveBook.name :  
            userInput = input('Please print the name of the book: ').split(" ")
            serv.removeBook(userInput)

    def write(self, recording):
        n_files = len(os.listdir(f_name_directory))

        filename = os.path.join(f_name_directory, '{}.wav'.format(n_files))

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        print('Written to file: {}'.format(filename))
        print('Returning to listening')
        self.postToTransformService(filename);

        return filename;

    def playAudio(self, filepath):

        wf = wave.open(filepath, 'rb')

        # create an audio object
        p = pyaudio.PyAudio()

        # open stream based on the wave object which has been input.
        stream = p.open(format=
                        p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # read data (based on the chunk size)
        data = wf.readframes(chunk)

        # play stream (looping from beginning of file to the end)
        while data != '':
            # writing to the stream is what *actually* plays the sound.
            stream.write(data)
            data = wf.readframes(chunk)

        stream.close()
        p.terminate()



    def listen(self):
        print('Listening beginning')
        while True:
            input = self.stream.read(chunk)
            rms_val = self.rms(input)
            if rms_val > Threshold:
                self.record()

a = Recorder()
a.postToTransformService(r'E:\4kurs\DV\Nlp-library-management\SpeechRecord\records\2.wav')

a.listen()
