import socket
import threading
import time
import random

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
BUFFER = 2048
FORMAT = 'utf-8'

connected = True
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

vector_clock = [0, 0, 0]

def send():
    global vector_clock

    while True:
        print("Before Sending Message : ", vector_clock[0:3])
        vector_clock.append(0)
        data = str(vector_clock)
        
        time.sleep(random.randint(0,3))
        client.send(data.encode(FORMAT))
        time.sleep(5)
        #time.sleep(random.randint(0,10))

def receive():
    global vector_clock
    
    while True:
        updated_time_string = client.recv(BUFFER).decode(FORMAT)
        print("After Sending Message",updated_time_string)
        
        updated_time_list = updated_time_string.strip('][').split(', ')
        received_clock = [int(x) for x in updated_time_list]
        vector_clock = received_clock

def client_process():
    send_message = threading.Thread(target=send)
    send_message.start()

    receive_message = threading.Thread(target=receive)
    receive_message.start()


if __name__ == '__main__':

    client_process()