## Nivel 1 (Algoritmo general)

1. **Recibir pedido para verificar stock** (order\_id + lista de productos).
2. **Revisar stock de cada SKU**.
3. **Decidir**: reservar stock (si alcanza) o marcar faltantes/pendientes.
4. **Responder al siguiente módulo** al siguiente paso.

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

4. **Responder al siguiente módulo**
   4.1 Actualizar **estado de disponibilidad** del pedido:
   \- `AVAILABLE` (todo reservado)
   \- `OUT_OF_STOCK` (sin reserva)
   4.3 Enviar **respuesta** al siguiente módulo.

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

4. **Responder al siguiente módulo**
   4.1 Determinar **estado**:
   \- Todos reservados → `AVAILABLE`
   \- Nada reservado → `OUT_OF_STOCK`
   4.2 Enviar resultado al siguiente paso 
      4.2.1 Si estado == "AVAILABLE" responder a **Verificación de pago** 
            Sino responder al cliente

---

# Pseudocódigo – Verificación de disponibilidad

```
INICIO VerificacionDisponibilidad

ENTRADA: order_id, deposito?, items[{sku, cantidad}]

1) PREPARAR
   deposito ← deposito si viene, sino DEPOSITO_POR_DEFECTO
   stock_check_id ← GENERAR_ID()

2) REVISAR STOCK POR ITEM
   PARA cada item EN items HACER
       disponible ← CONSULTAR_STOCK(item.sku, deposito)

       SI disponible < item.cantidad ENTONCES
          estado_disponibilidad ← "OUT_OF_STOCK"
       SINO 
         estado_disponibilidad = "AVAILABLE" 
       FIN SI

   FIN PARA

3) DECIDIR Y RESERVAR

   SI estado_disponibilidad == "AVAILABLE" ENTONCES
       expiracion ← AHORA + 30 minutos
       reserva_id ← CREAR_RESERVA(order_id, deposito, expiracion)
       pedido.estado ← STOCK RESERVADO
   SINO
       reserva_id ← NULO
       expiracion ← NULO
       pedido.estado ← RECHAZADO
   FIN SI

   

4) RESPONDER AL SIGUIENTE MÓDULO
   RESPUESTA ← {
      order_id, estado
   }
   SI estado_disponibilidad = "AVAILABLE" ENTONCES
      ENVIAR RESPUESTA A **Procesamiento de pago**
   SINO
       NOTIFICAR AL CLIENTE
   FIN SI

FIN VerificacionDisponibilidad
``