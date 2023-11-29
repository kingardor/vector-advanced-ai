import os
import time
import sys
sys.path.insert(1, 'src')

from whisperstt import WhisperSTT
from speechstream import StreamHandler

def main():
    try:
        handler = StreamHandler()
        while True:
            if not isinstance(handler.stt_result, type(None)):
                print('Output: {}'.format(handler.stt_result))
                handler.stt_result = None
            time.sleep(0.25)
    except (KeyboardInterrupt, SystemExit): pass
    finally:
        print("\n\033[93mQuitting..\033[0m")
        if os.path.exists('dictate.wav'): os.remove('dictate.wav')

if __name__ == '__main__':
    main()