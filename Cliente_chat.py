import threading
from socket import *
import sys

SERVER_IP = input("Digite o IP do servidor: ")
SERVER_PORT = int(input("Digite a porta: "))

client_socket = socket(AF_INET, SOCK_STREAM)

try:
    client_socket.connect((SERVER_IP, SERVER_PORT))
except Exception as e:
    print(f"Não foi possível conectar ao servidor: {e}")
    sys.exit(1)

# Flag para sinalizar encerramento entre threads
encerrado = threading.Event()


def receber():
    """Thread de recebimento: fica ouvindo o servidor continuamente."""
    while not encerrado.is_set():
        try:
            dados = client_socket.recv(1024)
            if not dados:
                print("\nConexão encerrada pelo servidor.")
                encerrado.set()
                break
            print(f"\n{dados.decode()}")
            print("> ", end="", flush=True)  # Reimprime o prompt após a mensagem
        except Exception as e:
            if not encerrado.is_set():
                print(f"\nErro ao receber mensagem: {e}")
            encerrado.set()
            break


# Inicia thread de recebimento em segundo plano
thread_recebimento = threading.Thread(target=receber, daemon=True)
thread_recebimento.start()

# Thread principal: cuida do envio (teclado)
print("Conectado! Digite suas mensagens (FIM para sair):\n")
while not encerrado.is_set():
    try:
        mensagem = input("> ")
        if encerrado.is_set():
            break

        client_socket.send(mensagem.encode())

        if mensagem.strip().upper() == 'FIM':
            encerrado.set()
            break

    except (EOFError, KeyboardInterrupt):
        # Usuário fechou o terminal ou pressionou Ctrl+C
        try:
            client_socket.send("FIM".encode())
        except Exception:
            pass
        encerrado.set()
        break
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        encerrado.set()
        break

client_socket.close()
print("Desconectado.")