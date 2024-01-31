import os
import subprocess

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

def Get_ID_Dispositivo():
    command = "cd "+CURRENT_DIR_PATH+"/../../../app/lib"
    command += " && "
    command += "python2 -c 'from Fun_Dispositivo import Get_ID_Dispositivo; "
    command += "print Get_ID_Dispositivo()'"
    output = subprocess.getoutput(command)
    return output
