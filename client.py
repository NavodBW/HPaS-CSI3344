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


    
person_ID = str(input("Please enter your person ID :"))
send(person_ID)

gradecounter = 1
failcounter = 0


while gradecounter<31:
    print("Enter unit " + str(gradecounter) +" score: (or press 'c' to cancel)")
    unitscore = input()
    
    if re.match(r"^([1-9]?\d|100)$", unitscore):
        send(unitscore)
        gradecounter +=  1


        if int(unitscore)<50:
            failcounter += 1

            if failcounter > 5:
                print ("DOES NOT QUALIFY FOR HONORS STUDY! Try Masters by course work.")
                break

            """ print("Did you attempt unit " + str(gradecounter) + " again?")
            attempt_again = input("Press Y for Yes, N for No: ")

            if attempt_again.lower() == "y":
                print("please enter the unitscore again!")
                    

           
            elif attempt_again.lower() == "n":
                continue

            else:
                print("Invalid input. Only Y or N is allowed") """

        
       

            

        
    

    elif unitscore.lower() == CALCULATE_MESSAGE:
        if gradecounter<13:
            print("at least 12 unit scores are required")
        
        else:
            send(CALCULATE_MESSAGE)

            break
    else:
        print("Invlaid input. Please try again!")

    
    
    



send(DISCONNECT_MESSAGE)