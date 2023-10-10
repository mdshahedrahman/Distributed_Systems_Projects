#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM

class RPC_Caller:
    def __init__(self, ip="127.0.0.1", port=8080):
        self.host_address = (ip, port)
        self.buffer_size = 65535
        self.connection_limit = 1024

    def call(self, procedure, args):
        with socket(AF_INET, SOCK_STREAM) as self.socket:
            self.socket.connect(self.host_address)

            procedure_call = "{}({})".format(procedure, args)
            self.socket.send(procedure_call.encode())

            print(procedure_call + ":")
            print(self.socket.recv(self.buffer_size).decode(), "\n")


if __name__ == "__main__":
    _client = RPC_Caller()

    # add - RPC
    i, j = 1, 2
    _client.call("add", f"{i}, {j}")

    # sort - RPC
    arrayA = [3, 5, 2, 1, 4]
    _client.call("sort", str(arrayA))

    # matrix_multiply - RPC
    matrixA = [[1, 2, 3],
               [4, 5, 6],
               [7, 8, 9]]

    matrixB = [[10, 11, 12],
               [13, 14, 15],
               [16, 17, 18]]

    matrixC = [[19, 20, 21],
               [22, 23, 24],
               [25, 26, 27]]

    _client.call("foo_function_as_matrix_multiplication", f"{matrixA}, {matrixB}, {matrixC}")
