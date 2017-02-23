# Eric Pak
# CSCE 365 Computer Networks
# Dr. Shawn Butler
# File Transfer Assignment

import socket
import sys

# Global variable for buffer size
bufferSize = 1024

# Creates and returns a socket
def createSocket(h, p):
    host = h
    port = p
    s = socket.socket()
    s.connect((host,port))
    return s

# The terminal user interface that sends the command to the server
def userCmd(s):
    while True:
        userInput = input("Enter cmd (get/list/exit): ")
        if userInput == 'exit':
            s.send(userInput.encode('utf-8'))
            break
        elif userInput == 'list':
            s.send(userInput.encode('utf-8'))
            data = s.recv(bufferSize)
            print(data)
        elif userInput[:4] == 'get ':
            s.send(userInput.encode('utf-8'))
            data = s.recv(bufferSize).decode('utf-8')
            if data[:6] == 'exists':
                filesize = int(data[6:])
                message = input("Sending " + userInput[4:] + ' ' + str(filesize) + " bytes, download? (y/n)? ")
                if message == 'y':
                    s.send(str.encode('yes'))
                    recvData(userInput, s, filesize)
                else:
                    s.send(str.encode('no'))
            else:
                print("File does not Exist!")
        else:
            print("Command not recognized")
        print("") # For readability
                
# Function that recieves the data
def recvData(userInput, s, filesize):
    f = open(userInput, 'wb')
    totalRecv = 0
    while totalRecv < filesize:
        data = s.recv(bufferSize)
        totalRecv += len(data)
        f.write(data)
        # Prints the percentage of the download complete but it just looks messy
        #print ("{0:.2f}".format((totalRecv/float(filesize))*100) +"% Done")
    print("Download Complete!")    

# The Main function that calls the other functions
def Main(host, portNumber):
    s = createSocket(host, portNumber)
    userCmd(s)
    s.close()

#~~~~ Main ~~~~#
if __name__ == '__main__':
    # Get server ip from user
    host = input("Enter server Ip address: ")
    
    # Default port number is 5000 if no arguments are made
    if len(sys.argv) == 1:
        Main(host, 5000)
        
    # If one argument is made then cast it as an int and set it as the port number
    elif len(sys.argv) == 2:
        Main(host, int(sys.argv[1]))