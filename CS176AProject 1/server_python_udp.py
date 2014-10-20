import socket
import sys

#I used code from http://www.binarytides.com/programming-udp-sockets-in-python/ to help me set up the UDP server
#Specifically, lines 73-91 contain code that I used to set up establish the UDP server. 
#The code from binarytides was a simple tutorial to set up a UDP server and client
#The author: Silver Moon (m00n.silv3r@gmail.com)
 
def executeCommand(command, keyValue, ACKCounter, messageSize):
 splitCommand = command.split("=")

 if (command[0] == '?'): #handles ?key
    key = command[1:]
    for i in keyValue:
       if i[0] == key:
          return (key + '=' + i[1])
    else:
       return (key + '=')

 if (command[0] != "?" and '=' in command): #handles key=value
    keyValue.append((splitCommand[0],splitCommand[1]))
    return("OK")

 if (command == 'list'): #handles list command
    string = ""
    for s in keyValue:
       string += (s[0] + '=' + s[1] + '\n')
    if string == "":
       return "ERROR: List is empty."
    else:
       return string[:-1]

 if (command[:5] == 'listc'): #handles listc num and listc num continuationkey command
    splitListcCommand = command.split() #split the listc command into seperate parts
    if len(splitListcCommand) == 2: #if we have two arguments, it must be listc num command
         string = ''
         if (int(splitListcCommand[1]) > len(keyValue)):
            for i in range(0,len(keyValue)): #if num argument is greater than # of key/value pairs, go through the entire list
               string += (keyValue[i][0] + '=' + keyValue[i][1] + '\n')
            string += "END"
            return string
         else:
            for i in range(int(splitListcCommand[1])):
               string += (keyValue[i][0] + '=' + keyValue[i][1] + '\n')
            string += splitListcCommand[1] #This returns the continuation key to the client after the key/values are printed
            return string
    else:
       string = ''
       if int(splitListcCommand[1]) + int(splitListcCommand[2]) < len(keyValue):
          for i in range(int(splitListcCommand[2]), int(splitListcCommand[1])+1):
             string += (keyValue[i][0] + '=' + keyValue[i][1] + '\n')
          continuationINT = int(splitListcCommand[1]) + int(splitListcCommand[2])
          string += str(continuationINT)
          return string
       else:
          for i in range(int(splitListcCommand[2]),len(keyValue)):
             string += (keyValue[i][0] + '=' + keyValue[i][1] + '\n')
          string += "END"
          return string

def main():

    if (len(sys.argv) != 2):                        #error checking for number of arguments
      print('ERROR: Invalid number of args. Terminating.')
      sys.exit()
    
    port = int(sys.argv[1])
    if (port < int("0") or port > int("65535")):    #checking for valid port number
      print('ERROR: Invalid port. Terminating.')
      sys.exit();

    try: #checking for correct binding
      serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a socket object
      host = 'localhost'                 # Get local machine name
      serverSocket.bind((host, port))              # Bind to the port
    except:
      print("ERROR: Could not bind port. Terminating")
      sys.exit();
    # Bind socket to local host and port
    keyValue = [] #array to store the key/value pairs
    while 1:
    # receive data from client (data, addr)
        d = serverSocket.recvfrom(65535)
        message = d[0].split('_')
        ACKCounter = message[0]
        messageSize = message[1]
        data = message[2]
        addr = d[1]
        value = executeCommand(data,keyValue,ACKCounter,messageSize)
        serverSocket.sendto(value , addr)
    s.close()

if __name__ == "__main__":
   main()

