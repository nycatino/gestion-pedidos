import json
import uuid
from datetime import datetime
from typing import Dict, Any, Union, Callable, Optional, List
from modelos.pedido import Pedido, Item


class ModuloRecepcion:
    def __init__(self, pedidos_source: Union[Dict[str, Pedido], Callable[[str], Optional[Pedido]]] = None):
        """
        pedidos_source puede ser:
         - un diccionario compartido de pedidos
         - una función getter(order_id) -> Pedido | None
        """
        self._internal_pedidos: Dict[str, Pedido] = {}

        if pedidos_source is None:
            self._getter = lambda oid: self._internal_pedidos.get(oid)
            self._store = self._internal_pedidos
        elif isinstance(pedidos_source, dict):
            self._getter = lambda oid, _d=pedidos_source: _d.get(oid)
            self._store = pedidos_source
        elif callable(pedidos_source):
            self._getter = pedidos_source
            self._store = None
        else:
            raise ValueError("pedidos_source debe ser dict, callable o None")

    def recibir_pedido(self, pedido_json: str) -> Dict[str, Any]:
        """Recibe un pedido en formato JSON, valida los campos y lo guarda en pedidos_store."""
        errores = []
        try:
            data = json.loads(pedido_json)
        except json.JSONDecodeError:
            return {"estado": "RECHAZADO", "errores": ["JSON inválido"]}

        # --- Validaciones básicas ---
        if not data.get("cliente"):
            errores.append("Falta nombre del cliente")
        if not data.get("email"):
            errores.append("Falta email del cliente")
        if not data.get("direccion_envio"):
            errores.append("Falta dirección de envío")
        if not data.get("productos"):
            errores.append("Falta lista de productos")

        if errores:
            return {"estado": "RECHAZADO", "errores": errores}

        # --- Crear objetos Item ---
        items = []
        for p in data["productos"]:
            try:
                sku = p["sku"]
                cantidad = int(p["cantidad"])
                items.append(Item(sku=sku, cantidad=cantidad))
            except Exception as e:
                errores.append(f"Producto inválido: {p} ({e})")

        if errores:
            return {"estado": "RECHAZADO", "errores": errores}

        # --- Generar pedido ---
        order_id = f"ORDER-{str(uuid.uuid4())[:8]}"
        pedido = Pedido(
            id=order_id,
            cliente=data["cliente"],
            estado="RECIBIDO",
            items=items
        )

        # --- Guardar pedido ---
        if self._store is not None:
            self._store[order_id] = pedido

        return {
            "estado": "RECIBIDO",
            "order_id": order_id,
            "cliente": pedido.cliente,
            "total_items": len(items)
        }
