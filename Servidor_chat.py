import threading
from socket import *

HOST = '192.168.0.106'
PORT = 12000

clientes = {}
lock = threading.Lock()

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)
print(f"Servidor ativo na porta {PORT}. Aguardando conexões...")


def broadcast(mensagem, remetente=None):
    """Envia mensagem para todos os clientes conectados, exceto o remetente."""
    with lock:
        destinos = list(clientes.items())
    for nome, sock in destinos:
        if nome != remetente:
            try:
                sock.send(mensagem.encode())
            except Exception:
                pass


def handle_client(conn, addr):
    """Thread de trabalho dedicada a cada cliente."""
    nome = None
    try:
        # Solicita o nome do cliente
        conn.send("Digite seu nome: ".encode())
        nome = conn.recv(1024).decode().strip()

        # Verifica se o nome já está em uso
        with lock:
            if nome in clientes:
                conn.send(f"Nome '{nome}' já está em uso. Conexão encerrada.".encode())
                conn.close()
                return
            clientes[nome] = conn

        print(f"[+] {nome} entrou no chat. (Total: {len(clientes)})")
        conn.send(f"Bem-vindo ao chat, {nome}! Use /p <nome> <msg> para mensagem privada.".encode())
        broadcast(f"*** {nome} entrou no chat! ***", remetente=nome)

        # Loop de recebimento de mensagens
        while True:
            try:
                dados = conn.recv(1024)
                if not dados:
                    break

                mensagem = dados.decode().strip()

                # Encerramento voluntário
                if mensagem.upper() == 'FIM':
                    break

                # Mensagem privada: /p <destino> <texto>
                if mensagem.startswith('/p '):
                    partes = mensagem.split(' ', 2)
                    if len(partes) < 3:
                        conn.send("Uso correto: /p <nome_destino> <mensagem>".encode())
                        continue

                    destino = partes[1]
                    texto = partes[2]

                    with lock:
                        sock_destino = clientes.get(destino)

                    if sock_destino is None:
                        conn.send(f"Usuário '{destino}' não encontrado.".encode())
                    else:
                        try:
                            sock_destino.send(f"[Privado de {nome}]: {texto}".encode())
                            conn.send(f"[Privado para {destino}]: {texto}".encode())
                        except Exception:
                            conn.send(f"Erro ao enviar mensagem privada para '{destino}'.".encode())
                else:
                    # Broadcast para todos
                    print(f"[{nome}]: {mensagem}")
                    broadcast(f"[{nome}]: {mensagem}", remetente=nome)

            except Exception as e:
                print(f"Erro ao receber mensagem de {nome}: {e}")
                break

    except Exception as e:
        print(f"Erro na conexão com {addr}: {e}")
    finally:
        # Remove cliente e notifica os demais
        if nome:
            with lock:
                clientes.pop(nome, None)
            print(f"[-] {nome} saiu do chat. (Total: {len(clientes)})")
            broadcast(f"*** {nome} saiu do chat. ***")
        try:
            conn.close()
        except Exception:
            pass


# Thread principal: aceita conexões indefinidamente
while True:
    try:
        conn, addr = server_socket.accept()
        print(f"Nova conexão de {addr}")
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        break

server_socket.close()