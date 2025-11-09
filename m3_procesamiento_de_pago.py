from datetime import datetime
import uuid
from modelos.pedido import Pedido


class ModuloPago:
    def __init__(self, pedidos_store):
        self.pedidos_store = pedidos_store

    def procesar_pago(self, order_id: str, metodo: str, monto: float, datos: dict = None):
        pedido = self.pedidos_store.obtener_pedido(order_id)
        if not pedido:
            return {"error": "Pedido no encontrado"}

        errores = []
        if not metodo:
            errores.append("Falta método de pago")
        if monto <= 0:
            errores.append("Monto inválido")

        if metodo == "tarjeta":
            if not datos or not all(k in datos for k in ["numero_enmascarado", "vencimiento", "titular"]):
                errores.append("Datos de tarjeta incompletos")
        elif metodo == "transferencia":
            if not datos or "referencia_bancaria" not in datos:
                errores.append("Falta referencia bancaria")
        else:
            errores.append("Método de pago no soportado")

        if errores:
            pedido.estado = "PAGO_RECHAZADO"
            return {"estado": "RECHAZADO", "errores": errores}

        # Simular aprobación
        if monto <= 200000:
            pedido.estado = "PAGO_APROBADO"
            pedido.pago = {
                "id": str(uuid.uuid4())[:8],
                "metodo": metodo,
                "monto": monto,
                "estado": "APROBADO"
            }
        else:
            pedido.estado = "PAGO_RECHAZADO"

        return {"order_id": pedido.id, "estado": pedido.estado, "monto": monto}
