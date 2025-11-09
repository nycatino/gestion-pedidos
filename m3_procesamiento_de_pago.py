from datetime import datetime
import uuid
from typing import Dict, Optional, Callable, Union
from modelos.pedido import Pedido

class ModuloPago:
    def __init__(self, pedidos_source: Union[Dict[str, Pedido], Callable[[str], Optional[Pedido]]] = None):
        """
        pedidos_source puede ser:
         - un dict que mapea order_id -> Pedido
         - una función getter(order_id) -> Pedido | None
        """
        self._internal_pedidos: Dict[str, Pedido] = {}

        # Según el tipo recibido, definimos cómo obtener un pedido
        if pedidos_source is None:
            # Si no se pasa nada, usamos un diccionario interno vacío
            self._getter: Callable[[str], Optional[Pedido]] = lambda oid: self._internal_pedidos.get(oid)
        elif isinstance(pedidos_source, dict):
            # Si es un diccionario, usamos get()
            self._getter = lambda oid, _d=pedidos_source: _d.get(oid)
        elif callable(pedidos_source):
            # Si es una función, la usamos directamente
            self._getter = pedidos_source
        else:
            raise ValueError("pedidos_source debe ser dict, callable o None")

    def procesar_pago(self, order_id: str, metodo: str, monto: float, datos: dict = None):
        """Procesa un pago ficticio para el pedido indicado"""
        pedido = self._getter(order_id)
        if not pedido:
            return {"error": "Pedido no encontrado"}

        errores = []

        # Validaciones básicas
        if not metodo:
            errores.append("Falta método de pago")
        if monto <= 0:
            errores.append("Monto inválido")

        # Validaciones según método
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

        # --- Simulación de aprobación del pago ---
        if monto <= 200000:
            pedido.estado = "PAGO_APROBADO"
            pedido.pago = {
                "id": str(uuid.uuid4())[:8],
                "metodo": metodo,
                "monto": monto,
                "fecha": datetime.now().isoformat(),
                "estado": "APROBADO"
            }
        else:
            pedido.estado = "PAGO_RECHAZADO"

        return {
            "order_id": pedido.id,
            "estado": pedido.estado,
            "monto": monto,
            "metodo": metodo
        }
