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

TAM = 10

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

#define a hora

def horario_segundos():
    horario = datetime.now()
    hora = horario.hour
    minuto = horario.minute
    segundo = horario.second
    total_segundos = (hora * TAM * TAM) + (minuto * TAM) + (segundo)
    return total_segundos

def horario_limite_segundos(tempo_limite):
    tempo_stop = tempo_limite * TAM
    hora_inicial = horario_segundos()
    hora_final = hora_inicial + tempo_stop
    return hora_final


            
from kivy.lang import Builder

Builder.load_file("GPIO_TK.kv")

class GPIO_TK(App,BoxLayout):
    GPIO.output(Alav_Esquerda,GPIO.LOW)
    GPIO.output(Alav_Direita,GPIO.LOW)
    GPIO.output(House_Light,GPIO.LOW)
    GPIO.output(Lamp_Esquerda,GPIO.LOW)
    GPIO.output(Lamp_Direita,GPIO.LOW)
    GPIO.output(Alimento,GPIO.LOW)
    Direita_press = 0
    Esquerda_press = 0
    tempo = 2
    alavanca_ativa = "padrao"
    def Direita(self):
            alavanca_ativa="Direita"
    def Esquerda(self):
            alavanca_ativa="Direita"
    def GPIO_activate(self):
        
        #pega os text inputs
        identificacao_soinho = self.ids.TI_Identificacao.text
        tempo_limite=int(self.ids.TI_TempoLimite.text)
        alavanca_ativa = self.ids.TI_AlavancaAtiva.text
                  
        #pega as horas inicial e final
        data_hora_inicial = time.asctime(time.localtime(time.time()))
             
        
        for tempo in range(tempo_limite*TAM):
            GPIO.output(Alav_Direita,GPIO.HIGH)
            GPIO.output(Alav_Esquerda,GPIO.HIGH)
            tempo +=1
            Direita_Press=tempo
            if tempo == tempo_limite*TAM:
                time.sleep(1)
                GPIO.output(Alav_Direita,GPIO.LOW)
                GPIO.output(Alav_Esquerda,GPIO.LOW)
                self.ids.Lbl_Data_Hora_Inicio.text=str(data_hora_inicial)
                data_hora_final = time.asctime(time.localtime(time.time()))
                self.ids.Lbl_Data_Hora_termino.text=str(data_hora_final)
                self.ids.Lbl_Identificacao_saida.text=str(identificacao_soinho)
                self.ids.Lbl_Alav_Ativa.text=alavanca_ativa
                # arquivo csv
                with open("exit.csv", "a") as csvfile:
                    ExitFile = csv.writer(csvfile)
                    ExitFile.writerow([identificacao_soinho,data_hora_inicial,alavanca_ativa,data_hora_final]) # escreve as strings de saida no csv
            
            time.sleep(1)
                
                
            
        
        
      
    def build(self):
        self.title="Soinhos Box - Version 0.0.2"
        return GPIO_TK()
 
if __name__ == '__main__':
    GPIO_TK().run()
    


    