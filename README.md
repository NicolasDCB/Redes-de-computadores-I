# Redes de Computadores I

Trabalhos práticos da disciplina de Redes de Computadores I, abordando comunicação via sockets TCP e UDP em Python.

---

## 📁 Estrutura do Repositório

```
Redes-de-computadores-I/
├── Trabalho de Redes TCP/
│   ├── TCPServer.py
│   └── TCPClient.py
└── Trabalho de Redes UDP/
    ├── UDPServer.py
    └── UDPClient.py
```

---

## Trabalho 1 — Sockets TCP (Comunicação Sequencial)

### Objetivo
Compreender o ciclo de vida de uma conexão de rede e a natureza **síncrona (Stop-and-Wait)** entre cliente e servidor.

O servidor é **iterativo**: atende um cliente por vez, do início ao fim, antes de estar disponível para o próximo.

### Como funciona

**Servidor (`TCPServer.py`)**
- Cria um socket TCP (`AF_INET`, `SOCK_STREAM`)
- Faz o `bind` na porta `12000`
- Aguarda conexões com `listen` e `accept`
- Recebe mensagens em loop e responde com `"Mensagem recebida com sucesso"`
- Ao receber `"FIM"`, encerra a conexão e volta a aguardar um novo cliente

**Cliente (`TCPClient.py`)**
- Solicita o IP e porta via `input()`
- Conecta ao servidor com `connect`
- Envia mensagens e aguarda a confirmação a cada envio (comportamento síncrono)
- Ao digitar `"FIM"`, encerra a conexão

### Como executar

```bash
# Terminal 1 — inicie o servidor
python TCPServer.py

# Terminal 2 — inicie o cliente
python TCPClient.py
```

### Conceitos demonstrados

| Termo | O que faz |
|-------|-----------|
| `socket` | Cria o endpoint de comunicação |
| `bind` | Reserva a porta no sistema operacional |
| `listen` | Coloca o servidor em modo de espera |
| `accept` | Aceita a conexão de um cliente |
| `connect` | Conecta o cliente ao servidor |

---

## Trabalho 2 — Sockets UDP (Comunicação sem Conexão)

### Objetivo
Compreender a comunicação **sem conexão** (connectionless) e a diferença em relação ao TCP.

Ao contrário do TCP, o UDP **não garante entrega, ordem ou integridade** dos pacotes — é mais simples e rápido.

### Como funciona

**Servidor (`UDPServer.py`)**
- Cria um socket UDP (`AF_INET`, `SOCK_DGRAM`)
- Faz o `bind` na porta definida
- Aguarda mensagens com `recvfrom` (que também retorna o endereço do remetente)
- Responde diretamente ao endereço do cliente com `sendto`

**Cliente (`UDPClient.py`)**
- Cria um socket UDP sem precisar de `connect`
- Envia mensagens diretamente com `sendto`
- Aguarda resposta com `recvfrom`

### Como executar

```bash
# Terminal 1 — inicie o servidor
python UDPServer.py

# Terminal 2 — inicie o cliente
python UDPClient.py
```

### Diferenças entre TCP e UDP

| Característica | TCP | UDP |
|----------------|-----|-----|
| Conexão | Sim (`connect`/`accept`) | Não |
| Garantia de entrega | Sim | Não |
| Ordem dos pacotes | Garantida | Não garantida |
| Velocidade | Menor | Maior |
| Uso típico | Web, e-mail, arquivos | Streaming, jogos, VoIP |

---

## Requisitos

- Python 3.x
- Nenhuma biblioteca externa necessária (apenas o módulo `socket` da biblioteca padrão)

---

## Autor

**Nicolas DCB** — Redes de Computadores I
