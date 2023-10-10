#!/usr/bin/env python3

from math import acos
import numpy as np
from functools import reduce
from socket import socket, AF_INET, SOCK_STREAM

#################### PROCEDURES ####################

add = lambda i, j: i + j
sort = lambda arrayA: sorted(arrayA)
foo_function_as_matrix_multiplication = lambda matrixA, matrixB, matrixC: reduce(np.dot, list(map(np.array, [matrixA, matrixB, matrixC])))

####################################################

class RPC_Executer:
    def __init__(self, ip="127.0.0.1", port=8080):
        self.host_address = (ip, port)
        self.buffer_size = 65535
        self.connection_limit = 1024

    def run(self, run_server=True):
        with socket(AF_INET, SOCK_STREAM) as self.socket:
            self.socket.bind(self.host_address)
            self.socket.listen(self.connection_limit)

            while run_server:
                connection, (cip, cport) = self.socket.accept()
                _call = connection.recv(self.buffer_size)
                procedure_call = _call.decode().strip()

                print(f"New connection from {cip}:{cport}")
                print("---")
                print(f"Remote Procedure Call: {procedure_call}")
                reply = str(eval(procedure_call))
                print(f"Reply: {reply}")
                print("\n\n")

                connection.send(reply.encode())
                connection.close()

if __name__ == "__main__":
    server = RPC_Executer()
    server.run()


