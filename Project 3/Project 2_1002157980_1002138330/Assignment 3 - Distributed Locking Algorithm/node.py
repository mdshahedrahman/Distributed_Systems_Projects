import os
import json
from sys import stderr
from threading import Thread
from random import getrandbits

from socket import AF_INET, SOCK_STREAM
from socket import SOL_SOCKET, SO_REUSEADDR
from socket import socket

class Node:
    def __init__(self, node_id: str, hostaddr: str, port: int, directory: str, nodes: list):
        self.node_id = node_id
        self.hostaddr = hostaddr
        self.port = port
        self.fspath = os.path.join(os.getcwd(), directory)
        # self.config_file = self.init_config()
        self.address = (self.hostaddr, self.port)
        self.buffer_size = 65535
        self.connection_limit = 500
        self.nodes = nodes

    # def init_config(self, config_name='.config.json'):
    #     file_count_map = {fname: 0 for fname in os.listdir(self.fspath)}
    #     if not os.path.exists(os.path.join(self.fspath, config_name)):
    #         with open(file=config_name, mode="w") as fhand:
    #             fhand.write(json.dumps(file_count_map, indent=4))
    #     return config_name

    def listen(self):
        with socket(AF_INET, SOCK_STREAM) as self.socket:
            self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            self.socket.bind(self.address)
            self.socket.listen(self.connection_limit)
            print("[+]", f"[{self.node_id.upper()}] serving at {self.hostaddr}:{self.port}", "\n")
            while True:
                client, client_address = self.socket.accept()
                print(f"=> New connection from {client_address[0]}:{client_address[1]}")
                request = client.recv(self.buffer_size)
                try:
                    transaction = json.loads(request.decode())
                    transaction['node_address'] = self.address
                    print("[NEW]", transaction)
                    Thread(target=self.process_transaction, args=[transaction, client]).start()
                except Exception as ex:
                    print("[ERROR] -", "Unable to process transaction", file=stderr)
                    print(f"Transaction: {request.decode()}")
                    print(ex, file=stderr)
                    continue

    def process_transaction(self, transaction: dict, client: object) -> None:
        ready = bool(getrandbits(1))
        if ready:
            if transaction['action'] == 'lock':
                transaction['status'] = 'success'
                transaction['message'] = f'locked {transaction.get("filename")}'
                self.__lock(transaction['filename'])
            elif transaction['action'] == 'unlock':
                transaction['status'] = 'success'
                transaction['message'] = f'unlocked {transaction.get("filename")}'
                self.__unlock(transaction['filename'])
            else:
                transaction['status'] = 'failed'
                transaction['message'] = f'unknown action - {transaction.get("action")}'
            client.send(json.dumps(transaction).encode())
        else:
            done = False
            for node in self.nodes:
                done = self._forward_transaction(transaction, node)
                if done: # transaction success in forwarded node
                    transaction['status'] = 'success'
                    transaction['message'] = f"{transaction['action']}ed <transaction['filename']>"
                    client.send(json.dumps(transaction).encode())
                    break
            if not done: # feedback-mechanism (recursive)
                self.process_transaction(transaction, client)
        print("\n") # gap for console-log between each transaction
        client.close()

    def _forward_transaction(self, transaction: dict, node: object) -> bool:
        with socket(AF_INET, SOCK_STREAM) as neighbour:
            neighbour.connect(node)
            neighbour.send(json.dumps(transaction).encode())
            response = json.loads(neighbour.recv(self.buffer_size).decode())
        return True if response['status'] == 'success' else False

    def __lock(self, filename: str) -> bool:
        try:
            with open(file=os.path.join(self.fspath, filename), mode='r') as fhand:
                contents = json.loads(fhand.read())
            with open(file=os.path.join(self.fspath, filename), mode='w') as fhand:
                if contents['status'] != 'locked':
                    contents['status'] = 'locked'
                    contents['counter'] = int(contents['counter']) + 1
                    fhand.seek(os.SEEK_SET)
                    fhand.write(json.dumps(contents) + "\n")
                    fhand.truncate()
                    os.chmod(os.path.join(self.fspath, filename), 0o444)
                    print("\t", f"{filename} locked")
        except Exception as ex:
            print("[ERROR] -", f"Unable to acquire lock for <{filename}>", file=stderr)
            print(ex, file=stderr)
            return False
        return True

    def __unlock(self, filename: str) -> bool:
        try:
            os.chmod(os.path.join(self.fspath, filename), 0o644)
            with open(file=os.path.join(self.fspath, filename), mode='r') as fhand:
                contents = json.loads(fhand.read())
            with open(file=os.path.join(self.fspath, filename), mode='w') as fhand:
                if contents['status'] != 'unlocked':
                    contents['status'] = 'unlocked'
                    fhand.seek(os.SEEK_SET)
                    fhand.write(json.dumps(contents) + "\n")
                    fhand.truncate()
                    print("\t", f"{filename} unlocked")
                else:
                    print("[WARNING] -", f"{filename} not locked! No need to unlock specially.")
        except Exception as ex:
            print("[ERROR] -", f"Unable to unlock <{filename}>", file=stderr)
            print(ex, file=stderr)
            return False
        return True
