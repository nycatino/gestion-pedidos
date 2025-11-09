from datetime import datetime, timedelta
import random

DEPOSITO_POR_DEFECTO = "deposito1"

class Verificacion_disponibilidad_producto:
    def __init__(self,order_id, deposito = DEPOSITO_POR_DEFECTO):
        self.order_id = order_id
        self.deposito = deposito
        self.reserva_id = f"STOCK_CHECK_{self.order_id}"
        self.disponibilidad_total = True
        self.consulta_disponibilidad_productos = []
        self.stock_reservado = []
        self.berna = 10

    def consultar_stock(self):
        
        for producto in self.order_id.productos:
            #order_id tendria que tener un atributo productos, que deberia ser una lista donde cada elemento es un diccionario {sku, nombre, cantidad_solicitada}
            sku = producto.sku
            cantidad_solicitada = producto.cantidad_solicitada
            cant_disponible = self.deposito.disponibilidad(sku)
            ## funcion que recibe sku y devuelva aleatorio.

            if cant_disponible >= cantidad_solicitada :
                estado_disponibilidad_producto = "STOCK_DISPONIBLE"
            else: 
                estado_disponibilidad_producto = "SIN_STOCK"
                self.disponibilidad_total = False
            self.consulta_disponibilidad_productos.append = {
                "producto": producto.nombre,
                "sku": producto.sku,
                "cantidad_solicitada": cantidad_solicitada,
                "cantidad_disponible": cant_disponible,
                "disponibilidad": estado_disponibilidad_producto
                }
            
        return self.disponibilidad_total

    def reservar(self):

        stock_disponible = self.consultar_stock()
        if stock_disponible:
            self.stock_reservado = self.deposito.reservar( fecha_hora_reserva = datetime.now(),
            productos = self.consulta_disponibilidad_productos)

        return self.stock_reservado

class Deposito:
    def __init__(self, reserva_id, nombre = DEPOSITO_POR_DEFECTO):
        self.nombre = nombre,
        self.reserva_id = reserva_id

    def disponibilidad(self,sku):
        cant_disponible = random.randint(0, 100)
        return cant_disponible
    
    def reservar(self, fecha_hora_reserva , productos):
        reservas=[]
        expiracion = fecha_hora_reserva + timedelta(minutes=30)
        for producto in productos:

            reservas.append({"nombre":productos["nombre"],
                    "sku": productos["sku"],
                    "cantidad_solicitada": productos["cantidad_solicitada"],
                    "cantidad_reservada": productos["cantidad_solicitada"],
                    "fecha_hora_reserva":fecha_hora_reserva,
                    "expiracion": expiracion
                })
        return reservas

        


            
    