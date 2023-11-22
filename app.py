import time
import numpy as np
import cv2
import anki_vector

def sleep(function):
    def wrapper(*args, **kwargs):
        retval = function(*args, **kwargs)
        print("Sleeping for 0.25 seconds...")
        time.sleep(0.25)
        return retval
    return wrapper

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
    def tts(self, text: str) -> None:
        print("{}".format(text))
        self.robot.behavior.say_text(text)
    
    @sleep
    def eyecolor(self, hue: float, saturation: float) -> None:
        self.robot.behavior.set_eye_color(hue=hue, saturation=saturation)

def main():
    args = anki_vector.util.parse_command_args()
    robot = anki_vector.Robot(
        args.serial,
        behavior_activation_timeout=30.0,
        cache_animation_lists=False
    )

    robot_action = Action(robot)
    robot_data = Data(robot)

    robot.connect()
    robot.camera.init_camera_feed()

    robot_action.eyecolor(1.0, 1.0)
    robot_action.tts("I'm alive!")
    robot_action.eyecolor(0.0, 0.0)    
    
    while True:
        frame = robot_data.getframe()

        cv2.imshow("Vector", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
    robot.disconnect()

if __name__ == "__main__":
    main()