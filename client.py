import socket

client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 9999))

client_socket.sendall(b"Hi I'm client 1 ")

res=client_socket.recv(1024).decode('utf-8')


prob=input(f"server answer: {res}")
client_socket.sendall(f"{prob}".encode('utf-8'))

res2=client_socket.recv(1024).decode('utf-8')
print(f"server answer: {res2}")
