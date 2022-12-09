import socket
import threading
from tkinter import *
from tkinter import simpledialog

class Chat:
    def __init__(self):
        HOST = 'localhost'
        PORT = 8000
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        self.client.connect((HOST, PORT))
        login = Tk()
        login.withdraw()

        self.janela_carregada = False
        self.ativo = True

        self.nome = simpledialog.askstring('Nome', 'Digite seu nome: ', parent=login)
        self.sala = simpledialog.askstring('Sala', 'Digite o nome da sala: ', parent=login)

        threa = threading.Thread(target=self.conecta)
        threa.start()

        self.janela()

    def janela(self): # RESPONSÁVEL PELA JANELA DO CHAT
        self.root = Tk()
        self.root.geometry("800x800")
        self.root.title("Chat")

        self.caixa_texto = Text(self.root)
        self.caixa_texto.place(relx=0.05, rely=0.01, width=700, height=600)

        self.campo_mensagem = Entry(self.root)
        self.campo_mensagem.place(relx=0.05, rely=0.8, width=500, height=40)

        self.btn_enviar = Button(self.root, text="Enviar", command=self.confirmarEnvioMsg)
        self.btn_enviar.place(relx=0.7, rely=0.8, width=100, height=40)

        self.root.protocol("WM_DELETE_WINDOW", self.fecharJanela)

        self.root.mainloop()

    def fecharJanela(self):
        self.root.destroy()
        self.client.close()

    def conecta(self):
        while True:
            mensagem_recebida = self.client.recv(1024)
            if mensagem_recebida == b'SALA':
                self.client.send(self.sala.encode())
                self.client.send(self.nome.encode())
            else:
                try:
                    self.caixa_texto.insert('end', mensagem_recebida.decode())
                except:
                    pass    

    def confirmarEnvioMsg(self): # FUNÇÃO PARA ENVIO DA MSG COM O BOTÃO
        mensagem = self.campo_mensagem.get()
        self.client.send(mensagem.encode())

chat = Chat()
