#!/usr/bin/env python3
#  Andriely Franca (mraasf)




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
from kivy.lang import Builder

TAM = 12
# atribui variaveis as saidas
Alimento = 40
Alav_Esquerda = 38
Alav_Direita = 36
House_Light = 33
Lamp_Esquerda = 31
Lamp_Direita = 29
Press_Direita = 16
Press_Esquerda = 18

GPIO.setmode(GPIO.BOARD)


#define as entradas
GPIO.setup(Alimento,GPIO.OUT)
GPIO.setup(Alav_Esquerda,GPIO.OUT)
GPIO.setup(Alav_Direita,GPIO.OUT)
GPIO.setup(House_Light,GPIO.OUT)
GPIO.setup(Lamp_Esquerda,GPIO.OUT)
GPIO.setup(Lamp_Direita,GPIO.OUT)

#define as saidas
GPIO.setup(Press_Direita,GPIO.IN)
GPIO.setup(Press_Esquerda,GPIO.IN)
           


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

# libera o alimento quando a alavanca correta é pressionada no pré treino
def LiberaAliento(self):
    global Alimento_lib
    GPIO.output(Alimento,1)
    time.sleep(0.1)
    Alimento_lib += 1
    print(Alimento_lib)
    GPIO.output(Alimento,0)  
def Alim_Treinamento(self):
           global Alimento_lib
           global Acertos
           Cont_Press(self)
           if self.ids.Ck_Treinamento.active:
               if alavanca_ativa == "Direita" and GPIO.input(Press_Direita) == 0:
                   LiberaAliento(self)                   
               if alavanca_ativa == "Esquerda" and GPIO.input(Press_Esquerda) == 0:
                   LiberaAliento(self)
           print(Acertos)
                        
            #return Alimento_lib
# libera o alimento quando a alavanca correta é pressionada cinco vezes
def Alim_Reativacao(self):
           global Alimento_lib
           global Acertos
           Cont_Press(self)
           #if self.ids.Ck_Reativacao.active:
           if Acertos % 5 == 0:
               LiberaAliento(self)
           #        return Alimento_lib
def Alim_Omission(self):
           global Alimento_lib
           global Acertos
           if self.ids.Ck_Omission.active:
               if Acertos % 5 == 0:
                   if alavanca_ativa == "Direita" :
                       LiberaAliento(self)
                   elif alavanca_ativa == "Esquerda":
                       LiberaAliento(self)
           #return Alimento_lib           
def Cont_Press(self):
            global Acertos
            global Erros
            global Direita_press
            global Esquerda_press
            #pega as entradas e incrementa os toques na Direita
            if GPIO.input(Press_Direita) == 0:
                if alavanca_ativa == "Direita":
                    GPIO.output(Lamp_Direita,1)
                    GPIO.output(Lamp_Esquerda,0)
                    time.sleep(1)
                    GPIO.output(Lamp_Direita,0)
                    GPIO.output(Lamp_Esquerda,0)
                    Acertos += 1
                else:
                    Erros += 1
                Direita_press +=1    
            #pega as entradas e incrementa os toques na Esquerda
            if GPIO.input(Press_Esquerda) == 0:
                if alavanca_ativa == "Esquerda":
                    GPIO.output(Lamp_Esquerda,1)
                    GPIO.output(Lamp_Direita,0)
                    time.sleep(1)
                    GPIO.output(Lamp_Esquerda,0)
                    GPIO.output(Lamp_Direita,0)
                    Acertos += 1
                else:
                    Erros += 1
                Esquerda_press+=1 

class GPIO_TK(App,BoxLayout):    
    GPIO.output(Alav_Esquerda,1)
    GPIO.output(Alav_Direita,1)
    GPIO.output(House_Light,1)
    GPIO.output(Lamp_Esquerda,0)
    GPIO.output(Lamp_Direita,0)
    GPIO.output(Alimento,0)
        
    #acao quando o botao iniciar teste é pressionado
    def GPIO_activate(self):
        global  Direita_press
        global Esquerda_press
        global Acertos
        global Erros
        global alavanca_ativa
        global tempo_limite
        global Alimento_lib
        #inicializacao das variaveis
        Direita_press = 0
        Esquerda_press = 0
        Acertos =0 
        Erros =0
        #tempo = 0
        tempo2 = 0
        tempo3 = 0
        #Alimento_lib = 0
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
               #define o tempo limite em  30 minutos para o treianamento , no teste e no omission
            tempo_limite = TAM/4
            #Reativacao
        if self.ids.Ck_Reativacao.active:
            tempo_limite = TAM/3
            #pega os text inputs
        encerra = int(tempo_limite*TAM*4.5)    
        identificacao_soinho = self.ids.TI_Identificacao.text
        Pesquisador = self.ids.TI_Pesquisador.text
        #ativa as alavancas e a luz geral
        GPIO.output(Alav_Direita,1)
        GPIO.output(Alav_Esquerda,1)
        GPIO.output(House_Light,1)       
        #pega a hora inicial
        data_hora_inicial = time.asctime(time.localtime(time.time()))
        #inicia o tempo de controle do alimento com um valor randomico entre 30 e 90
        TempoRand = randint(6,16)
        print("ncerra ",encerra)
        for tempo in range(int(encerra)):
            #verifica o tipo de teste e e executa de acordo com as condicoes
            #pre treino
            if self.ids.Ck_Pre_Treino.active:
               TipoTest = "Pre treino"
               Cont_Press(self)
               #libera um alimeto a cada minuto
               if tempo == TempoRand :
                   LiberaAliento(self)
                   #incrementa a variavel que controla o tempo do alimento com valores aleatorios entre 30 e 90
                   TempoRand += randint(6,16)
            #treinamento
            if self.ids.Ck_Treinamento.active:
               TipoTest = "Treinamento"
               print("tempo : ",tempo)
               Alim_Treinamento(self)
               if Acertos ==  60:
                   tempo = int(encerra-1)
                   print("tempo : ",tempo)
                   
            #reativacao
            if self.ids.Ck_Reativacao.active:
               TipoTest = "Reativacao"
               Alim_Reativacao(self)
               if Acertos ==  20:
                   tempo = int(encerra-1)
                   print("tempo : ",tempo)
            #test
            if self.ids.Ck_Test.active:
               TipoTest = "Test"
               Cont_Press(self)
            #omission
            if self.ids.Ck_Omission.active:
               TipoTest = "Omission"   
            #pausa o processo por meio segundo garantindo o lag da leitura   
            
            #continua contadndo o tempo
            #tempo +=1
            time.sleep(0.1)   
            # verifica se o tempo limite foi alcancado
            if tempo == int(encerra-1):
                #quando otempo limite for alcancado desliga as saidas exibe as saidas na tela e gera o relatorio em csv
                GPIO.output(Alav_Direita,0)
                GPIO.output(Alav_Esquerda,0)
                GPIO.output(House_Light,0)
                self.ids.Lbl_Data_Hora_Inicio.text=str(data_hora_inicial)
                self.ids.Lbl_Identificacao_saida.text=str(identificacao_soinho)
                self.ids.Lbl_Alav_Ativa.text=str(alavanca_ativa)
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
                
                Direita_press = 0
                Esquerda_press = 0
                Acertos =0 
                Erros =0
                tempo = 0
                tempo2 = 0
                tempo3 = 0
                Alimento_lib = 0
                tempo_limite = 10
                encerra = 0
                alavanca_ativa =StringProperty("padrao")
                
                # arquivo csv
                with open("exit.csv", "a") as csvfile:
                    ExitFile = csv.writer(csvfile)
                    ExitFile.writerow([identificacao_soinho,data_hora_inicial,Direita_press,alavanca_ativa,Acertos,Pesquisador,Esquerda_press,data_hora_final,Erros,Alimento_lib,TipoTest]) # escreve as strings de saida no csv
                    break
                
                break
       
    def build(self):
        self.title=" Box - Version 0.0.0"
        return GPIO_TK()
 
if __name__ == '__main__':
    GPIO_TK().run()
    


    