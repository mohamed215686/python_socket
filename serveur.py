import socket

serveur_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
