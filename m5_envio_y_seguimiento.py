from dataclasses import dataclass
from datetime import datetime
import uuid
from typing import Dict, Optional, Callable, Any, Union
from modelos.pedido import Pedido

@dataclass 
class Envio:
    order_id: str
    tracking_id: str
    carrier: str
    estado: str
    historial: list[Dict]

class ModuloEnvios:
    def __init__(self, pedidos_source: Union[Dict[str, Pedido], Callable[[str], Optional[Pedido]]] = None):
        """
        pedidos_source puede ser:
         - un dict que mapea order_id -> Pedido
         - una función getter: getter(order_id) -> Pedido | None
        """
        self._internal_pedidos: Dict[str, Pedido] = {}
        self.envios: Dict[str, Envio] = {}
        self.notificaciones = []

        # Normalizamos la fuente a una callable
        if pedidos_source is None:
            self._getter = lambda oid: self._internal_pedidos.get(oid)
        elif isinstance(pedidos_source, dict):
            self._getter = lambda oid, _d=pedidos_source: _d.get(oid)
        elif callable(pedidos_source):
            self._getter = pedidos_source
        else:
            raise ValueError("pedidos_source debe ser dict, callable o None")

    def registrar_pedido_local(self, pedido: Pedido) -> None:
        self._internal_pedidos[pedido.id] = pedido

    def seleccionar_carrier(self, metodo_envio: str) -> str:
        carriers = {
            "estandar": "CarrierFast",
            "express": "CarrierExpress",
            "pickup": "CarrierLocal"
        }
        return carriers.get(metodo_envio, "CarrierFast")

    def generar_tracking(self) -> str:
        return f"TRK-{str(uuid.uuid4())[:8].upper()}"

    def enviar_notificacion(self, cliente: str, tracking: str, carrier: str) -> str:
        mensaje = f"Hola {cliente}: Tu pedido está en camino!\nTracking: {tracking}\nCarrier: {carrier}"
        self.notificaciones.append({
            "cliente": cliente,
            "mensaje": mensaje,
            "fecha": datetime.now()
        })
        return mensaje

    def obtener_pedido(self, order_id: str) -> Optional[Pedido]:
        return self._getter(order_id)

    def procesar_envio(self, order_id: str, metodo_envio: str = "estandar") -> Dict[str, Any]:
        pedido = self.obtener_pedido(order_id)
        if not pedido:
            return {"error": "Pedido no encontrado", "order_id": order_id}
        
        if pedido.estado != "LISTO_PARA_ENVIO":
            return {"error": "Pedido no listo para envío", "order_id": order_id, "estado_actual": pedido.estado}

        carrier = self.seleccionar_carrier(metodo_envio)
        tracking_id = self.generar_tracking()

        envio = Envio(
            order_id=order_id,
            tracking_id=tracking_id,
            carrier=carrier,
            estado="CREADO",
            historial=[{
                "estado": "CREADO",
                "fecha": datetime.now().isoformat()
            }]
        )
        self.envios[tracking_id] = envio

        pedido.estado = "EN_TRANSITO"
        pedido.guia = tracking_id
        pedido.carrier = carrier

        notificacion = self.enviar_notificacion(
            pedido.cliente, 
            tracking_id, 
            carrier
        )

        return {
            "pedido_id": order_id,
            "tracking_id": tracking_id,
            "carrier": carrier,
            "estado": pedido.estado,
            "notificacion": notificacion
        }

# Test local
def test_modulo_con_store_externa():
    store_pedidos: Dict[str, Pedido] = {}
    pedido = Pedido(id="ORDER-001", cliente="Ana Gómez", estado="LISTO_PARA_ENVIO")
    store_pedidos[pedido.id] = pedido

    modulo = ModuloEnvios(pedidos_source=store_pedidos)
    resultado = modulo.procesar_envio(pedido.id, metodo_envio="express")

    print("\n=== Resultado del envío (store externa) ===")
    for k, v in resultado.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    test_modulo_con_store_externa()
