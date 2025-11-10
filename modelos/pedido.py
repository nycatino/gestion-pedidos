import random


class Pedido:
    def __init__(self, id, cliente, estado, productos=None):
        self.id = id
        self.cliente = cliente
        self.estado = estado
        self.productos = productos or []
        self.datos_del_pago = None
        self.total_a_pagar = 0
    
    def calcular_total_a_pagar(self):
        for producto in self.productos:
            self.total_a_pagar += producto["precio"]

    def __repr__(self):
        return f"<Pedido {self.id} - {self.estado}>"

class Producto:
    def __init__(self, sku, nombre, precio, cantidad_solicitada=None):
        self.sku = sku
        self.nombre = nombre
        self.cantidad_solicitada = cantidad_solicitada
        self.precio = precio

    @staticmethod
    def crear_productos():
        productos=[]
        for i in range (5):
            nombre = f"Articulo{i}"
            sku = f"ART_{i}"
            precio = random.randint(1000, 20000)
            producto = Producto(sku, nombre, precio)
            productos.append(producto)
        return productos    

    def __repr__(self):
        return f"<Producto: {self.nombre} (sku: {self.sku}, Precio: {self.precio})>"
