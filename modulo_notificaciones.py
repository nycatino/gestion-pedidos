from datetime import datetime


class Modulo_Notificaciones:

    def __init__(self ):
        self.notificaciones = []

    def pedido_rechazado(self, errores):
        # unir los errores en una cadena legible
        errores_texto = ", ".join(errores)
        mensaje = f"Hola! Tu pedido ha sido rechazado por los siguientes motivos: {errores_texto}"
        # guardar la notificación correctamente
        print(mensaje) 


    def enviar_seguimiento(self, tracking, carrier):
        mensaje = f"Hola! Tu pedido está en camino!\nTracking: {tracking}\nCarrier: {carrier}"
        print(mensaje) 
    
    def notificar(self, mensaje):
        print(mensaje)
    