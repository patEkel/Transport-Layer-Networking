import socket
serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	serverSocket.bind(('localhost', serverPort))
except Exception:
	print('in catch')
serverSocket.listen(1)
print('The Server is ready to receive')
while True:
	connectionSocket, addr = serverSocket.accept()
	sentence = connectionSocket.recv(1024).decode()
	capitalizedSentence = sentence.upper()
	print(capitalizedSentence)
	connectionSocket.send(capitalizedSentence.encode())
	connectionSocket.close()

	# if empy string break loop

