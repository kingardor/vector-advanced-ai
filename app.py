import sys
sys.path.insert(1, 'src')
import time
from threading import Thread
from queue import Queue
import re
from ui import UserInterface
from vectorbot import VectorBot, Data, Action
from speechstream import StreamHandler
from customgpt import CustomGPT
import owl

commandqueue = Queue()

def parse_commands(text: str) -> str:
    # Remove all \n and \t
    text = text.replace("\n", "")
    text = text.replace("\t", "")

    # Replace AI with A.I.
    text = text.replace("AI", "A.I.")

    # Extract all text between ! and ! using regex
    commands = re.findall(r"!(.*?)!", text)

    # Add all commands to queue
    for command in commands:
        commandqueue.put(command)
    
    # Remove all commands from text
    for command in commands:
        text = text.replace(f"!{command}!", "")
    
    print(commandqueue.queue)
    return text
def conversation(
        ui: UserInterface,
        handler: StreamHandler,
        gpt: CustomGPT,
        robot_data: Data,
        robot_action: Action
    ) -> None:
    while True:
        if not isinstance(handler.stt_result, type(None)):
            user_input = handler.stt_result
            handler.stt_result = None
            ui.add_text("Me", user_input)

            robot_output = gpt.get_answer(user_input)
            robot_output = parse_commands(robot_output)
            robot_action.tts(robot_output)
            ui.add_text("Vector", robot_output)
            
        time.sleep(0.25)

def main():
    
    # Initialise Nano OWL
    owlpred = owl.HootHoot()

    # Initialise Whisper
    handler = StreamHandler()

    # Initialise ChatGPT
    gpt = CustomGPT()
    
    # Initialise UI
    ui = UserInterface()

    # Initialise VectorBot
    vectorbot = VectorBot()
    robot_action = Action(vectorbot.robot)
    robot_data = Data(vectorbot.robot)

    # Startup Sequence
    robot_action.eyecolor(1.0, 1.0)
    robot_action.animation('GreetAfterLongTime')
    robot_action.tts("I'm alive now!")
    robot_action.eyecolor(0.0, 0.0)    
    
    conversation_thread = Thread(
        target=conversation, 
        args=(
                ui,
                handler,
                gpt,
                robot_data,
                robot_action    
            )
        )
    conversation_thread.daemon = True
    conversation_thread.start()

    ui.start_ui()

if __name__ == "__main__":
    main()

    
    # while True:
    #     time.sleep(0.25)
    #     frame = robot_data.get_pil_frame()
    #     if isinstance(frame, type(None)):
    #         continue
    #     output, image = owlpred.predict(
    #         frame, 
    #         "[a person, toys]",
    #         threshold=0.2
    #     )

    #     frame = np.array(image)
    #     frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    #     cv2.imshow("Vector", frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    
    # cv2.destroyAllWindows()