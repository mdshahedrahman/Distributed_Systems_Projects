How to Run the program:
------------------------
There must be two terminals running simultaneously. On terminal should be at the server directory and another should be at the client directory.

You can activate the server by running the command 
python3 TCP_Single_Thread_Server.py

You can activate the client by running the command
python3 TCP_Client.py

Performing the client functionalities: 
---------------------------------------
1. Type LIST to view all the available files in the server, 

2. For Rename, the client can enter an additional command called LIST which will show the client a list of all the files available at the server. The client can then enter the command RENAME <old_filename> <new_filename> (ex. RENAME serverFile.txt newServerFile.txt) to rename the file. The file will be renamed at the server.
The file to be renamed must exist on the “server_data” folder of the server; otherwise, there will be a “No file found” message, and no file will be renamed.

3. At the end, the client can enter the command DISCONNECT which will close the socket connection and leave the server free to accept other clients. Since this is a single-threaded server, the server can only perform tasks for one client at a time. If multiple clients try to connect to the server, they will be left in a queue and can only be served when the earlier machine has disconnected from the server.

