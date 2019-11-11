#! python3
import col
import socket
import threading
import json
import math

def floorToMultiple(number,multiple):
    return number - (number % multiple)

global pixelSize
global screenW
global screenH
global timesMod
global pixels

#Função que salva as modificações num log. Quando o limite do log for ultrapassado, aplica todas modificações documentadas para o snapshot, e prossegue com o logging
def log(x=0, y=0, color=col.white):
    global timesMod
    #Se não atingimos o limite de ações em log (determinado como a quantidade de pixels na malha divido por 32 e arredondado para baixo)...
    if (timesMod < math.floor(screenH//pixelSize * screenW//pixelSize / 32)-1):
        if (timesMod == 0):
            logFile = open("log.pixc", 'w', encoding="utf-8")
        else:
            logFile = open("log.pixc", 'a', encoding="utf-8")        
        logFile.write(str(x) + " " + str(y) + " " + str(color[0]) + " " + str(color[1]) + " " + str(color[2]) + "  ")
        logFile.close()
        timesMod += 1
    else:#Quando a modificação de número máximo de timesMod for ser feita, ela não será logada, mas sim passada pro snapshot
        dados = {"pixelSize": pixelSize, "screenW": screenW, "screenH": screenH, "pixels": pixels}
        dataFile = open("snapshot.pixc", 'w', encoding="utf-8")
        dataFile.write(json.dumps(dados, skipkeys=True))
        dataFile.close()
        logFile = open("log.pixc", 'w', encoding="utf-8")
        logFile.write("")
        logFile.close()
        timesMod = 0

#Função que lê um arquivo log e aplica todas as modificações nele na malha de pixels. Se nenhum arquivo for encontrado, ou o arquivo estiver vazio, não faz nada na malha de pixels
def logRead():
    try:
        logFile = open("log.pixc","r")
        logStr = logFile.read()
        logFile.close()
        #print("Log lido em string: " + logStr + "\n")
        if (logStr == ''):
            print("Arquivo log encontrado, mas vazio. Prosseguindo sem modificações à malha\n")
        else:
            print("Arquivo log encontrado. Modificando a malha...\n")
            logList = logStr.split()
            #print("Log lido em lista: " + str(logList) + "\n")

            #Modificando a malha...
            for i in range (0,len(logList),5):
                pixels[int(logList[i])][int(logList[i+1])] = (int(logList[i+2]), int(logList[i+3]), int(logList[i+4]))
            #Salvando os dados na snapshot...
            dados = {"pixelSize": pixelSize, "screenW": screenW, "screenH": screenH, "pixels": pixels}
            dataFile = open("snapshot.pixc", 'w', encoding="utf-8")
            dataFile.write(json.dumps(dados, skipkeys=True))
            dataFile.close()
            #Limpando o arquivo de log...
            logFile = open("log.pixc","w")
            logFile.write('')
            logFile.close()
            print("Malha modificada. Estado carregado com sucesso.\n")
    except OSError as e:
        print("Arquivo log não encontrado. Prosseguindo sem modificações à malha\n")
        pass

useFile = False
#Tentando ler snapshot salvo
try:
    dataFile = open("snapshot.pixc","r")
    print("Arquivo snapshot encontrado. Utilizá-lo? S para sim e N para não (apenas pressione enter para inserir o valor padrão = S")
    while(True):
        input_ = input()
        if (input_ == '' or input_ == 's' or input_ == 'S'):
            useFile = True
            break
        elif (input_ == 'n' or input_ == 'N'):
            break
        print("Favor inserir uma entrada válida!")
    #Armazenando os dados num dict...
    print("\n")
    dataDict = json.loads(dataFile.read())
except OSError as e:
    print("Arquivo snapshot não encontrado. Prosseguindo com uma malha de pixels nova\n")
    pass

if (useFile == False):
    #Selecionando o tamanho do pixel da malha
    print("Insira o tamanho do pixel da malha (Apenas pressione enter para inserir o valor padrão = 32)")
    input_ = ''
    input_ = input()
    while (True):
        try:
            if (input_ == ''):
                pixelSize = 32
                print("Tamanho do pixel escolhido: 32\n")
                break
            pixelSize = int(input_)
            if (pixelSize > 0):
                print("Tamanho do pixel escolhido: " + str(pixelSize) + "\n")
                break
            else:
                raise ValueError
                
        except:
            print("Favor inserir um valor numérico válido")
            input_ = input()

    #Selecionando a largura da tela
    print("Insira a largura da tela de exibição. Será arredondado para o menor múltiplo do tamanho do pixel! (Apenas pressione enter para inserir o valor padrão = 1024)")
    input_ = input()
    while (True):
        try:
            if (input_ == ''):
                screenW = floorToMultiple(1024,pixelSize)
                print("Largura da tela escolhida: " + str(screenW) + "\n")
                break
            screenW = floorToMultiple(int(input_),pixelSize)
            if (screenW < pixelSize):
                screenW = pixelSize
            print("Largura da tela escolhida: " + str(screenW) + "\n")
            break
        except:
            print("Favor inserir um valor numérico válido")
            input_ = input()


    #Selecionando a altura da tela
    print("Insira a altura da tela de exibição. Será arredondado para o menor múltiplo do tamanho do pixel! (Apenas pressione enter para inserir o valor padrão = 768)")
    input_ = input()
    while (True):
        try:
            if (input_ == ''):
                screenH = floorToMultiple(768,pixelSize)
                print("Altura da tela escolhida: " + str(screenH) + "\n")
                break
            screenH = floorToMultiple(int(input_),pixelSize)
            if (screenH < pixelSize):
                screenH = pixelSize
            print("Altura da tela escolhida: " + str(screenH) + "\n")
            break
        except:
            print("Favor inserir um valor numérico válido")
            input_ = input()

    #Salvando informações em arquivo snapshot novo
    dados = {"pixelSize": pixelSize, "screenW": screenW, "screenH": screenH, "pixels": None}
    dataFile = open("snapshot.pixc", 'w', encoding="utf-8")
    dataFile.write(json.dumps(dados, skipkeys=True))
    dataFile.close()

    #Cria malha nova
    pixels = [[col.white for i in range(screenH//pixelSize)] for j in range(screenW//pixelSize)]

else:#Se estivermos utilizando o arquivo snapshot...
    pixelSize = dataDict["pixelSize"]
    print("Tamanho do pixel lido: " + str(pixelSize) + "\n")
    screenW = dataDict["screenW"]
    print("Largura da tela lido: " + str(screenW) + "\n")
    screenH = dataDict["screenH"]
    print("Altura da tela lido: " + str(screenH) + "\n")

    if (dataDict["pixels"] != None):#Se houver uma malha de pixels salva...        
        pixels = [[col.white for i in range(screenH//pixelSize)] for j in range(screenW//pixelSize)]
        pixelsTemp = dataDict["pixels"]
        #print("pixels do arquivo:\n" + str(pixelsTemp) + "\n")
        #Convertendo a lista interna de volta para tuplas...
        i = 0  
        for l1 in pixelsTemp:
            j = 0
            for l2 in pixelsTemp[i]:
                pixels[i][j] = (pixelsTemp[i][j][0], pixelsTemp[i][j][1], pixelsTemp[i][j][2])
                j += 1
            i += 1
        #print("pixels convertidos:\n" + str(pixels) + "\n")

        #Lendo arquivo log e aplicando as modificações
        logRead()

    else:#Se não houver uma malha de pixels salva...
        pixels = [[col.white for i in range(screenH//pixelSize)] for j in range(screenW//pixelSize)]

while(True):
    #Selecionando o ip
    print("Insira o IP para este servidor (Apenas pressione enter para deixar o valor padrão = localhost)")
    while(True):
        try:
            ip = input()
            break
        except:
            print("Favor inserir um valor válido!")
    if (ip == ''):
        ip = 'localhost'
    print("IP inserido: " + ip + "\n")

    #Selecionando a porta
    input_ = ''
    print("Insira a porta para este servidor (Apenas pressione enter para deixar o valor padrão = 8080)")
    while(True):
        try:         
            input_ = input()
            if (input_ == ""):
                port = 8080
                break
            port = int(input_)
            if (port < 0):
                raise ValueError
            break
        except:
            print("Favor inserir um valor válido!")
    print("Porta inserida: " + str(port) + "\n")

    #ip='localhost'
    #port= 8080

    try:
        server= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error as e:
        print("Erro ao estabelecer a conexão:\n" + str(e) + "\nTente novamente...\n")
        continue
    try:
        server.bind((ip,port))
    except socket.error as e:
        print("Erro ao estabelecer a conexão:\n" + str(e) + "\nTente novamente...\n")
        continue
    server.listen(5)
    break
    #client_envia= threading.Thread(target=envia, args=(clientes,))
    #client_envia.start()

print ('[*] Escutando %s:%d' %(ip,port))

#def envia(lista_clientes):
#    while True:
#
#        if len(lista_clientes)!=0:
#            for x in lista_clientes:
#                data = json.dumps({"pixels": pixels,"updateRequest": None, "x": None, "y": None, "color": None, "sair": None})
#                x.send(data.encode())

def handle_client(client_socket):
    print ('\n-------------------\n')
    client_socket.send(('\nMensagem destinada ao cliente: %s \n' %addr[0]).encode())
    client_socket.send('\nACK!\nRecebido pelo servidor\n'.encode())
    while True :
        resposta=client_socket.recv(4096)
        resposta = json.loads(resposta.decode())
        #Lidando com pedido de saída
        if (resposta["sair"] != None) and (resposta["sair"] == 's' or resposta["sair"] =='sim' or resposta["sair"] =='y' or resposta["sair"] =='yes'):
            client_socket.send(json.dumps({"pixels": None,"updateRequest": None, "infoRequest": None, "x": None, "y": None, "color": None, "sair": 'y'}).encode())
            client_socket.close()
            print ('[*] Conexao de fechada\n:')
            clientes.remove(client_socket)
            break
        #Lidando com pedido de informação
        elif (resposta["infoRequest"] != None) and (resposta["infoRequest"] == 's' or resposta["infoRequest"] == 'sim' or resposta["infoRequest"] == 'y' or resposta["infoRequest"] == 'yes'):
            resp = json.dumps({"pixels": pixelSize,"updateRequest": None, "infoRequest": None, "x": screenW, "y": screenH, "color": None, "sair": 'n'}).encode()
            client_socket.send(resp)
        #Lidando com pedido de update da malha
        elif (resposta["updateRequest"] != None) and (resposta["updateRequest"] == 's' or resposta["updateRequest"] == 'sim' or resposta["updateRequest"] == 'y' or resposta["updateRequest"] == 'yes'):
            resp = json.dumps({"pixels": pixels,"updateRequest": None, "infoRequest": None, "x": None, "y": None, "color": None, "sair": 'n'}).encode()
            client_socket.send(resp)
        #Lidando com modificação na malha
        elif resposta["x"] != None and resposta["y"] != None and resposta["color"] != None:
            pixels[resposta["x"]][resposta["y"]] = resposta["color"]
            log(resposta["x"], resposta["y"], resposta["color"])

clientes=[]
timesMod = 0

while True:
    client, addr = server.accept()
    clientes.append(client)
    print ('[*] Conexao aceita de %s:%d' %(addr[0],addr[1]))
    client_handler= threading.Thread(target=handle_client, args=(client,))
    client_handler.start()