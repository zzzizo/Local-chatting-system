import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#2e3b4e")

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=20, bg="#1c2535", fg="#f8f8f2", font=("Arial", 10))
        self.chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)

        # Message entry box
        self.entry_msg = tk.Entry(self.root, width=50, font=("Arial", 12), bg="#3a4e6c", fg="#f8f8f2", bd=0, relief="flat", insertbackground="white")
        self.entry_msg.pack(pady=5, padx=10, fill=tk.X)
        self.entry_msg.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(self.root, text="Send", font=("Arial", 12), fg="#f8f8f2", bg="#4CAF50", bd=0, relief="flat", command=self.send_message)
        self.send_button.pack(pady=5, padx=10, ipady=5)
        self.send_button.bind("<Enter>", self.on_hover)
        self.send_button.bind("<Leave>", self.on_leave)

        # Initialize socket connection
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((SERVER_HOST, SERVER_PORT))
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.username = simpledialog.askstring("Username", "Enter your username:")
            if self.username:
                self.client_socket.send(self.username.encode('utf-8'))
                self.display_message("Connected to the server.", outgoing=False)
            else:
                messagebox.showerror("Error", "Username cannot be empty!")
                self.root.quit()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Cannot connect to server: {e}")
            self.root.quit()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.display_message(message)
                else:
                    break
            except:
                break
        self.client_socket.close()

    def send_message(self, event=None):
        message = self.entry_msg.get()
        if message:
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.entry_msg.delete(0, tk.END)
                self.display_message(f"You: {message}", outgoing=True)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send message: {e}")
                self.root.quit()

    def display_message(self, message, outgoing=False):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

    def on_hover(self, event):
        self.send_button.config(bg="#45a049")

    def on_leave(self, event):
        self.send_button.config(bg="#4CAF50")

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
