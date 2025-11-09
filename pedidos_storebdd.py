from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import uuid

@dataclass
class Producto:
    sku: str
    nombre: str
    cantidad: int
    precio: float

@dataclass
class Pedido:
    id: str
    cliente: str
    email: str
    direccion_envio: str
    productos: List[Producto]
    estado: str = "INICIAL"
    total: float = 0.0
    fecha_creacion: datetime = field(default_factory=datetime.now)
    pago: Optional[dict] = None
    guia: Optional[str] = None
    carrier: Optional[str] = None

class PedidoStore:
    def __init__(self):
        self.pedidos: Dict[str, Pedido] = {}
        self.stock = {
            "SKU001": 10,
            "SKU002": 5,
            "SKU003": 15
        }

    def generar_id(self) -> str:
        return f"ORD-{str(uuid.uuid4())[:8].upper()}"

    def guardar_pedido(self, pedido: Pedido):
        self.pedidos[pedido.id] = pedido

    def obtener_pedido(self, order_id: str) -> Optional[Pedido]:
        return self.pedidos.get(order_id)

    def actualizar_stock(self, sku: str, cantidad: int):
        if sku in self.stock:
            self.stock[sku] -= cantidad
