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
    print(f"[+] {addr} Client connected")
    conn.send(
        "OK@Welcome to the Single Thread Web Server."
        "\nPlease type in your desired function (Case sensitive):\n"
        "# LIST - to see the list of images in the web server\n"
        "# RENAME <filename> - to rename a image file on the server\n"
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
                send_data += "The file is not available in the server directory."
            else:
                send_data += "\n".join(f for f in files)
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
    print("[+] Single Thread Server in TCP is starting.....")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[+] Started Listening...")

    while True:
        conn, add = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, add))
        thread.start()


if __name__ == "__main__":
    main()