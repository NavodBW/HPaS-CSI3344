import socket
import re

HEADER = 64
PORT = 10000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
CALCULATE_MESSAGE = "c"
SERVER = "localhost"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


    


gradecounter = 1



while gradecounter<31:
    print("Enter unit " + str(gradecounter) +" score: (or press 'c' to cancel)")
    unitscore = input()
    
    if re.match(r"^([1-9]?\d|100)$", unitscore):
        send(unitscore)
        gradecounter +=  1
    
    elif unitscore.lower() == CALCULATE_MESSAGE:
        if gradecounter<13:
            print("at least 12 unit scores are required")
        
        else:
            send(CALCULATE_MESSAGE)

            break
    else:
        print("Invlaid input. Please try again!")

    
    
    



send(DISCONNECT_MESSAGE)