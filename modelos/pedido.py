class Pedido:
    def __init__(self, id, cliente, estado, items=None):
        self.id = id
        self.cliente = cliente
        self.estado = estado
        self.items = items or []

    def __repr__(self):
        return f"<Pedido {self.id} - {self.estado}>"

class Item:
    def __init__(self, sku, cantidad):
        self.sku = sku
        self.cantidad = cantidad

    def __repr__(self):
        return f"<Item {self.sku} x {self.cantidad}>"
