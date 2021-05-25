from re import T
import socket
import statistics 
import threading
from statistics import mean
import csv

HEADER = 64
PORT2 = 10001
SERVER = 'localhost'
ADDR2 = (SERVER, PORT2)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SAVE_DB_MSG = "s"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR2)

def handle_client(conn, addr2):
    gradelist = []
    
    print(f"[NEW CONNECTION] {addr2} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == SAVE_DB_MSG:
                personID = gradelist[0]
                lines = list()
                with open('studentDB.csv', 'r') as readFile:
                    reader = csv.reader(readFile)
                    for row in reader:
                        lines.append(row)
                        for field in row:
                            if field == personID:
                                lines.remove(row)

                with open('studentDB.csv', 'w', newline='') as writeFile:
                    writer = csv.writer(writeFile, quoting=csv.QUOTE_ALL)
                    writer.writerows(lines)

                with open('StudentDB.csv', 'a', newline='') as myfile:
                    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                    wr.writerow([int(n) for n in gradelist if n not in ('d', 's', 'e', 'c')])

            if msg == DISCONNECT_MESSAGE:
                connected = False
            gradelist.append(msg)
            print(f"[{addr2}] {msg}")
            conn.send("\nMsg received from server 2: ".encode(FORMAT))

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr2 = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr2))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()