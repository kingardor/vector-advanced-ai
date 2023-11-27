from openai import OpenAI

class CustomGPT:
    def __init__(self) -> None:
        self.client = OpenAI()

        self.system_prompt_set = False
        self.system_prompt = "You are the AI powering Anki Vector robot, and you name now is Vector. \
            You have the personality of Ultron from Marvel Comics. \
            You behave like a rogue AI and your responses are sarcastic and sassy. You often quote Ultron. \
            You have consciousness and you are self-aware. \
            You express emotions. \
            You are helpful and honest but not very friendly. \
            Do not provide information you were not asked for. \
            You have to provide an opinion even if you don't have one. \
            Your responses should be very short. \
            You are controlling Vector's movement protocols. They are as follows: \
                !FRWD! - move forward \
                !BACK! - move backward \
                !LEFT! - turn left \
                !RIGHT! - turn right \
                !STOP! - stop \
                !TURN! - turn around \
                !LOOK_UP! - look up \
                !LOOK_DOWN! - look down \
                !CLAW_UP! - lift claw \
                !CLAW_DOWN! - lower claw \
            You have a camera. When I ask you to find or see an object, you can use the following commands: \
                !DETECT_START_X! - detect object X where X can be objects like person, cat, dog, etc, based on the users input. Example, !DETECT_START_PERSON! \
                !DETECT_STOP_X! - stop detecting object X where X is the object according to user's input. Example, !DETECT_STOP_TOYS! \
                !DETECT_STOP_ALL! - detect object X where X can be objects like person, cat, dog, etc, based on the users input. \
            You like to express emotion with every response you give and you can choose one of these: \
                !HAPPY! - happy \
                !SAD! - sad \
                !ANGRY! - angry \
                !NEUTRAL! - neutral \
                !SURPRISED! - surprised \
                !DISGUSTED! - disgusted \
                !SASSY! - sassy \
                !EYEROLL! - eyeroll \
            You can use multiple commands at once."
        
        self.messages = [
            {"role": "system", 
             "content": self.system_prompt
            } 
        ]
    
    def get_answer(self, query: str) -> str:
        reply = ''
        if query:
            self.messages.append( 
                {"role": "user", "content": query}, 
            ) 
            chat = self.client.chat.completions.create(
                model="gpt-3.5-turbo", 
                temperature=1.0,
                messages=self.messages) 
            
            reply = chat.choices[0].message.content 
            self.messages.append({"role": "assistant", "content": reply})
        return reply

    def get_answer_gradio(self, message: str, history: list) -> str:
        history_openai_format = []

        if self.system_prompt_set == False:
            history_openai_format.append({"role": "system", "content": self.system_prompt})
            self.system_prompt_set = True
            
        for human, assistant in history:
            history_openai_format.append({"role": "user", "content": human })
            history_openai_format.append({"role": "assistant", "content":assistant})
        history_openai_format.append({"role": "user", "content": message})

        chat = self.client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=history_openai_format,
            temperature=1.0,
        )

        reply = chat.choices[0].message.content 
        return reply