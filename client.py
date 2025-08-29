import socket
import tkinter as tk
import threading

client_socket = None
listening_thread = None
stop_listening = False

def clientStart():
    global client_socket, listening_thread, stop_listening
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 9999))
        lb = tk.Label(root, text='You are connected')
        lb.pack()
        stop_listening = False
        listening_thread = threading.Thread(target=listen_for_messages, daemon=True)
        listening_thread.start()
        return client_socket
    except Exception as e:
        error_label = tk.Label(root, text=f'connection error: {e}')
        error_label.pack()
        return None


def sendmessage():
    global client_socket
    if client_socket is not None:
        data = ToSent.get()
        client_socket.sendall(data.encode('utf-8'))
        lb = tk.Label(root, text=f"your message << {data} >> has been sent")
        lb.pack()



def listen_for_messages():
    global client_socket, stop_listening
    while not stop_listening and client_socket:
        try:
            # Set timeout to allow checking for stop condition
            client_socket.settimeout(1.0)
            ans = client_socket.recv(1024).decode('utf-8')
            if ans:  # Only update if we actually received something
                # Use after() to safely update the GUI from another thread
                root.after(0, update_received_message, ans)
        except socket.timeout:
            continue  # Timeout is normal, just continue listening
        except Exception as e:
            if not stop_listening:
                error_label = tk.Label(root, text=f'error: {e}')
                error_label.pack()
            break

def update_received_message(message):
    receved.delete(0, tk.END)
    receved.insert(0, message)
    lb = tk.Label(root, text=f"New message received!")
    lb.pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('400x500')
    root.title('Socket Client')
    label = tk.Label(root, text='Socket Client')
    label.pack()
    label = tk.Label(root, text='send a message')
    label.pack()
    ToSent = tk.Entry(root)
    ToSent.pack()
    label = tk.Label(root, text='receive a message')
    label.pack()
    receved = tk.Entry(root)
    receved.pack()
    btn = tk.Button(root, text='send', command=sendmessage)
    btn.pack()
    btn = tk.Button(root, text='Start', command=clientStart)
    btn.pack()
    root.mainloop()
