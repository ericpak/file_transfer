# Eric Pak
# CSCE 365 Computer Networks
# Dr. Shawn Butler
# File Transfer Assignment

import socket
import threading
import os
import sys

# Global variable for buffer size
bufferSize = 1024

# Creates and returns a socket
def createSocket(p):
    port = p
    s = socket.socket()
    s.bind(('', port))
    s.listen(5)
    print ("Server Started")
    return s

# While the user is connected gets the users next command
def RetrCmd(name, c):
    while True:
        filename = c.recv(bufferSize).decode()
        if filename[:4] == 'list':
            sendList(c)
        elif filename[:4] == 'get ':
            print("filename: " + filename[4:])
            if os.path.isfile(filename[4:]):
                c.send(str.encode("exists" + str(os.path.getsize(filename[4:]))))
                userResponse = c.recv(bufferSize).decode()
                if userResponse[:3] == 'yes':
                    sendData(c, filename)
            else:
                c.send(str.encode("error"))
        elif filename[:4] == 'exit':
            c.close()
            break

# Sends a list of files at the server.py directory to the user
def sendList(c):
    dirList = os.listdir(path='.')
    c.send(str.encode(str(dirList)))

# Sends data to the user
def sendData(c, filename):
    with open(filename[4:], 'rb') as file:
        bytesToSend = file.read(bufferSize)
        c.send(bytesToSend)
        while bytesToSend:
            bytesToSend = file.read(bufferSize)
            c.send(bytesToSend)
            
# Allows he server to accept multiple users
def multiThread(s):
    while True:
        c, addr = s.accept()
        print("Client connected ip:<" + str(addr) + ">")
        t = threading.Thread(target=RetrCmd, args=("retrThread", c))
        t.start()
    s.close()

# The Main function that calls the other functions
def Main(portNumber):
    s = createSocket(portNumber)
    multiThread(s)
    
#~~~~ Main ~~~~#
if __name__ == '__main__':
    # Default port number is 5000 if no arguments are made
    if len(sys.argv) == 1:
        Main(5000)
    # If one argument is made then cast it as an int and set it as the port number
    elif len(sys.argv) == 2:
        Main(int(sys.argv[1]))