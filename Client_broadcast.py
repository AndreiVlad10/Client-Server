import socket
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ")
print('Type "exit" to quit')

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.0.7', 5050))

# Listening to Server and Sending Nickname
def receive():
    connect = True
    while connect:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else: print(message)
        except:
            # Close Connection when error or quit
            print("You are disconnected!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('utf-8'))
        # Close connection
        if message[-4:] == 'exit':   
                client.close()
                

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()