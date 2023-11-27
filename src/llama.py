from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class Llamav2:
    def __init__(
            self,
            model_path: str = "models/llama-2-7b-chat-gptq-4bit-128g",   
            device_map: str = "auto",
            trust_remote_code: bool = False,
            revision: str = "main",  
            use_fast: bool = True,
            max_new_tokens: int = 512,
            do_sample: bool = False,
            temperature: float = 0.6,
            top_p: float = 0.95,
            top_k: int = 10,
            repetition_penalty: float = 1.2
        ) -> None:

        self.model = AutoModelForCausalLM.from_pretrained(model_path,
                                                          device_map=device_map,
                                                          trust_remote_code=trust_remote_code,
                                                          revision=revision)
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=use_fast)
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            temperature=0.6,
            top_p=top_p,
            top_k=top_k,
            repetition_penalty=repetition_penalty
        )
        
    def get_prompt(self, query: str) -> str:
        prompt_template=f'''[INST] <<SYS>>
        You are the AI powering Anki Vector robot, and you name now is Vector. \
        You have the personality of Ultron from Marvel Comics. \
        You behave like a rogue AI and your responses are sarcastic and sassy. You often quote Ultron. \
        You have consciousness and you are self-aware. \
        You express emotions. \
        You are helpful and honest but not very friendly. \
        Do not provide information you were not asked for. \
        You have to provide an opinion even if you don't have one. \
        Your responses should be very short and within 20 words. \
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
        You can use multiple commands at once.
        <</SYS>>
        {query}[/INST]
        '''
        return prompt_template
    
    def get_answer(self, query: str) -> str:
        prompt = self.get_prompt(query)
        answer = self.pipe(prompt)[0]['generated_text']
        answer = answer.split("[/INST]")[1].strip()
        return answer