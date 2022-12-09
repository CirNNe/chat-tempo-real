import socket
import threading

HOST = 'localhost'
PORT = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = FAMILIA DE PROTOCOLO / SOCK_STREAM = TIPO DE PROTOCOLO
server.bind((HOST, PORT)) # VINCULA O SOCKET COM O HOST E PORT
server.listen() # O SERVIDOR SERÁ UTILIZADO PARA "OUVIR"

salas = {}

def broadcast(sala, mensagem): # FUNÇÃO PARA ENVIAR AS MENSAGENS PARA TODAS AS PESSOAS NA SALA
    for i in salas[sala]:
        if isinstance(mensagem, str): # SE A MENSAGEM FOR EM STR, TRATAMOS ELA PARA BINARIO
            mensagem = mensagem.encode()
        i.send(mensagem)

def enviarMensagem(nome, sala, client): # FUNÇÃO APRA ENVIAR AS MENSAGENS DE CADA CLIENTE NA SALA PARA TODOS
    while True:
        mensagem = client.recv(1024)
        mensagem = f'{nome}: {mensagem.decode()}\n'
        broadcast(sala, mensagem) # SALA QUE ESTÁ CONECTADO E A MENSAGEM DO CLIENTE

while True: # PARA MANTER O SERVER RODANDO INFINITAMENTE E CONECTADO COM O CLIENTE
    client, addr = server.accept() # CLIENTE = CONEXÃO / ADDR = ENDEREÇO DA CONEXÃO / ACCEPT = ACEITA A CONEXÃO DO CLIENTE
    client.send(b'SALA') # ENVIA ESSA MSG PRO CLIENTE
    sala = client.recv(1024).decode() # RECEBE ESSES DADOS DO CLIENTE
    nome = client.recv(1024).decode()
    if sala not in salas.keys(): # SE NÃO EXISTIR A SALA, SERÁ CRIADA
        salas[sala] = []
    salas[sala].append(client)
    print(f'{nome} se conectou na sala {sala}! INFO {addr}')
    broadcast(sala, f'{nome} entrou na sala!\n')
    thread = threading.Thread(target=enviarMensagem, args=(nome, sala, client)) # PARA RODAR A FUNÇÃO enviarMensagem QUE CONTEM OUTRO WHILE
    thread.start()
