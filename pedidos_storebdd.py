from dataclasses import dataclass
from typing import Dict, Optional, List
from datetime import datetime
import uuid
from modelos.pedido import Pedido, Item


class PedidoStore:
    """
    Simula una base de datos en memoria que almacena pedidos y maneja stock.
    Es usada por todos los módulos del sistema.
    """
    def __init__(self):
        # Diccionario que actúa como 'tabla' de pedidos
        self.pedidos: Dict[str, Pedido] = {}

        # Simulación de stock inicial
        self.stock: Dict[str, int] = {
            "SKU001": 10,
            "SKU002": 5,
            "SKU003": 15
        }

    def generar_id(self) -> str:
        """Genera un ID único de pedido."""
        return f"ORDER-{str(uuid.uuid4())[:8].upper()}"

    def guardar_pedido(self, pedido: Pedido) -> None:
        """Guarda o actualiza un pedido en el 'store'."""
        self.pedidos[pedido.id] = pedido

    def obtener_pedido(self, order_id: str) -> Optional[Pedido]:
        """Obtiene un pedido por su ID."""
        return self.pedidos.get(order_id)

    def actualizar_stock(self, sku: str, cantidad: int) -> bool:
        """
        Resta cantidad al stock de un SKU.
        Devuelve True si se actualizó correctamente, False si no había stock suficiente.
        """
        if sku not in self.stock:
            return False
        if self.stock[sku] < cantidad:
            return False
        self.stock[sku] -= cantidad
        return True

    def listar_pedidos(self) -> List[Pedido]:
        """Devuelve la lista de todos los pedidos registrados."""
        return list(self.pedidos.values())
