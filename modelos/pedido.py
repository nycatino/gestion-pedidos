class Pedido:
    def __init__(self, id, cliente, estado, items=None):
        self.id = id
        self.cliente = cliente
        self.estado = estado
        self.items = items or []

    def __repr__(self):
        return f"<Pedido {self.id} - {self.estado}>"
