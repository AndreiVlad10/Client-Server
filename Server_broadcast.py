import socket
import threading

#Connecting Data
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
LEAVE = 'exit'
clients = []
nicks = []

#Start Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

#Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

#Removing And Closing Clients
def remove(pers):
    index = clients.index(pers)
    clients.remove(pers)
    pers.close()
    nickname = nicks[index]
    broadcast('{} left!'.format(nickname).encode(FORMAT))
    print(f"Left: {nickname}")
    nicks.remove(nickname)

#Handling Messages From Clients
def handle(client):
    while True:
        try:
            #Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
            print(message)
            if message[-4:] == LEAVE: #because message is something like b'NICKNAME: MSG'
                remove(client)
                break
        except:
            remove(client)
            break

#Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        nicks.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode(FORMAT))
        client.send('Connected to server!'.encode(FORMAT))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
     

print("[STARTING] server is starting...") 
receive()
