import socket
import threading
import socket

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
BUFFER = 2048
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

vector_clock = [0, 0, 0]
machine_times =[]

def timer_manager(conn, address):
    while True:
        global machine_times,vector_clock
        
        clock_time_string = conn.recv(BUFFER).decode(FORMAT)
        clock_time_list = clock_time_string.strip('][').split(', ')
        
        machine_times = [int(x) for x in clock_time_list]

        machine_num = machine_times[3]
        vector_clock[machine_num] = max(machine_times[machine_num], vector_clock[machine_num])
        vector_clock[machine_num] = vector_clock[machine_num] + 1
        print(f"Vector Clock: {vector_clock}")
        
        send_data = str(vector_clock)
        conn.send(send_data.encode())

def incoming_client_connection():
    while True:
        client_server_connector, addr = server.accept()
        client_address = str(addr[0]) + ":" + str(addr[1])

        print(f"[+] {client_address} connected")

        client_thread = threading.Thread(target=timer_manager, args=(client_server_connector, client_address,))
        client_thread.start()


def server_process():
    server.listen(10)
    print("[+] Server started...")
    
    server_thread = threading.Thread(target=incoming_client_connection, args=())
    server_thread.start()

if __name__ == '__main__':

    server_process()