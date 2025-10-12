## Nivel 1 (Algoritmo general)

1. **Recibir pedido para verificar stock** (order\_id + lista de productos).
2. **Revisar stock de cada SKU**.
3. **Decidir**: reservar stock (si alcanza) o marcar faltantes/pendientes.
4. **Registrar resultado** y **responder** al siguiente paso.

---

## Nivel 2 (Refinamiento de cada paso)

1. **Recibir pedido para verificar stock**
   1.1 Tomo `order_id` y `productos` (cada item: `sku`, `cantidad`).
   1.2 Identifico **depósito/almacén** a consultar (por defecto o el indicado).
   1.3 Creo un **código de seguimiento** para esta verificación.

2. **Revisar stock de cada SKU**
   2.1 Para cada `sku` consulto **stock disponible** en el depósito.
   2.2 Calculo si **alcanza** para la `cantidad` solicitada.
   2.3 Si no alcanza, registro **cantidad faltante**.

3. **Decidir**
   3.1 Si **todos** los ítems alcanzan → **Reservar** stock temporalmente.
   3.2 Si **ninguno** alcanza → **Sin reserva** y **listar faltantes**.
   3.3 Definir **tiempo de expiración** de la reserva (ej.: 30 minutos).

4. **Registrar resultado y responder**
   4.1 Guardar detalle: reservados, parciales, faltantes, expiración.
   4.2 Actualizar **estado de disponibilidad** del pedido:
   \- `AVAILABLE` (todo reservado)
   \- `OUT_OF_STOCK` (sin reserva)
   4.3 Enviar **respuesta** al cliente si corresponde.

---

## Nivel 3

1. **Recibir pedido para verificar stock**
   1.1 Entrada esperada: `{ order_id, deposito?, items: [{sku, cantidad}] }`.
   1.2 Si no viene `deposito` → usar **depósito por defecto**.
   1.3 Generar `stock_check_id` (código de seguimiento).

2. **Revisar stock de cada SKU**
   2.1 Consultar `stock_disponible(sku, deposito)`.
   2.2 Comparar `stock_disponible` vs `cantidad`.
   \- 2.2.1 Si `disponible >= cantidad` → marcar **OK** para ese ítem.
   \- 2.2.2 Si `disponible == 0` → marcar **SIN STOCK**.

3. **Decidir y reservar**
   3.1 Si **todos OK** → crear **reserva** por la cantidad completa de cada ítem.
   3.2 Establecer `reserva_expira_en` (fecha/hora límite).
   3.3 Si no se logra reservar **nada** → estado `OUT_OF_STOCK`.

4. **Registrar y responder**
   4.1 Guardar `stock_check_result` con: `order_id`, `deposito`, `items_reservados`, `items_faltantes`, `expiracion`.
   4.2 Determinar **estado**:
   \- Todos reservados → `AVAILABLE`
   \- Nada reservado → `OUT_OF_STOCK`
   4.3 Enviar resultado al siguiente paso (p. ej., **Verificación de pago** o **comunicar faltantes**).

---

# Pseudocódigo – Verificación de disponibilidad

```
INICIO VerificacionDisponibilidad

ENTRADA: order_id, deposito?, items[{sku, cantidad}]

1) PREPARAR
   deposito ← deposito si viene, sino DEPOSITO_POR_DEFECTO
   stock_check_id ← GENERAR_ID()
   resultado ← { reservados: [], faltantes: [] }

2) REVISAR STOCK POR ITEM
   PARA cada item EN items HACER
       disponible ← CONSULTAR_STOCK(item.sku, deposito)

       SI disponible >= item.cantidad ENTONCES
           AGREGAR {sku: item.sku, cantidad: item.cantidad} a resultado.reservados
       SINO
           AGREGAR {sku: item.sku, faltan: item.cantidad} a resultado.faltantes
       FIN SI
   FIN PARA

3) DECIDIR Y RESERVAR
   SI resultado.reservados está vacío ENTONCES
       estado_disponibilidad ← "OUT_OF_STOCK"
       reserva_id ← NULO
       expiracion ← NULO
   SINO
       reserva_id ← CREAR_RESERVA(order_id, deposito, resultado.reservados)
       expiracion ← AHORA + 30 minutos
       SI resultado.faltantes está vacío ENTONCES
           estado_disponibilidad ← "AVAILABLE"
       FIN SI
   FIN SI

4) REGISTRAR RESULTADO
   GUARDAR {
       stock_check_id, order_id, deposito,
       reservados: resultado.reservados,
       faltantes: resultado.faltantes,
       reserva_id, expiracion, estado: estado_disponibilidad
   }

5) RESPONDER / SALIDA
   SI estado_disponibilidad = "AVAILABLE" ENTONCES
       RESPUESTA ← {
           order_id, estado: "AVAILABLE",
           reserva_id, expira: expiracion,
           detalle_reserva: resultado.reservados
       }
   SINO
       RESPUESTA ← {
           order_id, estado: "OUT_OF_STOCK",
           faltantes: resultado.faltantes
       }
   FIN SI

   ENVIAR RESPUESTA al siguiente proceso

FIN VerificacionDisponibilidad
``