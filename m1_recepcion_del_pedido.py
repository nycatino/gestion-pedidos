import json
import uuid
from datetime import datetime
from typing import Dict, Any, Union, Callable, Optional, List
from modelos.pedido import Pedido, Item


class RecepcionPedido:
    def __init__(self, pedidos_source):
       
       self.data = json.loads(pedidos_source)
       self.errores = [] 

    def validar_pedido(self):
        """ valida los campos """
        try:
            data = json.loads(self.pedido_json)
        except json.JSONDecodeError:
            return {"estado": "RECHAZADO", "errores": ["JSON inválido"]}

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
        
        # CREAMOS LISTA DE PRODUCTOS
        for producto in self.data["productos"]:
            try:
                sku = productos["sku"]
                cantidad_solicitada = int(producto["cantidad_solicitada"])
                precio = int(producto["precio"]),
                productos.append(Item(sku=sku, cantidad_solicitada = cantidad_solicitada, precio = precio))
                total_a_pagar += precio 
            except Exception as e:
                self.errores.append(f"Producto inválido: {producto} ({e})")

        # --- Generar orden de pedido ---

        order_id = f"ORDER-{str(uuid.uuid4())[:8]}"
        orden_pedido = Pedido(
            id = order_id,
            cliente = self.data["cliente"],
            fecha_recepcion = datetime.now(),
            estado = "RECIBIDO",
            productos = productos,
            datos_del_pago = self.data["datos_de_pago"],
            pedido_persistido = False,
            total_a_pagar = total_a_pagar
        )

        return {orden_pedido}
    