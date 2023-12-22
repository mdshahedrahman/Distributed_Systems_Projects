#!/usr/bin/env python3

import os
import json
from sys import stderr
from random import randint
from socket import socket, AF_INET, SOCK_STREAM

N = 3
nodes = {f"node_{i}": ("127.0.0.1", 8080 + i) for i in range(1, N + 1)}
shared_dir = os.path.join(os.getcwd(), "shared_directory/")

if __name__ == "__main__":
    while True:
        node_id = input("NODE ID: ")
        if node_id == "exit":
            break
        transaction = {'id': None,
                       'action': None,
                       'status': None,
                       'filename': None,
                       'node_address': None,
                       'client_address': None}
        while True:
            if node_id in nodes.keys():
                command = input("> ").split()
                if command[0] == "ls":
                    print("\n".join(os.listdir(shared_dir)))
                    continue
                elif command[0] == "end":
                    print(f":EOS <{node_id}>")
                    break
                with socket(AF_INET, SOCK_STREAM) as sock:
                    sock.connect(nodes[node_id])
                    transaction['id'] = randint(1000, 9999)
                    transaction['node_address'] = nodes[node_id]
                    transaction['client_address'] = tuple(sock.getsockname())
                    if command[0] in ["lock", "unlock"]:
                        transaction['action'] = command[0]
                        transaction['filename'] = command[1]
                        sock.send(json.dumps(transaction).encode())
                        print(sock.recv(65535))
                    else:
                        print("\n\t", "[WARNING] -", f"Command <{command[0]}> not found", "\n")
            else:
                print("[ERROR] -", f"<{node_id}> not found", "\n", file=stderr)
                print(f"Available nodes: {nodes.keys()}")
                break
