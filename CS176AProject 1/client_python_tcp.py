#!/usr/bin/python           # This is client.py file
#Daniel Reinhart CS176A Project 1

import socket               # Import socket module
import sys

#I used code from https://wiki.python.org/moin/TcpCommunication to help me set up the TCP client
#Specifically, lines 16-18 and 38-39 contain code that I used to set up establish communication with the server. 
#the code from this website explains how to write a simple echo server and client
#and was written by the managers of the python wiki page

#I also usec

if (len(sys.argv) != 3):                        #error checking for number of arguments
      print('ERROR: Invalid number of args. Terminating.')
      sys.exit()

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = int(sys.argv[2])             # Reserve a port for your service.
try:
	s.connect((host, port))
except:
	print('ERROR: Could not connect to server. Terminating.')
	sys.exit()

print (s.recv(65535)) #print the initial command
continuationKey = 0;
while(1):	
	command = raw_input()
	if (command == 'help'): #print out the help statement
    		print("?key ---> responds with 'key=value' without the quotes, or 'key=' if not set. \nkey=value ---> sets value for key and returns OK. \nlist ---> returns all key value pairs. \nlistc num ---> returns the first num keys and values, followed by continuation key\nlistc num continuationkey ---> returns first num keys and values after last set of keys/values.\nexit ---> closes the connection")
	if (command == "exit"): #close the socket if we enter exit
		s.close()
		sys.exit()
	if command[0] == "?": #this must be a ?key command
		keyCheck = command.split('=')
		keyCheck[0] += "="
		if "?=" in keyCheck[0] or len(keyCheck) > 2: #check to see if keys contain any ='s signs 
			print('ERROR: Invalid Command.')
		else: #valid ?key command
			s.send(str(command)) #send the command to the server to process it
			print (s.recv(65535)) #print the value returned by the server

	if command == "list" or (command[0] != "?" and '=' in command):
		s.send(str(command))
		print (s.recv(65535))

	if command[:5] == "listc": #check to make sure listc num is correct
		listcCheck = command.split()
		if len(listcCheck) == 2:
			try:
				int(listcCheck[1]) #check if we have valid integer
				s.send(str(command)) #send/reveive data
				data = s.recv(65535)
				print (data) #print data to console
				dataSplit = data.split()
				continuationKey = dataSplit[-1] #the last character in returned data is continuation key
			except:
				print('ERROR: Invalid Command.')
		
		if len(listcCheck) == 3: #we have the listc num continuationKey command
			if continuationKey == listcCheck[2]: #check to make sure we have valid continuation key
				try:
					int(listcCheck[1]) #check if we have integers
					int(listcCheck[2])
					s.send(str(command)) #send/receive data
					data = s.recv(65535)
					print (data) #print the data
					dataSplit = data.split()
					continuationKey = dataSplit[-1] #the last character in the returned data is the continution key
				except:
					print('ERROR: Invalid Command.')
			else:
				print("ERROR: Invalid continuation key.")

	#if none of the if statements are triggered, we have an invalid command
	elif not (command[0] == "?" or command == "list" or (command[0] != "?" and '=' in command) or command == "help" or command[:5] == "listc"):
		print('ERROR: Invalid Command.')
	
s.close()                    # Close the socket when done
