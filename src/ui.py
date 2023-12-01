import customtkinter
from customtkinter import END

class UserInterface:
	def start_ui(self) -> None:
		self.app.mainloop()
    
	def speak(self) -> None:
		if self.chat_entry.get():
			self.my_text.insert(END, "\n\nYou: " + self.chat_entry.get())
		else:
			self.my_text.insert(END, "\n\nHey! You Forgot To Type Anything!")

	def clear(self) -> None:
		self.my_text.delete(1.0,END)
		self.chat_entry.delete(0,END)

	def add_text(self, type:str, text: str) -> None:
		self.my_text.insert(END, f"\n\n{type}: {text}")

	def construct_ui(self) -> None:
		# Create Text Frame
		text_frame = customtkinter.CTkFrame(
            master=self.app,
            fg_color="#717378"
        )
		text_frame.pack(pady=5)

        # Add Text Widget to view conversation
		self.my_text = customtkinter.CTkTextbox(
		    master=text_frame,
            width=400,
            height=400,
            border_width=2
        )
		self.my_text.grid(row=0, column=0)

        # Create Scrollbar for text widget
		text_scoll = customtkinter.CTkScrollbar(
            master=text_frame,
            command=self.my_text.yview
        )
		text_scoll.grid(row=0,column=1,sticky="ns")

        # Add the scollbar to the textbox
		self.my_text.configure(yscrollcommand=text_scoll.set)

        # Entry Widget To type Stuff to ChatGPT
		self.chat_entry = customtkinter.CTkEntry(self.app,
            placeholder_text="Type something, human..",
            width=400,
            height=30,
            border_width=2
        )
		self.chat_entry.pack(pady=10)

        # Create Button Frame
		button_frame = customtkinter.CTkFrame(
            master=self.app,
            fg_color="#242424"
        )
		button_frame.pack(pady=10)

        # Create Submit Button
		submit_button=customtkinter.CTkButton(
            master=button_frame,
            text="Send",
            command=self.speak
        )
		submit_button.grid(row=0,column=0,padx=25)

        # Create Clear Button
		clear_button=customtkinter.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear
        )
		clear_button.grid(row=0,column=1,padx=35)

		self.camera = customtkinter.CTkLabel(
            master=self.app,
            width=400,
            height=400,
            text=""
        )
		self.camera.pack(pady=10)

	def __init__(self) -> None:
		self.app = customtkinter.CTk()
		self.app.title("VectorBot AI")
		self.app.geometry('500x1000')
		self.my_text = None
		self.chat_entry = None
		self.camera = None

		customtkinter.set_appearance_mode("dark")
		customtkinter.set_default_color_theme("dark-blue")

		self.construct_ui()
		self.my_text.insert(END, "Vector: Hey, human! I'm VectorBot, your personal AI assistant!\n\n")
        
