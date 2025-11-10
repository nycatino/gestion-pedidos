import random


class Pedido:
    def __init__(self, id, cliente, email, estado, productos=None, fecha_recepcion=None, datos_del_pago=None, total_a_pagar = 0 ):
        self.id = id
        self.cliente = cliente
        self.email = email
        self.estado = estado
        self.productos = productos or []
        self.datos_del_pago = datos_del_pago
        self.total_a_pagar = total_a_pagar
        self.fecha_recepcion = fecha_recepcion
        self.pedido_persistido = False
    
    def calcular_total_a_pagar(self):
        for producto in self.productos:
            self.total_a_pagar += producto["precio"]

    def __str__(self):
        productos_str = "\n".join([
            f" - {p.nombre} x{p.cantidad_solicitada} = ${p.precio * p.cantidad_solicitada}"
            for p in self.productos
        ])
        return (
            f"Pedido: {self.id}\n"
            f"Cliente: {self.cliente}\n"
            f"Fecha: {self.fecha_recepcion.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Estado: {self.estado}\n"
            f"Forma de pago: {self.datos_del_pago.get('metodo', 'N/A')}\n"
            f"Productos:\n{productos_str}\n"
            f"Total a pagar: ${self.total_a_pagar}\n"
        )

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
