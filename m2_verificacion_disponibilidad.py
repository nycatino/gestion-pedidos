from datetime import datetime, timedelta
import random

DEPOSITO_POR_DEFECTO = "deposito1"

class Verificacion_disponibilidad_producto:
    def __init__(self,orden_pedido, deposito = DEPOSITO_POR_DEFECTO):
        self.orden_pedido = orden_pedido
        self.deposito = deposito
        self.reserva_id = f"STOCK_CHECK_{self.orden_pedido}"
        self.stock_disponible = True
        self.consulta_disponibilidad_productos = []
        self.stock_reservado = []

    def consultar_stock(self):
        
        for producto in self.orden_pedido.productos:
            sku = producto.sku
            cantidad_solicitada = producto.cantidad_solicitada
            cant_disponible = self.deposito.disponibilidad(sku)
            ## funcion que recibe sku y devuelva aleatorio.

            if cant_disponible >= cantidad_solicitada :
                estado_disponibilidad_producto = "STOCK_DISPONIBLE"
            else: 
                estado_disponibilidad_producto = "SIN_STOCK"
                self.stock_disponible = False
            self.consulta_disponibilidad_productos.append = {
                "producto": producto.nombre,
                "sku": producto.sku,
                "cantidad_solicitada": cantidad_solicitada,
                "cantidad_disponible": cant_disponible,
                "disponibilidad": estado_disponibilidad_producto
                }
            
        return self.stock_disponible

    def reservar(self):

        stock_disponible = self.consultar_stock()

        if stock_disponible:
            self.stock_reservado = self.deposito.reservar( fecha_hora_reserva = datetime.now(),
            productos = self.consulta_disponibilidad_productos)

        return True
    

    

class Deposito:
    def __init__(self, nombre = DEPOSITO_POR_DEFECTO):
        self.nombre = nombre,
        self.reserva_id = None

    def disponibilidad(self, sku):
        sku +=0#no hace nada simplemente para molestar
        cant_disponible = random.randint(0, 100)
        return cant_disponible
    
    def reservar(self, fecha_hora_reserva , productos):
        productos_reservados=[]
        expiracion = fecha_hora_reserva + timedelta(minutes=30)
        
        for producto in productos:

            productos_reservados.append({"nombre":producto["nombre"],
                    "sku": producto["sku"],
                    "cantidad_solicitada": producto["cantidad_solicitada"],
                    "cantidad_reservada": producto["cantidad_solicitada"],
                    "fecha_hora_reserva":fecha_hora_reserva,
                    "expiracion": expiracion
                })
        return productos_reservados

        


            
    