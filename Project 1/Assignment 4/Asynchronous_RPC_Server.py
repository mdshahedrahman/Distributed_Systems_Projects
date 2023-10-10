import socket
from math import acos
import ast
import numpy as np

IP = socket.gethostbyname(socket.gethostname())
PORT = 4466
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

calculation_results = {}


def add(i, j):
    sum = i + j
    calculation_results.update({"add": sum})


def sort(array):
    sorted_array = sorted(array)
    calculation_results.update({"sorted array": sorted_array})
    return sorted_array


def foo_as_matrix_multiply(matrixA, matrixB, matrixC):
    matrixA = ast.literal_eval(matrixA)
    matrixB = ast.literal_eval(matrixB)
    matrixC = ast.literal_eval(matrixC)

    matrixA_np = np.array(matrixA)
    matrixB_np = np.array(matrixB)
    matrixC_np = np.array(matrixC)

    matrix_multiply = np.matmul(np.matmul(matrixA_np, matrixB_np), matrixC_np)

    calculation_results.update({"foo_as_matrix_multiply": matrix_multiply})


def main():
    print("[+] Asynchronous RPC on Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(5)
    print("[+] Listening...")

    while True:
        conn, addr = server.accept()
        print(f"[+] {addr} connected")
        conn.send("OK@Welcome to the RPC Server.\nPlease type in your desired function (Case sensitive):\n"
                  "1. Find sum of 2 numbers\n"
                  "2. Sort an Array\n"
                  "3. foo_as_matrix_multiply of 3 Matrices\n".encode(FORMAT))

        while True:
            data = conn.recv(SIZE).decode(FORMAT)
            data = data.split("@")
            cmd = data[0]

            if cmd == "1":
                i = float(data[1])
                j = float(data[2])

                conn.send(
                    f"Server has received request to calculate the sum of two numbers {i} and {j}, calculating now.".encode(
                        FORMAT))

                sum = add(i, j)

                conn.recv(SIZE).decode(FORMAT)
                sum = calculation_results["add"]

                send_data = str(sum)
                conn.send(send_data.encode(FORMAT))

            elif cmd == "2":
                array = data[1]
                conn.send(f"Server has received request to sort the array {array}, sorting now.".encode(FORMAT))

                array = array.strip('][').split(', ')

                sort(array)

                conn.recv(SIZE).decode(FORMAT)
                sorted_array = calculation_results["sorted array"]

                send_data = str(sorted_array)
                conn.send(send_data.encode(FORMAT))

            elif cmd == "3":
                matrixA = data[1]
                matrixB = data[2]
                matrixC = data[3]
                conn.send(f"Server has received request to multiply the 3 matrices, multiplying now.".encode(FORMAT))

                foo_as_matrix_multiply(matrixA, matrixB, matrixC)

                conn.recv(SIZE).decode(FORMAT)
                multiplication = calculation_results["matrix multiplication"]

                send_data = str(multiplication)
                conn.send(send_data.encode(FORMAT))

            elif cmd == "DISCONNECT":
                break

        print(f" {addr} disconnected")


if __name__ == "__main__":
    main()