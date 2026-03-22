from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print("O servidor está ativo")
while True:
    connectionSocket, addr = serverSocket.accept()
    print("Conexão estabelecida com", addr) 
    while True:
        sentence = connectionSocket.recv(1024).decode()
        print("Mensagem recebida:", sentence)
        if sentence == 'FIM':
            connectionSocket.send("Conexao encerrada".encode())
            print("Conexão encerrada")
            break
        else:
            connectionSocket.send("Mensagem recebida com sucesso".encode())
    connectionSocket.close()