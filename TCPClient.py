from socket import *
serverName = input("Digite o IP do servidor: ")
serverPort = int(input("Digite a porta: ")) 
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
while True:
    sentence = input("Escreva a frase: ")
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024)
    print("Do servidor:",modifiedSentence.decode())
    if sentence == 'FIM':
        break
clientSocket.close()