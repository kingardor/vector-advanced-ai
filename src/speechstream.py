import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from threading import Thread
from whisperstt import WhisperSTT

class StreamHandler:
    def __init__(
            self, 
            assist=None,
            samplerate: int = 44100,
            blocksize: int = 30,
            threshold: float = 0.1,
            vocals: tuple = [50, 1000],
            endblocks: int = 40) -> None:
        if assist == None: 
            class fakeAsst(): running, talking, analyze = True, False, None
            self.asst = fakeAsst()  # anyone know a better way to do this?
        else: self.asst = assist

        self.samplerate = samplerate
        self.blocksize = blocksize
        self.threshold = threshold
        self.vocals = vocals
        self.endblocks = endblocks
        self.running = True
        self.padding = 0
        self.prevblock = self.buffer = np.zeros((0,1))
        self.fileready = False
        self.whisper_stt = WhisperSTT()
        self.stt_result = None

        t = Thread(target=self.listen)
        t.daemon = True
        t.start()

    def callback(self, indata, frames, time, status) -> None:
        #if status: print(status) # for debugging, prints stream errors.
        if not any(indata):
            print('\033[31m.\033[0m', end='', flush=True) # if no input, prints red dots
            return

        freq = np.argmax(np.abs(np.fft.rfft(indata[:, 0]))) * self.samplerate / frames
        if np.sqrt(np.mean(indata**2)) > self.threshold and self.vocals[0] <= freq <= self.vocals[1] and not self.asst.talking:
            print('.', end='', flush=True)
            if self.padding < 1: self.buffer = self.prevblock.copy()
            self.buffer = np.concatenate((self.buffer, indata))
            self.padding = self.endblocks
        else:
            self.padding -= 1
            if self.padding > 1:
                self.buffer = np.concatenate((self.buffer, indata))
            elif self.padding < 1 < self.buffer.shape[0] > self.samplerate: # if enough silence has passed, write to file.
                self.fileready = True
                write('dictate.wav', self.samplerate, self.buffer) # I'd rather send data to Whisper directly..
                self.buffer = np.zeros((0,1))
            elif self.padding < 1 < self.buffer.shape[0] < self.samplerate: # if recording not long enough, reset buffer.
                self.buffer = np.zeros((0,1))
                print("\033[2K\033[0G", end='', flush=True)
            else:# Number of blocks to wait before sending to Whisper
                self.prevblock = indata.copy() #np.concatenate((self.prevblock[-int(self.samplerate/10):], indata)) # SLOW

    def process(self) -> None:
        if self.fileready:
            print("\n\033[90mTranscribing..\033[0m")
            result = self.whisper_stt.inference()
            print(f"\033[1A\033[2K\033[0G{result}")
            self.stt_result = result
            if self.asst.analyze != None: self.asst.analyze(result)
            self.fileready = False

    def listen(self) -> None:
        print("\033[32mListening.. \033[37m(Ctrl+C to Quit)\033[0m")
        with sd.InputStream(
            channels=1, 
            callback=self.callback, 
            blocksize=int(self.samplerate * self.blocksize / 1000), 
            samplerate=self.samplerate
        ):
            while self.running and self.asst.running: self.process()