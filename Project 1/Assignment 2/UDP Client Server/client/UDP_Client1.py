import os
import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4466
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"
CLIENT_DATA_PATH = "client_data"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "LIST":
            client.sendto(cmd.encode(FORMAT), ADDR)

        elif cmd == "REQUEST":
            if len(data) < 2:
                print("Usage: REQUEST <filename>")
                continue

            path = data[1]
            send_data = f"{cmd} {path}"
            client.sendto(send_data.encode(FORMAT), ADDR)

            response, server_address = client.recvfrom(SIZE)
            response = response.decode(FORMAT)
            response_data = response.split("@")

            if response_data[0] == "OK":
                filename = response_data[1]
                contents = response_data[2].encode(FORMAT)
                filepath = os.path.join(CLIENT_DATA_PATH, filename)

                with open(filepath, "wb") as f:
                    f.write(contents )

                print("File downloaded.")
            else:
                print(f"Error: {response_data[1]}")

        elif cmd == "DOWNLOAD":
            if len(data) < 2:
                print("Usage: DOWNLOAD <filename>")
                continue

            path = data[1]
            send_data = f"{cmd} {path}"
            client.sendto(send_data.encode(FORMAT), ADDR)

            file_data, server_address = client.recvfrom(SIZE)
            file_data = file_data.decode(FORMAT)
            file_data = file_data.split("@")

            if file_data[0] == "OK":
                name = file_data[1]
                contents = file_data[2]
                filepath = os.path.join(CLIENT_DATA_PATH, name)

                with open(filepath, "wb") as f:
                    f.write(contents)

                print("File downloaded.")
            else:
                print(f"Error: {file_data[1]}")

        elif cmd == "DELETE":
            if len(data) < 2:
                print("Usage: DELETE <filename>")
                continue

            path = data[1]
            send_data = f"{cmd} {path}"
            client.sendto(send_data.encode(FORMAT), ADDR)

        elif cmd == "RENAME":
            if len(data) < 3:
                print("Usage: RENAME <old_filename> <new_filename>")
                continue

            oldname = data[1]
            newname = data[2]
            send_data = f"{cmd} {oldname} {newname}"
            client.sendto(send_data.encode(FORMAT), ADDR)

        elif cmd == "DISCONNECT":
            client.sendto(cmd.encode(FORMAT), ADDR)
            break

    print("[-] Disconnected from the server")

if __name__ == '__main__':
    main()
