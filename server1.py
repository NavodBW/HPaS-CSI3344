from re import T
import socket
import statistics 
import threading
from statistics import mean

HEADER = 64
PORT = 10000
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
CALCULATE_MESSAGE = "c"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
gradelist = []



def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            
            msg = conn.recv(msg_length).decode(FORMAT)

        
            

            if msg == CALCULATE_MESSAGE or len(gradelist) ==30:

                #getting the personID from the gradelist
                personID = gradelist[0]
                print(personID)

                #using slicing to remove personID from the gradelist
                gradelist_without_personID = gradelist[1:]
                print(gradelist_without_personID)

                #converting the gradelist to an integer
                int_gradelist = [int(n) for n in gradelist_without_personID]

                #calculating the course average
                average_score = statistics.mean(int_gradelist)

                avg_score =  str(round(average_score, 2))

                print(avg_score)

                #sorting the gradelist
                int_gradelist.sort()

                #printing best 12 marks
                print("Best twelve Marks:" +str(int_gradelist[-12:]))

                best_twelve_avg_list = int_gradelist[-12:]

                #calculating the avg of best 12 scores
                best_twelve_avg = statistics.mean(best_twelve_avg_list)

                best_twelve_avg_score = str(round(best_twelve_avg, 2))
                print(best_twelve_avg_score)
                
                conn.send(("Course average: " + avg_score).encode(FORMAT))
                conn.send(("Average of the best 12 marks: " + best_twelve_avg_score+"\n").encode(FORMAT))

                """ evaluated = False
                while evaluated == False: """
                if float(avg_score) > 69:
                    conn.send(("PersonID: "+personID + ", Course Average: " + avg_score +", QUALIFIED FOR HONOURS STUDY!").encode(FORMAT))
            
                elif float(avg_score) < 70 and float(best_twelve_avg_score) > 79:
                    conn.send(("PersonID: "+personID + ", Course Average: " + avg_score + ", Best 12 Avg: " +best_twelve_avg_score+ ", MAY HAVE GOOD CHANCE! Need further assessment!").encode(FORMAT))

                elif float(avg_score) < 70 and 69 < float(best_twelve_avg_score) < 80:
                    conn.send(("PersonID: "+personID + ", Course Average: " + avg_score + ", Best 12 Avg: " +best_twelve_avg_score+ ", MAY HAVE A CHANCE! Must be carefully reassessed and get the coordinator’s special permission!!").encode(FORMAT))
            
                elif float(avg_score) < 70 and float(best_twelve_avg_score) < 70:
                    conn.send(("PersonID: "+personID + ", Course Average: " + avg_score + ", Best 12 Avg: " +best_twelve_avg_score+ ", DOES NOT QUALIFY FOR HONORS STUDY! Try Masters by course work.").encode(FORMAT))

                else:
                    print("Error in evaluation")

                """ evaluated = True """

                


            elif msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            gradelist.append(msg)
            print(gradelist)
            conn.send("Msg received".encode(FORMAT))

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()