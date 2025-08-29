import socket
import tkinter as tk

import threading


'''serveur_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serveur_socket.bind(('localhost', 9999))

serveur_socket.listen(1)
print('Socket is listening')

conn, addr = serveur_socket.accept()
print('Connected by', addr)

data = conn.recv(1024).decode('utf-8')
print(f'Received : {data}')

conn.sendall(b"hi, client how can I help you?")

ans=conn.recv(1024).decode('utf-8')
print(f'the answer is: {ans}')
sol=input("the solution is:")
conn.sendall(f"the solution to your problem is {sol}".encode('utf-8'))

conn.close()
serveur_socket.close()
'''



def serverStart():
    try:
        serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serveur_socket.bind(('localhost', 9999))
        serveur_socket.listen(1)
        lb = tk.Label(root, text='server is listening')
        lb.pack()

        def accept_connection():
            try:
                conn, addr = serveur_socket.accept()
                conn_label = tk.Label(root, text=f'Connected to: {addr}')
                conn_label.pack()
                global  client_conn, listening_thread, stop_listening
                client_conn = conn
                stop_listening = False
                listening_thread = threading.Thread(target=listen_for_messages, daemon=True)
                listening_thread.start()
            except Exception as e:
                error_label = tk.Label(root, text=f'Connection error: {e}')
                error_label.pack()

        accept_thread = threading.Thread(target=accept_connection, daemon=True)
        accept_thread.start()
        return serveur_socket
    except Exception as e:
        error_label = tk.Label(root, text=f'Server error: {e}')
        error_label.pack()
        return None


def sentamessage():
    global client_conn
    if client_conn is not None:
        try:
            message=ToSent.get()
            client_conn.sendall(message.encode('utf-8'))
            ToSent.delete(0, tk.END)
            lb = tk.Label(root, text=f"your message << {message} >> has been sent ")
            lb.pack()
        except Exception as e:
            error_label = tk.Label(root, text=f'error sending your message: {e}')
            error_label.pack()

def receivemessage():
    global client_conn
    if client_conn :
        try:
            ans = client_conn.recv(1024).decode('utf-8')
            receved.insert(0, ans)
            lb=tk.Label(root, text=f"you have received a message")
            lb.pack()
        except Exception as e:
            error_label = tk.Label(root, text=f'error receiving your message: {e}')
            error_label.pack()

def listen_for_messages():
    global client_conn, stop_listening
    while not stop_listening and client_conn:
        try:
            # Set timeout to allow checking for stop condition
            client_conn.settimeout(1.0)
            ans = client_conn.recv(1024).decode('utf-8')
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
    root.title('Socket Server')
    label1 = tk.Label(root, text='Socket Server')
    label1.pack()
    label2 = tk.Label(root, text='send a message')
    label2.pack()
    ToSent = tk.Entry(root )
    ToSent.pack()
    label3 = tk.Label(root, text='receive a message')
    label3.pack()
    receved = tk.Entry(root)
    receved.pack()
    btn = tk.Button(root, text='send', command=sentamessage)
    btn.pack()
    btn = tk.Button(root, text='Start', command=serverStart)
    btn.pack()
    root.mainloop()



