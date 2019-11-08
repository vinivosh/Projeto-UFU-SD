﻿#! python3
import col
import socket
import threading
import json

def floorToMultiple(number,multiple):
    return number - (number % multiple)

#Selecionando o tamanho do pixel da malha
print("Insira o tamanho do pixel da malha (padrão = 32)")
input_ = ''
input_ = input()
while (True):
    try:
        pixelSize = int(input_)
        if (int(input_) > 0):
            print("Tamanho do pixel escolhido: " + str(pixelSize))
            break
        else:
            raise ValueError
    except:
        print("Favor inserir um valor numérico válido")
        input_ = input()

#Selecionando a largura da tela
print("Insira a largura da tela de exibição. Será arredondado para o menor múltiplo do tamanho do pixel! (padrão = 1024)")
input_ = input()
while (True):
    try:
        screenW = floorToMultiple(int(input_),pixelSize)
        if (screenW < pixelSize):
            screenW = pixelSize
        print("Largura da tela escolhida: " + str(screenW))
        break
    except:
        print("Favor inserir um valor numérico válido")
        input_ = input()

#Selecionando a altura da tela
print("Insira a altura da tela de exibição. Será arredondado para o menor múltiplo do tamanho do pixel! (padrão = 768)")
input_ = input()
while (True):
    try:
        screenH = floorToMultiple(int(input_),pixelSize)
        if (screenH < pixelSize):
            screenH = pixelSize
        print("altura da tela escolhida: " + str(screenH))
        break
    except:
        print("Favor inserir um valor numérico válido")
        input_ = input()

#Variáveis do jogo
bgColor = col.white
gridColor = col.lightGrey
gridThickness = pixelSize//16

global pixels
pixels = [[col.white for i in range(screenH//pixelSize)] for j in range(screenW//pixelSize)]

#def envia(lista_clientes):
#    while True:
#
#        if len(lista_clientes)!=0:
#            for x in lista_clientes:
#                data = json.dumps({"pixels": pixels,"updateRequest": None, "x": None, "y": None, "color": None, "sair": None})
#                x.send(data.encode())


ip='localhost'
port= 8080
clientes=[]
server= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((ip,port))
server.listen(5)
#client_envia= threading.Thread(target=envia, args=(clientes,))
#client_envia.start()

print ('[*] Escutando %s:%d' %(ip,port))

def handle_client(client_socket):
    print ('\n-------------------\n')
    client_socket.send(('\nMensagem destinada ao cliente: %s \n' %addr[0]).encode())
    client_socket.send('\nACK!\nRecebido pelo servidor\n'.encode())
    while True :
        resposta=client_socket.recv(4096)
        resposta = json.loads(resposta.decode())
        #print (resposta)
        if (resposta["sair"] != None) and (resposta["sair"] == 's' or resposta["sair"] =='sim' or resposta["sair"] =='y' or resposta["sair"] =='yes'):
            client_socket.send(json.dumps({"pixels": None,"updateRequest": None, "x": None, "y": None, "color": None, "sair": 'y'}).encode())
            client_socket.close()
            print ('[*] Conexao de fechada\n:')
            clientes.remove(client_socket)
            break
        elif (resposta["updateRequest"] != None) and (resposta["updateRequest"] == 's' or resposta["updateRequest"] == 'sim' or resposta["updateRequest"] == 'y' or resposta["updateRequest"] == 'yes'):
            resp = json.dumps({"pixels": pixels,"updateRequest": None, "x": None, "y": None, "color": None, "sair": 'n'}).encode()
            client_socket.send(resp)
            #print ('Malha de pixels enviada ao cliente!:\n')
            #print(resp)
        elif resposta["x"] != None and resposta["y"] != None and resposta["color"] != None:
            #print(resposta["x"])
            #print(resposta["y"])
            #print(resposta["color"])
            pixels[resposta["x"]][resposta["y"]] = resposta["color"]

while True:
    client, addr = server.accept()
    clientes.append(client)
    print ('[*] Conexao aceita de %s:%d' %(addr[0],addr[1]))
    client_handler= threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

