#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
"""

Autor: Anderson Amaya Pulido

Libreria personal para procesar un qr.




# ideas a implementar




# dmesg | grep tty
"""
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------


import commands
import serial
import os, time
from serial import SerialException
from threading import Thread



#---------------------------------
#           Librerias personales
#---------------------------------
from lib.Fun_Serial_S2 import *  # importar con los mismos nombres



#---------------------------------------------------------
#---------------------------------------------------------
#----       Clase para multiples lectoras por serial y rs485
#---------------------------------------------------------
#---------------------------------------------------------

class LECTORAS(object):

    #---------------------------------------------------------
    def __init__(self, Port_Config, Lectoras):

        self.Puerto = Port_Config
        if self.Puerto == '0':   Puerto_Serial  = '/dev/ttyUSB0'
        if self.Puerto == '1':   Puerto_Serial  = '/dev/ttyUSB1'
        if self.Puerto == '2':   Puerto_Serial  = '/dev/ttyUSB2'

        self.Lectora = Lectoras
        Baudios = Baut_Serial(self.Lectora)

        self.Port = serial.Serial(Puerto_Serial, baudrate=Baudios, timeout=1)
        print 'Inicio: ' + Puerto_Serial
    #---------------------------------------------------------
    def Transmitir_Datos(self):
        data = ''
        data = Procesar_TX(self.Lectora)
        if len(data) >1:    self.Port.write(data)
    #---------------------------------------------------------
    def Recivir_Datos(self):
        rcv = self.Port.read(250)
        if len(rcv) >= 1:  Procesar_RX(self.Lectora, rcv)
    #---------------------------------------------------------
    def Proceso_Serial(self):
        while True:
            try :

                self.Transmitir_Datos()
                self.Recivir_Datos()

            except SerialException:
                    """
                    if Iniciar_Serial() == 0:
                        if FS_Mensajes: print 'Serrando el proceso por fallo grave en el Puerto'
                        break;
                    """
                    print 'Error'
    #---------------------------------------------------------
    def Inicio_Lectora(self):
        self.th_swrite = Thread(target=self.Proceso_Serial)
        self.th_swrite.start()




#---------------------------------------------------------
#---------------------------------------------------------
#----                FIN    Clase
#---------------------------------------------------------
#---------------------------------------------------------


LECTORA_1 = LECTORAS ('1', 'QR600-VHK-E')
LECTORA_2 = LECTORAS ('0', 'QR600-VHK-E')


LECTORA_1.Inicio_Lectora()
LECTORA_2.Inicio_Lectora()
