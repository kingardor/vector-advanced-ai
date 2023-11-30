import time
import concurrent.futures
import numpy as np
import cv2
import PIL.Image
import anki_vector
from anki_vector.connection import ControlPriorityLevel

import traceback

def sleep(func):
    def exec(*args, **kwargs):
        retval = func(*args, **kwargs)
        time.sleep(0.25)
        return retval
    return exec

def latency(func):
    def exec(*args, **kwargs):
        start = time.time()
        retval = func(*args, **kwargs)
        end = time.time()
        print("Execution time {}: {}".format(func.__name__, end - start))
        return retval
    return exec

class VectorBot:
    def __init__(
            self, 
            behavior_activation_timeout: float = 60.0, 
            cache_animation_lists: bool = False
    ) -> None:

        args = anki_vector.util.parse_command_args()
        self.robot = anki_vector.AsyncRobot(
            args.serial,
            behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY,
            behavior_activation_timeout=behavior_activation_timeout,
            cache_animation_lists=cache_animation_lists
        )

        self.robot.connect()
        # Initialize the camera feed
        self.robot.camera.init_camera_feed()

        # Load the animation triggers
        result = self.robot.anim.load_animation_list()
        while True:
            try:
                if isinstance(result, concurrent.futures.Future):
                    time.sleep(1.0)
                    result.result()
                break
            except:
                # print(traceback.format_exc())
                pass
    
        result = self.robot.anim.load_animation_trigger_list()
        while True:
            try:
                if isinstance(result, concurrent.futures.Future):
                    time.sleep(1.0)
                    result.result()
                break
            except:
                # print(traceback.format_exc())
                pass

        # Get off the charger
        # self.robot.behavior.drive_off_charger()
    
    def __del__(self) -> None:
        self.robot.disconnect()
        
class Data:
    def __init__(self, robot: anki_vector.Robot) -> None:
        self.robot = robot
    
    @sleep
    def get_numpy_frame(self) -> np.ndarray:
        try:
            frame = self.robot.camera.latest_image.raw_image
            frame = np.array(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        except:
            frame = None
            print(traceback.format_exc())
        return frame

    @sleep
    def get_pil_frame(self) -> PIL.Image.Image:
        try:
            frame = self.robot.camera.latest_image.raw_image
        except:
            frame = None
            print(traceback.format_exc())
        return frame
    
class Action:
    def __init__(self, robot: anki_vector.Robot) -> None:
        self.robot = robot
    
    @sleep
    @latency
    def tts(self, text: str) -> None:
        print("{}".format(text))
        self.robot.behavior.say_text(text)
    
    @sleep
    @latency
    def eyecolor(self, hue: float, saturation: float) -> None:
        self.robot.behavior.set_eye_color(hue=hue, saturation=saturation)
    
    @sleep
    @latency
    def animation(self, name: str) -> None:
        print("Playing Animation: {}".format(name))
        self.robot.anim.play_animation_trigger(name)