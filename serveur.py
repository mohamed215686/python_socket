import socket
import tkinter as tk
from logging import exception
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
                global  client_conn
                client_conn = conn
            except exception as e:
                error_label = tk.Label(root, text=f'Connection error: {e}')
                error_label.pack()

        accept_thread = threading.Thread(target=accept_connection, daemon=True)
        accept_thread.start()
        return serveur_socket
    except Exception as e:
        error_label = tk.Label(root, text=f'Server error: {e}')
        error_label.pack()
        return None





if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('400x500')
    root.title('Socket Server')
    label = tk.Label(root, text='Socket Server')
    label.pack()
    entry = tk.Entry(root )
    entry.pack()
    btn = tk.Button(root, text='Start', command=serverStart)
    btn.pack()
    root.mainloop()



