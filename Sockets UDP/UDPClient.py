from socket import *
servername = '192.168.0.106'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Digite o texto:')
clientSocket.sendto(message.encode(), (servername,serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()