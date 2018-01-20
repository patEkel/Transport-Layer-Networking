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
	print("patrick")
	connectionSocket, addr = serverSocket.accept()
	sentence = connectionSocket.recv(1024).decode()
	clientRequest = sentence.split(' ')
	# do check for 3 itms, first get last something specific

	endConnectionSocket, endAddr = serverSocket.accept() #port should be 80
	endSentence = endConnectionSocket.recv(1024).decode()
	
	#connectionSocket.send(capitalizedSentence.encode())
	connectionSocket.send(clientRequest[0].encode())
	connectionSocket.send(clientRequest[1].encode())
	connectionSocket.send(clientRequest[2].encode())
	connectionSocket.send(clientRequest[3].encode())
	connectionSocket.send(clientRequest[4].encode())
	connectionSocket.close()
	# if empy string break loop
