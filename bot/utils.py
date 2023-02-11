from wsmsg import send_message, send_image

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