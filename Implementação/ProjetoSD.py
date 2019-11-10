#! python3
import pygame
import math
import col
import time
import socket
#import threading
import json

#Inicializando e conectando com o servidor
global ip, port, server

while(True):
    #Selecionando o ip
    print("\nInsira o IP do servidor (Apenas pressione enter para deixar o valor padrão = localhost)")
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
    print("Insira a porta do servidor (Apenas pressione enter para deixar o valor padrão = 8080)")
    while(True):
        try:            
            input_ = input()
            if (input_ == ''):
                port = 8080
                break
            port = int(input_)
            if (port < 0):
                raise ValueError
            break
        except:
            print("Favor inserir um valor válido!")
    print("Porta inserida: " + str(port) + "\n")

    #Conectando ao servidor
    server= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        server.connect((ip,port))
        resposta=server.recv(4096)
        resposta=server.recv(4096)
        break
    except Exception as e:
        print("Erro ao tentar se conectar ao servidor:\n" + str(e) + "\nTente novamente.")

#Inicializando o pygame
x = pygame.init()
print(str(x[0]) + " sucessos e " + str(x[1]) + " erros na inicialização do pygame.\n")

#Obtendo informações do servidor...
message = {"pixels": None,"updateRequest": None, "infoRequest": 'y', "x": None, "y": None, "color": None, "sair": None}
server.send(json.dumps(message).encode())
#Espera a resposta do servidor e retorna a resposta correta caso não haja erro. Se ouver, retorna lista vazia
resposta = server.recv(4096)
data = json.loads(resposta.decode())
pixelSize = data["pixels"]
screenW = data["x"]
screenH = data["y"]

#Setup do display
gameDisplay = pygame.display.set_mode((screenW,screenH))
pygame.display.set_caption('pixClone')

#Fonte do jogo inteiro
font = pygame.font.SysFont(None,35)

#Variáveis do jogo
bgColor = col.white
gridColor = col.lightGrey
if (pixelSize > 16):
    gridThickness = pixelSize//16
elif (pixelSize > 2):
    gridThickness = 1
else:
    gridThickness = 0

pixelGrid = [[col.white for i in range(screenH//pixelSize)] for j in range(screenW//pixelSize)]

def floorToMultiple(number,multiple):
    return number - (number % multiple)

def calcMessageSize():
    #Calcula o tamanho da mensagem que contém toda a malha de pixels (+ as outras possíveis variáveis, como 'y', 'x', etc)
    size = math.ceil(((screenW/pixelSize) * (screenH/pixelSize))*18)
    if (size < 2048):
        size = 2048
    return size

def getPixels():
    #Pede que o servidor envie a malha de pixels
    message = {"pixels": None,"updateRequest": 'y', "infoRequest": None, "x": None, "y": None, "color": None, "sair": None}
    server.send(json.dumps(message).encode())
    #Espera a resposta do servidor e retorna a resposta correta caso não haja erro. Se ouver, retorna lista vazia
    resposta = server.recv(calcMessageSize())
    data = json.loads(resposta.decode())
    if data["sair"] == 'sim' or data["sair"] == 's' or data["sair"] == 'y' or data["sair"] == 'yes':
        return []
    if data["pixels"] == None:
        return []
    return data["pixels"]

def setPixel(x,y,value):
    message = {"pixels": None,"updateRequest": None, "infoRequest": None, "x": x, "y": y, "color": value, "sair": None}
    server.send(json.dumps(message).encode())

def messageToScreen(msg,color,x,y):
    screenText = font.render(msg,True,color)
    gameDisplay.blit(screenText, [x, y])
    pygame.display.update()

def gameLoop():
    gameExit = False

    clock = pygame.time.Clock()
    fps = 60

    #Loop do jogo
    while not gameExit:
        pixelGridTemp = getPixels()#Obtendo a malha de pixels atual...
        #Convertendo as listas internas de volta para tuplas...
        i = 0        
        for l1 in pixelGridTemp:
            j = 0
            for l2 in pixelGridTemp[i]:
                pixelGrid[i][j] = (pixelGridTemp[i][j][0], pixelGridTemp[i][j][1], pixelGridTemp[i][j][2])
                j += 1
            i += 1

        #Loop de eventos
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameExit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Pegando a posição do mouse e encontrando qual "pixel" ele se encontra no grid
                pixX = floorToMultiple(pygame.mouse.get_pos()[0],pixelSize)//pixelSize
                pixY = floorToMultiple(pygame.mouse.get_pos()[1],pixelSize)//pixelSize
                if event.button == pygame.BUTTON_LEFT:                    
                    if pixelGrid[pixX][pixY] == col.white:
                        setPixel(pixX,pixY,col.black)
                    elif pixelGrid[pixX][pixY] == col.black:
                        setPixel(pixX,pixY,col.white)
            elif event.type == pygame.QUIT:
                gameExit = True

        #Desenhando na tela...
        gameDisplay.fill(bgColor)#Desenhando fundo

        #Desenhando o preenchimento dos pixels...
        for i in range(0,screenW,pixelSize):
            for j in range(0,screenH,pixelSize):
                pygame.draw.rect(gameDisplay, pixelGrid[i//pixelSize][j//pixelSize],[i,j,pixelSize,pixelSize])
        
        #Desenhando o grid
        if (gridThickness > 0):
            for i in range(0,screenW):#Linhas verticais...
                if i%pixelSize == 0:
                    pygame.draw.rect(gameDisplay, col.lightGrey,[i,0,gridThickness,screenH])
            for i in range(0,screenH):#Linhas horizontais...
                if i%pixelSize == 0:
                    pygame.draw.rect(gameDisplay, col.lightGrey,[0,i,screenW,gridThickness])

        #Update gráfico
        pygame.display.update()
        clock.tick(fps)

    #Informa ao servidor que deseja sair
    message = {"pixels": None,"updateRequest": None, "infoRequest": None, "x": None, "y": None, "color": None, "sair": 'y'}
    server.send(json.dumps(message).encode())
    pygame.quit()

#Iniciando o loop do jogo
gameLoop()