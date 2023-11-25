import os
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import sys
sys.path.insert(1, 'src')

from whisperstt import WhisperSTT
from speechstream import StreamHandler

def main():
    try:
        handler = StreamHandler()
        handler.listen()
    except (KeyboardInterrupt, SystemExit): pass
    finally:
        print("\n\033[93mQuitting..\033[0m")
        if os.path.exists('dictate.wav'): os.remove('dictate.wav')

if __name__ == '__main__':
    main()