import socket
import sys
if (len(sys.argv) != 2):
	print("A valid port must be provided.")
	exit()
serverPort = int(sys.argv[1])
serverName = 'localhost'
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input('Input GET request:')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('From Server:\n', modifiedSentence.decode())
clientSocket.close()

