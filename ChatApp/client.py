import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = '127.0.0.1'
PORT = 12345

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("OIBSIP Chat App")
        self.master.geometry("400x500")

        self.nickname = None
        self.client = None

        self.build_login_ui()

    def build_login_ui(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text="Enter your nickname:", font=("Arial", 12)).pack(pady=20)
        self.entry_nick = tk.Entry(self.master, font=("Arial", 12))
        self.entry_nick.pack(pady=10)
        tk.Button(self.master, text="Connect", command=self.connect_to_server, bg="#4CAF50", fg="white").pack(pady=10)

    def build_chat_ui(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.chat_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, font=("Arial", 11))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)

        self.msg_entry = tk.Entry(self.master, font=("Arial", 12))
        self.msg_entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        tk.Button(self.master, text="Send", command=self.send_message, bg="#2196F3", fg="white").pack(side=tk.RIGHT, padx=10, pady=10)

    def connect_to_server(self):
        self.nickname = self.entry_nick.get().strip()
        if not self.nickname:
            messagebox.showwarning("Warning", "Please enter a nickname.")
            return

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((HOST, PORT))
            self.client.send(self.nickname.encode('utf-8'))
            self.build_chat_ui()
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Unable to connect to server:\n{e}")

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if not message:
                    break
                self.chat_area.config(state=tk.NORMAL)
                self.chat_area.insert(tk.END, message + "\n")
                self.chat_area.config(state=tk.DISABLED)
                self.chat_area.yview(tk.END)
            except:
                break

    def send_message(self):
        message = self.msg_entry.get().strip()
        if message:
            self.client.send(f"{self.nickname}: {message}".encode('utf-8'))
            self.msg_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()
