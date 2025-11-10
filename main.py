import random
from m0_compras import seleccionar_productos 
from m1_recepcion_del_pedido import RecepcionPedido
from m2_verificacion_disponibilidad import Verificacion_disponibilidad_producto, Deposito
from m3_procesamiento_de_pago import ModuloPago, Api_banco
from modelos.pedido import Pedido, Producto

##CREAMOS LOS PRODCUTOS DISPONIBLES
productos_disponibles = Producto.crear_productos()

if __name__ == "__main__":
    
    ##EL CLIENTE SELECCIONA EL PEDIDO
    pedido_source = seleccionar_productos(productos_disponibles)
    #####VALIDAMOS DATOS PEDIDO MODULO1########
    recepcion_pedido = RecepcionPedido(pedido_source)
    validacion_datos_pedido = recepcion_pedido.validar_pedido()
    #CREAMOS PEDIDO 
    if validacion_datos_pedido:
        print (f"el pedido fue validado {validacion_datos_pedido}")##MODULO NOTIFICACIONES
        orden_pedido = recepcion_pedido.crear_pedido()
        print (f"el pedido fue CREADO CON EXITO {orden_pedido}")

        ######VERIFICAMOS DISPONIBILIDAD MODULO 2#############   
        deposito = Deposito()  
        verificacion_disponibilidad = Verificacion_disponibilidad_producto(orden_pedido, deposito)
        disponibilidad_stock = verificacion_disponibilidad.consultar_stock()
        print (f"disponibilidad productos: {disponibilidad_stock}")

        if disponibilidad_stock:
            #CREAMOS LA RESERVA
            reserva = verificacion_disponibilidad.reservar()
            stock_reservado = verificacion_disponibilidad.stock_reservado
            print("STOCK RESERVADO: \n")
            for producto in verificacion_disponibilidad.stock_reservado:
                print(f"""
                Producto reservado:
                ▸ Nombre: {producto['nombre']}
                ▸ SKU: {producto['sku']}
                ▸ Cantidad solicitada: {producto['cantidad_solicitada']}
                ▸ Cantidad reservada: {producto['cantidad_reservada']}
                ▸ Fecha de reserva: {producto['fecha_hora_reserva'].strftime('%Y-%m-%d %H:%M:%S')}
                ▸ Expira: {producto['expiracion'].strftime('%Y-%m-%d %H:%M:%S')}
                """)
                #######VERIFICACION DE PAGO MODULO 3########
                api_banco=Api_banco
                moduloPago = ModuloPago(orden_pedido, api_banco)
                aprobacion_pago = moduloPago.verificar_pago()
                
                if aprobacion_pago:
                    print(f"PAGO APROBADO: {aprobacion_pago}" )
                    #NOTIFICAR ACEPTAR PEDIDO
                else:#MODULO 3
                    #NOTIFICAR RECHAZAR PROBLEMA DE PAGO
                    print("rechazo por problemas con el pago")
        else:#MODULO 2
            print("stock insuficiente")
            #NOTIFICAR POR FALTA DE STOCK
    
    else:#MODULO1
        for error in recepcion_pedido.errores_pedido():
            print (error)
            #NOTIFICAR FALTA DE DATOS EN LA SOLICITUD DE PEDIDO
            #FALTA PERSISTIR DESDE EL MODULO RECEPCION Y NOTIFICAR








    