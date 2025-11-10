class Pedido:
    def __init__(self, id, cliente, estado, productos=None):
        self.id = id
        self.cliente = cliente
        self.estado = estado
        self.productos = productos or []
        self.datos_del_pago = None
        self.total_a_pagar = None

    def __repr__(self):
        return f"<Pedido {self.id} - {self.estado}>"

class Producto:
    def __init__(self, sku, cantidad_solicitada, precio):
        self.sku = sku
        self.cantidad_solicitada = cantidad_solicitada
        self.precio = precio
        

    def __repr__(self):
        return f"<Item {self.sku} x {self.cantidad_solicitada}>"
