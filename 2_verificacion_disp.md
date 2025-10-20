# Módulo 1 – Recepción del pedido

## ► Idea general

◆ Este proceso es simplemente **recibir el pedido que envía el cliente en formato JSON**, revisar que tenga los datos básicos necesarios y luego **guardarlo/ponerlo en una lista (cola)** para que lo tomen los demás pasos (verificación de disponibilidad, pago, etc.).

---

## ► Datos mínimos que debería traer el JSON

◆ **Cliente**

* ID del cliente o al menos un email.

◆ **Productos**

* Una lista con al menos un producto.
* Cada producto con: código (SKU o nombre) y cantidad.

◆ **Dirección de envío**

* La dirección escrita, o un identificador guardado en el sistema.

◆ **Forma de pago**

* Tarjeta/Transferencia.

---

## Nivel 1 (Algoritmo general)

► 1) **Recibir pedido** (llega en JSON).
► 2) **Revisar campos obligatorios**.
► 3) **Encolar** para el siguiente proceso.
► 4) **Responder** al cliente con la confirmación/rechazo.

---

## Nivel 2 (Refinamiento de cada paso)

### 1) Recibir pedido (JSON)

► 1.1 Leo el contenido.
► 1.2 Chequeo que **no esté vacío**.
► 1.3 Convierto el texto a **objeto JSON**.
► 1.4 Creo un **código de seguimiento**.
► 1.5 Agrego la **fecha y hora** de llegada.

### 2) Chequear contenido

► 2.1 Por cada campo obligatorio, **revisar**.
✦ 2.2 **Si falta algo → Rechazar, informar y guardar**.
✦ 2.3 **Si está completo → Armar pedido**.

### 3) Encolar

► 3.1 Preparar un **mensaje simple** con `order_id`.
► 3.2 Ponerlo en la **cola de pedidos pendientes**.

### 4) Responder al cliente

► 4.1 Armar una **respuesta de confirmación/rechazo**.
► 4.2 **Enviar** la respuesta.

---

## Nivel 3

### 1) Recibir pedido (JSON)

► 1.1 Leer el contenido.
► 1.2 Chequear que **no esté vacío**.
✦ 1.2.1 Si está vacío → pasar a **Paso 2.2** (rechazar).
► 1.3 Convertir el texto a **objeto JSON**.
► 1.4 Crear un **código de seguimiento**.
► 1.5 Agregar **fecha y hora** de llegada.

### 2) Chequear contenido (validaciones detalladas)

► 2.1 Para cada campo obligatorio, **revisar**:
✦ 2.1.1 Cliente: debe traer **email**.
✦ 2.1.2 Productos: debe haber **al menos uno**.
✦ 2.1.3 Por cada producto: tener **código (sku)** y **cantidad > 0** (y **precio > 0** si viene en el JSON).
✦ 2.1.4 Dirección de envío: texto o identificador válido.
✦ 2.1.5 Pago: verificar que exista un **método de pago** (p. ej. tarjeta).

► 2.2 **Si falta algo → Rechazar e informar**:
✦ 2.2.1 Armar la **lista de errores** (qué falta o qué está mal).
✦ 2.2.2 Marcar el pedido como **RECHAZADO** (no encolar).
✦ 2.2.3 **Guardar** el registro.
✦ 2.2.4 **Saltar al paso 4** (responder).

► 2.3 **Si está completo → Armar pedido y guardar**:
✦ 2.3.1 Generar un **número de pedido (order_id)** único.
✦ 2.3.2 Armar un **registro básico** con cliente, productos, dirección y pago.
✦ 2.3.3 Poner **estado = “RECIBIDO”**.

### 3) Encolar

► 3.1 Preparar un **mensaje simple** con `order_id`.
► 3.2 Ponerlo en la **cola de pedidos pendientes**.

### 4) Responder al cliente

► 4.1 Armar un **mensaje de confirmación**:
✦ Si el pedido está marcado como **RECIBIDO** → **éxito**: “Pedido recibido”, incluir `order_id`.
✦ Si no (viene desde 2.2.2) → **error**: “Pedido rechazado”, incluir **lista de errores**.
► 4.2 **Enviar** la respuesta.

---

# Pseudocódigo – Recepción de Pedido

INICIO RecepcionPedido

1. RECIBIR pedido (JSON)
   • LEER contenido
   • SI contenido está vacío ENTONCES
   – ERRORES ← ["Pedido vacío"]
   – IR A Paso 4  (Responder con error)
   – FIN SI
   • CONVERTIR contenido a objeto_JSON
   (función que crea instancia/s con los atributos necesarios del pedido)
   • CREAR codigo_seguimiento
   • GUARDAR fecha_hora_actual

2. CHEQUEAR contenido (validar campos)
   • ERRORES ← []
   • SI cliente.email no existe → agregar "Falta email de cliente"
   • SI productos no existe O está vacío → agregar "Falta al menos un producto"
   – SINO, para cada producto:
   ▪ SI producto.sku no existe → "Falta código de producto"
   ▪ SI producto.cantidad ≤ 0 → "Cantidad inválida"
   ▪ SI producto.precio ≤ 0 → "Precio inválido"
   • SI direccion_envio no existe → "Falta dirección de envío"
   • SI pago.metodo no existe → "Falta método de pago"
   • SI ERRORES no está vacío ENTONCES
   – ESTADO ← "RECHAZADO"
   – GUARDAR registro
   – IR A Paso 4  (Responder con error)
   – SINO
   ▪ CREAR Pedido
   ▪ order_id ← GENERAR nuevo número único
   ▪ Asignar registros con datos del objeto_JSON
   ▪ ESTADO ← "RECIBIDO"
   – FIN SI

3. ENCOLAR pedido
   • mensaje ← { order_id, cliente, productos }
   • AGREGAR mensaje a ColaPedidosPendientes

4. RESPONDER al cliente
   • SI ESTADO = "RECIBIDO" → RESPUESTA: "Pedido recibido", incluir order_id
   • SINO → RESPUESTA: "Pedido rechazado", incluir lista de ERRORES
   • ENVIAR RESPUESTA al cliente

FIN RecepcionPedido
