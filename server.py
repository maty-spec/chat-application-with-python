import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk

# Starts the server and accepts one client connection
def start_server():
    global client, address
    server_socket.listen(1)
    client, address = server_socket.accept()
    chat_box.insert(tk.END, f'Client {address} connected.\n')
    chat_box.tag_add("center", "end-2l", "end-1l")
    receive_messages()

# Continuously receives messages from the client
def receive_messages():
    while True:
        try:
            message_from_client = client.recv(1024).decode("utf-8")
            if message_from_client == "...typing...":
                typing_label.config(text="Client is typing...")
            else:
                typing_label.config(text="")
                chat_box.insert(tk.END, f'Client: {message_from_client}\n', "left")
        except ConnectionResetError:
            update_status("Client disconnected.", "red")
            break
        except Exception as e:
            update_status(f"Error: {e}", "red")
            break

# Sends a message to the client
def send_message():
    message = message_entry.get()
    client.send(bytes(message, "utf-8"))
    chat_box.insert(tk.END, f'Server: {message}\n', "right")
    message_entry.delete(0, tk.END)

# Sends typing status to client
def notify_typing(event):
    client.send(bytes("...typing...", "utf-8"))

# === Socket setup ===
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST_NAME = socket.gethostname()
PORT = 12345
server_socket.bind((HOST_NAME, PORT))

# === GUI setup ===
root = tk.Tk()
root.title("Server Chat")
root.geometry("400x500")
root.configure(bg="#2c3e50")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5)

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

# Start server in a background thread
threading.Thread(target=start_server, daemon=True).start()
root.mainloop()