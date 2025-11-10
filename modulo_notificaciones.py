from datetime import datetime


class modulo_Notificaciones:
    
    def enviar_notificacion(self, cliente: str, tracking: str, carrier: str) -> str:
        mensaje = f"Hola {cliente}: Tu pedido está en camino!\nTracking: {tracking}\nCarrier: {carrier}"
        self.notificaciones.append({
            "cliente": cliente,
            "mensaje": mensaje,
            "fecha": datetime.now()
        })
        return mensaje