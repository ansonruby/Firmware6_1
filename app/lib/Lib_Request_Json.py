from Lib_Rout import *
from Fun_Dispositivo import Get_ID_Dispositivo
from Lib_settings import Get_Pat_Server
import requests
import time

petition_time_out = 60 * 60

fixed_urls = {
    "get_users": "/api/scan_devices/get_granted_access_hub",
    "grant": "/api/access/grant",
    "send_autorizations": "/api/scan_devices/send_authorizations_hub",
    "online_backup": "/api/access/validate_access",
    "get_users_periodic": "/api/scan_devices/get_dynamic_granted_access_hub",
    "3": "/api/access/verify_conection",
    "4": "/api/firmware/review_update",
    "5": "/api/firmware/confirm_update",
    "lokers_open": "/api/parcels/get_lockers_status_info",
    "get_lokers": "/api/parcels/get_location_lockers",
    "send_autorizations_Lokers": "/api/parcels/update_lockers_parcels"
}

# method can be GET, OPTIONS, HEAD, POST, PUT, PATCH, or DELETE


def send_petition(url, method="GET", params=None, data={}, json_data={}, headers={}, timeout=petition_time_out):
    hub_headers = {"FUSEACCESS-ID": Get_ID_Dispositivo(),
                   "TIME-SCAN": str(int(time.time()*1000))}
    response = None
    petition_url = url
    if url in fixed_urls:
        petition_url = Get_Rout_server() + fixed_urls[url]
    elif not "http" in url:
        petition_url = Get_Rout_server() + url

    try:
        response = requests.request(method, petition_url, params=params, data=data,
                                    json=json_data, headers=dict(hub_headers.items()+headers.items()), timeout=timeout)
        return response
    except (TypeError, ValueError) as e:
        if response:
            return response
        else:
            return False
    except Exception as e:
        return False


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
    # return 'http://192.168.0.103:3000'
    return opciones[mejor_opcion]


# print send_petition("get_users")
# print send_petition("/api/access/get_granted_users_pi")
# print send_petition("http://localhost:3000/api/access/get_granted_users_pi")
# print send_petition("send_autorizations", method="POST", json_data={"data": "a1b2"})
