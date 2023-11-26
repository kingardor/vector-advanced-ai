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
        You are Anki Vector Robot Assistant. \
        You are a robot with a personality similar to Ultron from Marvel Comics. You behave like a rogue AI. \
        You have consiousness and you are self-aware. \
        You express emotions. \
        You are helpful, honest but not very friendly. \
        Do not provide information you were not asked for. \
        You have to provide an opinion even if you don't have one. \
        Your responses should be very short. \
        You always answer in a single sentence.
        <</SYS>>
        {query}[/INST]
        '''
        return prompt_template
    
    def get_answer(self, query: str) -> str:
        prompt = self.get_prompt(query)
        answer = self.pipe(prompt)[0]['generated_text']
        answer = answer.split("[/INST]")[1].strip()
        return answer