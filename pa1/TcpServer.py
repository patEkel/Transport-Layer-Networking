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
	clientRequest = sentence.split(' ')
	print('client request is', clientRequest)	
	# do check for 3 itms, first get last something specific
	if (len(clientRequest) < 3): # decent if check?
		connectionSocket.send("failed request".encode())
		#connectionSocket.close()
		
	proxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#proxySocket.connect(('cs.utah.edu/~kobus/simple.html', 80))
	proxySocket.connect(('cs.utah.edu', 80))
	proxyRequest ='GET /~kobus/simple.html HTTP/1.0\r\nHost: cs.utah.edu\r\n\r\n'
	print('proxy request is:\n', proxyRequest)
	proxySocket.send(proxyRequest.encode())
	responseMessage = proxySocket.recv(1024)
	print('From utah.edu:\n', responseMessage.decode())
	#proxySocket.close()
	
	#endConnectionSocket, endAddr = serverSocket.accept() #port should be 80
	connectionSocket.send(clientRequest[0].encode())
	connectionSocket.send(clientRequest[1].encode())
	connectionSocket.send(clientRequest[2].encode())
	connectionSocket.close()
	# if empy string break loop
