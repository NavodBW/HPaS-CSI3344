import socket
import re

HEADER = 64
PORT = 10000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
CALCULATE_MESSAGE = "c"
SAVE_DB_MSG = "s"
SEARCH_DB_MSG = "d"
EVALUATE_EXST_MSG = "e"
SERVER = "localhost"
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print("Welcome to Honours Pre-assessment System!")


#user authentication
def authUser():
    valid_login = False

    while valid_login == False:
        userName = input("\nPlease Enter your Username: ") 
        password = input("Please Enter your Password: ")
        
    
        if userName == 'user' and password == 'password':
            print("Successfully logged in!")
            valid_login = True
            break #they are in, exit loop
        else:
            print("Invalid username And / Or Password! Please try again (Hint: user / password)")
            exit
            

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


    
def validID():

    validPersonID = False

    while validPersonID == False:
        person_ID = str(input("Please enter your 4 digit person ID :"))
        if re.match(r"[0-9][0-9][0-9][0-9]$", person_ID):
            validPersonID = True
            send(person_ID)
            send(SEARCH_DB_MSG)

            evaluateResult = str(input("press e to view if there is an existing result, or press any other key to continue: "))
            if evaluateResult.lower() == "e":
                send(EVALUATE_EXST_MSG)
                exit
        else:
            print("Invalid personID! It should be 4 digits!")
            exit


def savetoStudentDB():

    saveToLog = False

    while saveToLog == False:
        saveprompt = str(input("Press x to escape, Press s if you want to save your results to Database, otherwise press any other key to continue :"))

        if saveprompt.lower() == "s":
            print("Results will be saved to DB")
            send(SAVE_DB_MSG)
            saveToLog == True
            break
        
        if saveprompt.lower() == "x":
            send(DISCONNECT_MESSAGE)
            
            exit()
            

        else:
            print("Results won't be saved to DB")
            saveToLog == True
            break
        

def enterResults():
    gradecounter = 1
    failcounter = 0

    def maxUnitsReached():

        if gradecounter == 31:
            send(CALCULATE_MESSAGE)
        else:
            pass
           
    while gradecounter<31:
        print("Enter unit " + str(gradecounter) +" score: (or press 'c' to cancel)")
        unitscore = input()
        
        if re.match(r"^([1-9]?\d|100)$", unitscore):
            send(unitscore)
            gradecounter +=  1

            maxUnitsReached() 

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


    
    
""" authUser() """
validID()
savetoStudentDB()
enterResults()




send(DISCONNECT_MESSAGE)