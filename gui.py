from tkinter import *
from tkinter import simpledialog


class GUI:
    def __init__(self, client, debug=False):
        self.client = client

        self.chat_message = None
        self.debug = debug

        # Create a chat window and then hide it
        self.chat_window = Tk()

        self.username_label = Label(self.chat_window, bg="#17202A", fg="#EAECEE", pady=5)
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

        self.quit_button = Button(self.chat_window, text="Quit", command=self.quit)
        self.quit_button.pack(pady=20)
        self.quit_button.place(relx=0.77, rely=0.012, relheight=0.06, relwidth=0.22)

        self.chat_window.withdraw()

        self.username = simpledialog.askstring(title="Start Chatting", prompt="Enter a username")

        if self.username is None:
            exit(0)

    def start_chatting(self):
        self.layout_chat_window(self.username)
        self.client.start_chatting(username=self.username)
        self.chat_window.mainloop()
        exit(0)

    def layout_chat_window(self, username):
        self.username = username

        # Show the chat window
        self.chat_window.deiconify()
        self.chat_window.title("Chat App")
        self.chat_window.resizable(width=False, height=False)
        self.chat_window.configure(width=480, height=550, bg="#17202A")

        self.username_label.text = username
        self.chat_contents.config(cursor="arrow")

        # They see me scrollin, they hatin
        scrollbar = Scrollbar(self.chat_contents)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.chat_contents.yview)

        self.chat_contents.config(state=DISABLED)

    def handle_send(self, chat_message):
        self.debug_print("Sending message - '%s'" % chat_message)
        self.chat_contents.config(state=DISABLED)
        self.chat_message = chat_message
        self.message_input.delete(0, END)

        # Passed on init
        self.chat_contents.config(state=DISABLED)
        self.client.send_message(next_message=chat_message)
        self.message_received("(you) > %s" % chat_message)

    def message_received(self, message):
        self.debug_print("Received message - '%s'" % message)
        self.chat_contents.config(state=NORMAL)
        self.chat_contents.insert(END, message + "\n\n")
        self.chat_contents.config(state=DISABLED)
        self.chat_contents.see(END)

    def quit(self):
        self.chat_window.destroy()
        self.client.quit()

    def debug_print(self, debug_msg):
        if self.debug:
            print("GUI-DBG: %s" % debug_msg)
