import random
from m0_compras import armar_pedido, obtener_cliente, seleccionar_productos 
from m1_recepcion_del_pedido import RecepcionPedido
from m2_verificacion_disponibilidad import Verificacion_disponibilidad_producto, Deposito
from m3_procesamiento_de_pago import ModuloPago, Api_banco
from m4_preparacion_de_pedido import ModuloPreparacion
from m5_envio_y_seguimiento import ModuloEnvios
from modelos.pedido import Pedido, Producto
from modulo_notificaciones import Modulo_Notificaciones

##CREAMOS LOS PRODUCTOS DISPONIBLES
stock = "stock.json"
deposito = Deposito()  

modulo_Notificaciones = Modulo_Notificaciones()
print("\n++++++++++++++++++ BIENVENIDO AL SISTEMA DE COMPRAS ONLINE ++++++++++++++++++\n")

##EL CLIENTE SELECCIONA EL PEDIDO
pedido_source = armar_pedido(deposito)
recepcion_pedido = RecepcionPedido(pedido_source)

if __name__ == "__main__":

    #####VALIDAMOS DATOS PEDIDO MODULO1########
    validacion_datos_pedido = recepcion_pedido.validar_pedido()
    #CREAMOS PEDIDO 
    if validacion_datos_pedido:
        print (f"Validez del pedido: {validacion_datos_pedido}")##MODULO NOTIFICACIONES
        orden_pedido = recepcion_pedido.crear_pedido()
        print (f"\n--------- Pedido CREADO CON EXITO ---------\n")
        print(orden_pedido)
        print (f"-------------------------------------------\n")

        ######VERIFICAMOS DISPONIBILIDAD MODULO 2#############   
        # deposito = Deposito()  
        verificacion_disponibilidad = Verificacion_disponibilidad_producto(orden_pedido, deposito)
        disponibilidad_stock = verificacion_disponibilidad.consultar_stock()
        print (f"Disponibilidad de productos: {disponibilidad_stock}")

        if disponibilidad_stock:
            #CREAMOS LA RESERVA
            reserva = verificacion_disponibilidad.reservar()
            stock_reservado = verificacion_disponibilidad.reservas

            print("\n--------- STOCK RESERVADO ---------\n")
            i=1
            for producto in verificacion_disponibilidad.stock_reservado:
                print(f"Producto {i}:\n▸ Nombre: {producto['nombre']}\n▸ SKU: {producto['sku']}\n▸ Cantidad reservada: {producto['cantidad_solicitada']}\n")
                i += 1
                #▸ Expiración: {producto['expiracion'].strftime('%Y-%m-%d %H:%M:%S')}
                #######VERIFICACION DE PAGO MODULO 3########
                api_banco=Api_banco
                moduloPago = ModuloPago(orden_pedido, api_banco)
                aprobacion_pago = moduloPago.verificar_pago()
                
            if aprobacion_pago:
                #NOTIFICAR ACEPTAR PEDIDO
                modulo_Notificaciones.notificar("\n--------- PAGO APROBADO ---------\n")

                ######PREPARACION DEL PEDIDO MODULO 4############# 
                moduloPreparacion = ModuloPreparacion() 
                preparacion_pedido = moduloPreparacion.preparar_pedido(orden_pedido)

                if preparacion_pedido:
                    print("\n--------- PEDIDO PREPARADO ---------\n")

                    ######ENVIO Y SEGUIMIENTO MODULO 5############# 
                    moduloEnvios = ModuloEnvios()
                    envio = moduloEnvios.procesar_envio(orden_pedido)
                    #print (f"el pedido fue ENVIADO CON EXITO {orden_pedido}")
                    modulo_Notificaciones.enviar_seguimiento(envio.tracking_id, envio.carrier)

                else: #MODULO 4
                    print("\n--------- PEDIDO RECHAZADO ---------\n")
                    modulo_Notificaciones.pedido_rechazado(moduloPreparacion.errores)

            else:#MODULO 3
                #NOTIFICAR RECHAZAR PROBLEMA DE PAGO
                #print("rechazo por problemas con el pago")
                modulo_Notificaciones.pedido_rechazado(moduloPago.errores)
    else:#MODULO 2
        #print("stock insuficiente")
        #NOTIFICAR POR FALTA DE STOCK
        modulo_Notificaciones.pedido_rechazado(["No hay stock suficiente"])
    
else:#MODULO1
    # for error in recepcion_pedido.errores_pedido():
    #     print (error)
    #NOTIFICAR FALTA DE DATOS EN LA SOLICITUD DE PEDIDO
    modulo_Notificaciones.pedido_rechazado(recepcion_pedido.errores)
    #FALTA PERSISTIR DESDE EL MODULO RECEPCION Y NOTIFICAR








    



