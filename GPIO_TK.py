#!/usr/bin/env python3
# Gambiarrista :  Andriely Franca (mraasf)



#from Method import Method
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import RPi.GPIO as GPIO
from datetime import datetime
from random import randint
import time
import csv
from kivy.properties import ObjectProperty

TAM = 60
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
alavanca_ativa = "padrao"

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
        #inicializacao das variaveis
        Direita_press = 0
        Esquerda_press = 0
        Acertos =0 
        Erros =0
        tempo = 0
        tempo2 = 0
        tempo3 = 0
        Alimento_lib = 0
        alavanca_ativa = "padrao"
        
         
        #pega os text inputs
        identificacao_soinho = self.ids.TI_Identificacao.text
        tempo_limite=int(self.ids.TI_TempoLimite.text)
        alavanca_ativa = str(self.ids.TI_AlavancaAtiva.text)
                          
        
        #ativa as alavancas e a luz geral
        GPIO.output(Alav_Direita,GPIO.HIGH)
        GPIO.output(Alav_Esquerda,GPIO.HIGH)
        GPIO.output(House_Light,GPIO.HIGH)       
        
        #pega a hora inicial
        data_hora_inicial = time.asctime(time.localtime(time.time()))
        
        for tempo in range(tempo_limite*TAM*2):
            #pega as entradas e incrementa os toques na Direita
            if GPIO.input(Direita) == 0:
                #nao acontece nada pois a saida trabalha ativada
                Direita_press = Direita_press
            else: #alavanca direita e incrementada
                Direita_press +=1
                if alavanca_ativa == "Direita":
                    Acertos += 1
                else:
                    Erros += 1
                    
            #pega as entradas e incrementa os toques na Esquerda
            if GPIO.input(Esquerda) == 0:
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
            time.sleep(0.5)
            # verifica se o tempo lmit foi alcancado
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
                self.ids.Lbl_Status.text="Test Finalizado"
                
                # arquivo csv
                with open("exit.csv", "a") as csvfile:
                    ExitFile = csv.writer(csvfile)
                    ExitFile.writerow([identificacao_soinho,data_hora_inicial,Direita_press,alavanca_ativa,Acertos,Esquerda_press,data_hora_final,Erros,Alimento_lib,"Test"]) # escreve as strings de saida no csv
                    break
            
                
    def GPIO_Omission(self):
        global  Direita_press
        global Esquerda_press
        global Acertos
        global Erros
        global tempo2
        global Alimento_lib
        Direita_press = 0
        Esquerda_press = 0
        Acertos =0 
        Erros =0
        tempo = 0
        tempo2 = 0
        tempo3 = 0
        Alimento_lib = 0
        alavanca_ativa = "padrao"
         
        #pega os text inputs
        identificacao_soinho = self.ids.TI_Identificacao.text
        tempo_limite=int(self.ids.TI_TempoLimite.text)
        alavanca_ativa = str(self.ids.TI_AlavancaAtiva.text)
                          
        
        #ativa as alavancas e a luz geral
        GPIO.output(Alav_Direita,GPIO.HIGH)
        GPIO.output(Alav_Esquerda,GPIO.HIGH)
        GPIO.output(House_Light,GPIO.HIGH)       
        
        #pega a hora inicial
        data_hora_inicial = time.asctime(time.localtime(time.time()))
        
        for tempo in range(tempo_limite*TAM*2):
            #pega as entradas e incrementa os toques na Direita
            if GPIO.input(Direita) == 0:
                #nao acontece nada pois a saida trabalha ativada
                Direita_press = Direita_press
            else: #alavanca direita e incrementada
                Direita_press +=1
                if alavanca_ativa == "Direita":
                    Acertos += 1
                else:
                    Erros += 1
                    
            #pega as entradas e incrementa os toques na Esquerda
            if GPIO.input(Esquerda) == 0:
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
            tempo2 +=1
            #libera o alimento a cada 30 segundos e deliga a saida logo apos
            if tempo2 == 60:
                GPIO.output(House_Light,GPIO.HIGH)
                Alimento_lib +=1
                tempo2 = 0
            time.sleep(0.5)    
            # verifica se o tempo lmit foi alcancado
            if tempo == (tempo_limite*TAM)*2:
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
                self.ids.Lbl_Status.text="Omission Finalizado"
                
                # arquivo csv
                with open("exit.csv", "a") as csvfile:
                    ExitFile = csv.writer(csvfile)
                    ExitFile.writerow([identificacao_soinho,data_hora_inicial,Direita_press,alavanca_ativa,Acertos,Esquerda_press,data_hora_final,Erros,Alimento_lib,"Omission"]) # escreve as strings de saida no csv
                    break
            
    def GPIO_Yoked(self):
        global  Direita_press
        global Esquerda_press
        global Acertos
        global Erros
        global tempo3
        global Alimento_lib
        Direita_press = 0
        Esquerda_press = 0
        Acertos =0 
        Erros =0
        tempo = 0
        tempo2 = 0
        tempo3 = 0
        Alimento_lib = 0
        alavanca_ativa = "padrao"
        
         
        #pega os text inputs
        identificacao_soinho = self.ids.TI_Identificacao.text
        tempo_limite=int(self.ids.TI_TempoLimite.text)
        alavanca_ativa = str(self.ids.TI_AlavancaAtiva.text)
                          
        
        #ativa as alavancas e a luz geral
        GPIO.output(Alav_Direita,GPIO.HIGH)
        GPIO.output(Alav_Esquerda,GPIO.HIGH)
        GPIO.output(House_Light,GPIO.HIGH)       
        
        #pega a hora inicial
        data_hora_inicial = time.asctime(time.localtime(time.time()))
        
        for tempo in range(tempo_limite*TAM*2):
            #pega as entradas e incrementa os toques na Direita
            if GPIO.input(Direita) == 0:
                #nao acontece nada pois a saida trabalha ativada
                Direita_press = Direita_press
            else: #alavanca direita e incrementada
                Direita_press +=1
                if alavanca_ativa == "Direita":
                    Acertos += 1
                else:
                    Erros += 1
                    
            #pega as entradas e incrementa os toques na Esquerda
            if GPIO.input(Esquerda) == 0:
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
            tempo3 +=1
            #libera o alimento a cada 30 segundos e deliga a saida logo apos
            if 30 > tempo3 < 90   :
                GPIO.output(House_Light,GPIO.HIGH)
                Alimento_lib +=1
                tempo3 = 0
            time.sleep(0.5)    
            # verifica se o tempo lmit foi alcancado
            if tempo == (tempo_limite*TAM)*2:
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
                self.ids.Lbl_Status.text="Yoked Finalizado"
                
                # arquivo csv
                with open("exit.csv", "a") as csvfile:
                    ExitFile = csv.writer(csvfile)
                    ExitFile.writerow([identificacao_soinho,data_hora_inicial,Direita_press,alavanca_ativa,Acertos,Esquerda_press,data_hora_final,Erros,Alimento_lib,"Yoked"]) # escreve as strings de saida no csv
                    break
            
           
        
      
    def build(self):
        self.title="Soinhos Box - Version 0.0.2"
        return GPIO_TK()
 
if __name__ == '__main__':
    GPIO_TK().run()
    


    