from wsmsg import send_message
import pycron 
from datetime import datetime 
from pytz import timezone
import subprocess

def handle_messages_tools(msgRecvd:str, remoteJid:str, instance:str):

    message = False
    if msgRecvd == "/comandos":
        message = """/ejemplo
/swcostos"""
    elif msgRecvd == "/ejemplo":
        message = "Por ejemplo, si elige el paquete de 8 juegos, trae su consola de Nintendo y yo procederé a instalar los juegos en ella. Es necesaria una tarjeta micro SD para la instalación. Después de instalados, se asegura de que todos funcionen correctamente y luego se lleva la consola."
    elif msgRecvd == "/swcostos":
        message = """COSTOS:

PAQUETES INICIALES DISPONIBLES: 

CLIENTES NUEVOS

3 JUEGOS: 29$ + 2 JUEGOS SORPRESA 🎮🎮 (ahorro de 5$)
4 JUEGOS: 39$ + 3 JUEGOS SORPRESA 🎮🎮 (ahorro de 5$)
6 JUEGOS: 59$ + 5 JUEGOS SORPRESA 🎮🎮 (ahorro de 10$)
8 JUEGOS: 69$ + 7 JUEGOS SORPRESA 🎮🎮 (ahorro de 10$)

CLIENTES VIEJOS

-POR CADA JUEGO INSTALADO RECIBE 1 JUEGO SORPRESA

-9$ C/U JUEGO ADICIONAL.

REQUISITOS PARA LA INSTALACION

- MEMORIA SD ( 128gb 35$, 256gb 60$.).
- CONSOLA NINTENDO SWITCH. ( VERIFICAR COMPATIBILIDAD PREGUNTEME COMO!!! ). 

METODOS DE PAGO:

-EFECTIVO  💸💸
-TRANSFERENCIA BANCARIA. 🏦🏦
-YAPPY."""

    if message:
        send_message(remoteJid, message, instance, False)

def check_cron(cron_expression: str) -> bool:
    # Get the current time
    now = datetime.now(timezone('America/Bogota'))

    # Check if the current time matches the cron expression
    return pycron.is_now(cron_expression, dt=now)


import re
import traceback
import subprocess

def list_new_files_gdrive(src:str = "TJSDrive,shared_with_me=true:", dest:str = "eliomiguelgs:TJS/shared files") -> any:
    
    # define the command
    cmd_check = ['rclone', 'check', src, dest, '--differ', '--error-on-no-transfer']
    cmd_copy = ['rclone', 'copy', src, dest, '-P']

    # run the command and capture the output
    try:
        output = subprocess.run(cmd_check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        traceback.print_exc()

    # extract the filenames from the output
    new_files = []
    modified_files = []
    string = ""
    for line in output.stderr.split('\n'):
        if 'ERROR' in line:
            # extract the filename and the error message
            match = re.match(r'.* : (.+): (.+)', line)
            if match:
                filename = match.group(1).strip()
                error_message = match.group(2).strip()

                # check if the error message indicates a new file or a modified file
                if "file not in Google drive root" in error_message:
                    new_files.append(filename)
                elif error_message == "sizes differ":
                    modified_files.append(filename)

    if new_files:
        string += "🆕 *NEW FILES:*\n\n"
        for file in new_files:
            string += f"  *- 📄 {file}*\n"

    if modified_files:
        string += "\n✏ *MODIFIED FILES:*\n\n"
        for file in modified_files:
            string += f"  *- 📝 {file}*\n"

    if string:
        subprocess.run(cmd_copy, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    return string
    