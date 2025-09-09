Módulo 5: Envío y seguimiento
    Objetivo: Gestionar el proceso de envío de un pedido, desde la confirmación de su estado hasta la notificación al cliente con un número de seguimiento.

Algoritmo
    1. Verificar que el pedido está en estado de envío.
    2. Generar una guía de envío.
    3. Actualizar el registro del pedido en el sistema.
    4. Notificar al cliente sobre el estado de su envío.

Nivel 1 de Refinamiento 
    1. Verificar estado del pedido:
        1.1 Obtener pedido por ID.
        1.2 Revisar que el estado sea “LISTO_PARA_ENVIO”.
        1.3 Si no está listo terminar el proceso o alertar.

    2. Generar guía de envío:
        2.1 Seleccionar transportista según método de envío.
        2.2 Crear tracking_id.
        2.3 Asociar guía al pedido.

    3. Actualizar registro del pedido:
        3.1 Cambiar estado del pedido a 'EN_TRANSITO'.
        3.2 Guardar número de guía y transportista.
        3.3 Persistir cambios en la base de datos.

    4. Notificar al cliente:
        4.1 Enviar correo o mensaje con número de guía y transportista.
        4.2 Registrar notificación en historial de pedidos.

Nivel 2 de Refinamiento
    1. Verificar estado del pedido:
        1.1 pedido = obtener_pedido(pedido_id)
        1.2 Verificar que pedido.estado == "LISTO_PARA_ENVIO"
        1.3 Si no, devolver error "Pedido no listo para envío"

    2. Generar guía de envío:
        2.1 carrier = seleccionar_carrier(metodo_envio)
        2.2 tracking_id = generar_tracking()
        2.3 Asociar guía al pedido
            2.3.1 Crear objeto envio con pedido_id, tracking_id, carrier, estado = "CREADO"
            2.3.2 Guardar envio en la base de datos.
        
    3. Actualizar registro del pedido:
        3.1 Cambiar estado del pedido a 'EN_TRANSITO'.
        3.2 Guardar número de guía y transportista.
        3.3 Persistir cambios en la base de datos.

    4. Notificar al cliente:
        4.1 enviar_notificacion(cliente, tracking_id, carrier)
        4.2 Registrar notificación en historial de pedidos.

Pseudocódigo
    FUNCTION procesar_envio(pedido_id, metodo_envio="estandar"):

    ### 1. Verificar estado del pedido ###
    pedido = obtener_pedido(pedido_id)

    IF pedido.estado != "LISTO_PARA_ENVIO":
        RETURN ERROR "Pedido no listo para envío"

    ### 2. Generar guía de envío ###
    carrier = seleccionar_carrier(metodo_envio)
    tracking_id = generar_tracking()

    envio = {
        "pedido_id": pedido_id,
        "tracking_id": tracking_id,
        "carrier": carrier,
        "estado": "CREADO",
        "historial": [
            { "estado": "CREADO", "ts": now() }
        ]
    }
    guardar_envio(envio)

    ### 3. Actualizar registro del pedido ###
    pedido.estado = "EN_TRANSITO"
    pedido.guia = tracking_id
    pedido.carrier = carrier
    guardar_pedido(pedido)

    ### 4. Notificar al cliente ###
    enviar_notificacion(pedido.cliente, tracking_id, carrier)
    registrar_notificacion(pedido.id, tracking_id, carrier)

    RETURN envio
