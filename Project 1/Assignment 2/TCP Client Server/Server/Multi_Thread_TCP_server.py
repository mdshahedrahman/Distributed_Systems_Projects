import os
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 4466
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"


def handle_client(conn, addr):
    print(f"[+] {addr} connected")
    conn.send(
        "OK@Welcome to the Web Server.\nPlease type in your desired function (Case sensitive):\n"
        "# LIST - to see the list of files in the server\n"
        "# REQUEST <filename> - to upload a file to the server\n"
        "# RENAME <filename> - to rename a file on the server\n"
        "# DISCONNECT - to disconnect from the server\n".encode(
            FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        if cmd == "LIST":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The server directory is empty."
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == "REQUEST":
            name = data[1]
            contents = data[2]

            filepath = os.path.join(SERVER_DATA_PATH, name)
            with open(filepath, "w") as f:
                f.write(contents)

            send_data = "OK@File Uploaded."

            conn.send(send_data.encode(FORMAT))

        elif cmd == "DOWNLOAD":
            send_data = ''

            path = data[1]
            filepath = os.path.join(SERVER_DATA_PATH, path)

            files = os.listdir(SERVER_DATA_PATH)
            if len(files) == 0:
                send_data += "The server directory is empty."
            else:
                if path in files:
                    with open(f"{filepath}", "r") as f:
                        contents = f.read()
                    filename = path.split("/")[-1]

                    send_data += f"{cmd}@{filename}@{contents}"

                else:
                    send_data += "File not found."

            conn.send(send_data.encode(FORMAT))

        elif cmd == "DELETE":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]

            if len(files) == 0:
                send_data += "The server directory is empty."
            else:
                if filename in files:
                    os.system(f"rm {SERVER_DATA_PATH}/{filename}")
                    send_data += "File deleted."
                else:
                    send_data += "File not found."

            conn.send(send_data.encode(FORMAT))

        elif cmd == "RENAME":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            oldname = data[1]
            newname = data[2]
            file_directory = os.getcwd()
            oldname_absolute = os.path.join(file_directory, SERVER_DATA_PATH, oldname)
            newname_absolute = os.path.join(file_directory, SERVER_DATA_PATH, newname)

            if len(files) == 0:
                send_data += "The server directory is empty."
            else:
                if oldname in files:
                    os.rename(oldname_absolute, newname_absolute)
                    send_data += "File renamed to " + newname
                else:
                    send_data += "File not found."

            conn.send(send_data.encode(FORMAT))

        elif cmd == "DISCONNECT":
            break

    print(f" {addr} disconnected")


def main():
    print("[+] Multi-Threaded TCP Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[+] Listening...")

    while True:
        conn, add = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, add))
        thread.start()


if __name__ == "__main__":
    main()