import random
from m0_compras import seleccionar_productos 
from m1_recepcion_del_pedido import RecepcionPedido
from m2_verificacion_disponibilidad import Verificacion_disponibilidad_producto, Deposito
from m3_procesamiento_de_pago import ModuloPago, Api_banco
from modelos.pedido import Pedido, Producto

productos_disponibles = Producto.crear_productos()

if __name__ == "__main__":
    productos_seleccionados = seleccionar_productos(productos_disponibles)

    recepcion_pedido = RecepcionPedido(productos_seleccionados)
    validacion = recepcion_pedido.validar_pedido()
