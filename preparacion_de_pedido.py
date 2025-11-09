from dataclasses import dataclass
from datetime import datetime
import random
from typing import Dict, Optional, Callable, Any, Union, List

# --- Datos de ejemplo (pueden compartirse entre módulos) ---

@dataclass
class Item:
    sku: str
    cantidad: int

@dataclass
class Pedido:
    id: str
    cliente: str
    estado: str
    items: List[Item]
    tiempo_estimado_preparacion: Optional[int] = None


# --- Módulo de preparación del pedido ---

class ModuloPreparacion:
    def __init__(self, pedidos_source: Union[Dict[str, Pedido], Callable[[str], Optional[Pedido]]] = None):
        """
        pedidos_source puede ser:
         - un dict que mapea order_id -> Pedido
         - una función getter(order_id) -> Pedido | None
        """
        self._internal_pedidos: Dict[str, Pedido] = {}
        if pedidos_source is None:
            self._getter: Callable[[str], Optional[Pedido]] = lambda oid: self._internal_pedidos.get(oid)
        elif isinstance(pedidos_source, dict):
            self._getter = lambda oid, _d=pedidos_source: _d.get(oid)
        elif callable(pedidos_source):
            self._getter = pedidos_source
        else:
            raise ValueError("pedidos_source debe ser dict, callable o None")

        self.preparaciones = {}  # Simula base de datos de preparaciones

    # --- Función auxiliar ---
    def simular_ubicacion(self, sku: str) -> str:
        """Devuelve una ubicación ficticia del depósito para el SKU"""
        pasillo = random.randint(1, 10)
        estante = random.randint(1, 5)
        nivel = random.choice(["A", "B", "C"])
        return f"P{pasillo}-E{estante}-{nivel}"

    # --- Confirmación ficticia ---
    def confirmar_preparacion(self, picking_list: list) -> bool:
        """Simula una confirmación del operario o sistema"""
        # En un caso real, esto podría ser una API, aquí siempre True
        return True

    # --- Lógica principal ---
    def preparar_pedido(self, order_id: str) -> Dict[str, Any]:
        pedido = self._getter(order_id)
        if not pedido:
            return {"error": "Pedido no encontrado", "order_id": order_id}

        if pedido.estado != "PAGO_APROBADO":
            return {
                "error": "Precondición no cumplida",
                "order_id": order_id,
                "estado_actual": pedido.estado
            }

        # Generar picking list
        picking_list = []
        for item in pedido.items:
            ubicacion = self.simular_ubicacion(item.sku)
            picking_list.append({
                "sku": item.sku,
                "cantidad": item.cantidad,
                "ubicacion": ubicacion
            })

        # Confirmar preparación
        confirmado = self.confirmar_preparacion(picking_list)
        if not confirmado:
            return {"error": "Preparación no confirmada", "order_id": order_id}

        # Calcular tiempos estimados
        tiempo_por_item = 2  # minutos
        tiempo_empaquetado = 5
        tiempo_total = (len(pedido.items) * tiempo_por_item) + tiempo_empaquetado

        # Actualizar pedido
        pedido.estado = "LISTO_PARA_ENVIO"
        pedido.tiempo_estimado_preparacion = tiempo_total
        self.preparaciones[order_id] = {
            "picking_list": picking_list,
            "tiempo_estimado": tiempo_total,
            "fecha_preparacion": datetime.now().isoformat()
        }

        # Retornar resultado (para pasar a módulo de envíos)
        return {
            "order_id": pedido.id,
            "estado": pedido.estado,
            "tiempo_estimado": tiempo_total,
            "picking_list": picking_list
        }


# --- Prueba rápida del módulo ---
def test_modulo_preparacion():
    # Base de pedidos compartida
    pedidos_store: Dict[str, Pedido] = {
        "ORDER-101": Pedido(
            id="ORDER-101",
            cliente="Juan Pérez",
            estado="PAGO_APROBADO",
            items=[Item("SKU123", 2), Item("SKU456", 1)]
        )
    }

    modulo = ModuloPreparacion(pedidos_source=pedidos_store)

    resultado = modulo.preparar_pedido("ORDER-101")

    print("\n=== Resultado de preparación ===")
    for k, v in resultado.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    test_modulo_preparacion()
