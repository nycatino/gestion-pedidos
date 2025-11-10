from datetime import datetime


class modulo_Notificaciones:

    def guardar_notificacion(self, cliente, mensaje):
        self.notificaciones.append({
            "cliente": cliente,
            "mensaje": mensaje,
            "fecha": datetime.now()
        })

    def pedido_rechazado(self, errores, cliente):
        # unir los errores en una cadena legible
        errores_texto = ", ".join(errores)
        mensaje = f"Hola {cliente}: Tu pedido ha sido rechazado por los siguientes motivos: {errores_texto}"

        # guardar la notificación correctamente
        self.guardar_notificacion(cliente, mensaje)
        return mensaje


    def enviar_seguimiento(self, cliente: str, tracking: str, carrier: str) -> str:
        mensaje = f"Hola {cliente}: Tu pedido está en camino!\nTracking: {tracking}\nCarrier: {carrier}"
        self.guardar_notificacion(cliente, mensaje)
        return mensaje
    