import uuid
from datetime import datetime
from typing import Dict, Any, Union, Callable, Optional, List
from modelos.pedido import Pedido, Producto


class RecepcionPedido:
    def __init__(self, pedidos_source):
       
       self.data = pedidos_source
       self.errores = [] 

    def validar_pedido(self):
        """ valida los campos """

        data = self.data
        
        # --- Validaciones básicas ---
        if not data.get("cliente"):
            self.errores.append("Falta nombre del cliente")
        if not data.get("email"):
            self.errores.append("Falta email del cliente")
        if not data.get("direccion_envio"):
            self.errores.append("Falta dirección de envío")
        if not data.get("productos"):
            self.errores.append("Falta lista de productos")
        if not data.get("datos_del_pago"):
            self.errores.append("Faltan datos del pago")
        if not data.get("metodo_envio"):
            self.errores.append("Falta método de envío")
        #FALTA REVISAR PRODUCTO POR PRODUCTO QUE ESTE EL SKU, PRECIO ETC, REALIZADO EN CREAR PEDIDO, DEBERIAMOS VER ESO ACA   

        if self.errores:
            return False 
        else:
            return True
        
    def errores_pedido(self):
        return self.errores
    
    def crear_pedido(self):
        # --- Crear objetos Item ---
        productos = []
        total_a_pagar = 0
        # CREAMOS LISTA DE PRODUCTOS
        for producto in self.data["productos"]:
            try:
                sku = producto["sku"]
                nombre = producto["nombre"]
                cantidad_solicitada = int(producto["cantidad_solicitada"])
                precio = int(producto["precio"])             
            
                producto_obj = Producto(
                    sku=sku,
                    nombre=nombre,
                    precio=precio,
                    cantidad_solicitada=cantidad_solicitada
                )

                productos.append(producto_obj)
                total_a_pagar += precio * cantidad_solicitada

            except Exception as e:
                self.errores.append(f"Producto inválido: {producto} ({e})")
                print(f" Error al crear producto: {producto} ({e})")

                return False 
             
        # --- Generar orden de pedido ---

        order_id = f"ORDER-{str(uuid.uuid4())[:8]}"
        orden_pedido = Pedido(
            id = order_id,
            cliente = self.data["cliente"],
            email = self.data["email"],
            estado = "RECIBIDO",
            metodo_envio = self.data["metodo_envio"],
            productos = productos,
            fecha_recepcion = datetime.now(),
            datos_del_pago = self.data["datos_del_pago"],
            total_a_pagar = total_a_pagar
        )

        return orden_pedido
