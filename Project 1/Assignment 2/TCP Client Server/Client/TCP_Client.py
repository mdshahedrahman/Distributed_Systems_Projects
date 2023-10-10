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

        elif cmd == "REQUEST":
            path = data[1]

            filepath = os.path.join(CLIENT_DATA_PATH, path)
            with open(f"{filepath}", "r") as f:
                contents = f.read()
            filename = path.split("/")[-1]
            send_data = f"{cmd}@{filename}@{contents}"

            client.send(send_data.encode(FORMAT))

        elif cmd == "DOWNLOAD":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))

            file_data = client.recv(SIZE).decode(FORMAT)
            file_data = file_data.split("@")

            name = file_data[1]
            contents = file_data[2]
            filepath = os.path.join(CLIENT_DATA_PATH, name)

            with open(filepath, "w") as f:
                f.write(contents)

            print("File downloaded.")

        elif cmd == "DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))

        elif cmd == "RENAME":
            client.send(f"{cmd}@{data[1]}@{data[2]}".encode(FORMAT))

        elif cmd == "DISCONNECT":
            client.send(cmd.encode(FORMAT))
            break

    print("[-] Disconnected from the server")
    client.close()


if __name__ == '__main__':
    main()