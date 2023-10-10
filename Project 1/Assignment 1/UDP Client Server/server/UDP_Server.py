import os
import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4466
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(ADDR)


def handle_client(data, client_address):

    global server_socket

    cmd, *params = data.split(" ")

    if cmd == "LIST":
        files = os.listdir(SERVER_DATA_PATH)
        send_data = "OK@"

        if len(files) == 0:
            send_data += "The server directory is empty."
        else:
            send_data += "\n".join(files)

        server_socket.sendto(send_data.encode(FORMAT), client_address)

    elif cmd == "REQUEST":
        if len(params) < 1:
            send_data = "ERROR@Invalid request."
            server_socket.sendto(send_data.encode(FORMAT), client_address)
            #return

        name = params[0]
        #contents = " ".join(params[1:])
        filepath = os.path.join(SERVER_DATA_PATH, name)

        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                contents = f.read()
            filename = os.path.basename(filepath)
            send_data = f"OK@{filename}@{contents.decode(FORMAT)}"
        else:
            send_data = "ERROR@File not found."

        server_socket.sendto(send_data.encode(FORMAT), client_address)

    elif cmd == "DOWNLOAD":
        if len(params) < 1:
            send_data = "ERROR@Invalid request."
            server_socket.sendto(send_data.encode(FORMAT), client_address)
            return

        path = params[0]
        filepath = os.path.join(SERVER_DATA_PATH, path)

        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                contents = f.read()
            filename = os.path.basename(path)
            send_data = f"OK@{filename}@{contents}"
        else:
            send_data = "ERROR@File not found."

        server_socket.sendto(send_data.encode(FORMAT), client_address)

    elif cmd == "RENAME":
        if len(params) < 2:
            send_data = "ERROR@Invalid request."
            server_socket.sendto(send_data.encode(FORMAT), client_address)
            return

        oldname = params[0]
        newname = params[1]
        oldname_absolute = os.path.join(SERVER_DATA_PATH, oldname)
        newname_absolute = os.path.join(SERVER_DATA_PATH, newname)

        if os.path.exists(oldname_absolute):
            os.rename(oldname_absolute, newname_absolute)
            send_data = f"OK@File renamed to {newname}"
        else:
            send_data = "ERROR@File not found."

        server_socket.sendto(send_data.encode(FORMAT), client_address)


def main():
    print("[+] UDP Server is starting...")
  #  server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   # server_socket.bind(ADDR)
    print("[+] Started Listening...")

    while True:
        data, client_address = server_socket.recvfrom(SIZE)
        data = data.decode(FORMAT)
        handle_client(data, client_address)


if __name__ == "__main__":
    main()
