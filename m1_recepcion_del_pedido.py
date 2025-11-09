import json
from datetime import datetime
from pedidos_storebdd import Pedido, Producto
from modelos.pedido import Pedido


class ModuloRecepcion:
    def __init__(self, pedidos_store):
        self.pedidos_store = pedidos_store

    def recibir_pedido(self, pedido_json: str):
        errores = []
        try:
            data = json.loads(pedido_json)
        except json.JSONDecodeError:
            return {"estado": "RECHAZADO", "errores": ["JSON inválido"]}

        # Validaciones básicas
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

        # Crear objetos Producto
        productos = []
        for p in data["productos"]:
            try:
                prod = Producto(
                    sku=p["sku"],
                    nombre=p.get("nombre", "Desconocido"),
                    cantidad=int(p["cantidad"]),
                    precio=float(p["precio"])
                )
                productos.append(prod)
            except Exception:
                errores.append(f"Producto inválido: {p}")

        if errores:
            return {"estado": "RECHAZADO", "errores": errores}

        total = sum(p.precio * p.cantidad for p in productos)
        pedido = Pedido(
            id=self.pedidos_store.generar_id(),
            cliente=data["cliente"],
            email=data["email"],
            direccion_envio=data["direccion_envio"],
            productos=productos,
            total=total,
            estado="RECIBIDO"
        )

        self.pedidos_store.guardar_pedido(pedido)

        return {"estado": "RECIBIDO", "order_id": pedido.id, "total": total}
