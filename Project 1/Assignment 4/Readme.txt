How to run the program:
-----------------------
Before running the program, the machine must have numpy installed. Numpy can be installed using the following command from the Ubuntu terminal.

pip install numpy

Once numpy has been installed, we can activate the server by navigating to the assignment directory and activate ther server using the command:

python3 server.py

Then, the client can be activated by opening another terminal in the same directory and using the command:

python3 client.py

Performing the client functionalities:
---------------------------------------
The server, once activated, listens for the client requests to connect to the server and when the client is activated, it connects to the server. When the client connects, the server shows the actions the client can take:

1. Add two numbers - To choose this option, the user must input "1" and press enter. The client then asks the user to input the first number to be1 added and then the second number. The client then sends the two numbers to the server for addition while it moves on to other tasks which we have shown in the form of a loop here. While the loop runs, we try to show that the client is busy with some work when the server is performing the computation. Then when the loop ends, the client is ready for the value and then queries the server for the result and displays it. 

2. Sort an array - To choose this option, the user must input "2" and press enter. The client then asks the user to input the size of the array to be sorted. The client then asks the user to input the values of the array to be sorted. Once all the values have been entered, the client sends the array to the server for sorting while it moves on to other tasks which we have shown in the form of a loop here. While the loop runs, we try to show that the client is busy with some work when the server is performing the computation. Then when the loop ends, the client is ready for the value and then queries the server for the result and displays the sorted array.  

3. foo_as_matrix_multiply of 3 Matrices - To choose this option, the user must input "3" and press enter. The client then asks the user to input the rows of the first matrix, columns of the first matrix and then the row-wise values of the first matrix. It then moves on to the second and third matrices in the same manner. Once all the values have been input, then the client sends the values to the server for multiplication and moves on to its other tasks which we have shown in the form of a loop here. While the loop runs, we try to show that the client is busy with some work when the server is performing the computation. Then when the loop ends, the client is ready for the value and then queries the server for the result of the matrix multiplication and displays it. 

