import time
import numpy as np
import cv2
import concurrent.futures
import anki_vector

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
            behavior_activation_timeout: float = 30.0, 
            cache_animation_lists: bool = False
        ) -> None:

        args = anki_vector.util.parse_command_args()
        self.robot = anki_vector.AsyncRobot(
            args.serial,
            behavior_activation_timeout=behavior_activation_timeout,
            cache_animation_lists=cache_animation_lists
        )

        self.robot.connect()

        # Initialize the camera feed
        self.robot.camera.init_camera_feed()

        # Load the animation triggers
        result = self.robot.anim.load_animation_list()
        time.sleep(2.0)
        if isinstance(result, concurrent.futures.Future):
            result.result()
        
        result = self.robot.anim.load_animation_trigger_list()
        time.sleep(2.0)
        if isinstance(result, concurrent.futures.Future):
            result.result()

        # Get off the charger
        self.robot.behavior.drive_off_charger()
        
class Data:
    def __init__(self, robot: anki_vector.Robot) -> None:
        self.robot = robot
    
    @sleep
    def getframe(self) -> np.ndarray:
        frame = self.robot.camera.latest_image.raw_image
        frame = np.array(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
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

def main():
    
    vectorbot = VectorBot()
    robot_action = Action(vectorbot.robot)
    robot_data = Data(vectorbot.robot)

    robot_action.eyecolor(1.0, 1.0)
    robot_action.animation('GreetAfterLongTime')
    robot_action.tts("Hi James!")
    robot_action.eyecolor(0.0, 0.0)    
    
    while True:
        frame = robot_data.getframe()

        cv2.imshow("Vector", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
    vectorbot.robot.disconnect()

if __name__ == "__main__":
    main()