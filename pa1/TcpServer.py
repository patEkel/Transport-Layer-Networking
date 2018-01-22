# Written by Patrick Ekel u0736878 for cs 4480 Spring 2018
import socket
import sys
import urllib.parse

if (len(sys.argv) != 2):
	print("A valid port must be provided.")
	exit()

serverPort = int(sys.argv[1])
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind to localhost on the given port
try:
	serverSocket.bind(('localhost', serverPort))
except Exception:
	print("Unable to bind to host.")
	exit()
serverSocket.listen(1)
print('The Server is ready to receive\n')

while True:
	connectionSocket, addr = serverSocket.accept()
	sentence = connectionSocket.recv(1024).decode()
	clientInput =""
	# build request from user, making sure entire request is received
	while '\r\n' != sentence:
		clientInput += sentence
		sentence = connectionSocket.recv(1024).decode()
	clientRequest = clientInput.split(' ')
	# make sure request is a get request
	if 'GET' not in clientRequest:
		errorMessage = 'HTTP/1.0 501 Not Implemented\r\nerror: only GET requests are supported\r\n\r\n'
		connectionSocket.send(errorMessage.encode())
		connectionSocket.close()
		exit()
	# set up connection with remote server		
	
	###
	#print("client request is: ", clientRequest, "\nand parsed client request is: ", urllib.parse.urlparse(clientInput))
	print("scheme is: ", urllib.parse.urlparse(clientInput).scheme)
	print("netloc is: ", urllib.parse.urlparse(clientInput).netloc)
	print("path is: ", urllib.parse.urlparse(clientInput).path)
	print("params are: ", urllib.parse.urlparse(clientInput).params)	
	print("query is: ", urllib.parse.urlparse(clientInput).query)	
	print("fragment is: ", urllib.parse.urlparse(clientInput).fragment)	
	print("port is: ", urllib.parse.urlparse(clientInput).port)	
	print"==============================================\n)
	###
	
	proxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if (len(clientRequest) == 3):
		proxySocket.connect((urllib.parse.urlparse(clientRequest[1]).netloc, 80))
		proxyRequest ='GET ' + urllib.parse.urlparse(clientRequest[1]).path + ' HTTP/1.0\r\nHost: ' + urllib.parse.urlparse(clientRequest[1]).netloc +'\r\n' +'Connection: close' + '\r\n\r\n'
	else:
		newstr = urllib.parse.urlparse(clientRequest[3]).path.replace('\r\n', '')
		proxySocket.connect((newstr, 80))
		proxyRequest ='GET ' + urllib.parse.urlparse(clientRequest[1]).path + ' HTTP/1.0\r\nHost: ' + newstr +'\r\n' +'Connection: close' + '\r\n\r\n'
	
	# forward request to end server, get response back
	proxySocket.send(proxyRequest.encode())
	responseMessage = proxySocket.recv(1024)
	proxySocket.close()

	# send response back to client
	connectionSocket.send(responseMessage)
	connectionSocket.close()

