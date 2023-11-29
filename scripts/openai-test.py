import sys
sys.path.insert(1, 'src')

from customgpt import CustomGPT
import gradio as gr

if __name__ == '__main__':
    gpt = CustomGPT()

    gr.ChatInterface(
        gpt.get_answer_gradio,
        chatbot=gr.Chatbot(height=300),
        textbox=gr.Textbox(placeholder="Type here, human..", container=False, scale=7),
        title="VectorBot",
        description="",
        theme="soft",
        examples=["Hey, who are you?", "Detect toys", "Do you know Ultron?"],
        cache_examples=False,
        retry_btn=None,
        undo_btn="Delete Previous",
        clear_btn="Clear",
    ).launch()