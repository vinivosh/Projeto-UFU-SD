#! python3
import pygame
import math
import col
import time
import socket
import json

import grpc
import pixClone_pb2
import pixClone_pb2_grpc
#from __future__ import print_function

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
    try:
        channel = grpc.insecure_channel(ip + ":" + str(port))
        stub = pixClone_pb2_grpc.pixCloneStub(channel)

        #Obtendo informações do servidor...
        info = stub.InfoRequest(pixClone_pb2.Nothing())
        pixelSize = info.pSize
        screenW = info.screenWidth
        screenH = info.screenHeight
        #print("[DEBUG] pixelSize="+str(pixelSize)+"\nscreenW="+str(screenW)+"\nscreenH="+str(screenH))
        break
    except Exception as e:
        print("Erro ao tentar se conectar ao servidor:\n" + str(e) + "\nTente novamente.")

#Inicializando o pygame
x = pygame.init()
print(str(x[0]) + " sucessos e " + str(x[1]) + " erros na inicialização do pygame.\n")

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

global pixelGrid
pixelGrid = [[col.white for i in range(screenH//pixelSize)] for j in range(screenW//pixelSize)]

def floorToMultiple(number,multiple):
    return number - (number % multiple)

def getPixels(stub):    
    #Pede ao servidor a malha de pixels e modifica a variável global
    global pixelGrid
    for pixel in stub.UpdateRequest(pixClone_pb2.Nothing()):
        pixelGrid[pixel.x][pixel.y] = (pixel.r, pixel.g, pixel.b)

def setPixel(stub,xCoor,yCoor,value): 
    stub.modPixels(pixClone_pb2.Pixel(x=xCoor, y=yCoor, r=value[0], g=value[1], b=value[2]))

def messageToScreen(msg,color,x,y):
    screenText = font.render(msg,True,color)
    gameDisplay.blit(screenText, [x, y])
    pygame.display.update()

def gameLoop(stub):
    global pixelGrid

    gameExit = False

    clock = pygame.time.Clock()
    fps = 24

    #Loop do jogo
    while not gameExit:
        #Obtendo a malha de pixels atual...
        getPixels(stub)

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
                        setPixel(stub, pixX, pixY, col.black)
                    elif pixelGrid[pixX][pixY] == col.black:
                        setPixel(stub, pixX, pixY, col.white)
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

    #Informa ao servidor que deseja sair [a implementar]    
    pygame.quit()

#Iniciando o loop do jogo
gameLoop(stub)