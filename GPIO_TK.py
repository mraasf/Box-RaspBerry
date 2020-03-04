#!/usr/bin/env python3
# Gambiarrista :  Andriely Franca (mraasf)



#from Method import Method
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import RPi.GPIO as GPIO
from datetime import datetime
from random import randint
import time
import csv
from kivy.properties import StringProperty

TAM = 12
# atribui variaveis as saidas
Alimento = 40
Alav_Esquerda = 38
Alav_Direita = 36
House_Light = 33
Lamp_Esquerda = 31
Lamp_Direita = 29
Direita = 16
Esquerda = 18

GPIO.setmode(GPIO.BOARD)


#define as entradas
GPIO.setup(Alimento,GPIO.OUT)
GPIO.setup(Alav_Esquerda,GPIO.OUT)
GPIO.setup(Alav_Direita,GPIO.OUT)
GPIO.setup(House_Light,GPIO.OUT)
GPIO.setup(Lamp_Esquerda,GPIO.OUT)
GPIO.setup(Lamp_Direita,GPIO.OUT)

#define as saidas
GPIO.setup(Direita,GPIO.IN)
GPIO.setup(Esquerda,GPIO.IN)
           
from kivy.lang import Builder

Builder.load_file("GPIO_TK.kv")
#inicializacao das variaveis
Direita_press = 0
Esquerda_press = 0
Acertos =0 
Erros =0
tempo = 0
tempo2 = 0
tempo3 = 0
Alimento_lib = 0
tempo_limite = 10
alavanca_ativa =StringProperty("padrao")


class GPIO_TK(App,BoxLayout):    
    GPIO.output(Alav_Esquerda,GPIO.LOW)
    GPIO.output(Alav_Direita,GPIO.LOW)
    GPIO.output(House_Light,GPIO.LOW)
    GPIO.output(Lamp_Esquerda,GPIO.LOW)
    GPIO.output(Lamp_Direita,GPIO.LOW)
    GPIO.output(Alimento,GPIO.LOW)
             
    def GPIO_activate(self):
        global  Direita_press
        global Esquerda_press
        global Acertos
        global Erros
        global alavanca_ativa
        global tempo_limite
        #inicializacao das variaveis
        Direita_press = 0
        Esquerda_press = 0
        Acertos =0 
        Erros =0
        tempo = 0
        tempo2 = 0
        tempo3 = 0
        Alimento_lib = 0
        TipoTest = "Escolha" 
        
        #verifica a alavanca a tiva
        if self.ids.Ck_Direita.active:
            alavanca_ativa = "Direita"
        if self.ids.Ck_Esquerda.active:
            alavanca_ativa = "Esquerda"    
   #altera o tempo limite e a libera;'ao da recompensa de acoprdo com o texto
        #Pre treino
        if self.ids.Ck_Pre_Treino.active:
            #TipoTest = "Pre treino"
               #define o tempo limite em 15 minutos
            tempo_limite = int(TAM/4)
               
            #Treinamento
        if self.ids.Ck_Treinamento.active or self.ids.Ck_Omission.active or self.ids.Ck_Test.active:
               #define o tempo limite em  30 minutos
            tempo_limite = TAM/2
               #time.sleep(0.2)
            
            #Reativacao
        if self.ids.Ck_Reativacao.active:
            #TipoTest = "Reativacao"
            #define o tempo limite em  20 minutos
            tempo_limite = TAM/3
               #time.sleep(0.2)
            #test
        
            #omission
        #if :    
         #   TipoTest = "Omission"
                 #define o tempo limite em  30 minutos
          #  tempo_limite = TAM/2
                #if tempo2 == 60:
                #    GPIO.output(House_Light,GPIO.HIGH)
                #    Alimento_lib +=1
                #    tempo2 = 0
                #    time.sleep(0.2)
            
        
         
        #pega os text inputs
        identificacao_soinho = self.ids.TI_Identificacao.text
        Pesquisador = self.ids.TI_Pesquisador.text
        #seta o tempo limite na tela e exibe a mensagem do tipo de teste inicializado
        #self.ids.Lbl_Status.text=TipoTest+" Iniciado "
        
        #ativa as alavancas e a luz geral
        GPIO.output(Alav_Direita,GPIO.HIGH)
        GPIO.output(Alav_Esquerda,GPIO.HIGH)
        GPIO.output(House_Light,GPIO.HIGH)       
        
        #pega a hora inicial
        data_hora_inicial = time.asctime(time.localtime(time.time()))
        
        for tempo in range(int(tempo_limite*TAM*2)):
            #pega as entradas e incrementa os toques na Direita
            if GPIO.input(Direita) == 1:
                #nao acontece nada pois a saida trabalha ativada
                Direita_press = Direita_press
            else: #alavanca direita e incrementada
                Direita_press +=1
                if alavanca_ativa == "Direita":
                    Acertos += 1
                else:
                    Erros += 1
                    
            #pega as entradas e incrementa os toques na Esquerda
            if GPIO.input(Esquerda) == 1:
                Esquerda_press = Esquerda_press
                #nao acontece nada pois a saida trabalha ativada
            else:
                #alavanca direita e incrementada
                Esquerda_press+=1
                if alavanca_ativa == "Esquerda":
                    Acertos += 1
                else:
                    Erros += 1
            #continua contadndo o tempo
            tempo +=1
            
 #verifica o tipo de teste e e executa de acordo com as condicoes
            #pre treino
            if self.ids.Ck_Pre_Treino.active:
               TipoTest = "Pre treino"
               #libera um alimeto a cada minuto
               if ((tempo_limite*TAM*2) % 60 )== 0 :
                   GPIO.output(Alimento,GPIO.HIGH)
                   Alimento_lib +=1
            #treinamento
            if self.ids.Ck_Treinamento.active:
               TipoTest = "Treinamento"
            #reativacao
            if self.ids.Ck_Reativacao.active:
               TipoTest = "Reativacao"
            #test
            if self.ids.Ck_Test.active:
               TipoTest = "Test"
            #omission
            if self.ids.Ck_Omission.active:
               TipoTest = "Omission"   
            #pausa o processo por meio segundo garantindo o lag da leitura   
            time.sleep(0.5)
            # verifica se o tempo limite foi alcancado
            if tempo == tempo_limite*TAM*2:
                #quando otempo limite for alcancado desliga as saidas exibe as saidas na tela e gera o relatorio em csv
                GPIO.output(Alav_Direita,GPIO.LOW)
                GPIO.output(Alav_Esquerda,GPIO.LOW)
                GPIO.output(House_Light,GPIO.LOW)
                self.ids.Lbl_Data_Hora_Inicio.text=str(data_hora_inicial)
                self.ids.Lbl_Identificacao_saida.text=str(identificacao_soinho)
                self.ids.Lbl_Alav_Ativa.text=alavanca_ativa
                self.ids.Lbl_Toques_direita.text=str(Direita_press)
                self.ids.Lbl_Toques_esquerda.text=str(Esquerda_press)
                self.ids.Lbl_Acertos.text=str(Acertos)
                self.ids.Lbl_Erros.text=str(Erros)
                #pega a hora final
                data_hora_final = time.asctime(time.localtime(time.time()))
                self.ids.Lbl_Data_Hora_termino.text=str(data_hora_final)
                self.ids.Lbl_Alimntos_liberados.text=str(Alimento_lib)
                self.ids.Lbl_TempoLimite2.text=str(tempo_limite)
                self.ids.Lbl_Status.text=TipoTest+" Finalizado "
                
                
                # arquivo csv
                with open("exit.csv", "a") as csvfile:
                    ExitFile = csv.writer(csvfile)
                    ExitFile.writerow([identificacao_soinho,data_hora_inicial,Direita_press,alavanca_ativa,Acertos,Pesquisador,Esquerda_press,data_hora_final,Erros,Alimento_lib,TipoTest]) # escreve as strings de saida no csv
                    break
            
       
    def build(self):
        self.title="Soinhos Box - Version 0.0.2"
        return GPIO_TK()
 
if __name__ == '__main__':
    GPIO_TK().run()
    


    