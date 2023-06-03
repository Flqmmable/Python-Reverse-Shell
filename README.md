**How to use the script:**

1. Install all files.
2. Install required Python modules with the "pip3 install -r requirements.txt" command.
3. Run the "server.py" file and modify socket settings via the "Socket Settings" option.
4. Select the "Listen" option to start listening on the specified socket.
5. In the "client.py" file, modify the host and port variables according to the socket settings you specified in step 3.
6. Once run, the "client.py" file will connect to the target machine via the listening socket.



**Additional notes:**

1. Make sure that your firewall isn't blocking the connection to your device.
2. To enable this script will work remotely (on different networks), you will need to utilize port forwarding on your router or setting up a VPS and running it from there.
