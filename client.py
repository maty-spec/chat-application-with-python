import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk

# Connects to the server on startup
def connect_to_server():
    global client_socket
    client_socket.connect((HOST_NAME, PORT))
    receive_messages()

# Continuously receives messages from the server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message == "...typing...":
                typing_label.config(text="Server is typing...")
            else:
                typing_label.config(text="")
                chat_box.insert(tk.END, f'Server: {message}\n', "left")
        except ConnectionResetError:
            update_status("Connection closed by server.", "red")
            break
        except Exception as e:
            update_status(f"Error: {e}", "red")
            break

# Sends a message to the server
def send_message():
    message = message_entry.get()
    client_socket.send(bytes(message, "utf-8"))
    chat_box.insert(tk.END, f'Client: {message}\n', "right")
    message_entry.delete(0, tk.END)

# Sends a typing status to the server
def notify_typing(event):
    client_socket.send(bytes("...typing...", "utf-8"))

# === Socket setup ===
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST_NAME = socket.gethostname()
PORT = 12345

# === GUI setup ===
root = tk.Tk()
root.title("Client Chat")
root.geometry("400x500")
root.configure(bg="#2c3e50")

chat_box = scrolledtext.ScrolledText(root, width=50, height=20, bg="#ecf0f1", font=("Arial", 12))
chat_box.pack(pady=10, padx=10)
chat_box.tag_configure("left", justify="left")
chat_box.tag_configure("right", justify="right")

typing_label = tk.Label(root, text="", fg="lightgray", bg="#2c3e50", font=("Arial", 10))
typing_label.pack()

message_entry = ttk.Entry(root, width=40, font=("Arial", 12))
message_entry.pack(pady=5)
message_entry.bind("<KeyPress>", notify_typing)

send_button = ttk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

# Display connection status
status_label = tk.Label(root, text="", fg="green", bg="#2c3e50", font=("Arial", 10))
status_label.pack(pady=5)

def update_status(message, color):
    status_label.config(text=message, fg=color)

# Start server connection in a separate thread
threading.Thread(target=connect_to_server, daemon=True).start()
root.mainloop()