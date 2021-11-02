from tkinter import *


class GUI:
    def __init__(self, send_message_handler, start_chatting_handler):
        self.send_message_handler = send_message_handler
        self.start_chatting_handler = start_chatting_handler

        # Create a chat window and then hide it
        self.chat_window = Tk()
        self.chat_window.withdraw()

        # Create a login window
        self.login_window = Toplevel()
        self.login_window_prompt = Label(self.login_window, text="Welcome", justify=CENTER)
        self.login_window_prompt.place(relheight=0.15, relx=0.2, rely=0.07)

        # Create the 'Username:' label
        self.login_username_label = Label(self.login_window, text="Username: ")
        self.login_username_label.place(relheight=0.2, relx=0.1, rely=0.2)

        # Create the username input box
        self.username_input = Entry(self.login_window)
        self.username_input.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)

        # Focus the cursor on the username input
        self.username_input.focus()

        # Create a button to connect to the chat session
        self.connect_button = Button(self.login_window, text="Connect",
                                     command=lambda: self.start_chatting(self.username_input.get()))

        self.connect_button.place(relx=0.4, rely=0.55)

        # Finally, start the main event loop
        self.chat_window.mainloop()

    def start_chatting(self, username):
        self.login_window.destroy()
        self.layout_chat_window(username)
        self.start_chatting_handler(username)

    def layout_chat_window(self, username):
        self.username = username

        # Show the chat window
        self.chat_window.deiconify()
        self.chat_window.title("Chat App")
        self.chat_window.resizable(width=False, height=False)
        self.chat_window.configure(width=480, height=550, bg="#17202A")

        self.username_label = Label(self.chat_window, bg="#17202A", fg="#EAECEE", text=self.username, pady=5)
        self.username_label.place(relwidth=1)

        self.chat_line = Label(self.chat_window, width=480, bg="#ABB2B9")
        self.chat_line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.chat_contents = Text(self.chat_window,
                                  width=20,
                                  height=2,
                                  bg="#17202A",
                                  fg="#EAECEE",
                                  padx=5,
                                  pady=5)

        self.chat_contents.place(relheight=0.745, relwidth=1, rely=0.08)

        self.bottom_label = Label(self.chat_window, bg="#ABB2B9", height=80)
        self.bottom_label.place(relwidth=1, rely=0.825)

        self.message_input = Entry(self.bottom_label, bg="#2C3E50", fg="#EAECEE")
        self.message_input.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.message_input.focus()

        self.send_button = Button(self.bottom_label,
                                  text="Send",
                                  width=20,
                                  bg="#ABB2B9",
                                  command=lambda: self.handle_send(self.message_input.get()))

        self.send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        self.chat_contents.config(cursor="arrow")

        # They see me scrollin, they hatin
        scrollbar = Scrollbar(self.chat_contents)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.chat_contents.yview)

        self.chat_contents.config(state=DISABLED)

    def handle_send(self, chat_message):
        self.chat_contents.config(state=DISABLED)
        self.chat_message = chat_message
        self.message_input.delete(0, END)

        # Passed on init
        self.chat_contents.config(state=DISABLED)
        self.send_message_handler(chat_message)

    def message_received(self, message):
        self.chat_contents.config(state=NORMAL)
        self.chat_contents.insert(END, message + "\n\n")
        self.chat_contents.config(state=DISABLED)
        self.chat_contents.see(END)
