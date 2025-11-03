from dataclasses import dataclass
from datetime import datetime
import uuid
from typing import Dict, Optional, Callable, Any, Union

@dataclass
class Pedido:
    id: str
    cliente: str
    estado: str
    guia: Optional[str] = None
    carrier: Optional[str] = None
    # Puedes añadir más campos que prepare el módulo de preparación (productos, direccion, etc.)

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

        Esto permite que el módulo de preparación pase solo el id y este módulo obtenga
        todos los datos necesarios del pedido.
        """
        self._internal_pedidos: Dict[str, Pedido] = {}  # fallback local si no se pasa fuente
        self.envios: Dict[str, Envio] = {}   # Simula BD de envíos
        self.notificaciones = [] # Simula registro de notificaciones

        # Normalizamos la fuente a una callable
        if pedidos_source is None:
            self._getter: Callable[[str], Optional[Pedido]] = lambda oid: self._internal_pedidos.get(oid)
        elif isinstance(pedidos_source, dict):
            self._getter = lambda oid, _d=pedidos_source: _d.get(oid)
        elif callable(pedidos_source):
            self._getter = pedidos_source
        else:
            raise ValueError("pedidos_source debe ser dict, callable o None")

    # Permite registrar en el store interno (útil para pruebas)
    def registrar_pedido_local(self, pedido: Pedido) -> None:
        self._internal_pedidos[pedido.id] = pedido

    def seleccionar_carrier(self, metodo_envio: str) -> str:
        """Selecciona carrier según método de envío"""
        carriers = {
            "estandar": "CarrierFast",
            "express": "CarrierExpress",
            "pickup": "CarrierLocal"
        }
        return carriers.get(metodo_envio, "CarrierFast")

    def generar_tracking(self) -> str:
        """Genera ID de tracking único"""
        return f"TRK-{str(uuid.uuid4())[:8].upper()}"

    def enviar_notificacion(self, cliente: str, tracking: str, carrier: str) -> str:
        """Simula envío de notificación al cliente"""
        mensaje = f"Hola {cliente}: Tu pedido está en camino!\nTracking: {tracking}\nCarrier: {carrier}"
        self.notificaciones.append({
            "cliente": cliente,
            "mensaje": mensaje,
            "fecha": datetime.now()
        })
        return mensaje

    def obtener_pedido(self, order_id: str) -> Optional[Pedido]:
        """Obtiene el pedido desde la fuente configurada"""
        return self._getter(order_id)

    def procesar_envio(self, order_id: str, metodo_envio: str = "estandar") -> Dict[str, Any]:
        """
        Procesa el envío de un pedido
        Entrada: 
            - order_id: ID del pedido (lo manda Preparación)
            - metodo_envio: tipo de envío (estandar/express/pickup)
        Salida:
            - Dict con resultado del proceso o error
        """
        # 1. Verificar estado del pedido usando la fuente externa
        pedido = self.obtener_pedido(order_id)
        if not pedido:
            return {"error": "Pedido no encontrado", "order_id": order_id}
        
        if pedido.estado != "LISTO_PARA_ENVIO":
            return {"error": "Pedido no listo para envío", "order_id": order_id, "estado_actual": pedido.estado}

        # 2. Generar guía de envío
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

        # 3. Actualizar pedido (si la fuente es mutable dict, intenta actualizarla también)
        pedido.estado = "EN_TRANSITO"
        pedido.guia = tracking_id
        pedido.carrier = carrier

        # Si la fuente es el store interno, ya se actualizó; si es un dict externo mutante,
        # asumimos que la referencia en store cambia automáticamente. Si la fuente es un getter
        # no mutante, el módulo que gestiona pedidos debe exponer una forma de persistir cambios.
        try:
            # intento actualizar si la fuente es el dict interno
            if hasattr(self._getter, "__self__") and isinstance(getattr(self._getter, "__self__", None), dict):
                pass
        except Exception:
            pass

        # 4. Notificar cliente
        notificacion = self.enviar_notificacion(
            pedido.cliente, 
            tracking_id, 
            carrier
        )

        # Devolver resultado
        return {
            "pedido_id": order_id,
            "tracking_id": tracking_id,
            "carrier": carrier,
            "estado": pedido.estado,
            "notificacion": notificacion
        }

def test_modulo_con_store_externa():
    """Ejemplo: la etapa de Preparación solo envía el id; este módulo lee la store externa."""
    # Simula store compartida entre módulos
    store_pedidos: Dict[str, Pedido] = {}
    pedido = Pedido(id="ORDER-001", cliente="Ana Gómez", estado="LISTO_PARA_ENVIO")
    store_pedidos[pedido.id] = pedido

    # Crear módulo enviando la referencia al dict (preparación pasaría solo el id)
    modulo = ModuloEnvios(pedidos_source=store_pedidos)

    # Procesa envío recibiendo solo el id
    resultado = modulo.procesar_envio(pedido.id, metodo_envio="express")

    print("\n=== Resultado del envío (store externa) ===")
    for k, v in resultado.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    test_modulo_con_store_externa()
