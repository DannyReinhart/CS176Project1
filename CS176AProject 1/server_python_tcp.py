#!/usr/bin/python           # This is server.py file
#Daniel Reinhart CS176A Project 1

#I used code from https://wiki.python.org/moin/TcpCommunication to help me set up the TCP server
#Specifically, lines 67-86 contain code that came directly from the website. 
#the code from this website explains how to write a simple echo server and client
#and was written by the managers of the python wiki page


import sys                  # Import sys
import socket               # Import socket module

#takes the error checked command from client and keyValue data structure (array) and executes the appropriate command
def executeCommand(command, keyValue): 
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
         return string[:-1] #removes unneeded newline character

   if (command[:5] == 'listc'): #handles listc num and listc num continuationkey command
      splitListcCommand = command.split() #split the listc command into seperate parts ex. listc 1 -> ['listc','1']
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
      else: #otherwise, this must be the listc num continuationKey command
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

#the main loop!
def main():

   if (len(sys.argv) != 2):                        #error checking for number of arguments
      print('ERROR: Invalid number of args. Terminating.')
      sys.exit()

   port = int(sys.argv[1]) # take the port argument 
   
   if (port < int("0") or port > int("65535")):    #checking for valid port number
      print('ERROR: Invalid port. Terminating.')
      sys.exit();
   try:                                            # checking for correct binding
      serverSocket = socket.socket()               # Create a socket object
      host = socket.gethostname()                  # Get local machine name
      serverSocket.bind((host, port))              # Bind to the port
   except:
      print("ERROR: Could not bind port. Terminating")
      sys.exit();
   
      
   keyValue = [] #array to store the key/value pairs
   serverSocket.listen(5) # Now wait for client connection.      
   while True:   
      client, addr = serverSocket.accept()     # Establish connection with client.
      client.sendall('Connected.')
      while True:
         data = client.recv(65535) #receives data from client
         if not data:
            break
         value = executeCommand(data,keyValue) #execute the appropriate command and return string to send back to client
         client.sendall(str(value)) #send message back to client

if __name__ == "__main__":
   main()

         




   
