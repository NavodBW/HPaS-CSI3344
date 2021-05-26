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
import sys

#CSI3344 A3
#Navod Gunasekara - 10513666
#Binara Malshan Hapugoda - 10457933 

#some exception handling stackoverflow.com/questions/779675/stop-python-from-closing-on-error
def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)


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
            print("\nSuccessfully logged in!")
            valid_login = True
            break 
        else:
            print("\nInvalid username And / Or Password! Please try again (Hint: user / password)")
            exit

authUser()           

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
        person_ID = str(input("\nPlease enter your 4 digit person ID :"))
        if re.match(r"[0-9][0-9][0-9][0-9]$", person_ID):
            validPersonID = True
            send(person_ID)
            send(SEARCH_DB_MSG)

            evaluateResult = str(input("\npress 'e' to view if there is an existing result, or press any other key to continue: "))
            if evaluateResult.lower() == "e":
                send(EVALUATE_EXST_MSG)
                exit
        else:
            print("Invalid personID! It should be 4 digits!")
            exit
validID()

def savetoStudentDB():

    saveToLog = False

    while saveToLog == False:
        saveprompt = str(input("\nPress 'x' to escape, \nPress 's' if you want to save new results to Database, \notherwise press any other key to evaluate without saving to database :"))

        if saveprompt.lower() == "s":
            print("\nResults will be saved to DB")
            send(SAVE_DB_MSG)
            saveToLog == True
            break
        
        if saveprompt.lower() == "x":
            send(DISCONNECT_MESSAGE)
            
            exit()
            

        else:
            print("\nResults won't be saved to DB")
            saveToLog == True
            break

savetoStudentDB()

#some counters to keep track of user input 
countattempt = 0    
unitcounter = 1
gradecounter = 1

#function to enter unit results
def enterResults():
    global gradecounter
    global unitcounter
    
    failcounter = 0
     
    #function to send the calculate msg if all 30 units are entered
    def maxUnitsReached():

        if gradecounter == 31:
            send(CALCULATE_MESSAGE)
        else:
            pass
    
    #function to disallow more 2 fail attempts 
    def uptoThreeattempts():
        global countattempt

        if int(unitscore) > 49:
            countattempt = 0

        if int(unitscore) < 50:
            
            global unitcounter
            global gradecounter
            
            
            print("Did you attempt unit " + str(unitcounter) + " again?")
            attempt_again = input("Press Y for Yes, any other key for No: ")

            if attempt_again.lower() == "y":
                countattempt += 1              
                print("please enter the unitscore again!")

            else:
                
                gradecounter +=1
                unitcounter += 1
                if gradecounter == 31:
                    send(CALCULATE_MESSAGE)           
                          
        else:
            pass

    #do not allow more than 30 inputs        
    while gradecounter<31:
        
        print("Enter unit " + str(unitcounter) +" score: (or press 'c' to evaluate)")
        unitscore = input()
        
        #input validation for unitscore
        if re.match(r"^([1-9]?\d|100)$", unitscore):

            uptoThreeattempts()
        
            if countattempt < 3:

                
                send(unitscore)
                gradecounter +=  1
                unitcounter += 1
                
                

                maxUnitsReached() 

                if int(unitscore)<50:
                    gradecounter -=1
                    if unitcounter > 1:
                        unitcounter -= 1
                    failcounter += 1

                    if failcounter > 5:
                        print ("Six or more failed units! DOES NOT QUALIFY FOR HONORS STUDY! Try Masters by course work.")
                        break
            else:
                print("Only two fail grades are allowed. Your input was not sent to the server!")
                               
            #check to see if there is at least 12 unit scores                
        elif unitscore.lower() == CALCULATE_MESSAGE:
            if gradecounter<13:
                print("at least 12 unit scores are required")
            
            else:
                send(CALCULATE_MESSAGE)

                break
            

        else:
            print("Invlaid input. Unit score must be 0-100!")
    
    

enterResults()
send(DISCONNECT_MESSAGE)
input("Press enter to exit")

sys.excepthook = show_exception_and_exit