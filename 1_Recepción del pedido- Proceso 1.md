

# Módulo 1 – Recepción del pedido

## ► Idea general

Este proceso es simplemente **recibir el pedido que envía el cliente en formato JSON**, revisar que tenga los datos básicos que necesitamos y luego **guardarlo/ponerlo en una lista (cola)** para que después lo tomen los demás pasos (verificación de disponibilidad, pago, etc.).

---

## ► Datos mínimos que debería traer el JSON

- **Cliente**
    - ID del cliente o al menos un email.
- **Productos**
    - Una lista con al menos un producto.
    - Cada producto con: código (SKU o nombre) y cantidad.
- **Dirección de envío**
    - O bien la dirección escrita, o un identificador guardado en el sistema.
- **Forma de pago**
    - Ejemplo: tarjeta, transferencia, efectivo.



---


## Nivel 1 (Algoritmo general)

1. **Recibir pedido** (llega en JSON).
2. **Revisar campos obligatorios**.
3. **Encolar** para el siguiente proceso.
4. **Responder** al cliente con la confirmación.

---
## Nivel 2 (Refinamiento de cada paso)

1. **Recibir pedido (JSON)**   
    1.1 Leo el contenido.  
    1.2 Chequeo que **no esté vacío**.  
    1.3 Convierto el texto a **objeto JSON**.  
    1.4 Creo un **código de seguimiento**.
    1.5 Agrego la fecha y hora de llegada.
    
2. **Chequear contenido**  
	2.1 Por cada campo obligatorio Revisar 
		2.2 **Si falta algo → Rechazar e informar**  
		2.3 **Si está completo → Asignar número y guardar**  

3. **Encolar**  
    3.1 Preparo un **mensaje simple** con `order_id`.  
    3.2 Lo pongo en la **cola de pedidos pendientes**.  
    
4. **Responder al cliente**  
    4.1 Armo un **mensaje de confirmación**.  
    4.2 Incluyo **número de pedido** y **estado actual**.  
    4.3 **Envió** la respuesta.
    

---

## Nivel 3

1. **Recibir pedido (JSON)**   
    1.1 Leo el contenido.  
    1.2 Chequeo que **no esté vacío**.  
	    1.2.1 Si esta vacío → pasar a **Paso 2.2** (rechazar).  
    1.3 Convierto el texto a **objeto JSON**.
    1.4 Creo un **código de seguimiento**.
    1.5 Agrego la fecha y hora de llegada.
    
2. **Chequear contenido**  
	2.1 Por cada campo obligatorio Revisar
	    2.1.1 Cliente: debe traer **email**.  
	    2.1.2 Productos: debe haber **al menos uno**.  
	    2.1.3 Por cada producto: tiene **código (sku)** y **cantidad > 0**.  
	    2.1.4 Dirección de envío: texto.  
	    2.1.5 Precio: precio del producto en el momento de la compra precio > 0
	    2.1.6 Pago: verificar que exista un método de pago (tarjeta, transferencia, etc.).
    
	2.2. **Si falta algo → Rechazar e informar**  
		2.2.1 Armo la **lista de errores** (qué falta o qué está mal).  
		2.2.2 Marco el pedido como **rechazado** (no lo encolo).  
		2.2.3 **Saltar al paso 4**.
	
	2.3. **Si está completo → Asignar número y guardar**  
	    2.3.1 Genero un **número de pedido (order_id)** único.  
	    2.3.2 Armo un **registro básico** con cliente, productos, dirección y pago.  
	    2.3.3 Pongo **estado = “RECIBIDO”**.  
	    2.3.4 **Guardo** el registro junto con el código de seguimiento.
    
3. **Encolar**  
    3.1 Preparo un **mensaje simple** con `order_id`.  
    3.2 Lo pongo en la **cola de pedidos pendientes**.  
    
4. **Responder al cliente**  
    4.1 Armo un **mensaje de confirmación**. 
	    Si el pedido esta marcado como recibido
		    4.1.1 Mensaje **éxito**: “Pedido recibido”, incluir `order_id` y estado “En espera de verificación”.
		si no
		    4.1.2 Mensaje **error** (si vino desde Paso 2.2.2): “Pedido rechazado”, incluir **lista de errores**.
    4.2 Incluyo **número de pedido** y **estado actual**.  
    4.3 **Envió** la respuesta.

# Pseudocódigo – Recepción de Pedido

```sql
INICIO RecepcionPedido

1) RECIBIR pedido (JSON)

   LEER contenido
   SI contenido está vacío ENTONCES
       ERRORES ← ["Pedido vacío"]
       IR A Paso 4 (Responder con error)
   FIN SI

   CONVERTIR contenido a objeto JSON

   CREAR codigo_seguimiento
   GUARDAR fecha_hora_actual

2) CHEQUEAR contenido (validar campos)

   ERRORES ← []

   SI cliente.email no existe ENTONCES
       AGREGAR "Falta email de cliente" a ERRORES
   FIN SI

   SI productos no existe O está vacío ENTONCES
       AGREGAR "Falta al menos un producto" a ERRORES
   SINO
       PARA cada producto EN productos HACER
           SI producto.sku no existe ENTONCES
               AGREGAR "Falta código de producto" a ERRORES
           FIN SI
           SI producto.cantidad <= 0 ENTONCES
               AGREGAR "Cantidad inválida" a ERRORES
           FIN SI
           
       FIN PARA
   FIN SI

   SI direccion_envio no existe ENTONCES
       AGREGAR "Falta dirección de envío" a ERRORES
   FIN SI
	
	SI producto.precio <= 0 ENTONCES
	               AGREGAR "Precio inválido" a ERRORES
	           FIN SI
   
   SI pago.metodo no existe ENTONCES
       AGREGAR "Falta método de pago" a ERRORES
   FIN SI

   SI ERRORES no está vacío ENTONCES
       ESTADO ← "RECHAZADO"
       IR A Paso 4 (Responder con error)
   SINO
       order_id ← GENERAR nuevo número único
       CREAR registro con datos del pedido
       ESTADO ← "RECIBIDO"
       GUARDAR registro
   FIN SI

3) ENCOLAR pedido

   mensaje ← { order_id, cliente, productos }
   ENVIAR mensaje a ColaPedidosPendientes

4) RESPONDER al cliente

   SI ESTADO = "RECIBIDO" ENTONCES
       RESPUESTA ← "Pedido recibido", incluir order_id
   SINO
       RESPUESTA ← "Pedido rechazado", incluir lista de ERRORES
   FIN SI

   ENVIAR RESPUESTA al cliente

FIN RecepcionPedido
```
