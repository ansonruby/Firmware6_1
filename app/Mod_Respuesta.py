#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
"""

Autor:  Luding Castaneda,
        Anderson Amaya Pulido

Libreria personal para procesar un qr.




# ideas a implementar




# dmesg | grep tty
"""
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
import time
from threading import Thread

#---------------------------------
#           Librerias personales
#---------------------------------
from lib.Lib_settings import *  # importar con los mismos nombres

#-----------------------------------------------------------
#                       CONTANTES
#-----------------------------------------------------------

MR_Mensajes = 0     # 0: NO print  1: Print
Config_Mod  = Get_Mod_Respuesta()
Tiempo_stop = float(Config_Mod['Time_Sleep_Mod'])
Tipo_Dispositivo = Get_Tipo_Dispositivo()
print Tipo_Dispositivo
#---------------------------------------------------------
#---------------------------------------------------------
#----       Clase respuestas para lso diferentes dispsotyivos cae cat hub
#---------------------------------------------------------
#---------------------------------------------------------

class SALIDAS_ACCIONES(object):

    #---------------------------------------------------------
    def __init__(self, Locacion, lectora, rele):

        self.Canal_lectora  = lectora
        self.Canal_rele  = rele
        self.Sede   = Locacion
        #---------------------------------------
        self.COM_Respuesta     = ''
        self.Salida_COM_RELE    = ''
        self.Salida_COM_LED     = ''
        self.Salida_COM_BUZZER  = ''

        #---------------------------------------
        self.Enrutar_Archivos_Salidas()
        #print self.Salida_COM_RES
    #---------------------------------------------------------
    def Ciclo_revicion(self):
        global Tiempo_stop
        while (True):
            time.sleep(Tiempo_stop)                # 0.05
            Comando = Get_File(self.COM_Respuesta)
            if Comando != '':
                self.Acciones_Dispositivo(Comando)
                Clear_File(self.COM_Respuesta)
    #---------------------------------------------------------
    def Enrutar_Archivos_Salidas(self):
        global Tipo_Dispositivo
        #-----------------------------------------------------------------------
        if Tipo_Dispositivo == 'CAT_Lectora':
            self.Salida_COM_LED     = os.path.join(FIRM,HUB,COM_LED)
            self.Salida_COM_BUZZER  = os.path.join(FIRM,HUB,COM_BUZZER)
            self.COM_Respuesta      = os.path.join(FIRM,HUB,COM_RES)
            self.Salida_COM_RELE    = os.path.join(FIRM,HUB,COM_RELE_S0)
            if MR_Mensajes :
                print 'Buzzer :', self.Salida_COM_BUZZER
                print 'Led :', self.Salida_COM_LED
                print 'Sede :', self.Sede
                print 'Ruta Respuesta :', self.COM_Respuesta
                print 'Ruta Rele :', self.Salida_COM_RELE
        #-----------------------------------------------------------------------
        elif Tipo_Dispositivo == 'HUB':
            if    self.Canal_lectora == '0': self.COM_Respuesta = os.path.join(FIRM,HUB,COM_RES)
            elif  self.Canal_lectora == '1': self.COM_Respuesta = os.path.join(FIRM,HUB,COM_RES_S1)
            elif  self.Canal_lectora == '2': self.COM_Respuesta = os.path.join(FIRM,HUB,COM_RES_S2)
            #--------------------------------------------------------------------
            if    self.Canal_rele == '0':   self.Salida_COM_RELE = os.path.join(FIRM,HUB,COM_RELE_S0)
            elif  self.Canal_rele == '1':   self.Salida_COM_RELE = os.path.join(FIRM,HUB,COM_RELE_S1)
            elif  self.Canal_rele == '2':   self.Salida_COM_RELE = os.path.join(FIRM,HUB,COM_RELE_S2)
            if MR_Mensajes :
                print 'Sede :', self.Sede
                print 'Ruta Respuesta :', self.COM_Respuesta
                print 'Ruta Rele :', self.Salida_COM_RELE



    #---------------------------------------------------------
    def Access_Entry_Users(self):
        global Tipo_Dispositivo
        #--------------------------------------------------------------------
        if MR_Mensajes : print 'Access granted-E :',self.Salida_COM_RELE
        if Tipo_Dispositivo == 'HUB':
            Set_File(self.Salida_COM_RELE,'Access granted-E')
        #--------------------------------------------------------------------
        elif Tipo_Dispositivo == 'CAT_Lectora':
            Set_File(self.Salida_COM_RELE,'Access granted-E')
            Set_File(self.Salida_COM_LED,'Access granted-E')
            Set_File(self.Salida_COM_BUZZER , '1')           # activar sonido por 500*1

    #---------------------------------------------------------
    def Access_Out_Users(self):
        global Tipo_Dispositivo
        #--------------------------------------------------------------------
        if MR_Mensajes : print 'Access granted-S :',self.Salida_COM_RELE
        if Tipo_Dispositivo == 'HUB':
            Set_File(self.Salida_COM_RELE,'Access granted-S')
        #--------------------------------------------------------------------
        elif Tipo_Dispositivo == 'CAT_Lectora':
            Set_File(self.Salida_COM_LED,'Access granted-S')
            Set_File(self.Salida_COM_BUZZER , '1')           # activar sonido por 500*1

    #---------------------------------------------------------
    def Access_Denied_Users(self):
        global Tipo_Dispositivo
        #--------------------------------------------------------------------
        if Tipo_Dispositivo == 'HUB':
            Set_File(self.Salida_COM_RELE,'Error')
        #--------------------------------------------------------------------
        elif Tipo_Dispositivo == 'CAT_Lectora':
            Set_File(self.Salida_COM_LED,'Error')
            Set_File(self.Salida_COM_BUZZER , '1')           # activar sonido por 500*1

    #---------------------------------------------------------
    def Acciones_Dispositivo(self, Comando):
        #--------- para usuarios
        if    'Access granted-E' in Comando :  self.Access_Entry_Users()
        elif  'Access granted-S' in Comando :  self.Access_Out_Users()
        elif  'Denied'           in Comando :  self.Access_Denied_Users()
        else:                                  self.Access_Denied_Users()
    #---------------------------------------------------------
    def Inicio_Revicion(self):
        self.th_swrite = Thread(target=self.Ciclo_revicion)
        self.th_swrite.start()


#-----------------------------------------
#           Configuraciones de Salidas
#-----------------------------------------
VECTOR_SALIDAS = []

data_Reles    = Get_Salidas()
data_Lectoras = Get_Lectoras()
VECTOR_Mapin = []

#-----------------------------------------
#           funcion de mapeo
#-----------------------------------------
for Lectora in data_Lectoras: #prioridad locaciones --
    Canal_lectora = Lectora['Puerto']
    Locacion_Lectora = Lectora['Locacion']
    for Rele in data_Reles: #prioridad locaciones --
        Canal_rele= Rele['Puerto']
        if Locacion_Lectora == Rele['Locacion']:
            #print 'posible ruta salida:'
            VECTOR_Mapin.append([Locacion_Lectora,Canal_lectora, Canal_rele])
#-----------------------------------------
"""
for Mapa in VECTOR_Mapin:
    #print Mapa
    try:
        if MR_Mensajes : print 'Mapa :',Mapa[0],Mapa[1],Mapa[2]
        VECTOR_SALIDAS.append(SALIDAS_ACCIONES ( Mapa[0], Mapa[1], Mapa[2] ))
    except:
        if MR_Mensajes : print 'Key Error no definidas'
"""
M1 = VECTOR_Mapin[0]
M2 = VECTOR_Mapin[1]
print 'M1 :',M1
print 'M2 :',M2
if MR_Mensajes : print 'Mapa :',M1[0], M1[1], M1[2]
if MR_Mensajes : print 'Mapa :','S1', M2[1], M2[2]
VECTOR_SALIDAS.append(SALIDAS_ACCIONES ( M1[0], M1[1], M1[2] ))
VECTOR_SALIDAS.append(SALIDAS_ACCIONES ( 'S0', '1', M2[2] ))


print 'Iniciando reviciones'
for Salida_Rele in VECTOR_SALIDAS:
    Salida_Rele.Inicio_Revicion()
