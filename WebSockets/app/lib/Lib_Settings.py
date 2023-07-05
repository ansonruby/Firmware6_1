import json
import os

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def Get_Pat_Server():
    file = open(CURRENT_DIR_PATH+"/../../../db/HUB/Config/Config.json")
    data = json.load(file)
    file.close()
    return data["HUB"]["Ser_Dominio"], data["HUB"]["Ser_Ip"], data["HUB"]["Mejor_Coneccion"]


def Get_Mod_Speaker():
    file = open(CURRENT_DIR_PATH+"/../../../db/HUB/Config/Config.json")
    data = json.load(file)
    file.close()
    if "Mod_Speaker" in data:
        return data["Mod_Speaker"]
    return {}

def Get_Rout_server():
    Domi_Ser, IP_Ser, mejor_opcion = Get_Pat_Server()

    opciones = {'0': 'http://' + IP_Ser,
                '1': 'http://' + Domi_Ser,
                '10': 'http://' + IP_Ser,
                '11': 'http://' + IP_Ser,
                '100': 'https://' + IP_Ser,
                '101': 'https://' + IP_Ser,
                '110': 'https://' + IP_Ser,
                '111': 'https://' + IP_Ser,
                '1000': 'https://' + Domi_Ser,
                '1001': 'https://' + Domi_Ser,
                '1010': 'http://' + IP_Ser,
                '1011': 'http://' + IP_Ser,
                '1100': 'https://' + IP_Ser,
                '1101': 'https://' + IP_Ser,
                '1110': 'https://' + IP_Ser,
                '1111': 'https://' + IP_Ser}

    # return 'https://solutions.fusepong.com'
    # return 'http://192.168.0.30:3000'
    return opciones[mejor_opcion]
