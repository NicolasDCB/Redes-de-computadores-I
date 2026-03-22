from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print("O servidor está ativo")
while True:
    connectionSocket, adrr = serverSocket.accept()
    while True:
     sentence = connectionSocket.recv(1024).decode()
     if sentence == 'FIM':
            sentence = "Conexao encerrada"
            connectionSocket.send(sentence.encode())
            break
     else:
      capitalizedSentence = sentence.upper()
      connectionSocket.send(capitalizedSentence.encode())

    connectionSocket.close()
