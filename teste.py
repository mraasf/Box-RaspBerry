#!/usr/bin/env python
#Autor : mraasf
 
 
import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BOARD)


#entradas das paletas // contador de toques
left = 16 #rightPaletMotor
right = 18 #leftPaletMotor

#Define os pinos como saida
  
GPIO.setup(36, GPIO.OUT)#rigthPaletSwitch 
GPIO.setup(38, GPIO.OUT)#leftPaletSwitch
GPIO.setup(22, GPIO.OUT)#nosePoke
GPIO.setup(31, GPIO.OUT)#leftStimulusLight
GPIO.setup(33, GPIO.OUT)#houseLight
GPIO.setup(29, GPIO.OUT)#rightStimulusLight
GPIO.setup(40, GPIO.OUT)#feeder  

#entradas das paletas
GPIO.setup(16, GPIO.IN)
GPIO.setup(18, GPIO.IN)


#desliga todos as saidas
GPIO.output(36,0)#pino 16
GPIO.output(38,0)#pino 18
GPIO.output(29,0)#pino 29
GPIO.output(31,0)#pino 31

GPIO.output(40,0)#pino 40 saida house light
contador = 1
TAM = 2
while(contador <8):

    if contador == 1:
        GPIO.output(36, 1)
        print ("paleta direita")
        contador+=1
        time.sleep(TAM)
        GPIO.output(36, 0)
    #Caso contador = 2, aciona a saida
    if contador == 2:
        GPIO.output(38, 1)
        print ("paleta esquerda")
        contador+=1
        time.sleep(TAM)
        GPIO.output(38, 0)
 
    #Caso contador = 3, aciona a saida
    if contador == 3:
        GPIO.output(29, 1)
        print ("lampada direita")  
        contador+=1
        time.sleep(TAM)
        GPIO.output(29, 0)
        #Caso contador = 4, aciona a saida
    if contador == 4:
        GPIO.output(31, 1)
        print ("lampada esquerda ")
        contador+=1
        time.sleep(TAM)
        GPIO.output(31, 0)
            #Caso contador = 5, aciona a saida
    if contador == 5:
        GPIO.output(33, 1)
        print ("hOUSE lIGHT ")
        contador+=1
        time.sleep(TAM)
        GPIO.output(33, 0)    
    if contador == 6:
        GPIO.output(40, 1)
        print ("aLIMENTO ")
        contador+=1
        time.sleep(TAM)
        GPIO.output(40, 0)
     
    #Caso contador = 7, desliga todas as saidas
    #zera a variavel contador
    if contador == 7:
        print ("teste terminou \n desligando as saidas e zerando o contador")
        GPIO.output(36,0)
        GPIO.output(38,0)
        GPIO.output(29,0)
        GPIO.output(31,0)
        GPIO.output(33,0)
        GPIO.output(40,0)
        contador = 0
    contador2 = 0
    if contador == 0:
        GPIO.output(36,1)
        GPIO.output(38,1)
        if GPIO.input(18) == 0:
            print("left desligado")
            contador2 = contador2+1
            if contador2 == 5:
                contador = 8
        if GPIO.input(18) == 1:
                print("left LIGADO")
                
        if GPIO.input(16) == 0:
                print("Right desligado")
                contador2 = contador2+1
        if contador2 == 5:
                contador = 8
                if GPIO.input(16) == 1:
                    print("right LIGADO")
          
   

