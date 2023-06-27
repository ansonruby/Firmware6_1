from lib.Lib_File import Clear_File, Get_File
from lib.Lib_Rout import *
from lib.Lib_Threads import Create_Thread_Daemon
from Mod_Validacion import Validar_QR_Antiguo, Validar_Acceso, Respaldo_Online
from lib.Lib_settings import Get_Mod_Procesamiento
import re
import time

Configs = Get_Mod_Procesamiento()


def Filtro_Tipos_QR_Antiguo(access_code, medio_acceso=1, lectora=0):
    access_list = re.findall("<(.*?)>", access_code)

    for access_text in access_list:
        access_data = access_text.split(".")
        tipo_acceso = False

        # Tipo 1 0 2 o 5: LLave de acceso o Reserva general con QR o Llave empleado
        if len(access_data) == 2:
            tipo_acceso = 1

        # Tipo 3: Invitacion de unico uso
        elif len(access_data) == 5 and access_data[0] == "3":
            tipo_acceso = 3

        # Tipo 4: Invitacion de multipes uso
        elif len(access_data) == 5:
            tipo_acceso = 4
        if tipo_acceso:
            Validar_QR_Antiguo(
                access_data, tipo_acceso, medio_acceso, lectora)
        else:
            Respaldo_Online({
                "access_medium": medio_acceso,
                "access_code": access_code,
                "data": access_code,
                "old_qr_code": True
            }, lectora)
            break


def Filtro_Tipos_Acceso(access_code, medio_acceso, lectora):
    tipo_acceso = None
    try:
        # Validaciones QR Antiguo
        if re.search("<(.*?)>", access_code):
            Filtro_Tipos_QR_Antiguo(access_code, medio_acceso, lectora)
            return True

        # Tipo 6: Dispositivos adicionales
        elif medio_acceso == 11:
            tipo_acceso = 6

        # Tipos [1-5]: QR
        elif medio_acceso == 1 and re.search("AA(.*?)AA", access_code):
            filter_access_code = re.findall("AA(.*?)AA", access_code)
            if len(filter_access_code) > 0:
                filter_access_code = filter_access_code[0]
                tipo_acceso = int(filter_access_code[0])
                access_code = filter_access_code[1:]

        # Tipo 7 pin:
        elif medio_acceso == 2:
            tipo_acceso = 7

        if tipo_acceso:
            Validar_Acceso(
                access_code, tipo_acceso, medio_acceso, lectora)
        else:
            Respaldo_Online({
                "access_medium": medio_acceso,
                "access_code": access_code,
                "reader": lectora
            }, lectora)
    except Exception as e:
        Respaldo_Online({
            "access_medium": medio_acceso,
            "access_code": access_code,
            "access_type": tipo_acceso,
            "reader": lectora
        }, lectora)


def Recibir_Codigo_Accesso():

    # Medio de acceso 1:QR
    qr_read_paths = [
        (STATUS_QR, COM_QR),
        (STATUS_QR_S1, COM_QR_S1),
        (STATUS_QR_S2, COM_QR_S2)
    ]

    # Medio de acceso 2:PIN
    keyboard_read_paths = [
        (STATUS_TECLADO, COM_TECLADO),
        (STATUS_TECLADO_S1, COM_TECLADO_S1),
        (STATUS_TECLADO_S2, COM_TECLADO_S2)
    ]

    # Medio de acceso 5-11:NFC
    nfc_read_paths = [
        (STATUS_NFC, COM_NFC),
        (STATUS_NFC_S1, COM_NFC_S1),
        (STATUS_NFC_S2, COM_NFC_S2)
    ]

    read_paths = {}
    if "Lectura_QR" in Configs and str(Configs["Lectura_QR"]).lower() == "true":
        read_paths["1"] = qr_read_paths
    if "Lectura_Teclado" in Configs and str(Configs["Lectura_Teclado"]).lower() == "true":
        read_paths["2"] = keyboard_read_paths
    if "Lectura_NFC" in Configs and str(Configs["Lectura_NFC"]).lower() == "true":
        read_paths["11"] = nfc_read_paths

    for medium in read_paths.keys():
        for lectora, (status, command) in enumerate(read_paths[medium]):
            if Get_File(os.path.join(FIRM, HUB, status)).strip() == '1':
                Create_Thread_Daemon(Filtro_Tipos_Acceso,
                                     Get_File(os.path.join(FIRM, HUB, command)), int(medium), lectora)
                Clear_File(os.path.join(FIRM, HUB, status))


while True:
    sleep_time = 0.5 if not "Time_Sleep_Mod" in Configs else float(
        Configs["Time_Sleep_Mod"])
    time.sleep(sleep_time)
    Recibir_Codigo_Accesso()
