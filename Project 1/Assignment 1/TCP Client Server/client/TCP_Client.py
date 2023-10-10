import os
import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4466
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"
CLIENT_DATA_PATH = "client_data"


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")

        if cmd == "OK":
            print(f"{msg}")
        elif cmd == "DISCONNECT":
            print(f"{msg}")
            break

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "LIST":
            client.send(cmd.encode(FORMAT))

        elif cmd == "RENAME":
            client.send(f"{cmd}@{data[1]}@{data[2]}".encode(FORMAT))

        elif cmd == "DISCONNECT":
            client.send(cmd.encode(FORMAT))
            break

    print("[-] Disconnected from the server")
    client.close()


if __name__ == '__main__':
    main()