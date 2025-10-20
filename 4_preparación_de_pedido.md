# Módulo 4 – Preparación del pedido

- **Objetivo**: organizar el *picking list*, confirmar preparación y calcular un tiempo estimado de preparación.  
- **Alcance**:  
  - Generar lista de productos con sus ubicaciones simuladas.  
  - Confirmar que el pedido fue preparado.  
  - Calcular tiempo estimado (por ítem + empaquetado).  
  - Marcar pedido como **“listo para envío”**.  

---

## 🔹 Algoritmo general

1. Verificar precondiciones del pedido.  
2. Generar *picking list* con ubicaciones simuladas.  
3. Confirmar preparación del pedido.  
4. Calcular tiempo estimado de preparación.  
5. Actualizar el pedido (estado y tiempo estimado).  
6. Enviar respuesta al módulo **Envío y seguimiento**.

---

## 🔹 Nivel 1 de refinamiento

1.1 Hallar pedido en la base de datos.  
1.2 Verificar que el estado sea **PAGO_APROBADO**.

2.1 Crear lista vacía `picking_list`.  
2.2 Por cada ítem del pedido, obtener ubicación simulada.  
2.3 Agregar ítem con su ubicación a la lista.

3.1 Confirmar que el pedido fue preparado correctamente (manual o automática).  

4.1 Calcular tiempo estimado = (tiempo por ítem × cantidad total) + tiempo de empaquetado.

5.1 Actualizar pedido con:  
   - Estado = **LISTO_PARA_ENVÍO**  
   - Tiempo estimado calculado  
5.2 Guardar pedido en la base de datos.

6.1 Enviar respuesta al módulo **Envío y seguimiento** con `order_id`.

---

## 🔹 Nivel 2 de refinamiento

1.1.1 `pedido ← db_pedidos.obtener_pedido(order_id)`  
1.2.1 Si `pedido.estado != 'PAGO_APROBADO'` entonces  
  1.2.2 Retornar **ERROR: precondiciones no cumplidas**

2.1.1 `picking_list ← []`  
2.1.2 Para cada `item` en `pedido.items`:  
  2.1.3 `ubicacion ← simular_ubicacion(item.sku)`  
  2.1.4 `picking_list.agregar({sku: item.sku, cantidad: item.cantidad, ubicacion: ubicacion})`

3.1.1 `confirmado ← confirmar_preparacion(picking_list)`  
3.1.2 Si `confirmado == False` entonces  
  3.1.3 Retornar **ERROR: preparación no confirmada**

4.1.1 `tiempo_por_item ← 2 minutos`  
4.1.2 `tiempo_empaquetado ← 5 minutos`  
4.1.3 `tiempo_total ← (len(pedido.items) * tiempo_por_item) + tiempo_empaquetado`

5.1.1 `pedido.estado ← 'LISTO_PARA_ENVIO'`  
5.1.2 `pedido.tiempo_estimado_preparacion ← tiempo_total`  
5.2.1 `db_pedidos.actualizar_pedido(pedido)`

6.1.1 `respuesta ← {order_id: pedido.id, estado: pedido.estado, tiempo_estimado: tiempo_total}`  
6.1.2 Enviar `respuesta` al módulo **Envío y seguimiento**

---

## 🔹 Pseudocódigo

```python
FUNCTION preparar_pedido(order_id):

    pedido = db_pedidos.obtener_pedido(order_id)
    IF pedido.estado != 'PAGO_APROBADO':
        RETURN ERROR("Precondiciones no cumplidas")

    picking_list = []
    FOR item IN pedido.items:
        ubicacion = simular_ubicacion(item.sku)
        picking_list.append({
            'sku': item.sku,
            'cantidad': item.cantidad,
            'ubicacion': ubicacion
        })

    # --- Confirmación de preparación ---
    confirmado = confirmar_preparacion(picking_list)
    IF NOT confirmado:
        RETURN ERROR("La preparación del pedido no fue confirmada")

    tiempo_por_item = 2  # minutos
    tiempo_empaquetado = 5
    tiempo_total = (len(pedido.items) * tiempo_por_item) + tiempo_empaquetado

    pedido.estado = 'LISTO_PARA_ENVIO'
    pedido.tiempo_estimado_preparacion = tiempo_total
    db_pedidos.actualizar_pedido(pedido)

    respuesta = {
        'order_id': pedido.id,
        'estado': pedido.estado,
        'tiempo_estimado': tiempo_total
    }

    enviar_a_envio_y_seguimiento(respuesta)
