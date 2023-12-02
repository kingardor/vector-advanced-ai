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
    def get_battery_details(self) -> None:
        self.battery_state_task = self.robot.get_battery_state()

        while True:
            if self.battery_state_task.done():
                self.battery_state = self.battery_state_task.result()
                self.battery_state_task = self.robot.get_battery_state()
                break
            time.sleep(0.25)

        if self.battery_state:
            self.batt = self.battery_state.battery_level

    def load_animations(self) -> None:
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
        
        # Get the battery level
        self.battery_level = 0
        self.get_battery_details()

        # Initialize the camera feed
        self.robot.camera.init_camera_feed()

        # Get off the charger
        if self.robot.status.is_on_charger and self.battery_level > 25:
            self.robot.behavior.drive_off_charger()
        
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
        self.prev_emote = None
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
    def emote(self, name: str) -> None:
        if self.prev_emote == name:
            return
        self.prev_emote = name
        print("Playing Animation: {}".format(name))
        self.robot.anim.play_animation_trigger(name)