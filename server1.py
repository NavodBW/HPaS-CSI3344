from re import T
import socket
import statistics 
import threading
from statistics import mean
import csv

HEADER = 64
PORT = 10000
PORT2 = 10001
SERVER = "localhost"
ADDR = (SERVER, PORT)
ADDR2 = (SERVER, PORT2)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
EVALUATE_EXST_MSG = "e"
CALCULATE_MESSAGE = "c"
SAVE_DB_MSG = "s"
SEARCH_DB_MSG = "d"



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR2)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


noresultsCounter = 1

def handle_client(conn, addr):
    gradelist = []
    


    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True

    def evaluator():
        #getting the personID from the gradelist
        personID = gradelist[0]
        print(personID)
        
        #using slicing to remove personID from the gradelist
        gradelist_without_personID = gradelist[1:]
        print(gradelist_without_personID)

        #converting the gradelist to an integer
        int_gradelist = [int(n) for n in gradelist_without_personID if n not in ('d', 's', 'e', 'c')]

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
        
        print("Course average: " + avg_score +"\n")
        print("Average of the best 12 marks: " + best_twelve_avg_score+"\n")

        
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

    
    saveToLog = False
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            
            msg = conn.recv(msg_length).decode(FORMAT)

        
            

            if msg == CALCULATE_MESSAGE:
                evaluator()
                

                        


                

            

            if msg == SAVE_DB_MSG:
                saveToLog = True     

            if msg == EVALUATE_EXST_MSG:
                global noresultsCounter

                

                    

                personID = gradelist[0]
                personIDstring = str(personID)
                
                
                with open('StudentDB.csv', 'r') as myfile1:
                    rd = csv.reader(myfile1)

                    for line in rd:
                        if personIDstring in line:
                            
                            
                            gradelist = list(line)
                            print(gradelist)
                            evaluator()   
                            
                            print("Evaluated existing gradelist : ")
                            print(gradelist)  
                            gradelist = gradelist[:1]
                            print("sliced gradelist")
                            print(gradelist)
                            
                        else:
                            while noresultsCounter == 1:
                                noresultsCounter += 1
                                conn.send("No existing results found".encode(FORMAT))
                            
                                
                                


                           
                            

            if msg == SEARCH_DB_MSG:
                personID = gradelist[0]
                personIDstring = str(personID)
                
                
                with open('StudentDB.csv', 'r') as myfile:
                    rd = csv.reader(myfile)

                    for line in rd:
                        if personIDstring in line:
                            
                            
                            gradelist = list(line)
                            print(gradelist)
                            evaluator()
                            conn.send((", ".join(line) + " [Match Found! FORMAT:(PersonID, Unit 1 Mark, Unit 2 Mark...etc.)]").encode(FORMAT))
                            gradelist = gradelist[:1]
                            print("sliced gradelist from search DB :")
                            print(gradelist)
                            
                            
                            
                            

                        else:
                            print("Not found in DB")
                            """ conn.send("Not found in DB".encode(FORMAT)) """
                
                    

            elif msg == DISCONNECT_MESSAGE:

                if saveToLog == True:
                    send(SAVE_DB_MSG)
                    """ lines = list()
                    with open('studentDB.csv', 'r', newline='') as readFile:
                        reader = csv.reader(readFile)
                        for row in reader:
                            lines.append(row)
                            for field in row:
                                if field == personID:
                                    lines.remove(row)

                    with open('studentDB.csv', 'w') as writeFile:
                        writer = csv.writer(writeFile)
                        writer.writerows(lines)

                    with open('StudentDB.csv', 'a', newline='') as myfile:
                        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                        wr.writerow([int(n) for n in gradelist if n not in ('d', 's', 'e', 'c')])
 """

                     
                 
                

            print(f"[{addr}] {msg}")
            
            gradelist.append(msg)

            if msg != SAVE_DB_MSG:
                send(msg)
           
            print(gradelist)
            conn.send("\n\nMsg received from server 1: ".encode(FORMAT))

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


