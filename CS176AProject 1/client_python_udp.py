import socket   #for sockets
import sys  #for exit
 
#I used code from http://www.binarytides.com/programming-udp-sockets-in-python/ to help me set up the UDP client
#Specifically, lines 37-39 and lines contain code that I used to set up establish the UDP client. 
#The code from binarytides was a simple tutorial to set up a UDP server and client
#The author: Silver Moon (m00n.silv3r@gmail.com)

def sendReceive(s,command,host,port):
    sizeOfCommand = sys.getsizeof(command) #client is determining the size of the message
    ACKcounter = 0; #acknowledgement counter
    message = str(ACKcounter) + '_' + str(sizeOfCommand) + '_' + command # sprend length,counter, and message to the server
    #chose delimiter to be _ so we can seperate command serverside

    dataDownloaded = 0;
    try:
        s.sendto(message, (host,port))
    except:
        print("ERROR: Failed to send message. Terminating.")
        sys.exit()
    try:
        d = s.recvfrom(2048)
        dataDownloaded += sys.getsizeof(d)
    except:
        print("ERROR: Failed to receive message. Terminating.")
        sys.exit()
    reply = d[0]
    print (reply)
    return d


def main():
    if (len(sys.argv) != 3):                        #error checking for number of arguments
      print('ERROR: Invalid number of args. Terminating.')
      sys.exit()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         # Create a socket object
    host = sys.argv[1] # Get local machine name
    port = int(sys.argv[2])             # Reserve a port for your service.

    while(1) :
        command = raw_input()
        if (command == 'help'): #print out the help statement
            print("?key ---> responds with 'key=value' without the quotes, or 'key=' if not set. \nkey=value ---> sets value for key and returns OK. \nlist ---> returns all key value pairs. \nlistc num ---> returns the first num keys and values, followed by continuation key\nlistc num continuationkey ---> returns first num keys and values after last set of keys/values.\nexit ---> closes the connection")

        if (command == "exit"): #close the socket if we enter exit
            s.close()
            sys.exit()
        if command[0] == "?": #initial check to see if commands are valid
            keyCheck = command.split('=')
            keyCheck[0] += "="
            if "?=" in keyCheck[0] or len(keyCheck) > 2: #check to see if keys contain any = sign re.match(^?\..*=$, keyCheck[0],flags=0)
                print('ERROR: Invalid Command.')
            else:
                sendReceive(s,command,host,port)
        if command == "list" or (command[0] != "?" and '=' in command):
            sendReceive(s,command,host,port)

        if command[:5] == "listc": #check to make sure listc num is correct
            listcCheck = command.split()
            if len(listcCheck) == 2:
                try:
                    int(listcCheck[1])
                    data = sendReceive(s,command,host,port)
                    dataSplit = data[0]
                    continuationKey = dataSplit[-1] #continuation key is the last character in the data we receive
                except:
                    print('ERROR: Invalid Command.')
            
            if len(listcCheck) == 3: #we have the listc num continuationKey command
                if continuationKey == listcCheck[2]: #check to make sure we have valid continuation key
                    try:
                        int(listcCheck[1])
                        int(listcCheck[2])
                        data = sendReceive(s,command,host,port)
                        dataSplit = data[0]
                        continuationKey = dataSplit[-1]
                    except:
                        print('ERROR: Invalid Command.')
                else:
                    print("ERROR: Invalid continuation key.")

        elif not (command[0] == "?" or command == "list" or (command[0] != "?" and '=' in command) or command == "help" or command[:5] == "listc"):
            print('ERROR: Invalid Command.')
    s.close()                    # Close the socket when done

if __name__ == "__main__":
   main()

