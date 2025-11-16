from datetime import datetime, timedelta
import json
import os
import random

DEPOSITO_POR_DEFECTO = "deposito1"
ARCHIVO_STOCK = "stock.json"
ARCHIVO_RESERVAS = "reservas.json"

class Verificacion_disponibilidad_producto:
    def __init__(self,orden_pedido, deposito):
        self.orden_pedido = orden_pedido
        self.deposito = deposito
        self.reserva_id = f"STOCK_CHECK_{random.randint(1,1000000)}"
        self.stock_disponible = True
        self.consulta_disponibilidad_productos = []
        self.stock_reservado = []
        self.reservas = []

        self.errores = []

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
            self.consulta_disponibilidad_productos.append({
                "nombre": producto.nombre,
                "sku": producto.sku,
                "cantidad_solicitada": cantidad_solicitada,
                "cantidad_disponible": cant_disponible,
                "disponibilidad": estado_disponibilidad_producto
                })
            
        return self.stock_disponible

    def reservar(self):

        self.stock_reservado = self.deposito.reservar( fecha_hora_reserva = datetime.now(),
            productos = self.consulta_disponibilidad_productos)
        
        if self.stock_reservado:
            return True
        else: return False
    


    


class Deposito:
    def __init__(self, nombre="deposito1"):
        self.nombre = nombre
        self.stock = self.cargar_stock()
        self.reservas = self._cargar_reservas()


    def cargar_stock(self):
        with open(ARCHIVO_STOCK, "r") as f:
            return json.load(f)

    def guardar_stock(self):
        with open(ARCHIVO_STOCK, "w") as f:
            json.dump(self.stock, f, indent=4)

    def _cargar_reservas(self):
        if not os.path.exists(ARCHIVO_RESERVAS):
            return []

        try:
            with open(ARCHIVO_RESERVAS, "r") as f:
                contenido = f.read().strip()

                if contenido == "":
                    return []  # archivo vacío

                return json.loads(contenido)

        except json.JSONDecodeError:
            # archivo corrupto → lo reinicio
            return []

    
    def _guardar_reservas(self):
        with open(ARCHIVO_RESERVAS, "w") as f:
            json.dump(self.reservas, f, indent=4)

    def _buscar_producto(self, sku):
        for p in self.stock:
            if p["sku"] == sku:
                return p
        return None

    def disponibilidad(self, sku):
        prod = self._buscar_producto(sku)
        return prod["stock"] if prod else 0
    

    def _limpiar_reservas_expiradas(self):
        ahora = datetime.now()
        nuevas_reservas = []
        cambio = False

        for r in self.reservas:
            exp = datetime.strptime(r["expiracion"], "%Y-%m-%d %H:%M:%S")

            if exp < ahora:
                # devolver stock
                prod = self._buscar_producto(r["sku"])
                if prod:
                    prod["stock"] += r["cantidad_reservada"]
                cambio = True
            else:
                nuevas_reservas.append(r)

        if cambio:
            self.reservas = nuevas_reservas
            self.guardar_stock()
            self._guardar_reservas()

    def reservar(self, fecha_hora_reserva, productos):
        self._limpiar_reservas_expiradas()

        productos_reservados = []
        expiracion = fecha_hora_reserva + timedelta(minutes=3)

        for p in productos:
            sku = p["sku"]
            cantidad = p["cantidad_solicitada"]

            prod = self._buscar_producto(sku)
            if not prod or prod["stock"] < cantidad:
                return None  # stock insuficiente

            # descuenta stock
            prod["stock"] -= cantidad
            productos_reservados.append(p)

            # generar registro de reserva
            self.reservas.append({
                "sku": sku,
                "cantidad_reservada": cantidad,
                "expiracion": expiracion.strftime("%Y-%m-%d %H:%M:%S")
            })

        # guardar cambios persistentes
        self.guardar_stock()
        self._guardar_reservas()

        return productos_reservados


            
    