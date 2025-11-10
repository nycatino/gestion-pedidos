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
    def __init__(self):

        self.envios: Dict[str, Envio] = {}

    def seleccionar_carrier(self, metodo_envio):
        carriers = {
            "estandar": "CarrierFast",
            "express": "CarrierExpress",
            "pickup": "CarrierLocal"
        }
        return carriers.get(metodo_envio, "CarrierFast")

    def generar_tracking(self):
        return f"TRK-{str(uuid.uuid4())[:8].upper()}"
    
# LLAMAR MODULO DE NOTIFIFCACIONES?
    # def enviar_notificacion(self, cliente: str, tracking: str, carrier: str) -> str:
    #     mensaje = f"Hola {cliente}: Tu pedido está en camino!\nTracking: {tracking}\nCarrier: {carrier}"
    #     self.notificaciones.append({
    #         "cliente": cliente,
    #         "mensaje": mensaje,
    #         "fecha": datetime.now()
    #     })
    #     return mensaje

    def procesar_envio(self, orden_pedido):

        carrier = self.seleccionar_carrier(orden_pedido.metodo_envio)
        tracking_id = self.generar_tracking()

        envio = Envio(
            order_id=orden_pedido.id,
            tracking_id=tracking_id,
            carrier=carrier,
            estado="CREADO",
            historial=[{
                "estado": "CREADO",
                "fecha": datetime.now().isoformat()
            }]
        )
        self.envios[tracking_id] = envio

        estado = "EN_TRANSITO"
# ------MAIN
        # notificacion = self.enviar_notificacion(
        #     pedido.cliente, 
        #     tracking_id, 
        #     carrier
        # )
        print("envio procesado")
        return envio

# Test local
def test_modulo_con_store_externa():
    store_pedidos: Dict[str, Pedido] = {}
    pedido = Pedido(id="ORDER-001", cliente="Ana Gómez", estado="LISTO_PARA_ENVIO")

    modulo = ModuloEnvios()
    resultado = modulo.procesar_envio(pedido)

    print("\n=== Resultado del envío (store externa) ===")
    for k, v in resultado.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    test_modulo_con_store_externa()
