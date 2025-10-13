**Módulo 3 – Procesamiento de pago**
(validar método de pago, simular autorización y marcar aprobado/rechazado)

---

## Nivel 1 (Algoritmo general)

1. **Recibir solicitud de pago** (order\_id + datos de pago).
2. **Validar método de pago**.
3. **Simular autorización**.
4. **Actualizar estado del pago** (aprobado o rechazado).
5. **Responder** con el resultado.

---

## Nivel 2 (Refinamiento de cada paso)

1. **Recibir solicitud de pago**
   1.1 Tomo `order_id` y el bloque `pago` (método + datos mínimos).
   1.2 Creo un **código de seguimiento** de pago.
   1.3 Anoto fecha y hora de inicio.

2. **Validar método de pago**
   2.1 Verificar que exista `pago.metodo` (tarjeta, transferencia, efectivo al retirar, etc.).
   2.2 Para **tarjeta**: chequear que vengan datos mínimos (número enmascarado/alias, vencimiento, nombre, monto).
   2.3 Para **transferencia**: chequear datos de referencia (CBU/alias, comprobante o intención).
   2.4 Si falta algo → **rechazar por datos insuficientes**.

3. **Simular autorización**
   3.1 Si método **tarjeta** → “llamar” a un **simulador** que devuelve aprobado/rechazado. (*)
   3.2 Si **transferencia** → “simular confirmación bancaria” (aprobado/rechazado).
   3.3 Guardar código de autorización simulado (si aplica).

4. **Actualizar estado del pago**
   4.1 Si **aprobado** → `pago_estado = APROBADO`.
   4.2 Si **rechazado** → `pago_estado = RECHAZADO` (con motivo).
   4.3 Registrar fecha/hora de resultado.

5. **Responder**
   5.1 Armar respuesta con `order_id`, `pago_estado` y detalles (autorización/motivo).
   5.2 Enviar al siguiente proceso (por ejemplo, **preparación/envío** si está aprobado).

---

## Nivel 3

1. **Recibir solicitud de pago**
   1.1 Entrada esperada: `{ order_id, pago: { metodo, monto, datos? } }`.
   1.2 Generar `payment_id` (código de seguimiento del pago).
   1.3 Registrar `inicio_pago_at`.

2. **Validar método de pago**
   2.1 Si no hay `metodo` → error “Falta método de pago”.
   2.2 Si `metodo = tarjeta`:
   \- 2.2.1 Validar `monto > 0`.
   \- 2.2.2 Validar presencia de datos mínimos (número enmascarado/alias, vencimiento, nombre).
   2.3 Si `metodo = transferencia`:
   \- 2.3.1 Validar `monto > 0`.
   \- 2.3.2 Validar referencia (CBU/alias) y comprobante/identificador.
   2.4 Si el método no es reconocido → error “Método no soportado”.

3. **Simular autorización**
   3.1 Para **tarjeta** y **transferencia**:
   \- 3.1.1 Calcular si `monto ≤ fondos_limite` → aprobado; si no → rechazado.
   \- 3.1.2 Generar `auth_code` si aprobado; si no, `motivo_rechazo` (“Fondos insuficientes”, por ejemplo).

4. **Actualizar estado del pago**
   4.1 `APROBADO` → guardar `auth_code`.
   4.2 `RECHAZADO` → guardar `motivo_rechazo`.
   4.3 `fin_pago_at` con fecha/hora.

5. **Responder**
   5.1 Éxito (aprobado): `{ order_id, payment_id, estado: "APROBADO", auth_code, monto }`.
   5.2 Rechazo: `{ order_id, payment_id, estado: "RECHAZADO", motivo }`.

---

# Pseudocódigo – Procesamiento de pago

```
INICIO ProcesamientoPago

ENTRADA: order_id, pago{metodo, monto, datos?}

1) PREPARAR
   payment_id ← GENERAR_ID()
   inicio_pago_at ← AHORA
   ERRORES ← []

2) VALIDAR METODO Y DATOS
   SI pago.metodo no existe ENTONCES
       ERRORES.AGREGAR("Falta método de pago")
   FIN SI

   SI pago.monto <= 0 ENTONCES
       ERRORES.AGREGAR("Monto inválido")
   FIN SI

   SEGUN pago.metodo HACER
       CASO "tarjeta":
           SI falta numero_enmascarado O vencimiento O nombre_titular ENTONCES
               ERRORES.AGREGAR("Datos de tarjeta incompletos")
           FIN SI
       CASO "transferencia":
           SI falta referencia_bancaria ENTONCES
               ERRORES.AGREGAR("Falta referencia bancaria")
           FIN SI
       OTRO:
           ERRORES.AGREGAR("Método no soportado")
   FIN SEGUN

   SI ERRORES no está vacío ENTONCES
       estado_pago ← "RECHAZADO"
       motivo ← UNIR(ERRORES, "; ")
       IR A Paso 4 (RESPONDER)
   FIN SI

3) SIMULAR AUTORIZACION
   auth_code ← NULO
   motivo ← NULO

   SI pago.metodo = "tarjeta" or pago.metodo = "transferencia" ENTONCES
       SI pago.monto <= 200000 ENTONCES
           estado_pago ← "APROBADO"
           auth_code ← GENERAR_AUTH_CODE()
       SINO
           estado_pago ← "RECHAZADO"
           motivo ← "Fondos insuficientes (simulado)"
       FIN SI

   FIN SI

4) REGISTRAR Y RESPONDER
   fin_pago_at ← AHORA
   GUARDAR { order_id, payment_id, estado_pago, auth_code, motivo, inicio_pago_at, fin_pago_at, monto: pago.monto }

   SI estado_pago = "APROBADO" ENTONCES
       RESPUESTA ← { order_id, payment_id, estado: "PAGO_APROBADO", auth_code, monto: pago.monto }
       ENVIAR RESPUESTA A **Preparación de pedido**
   SINO
       RESPUESTA ← { order_id, payment_id, estado: "PAGO_RECHAZADO", motivo }
       RESPONDER A CLIENTE
   FIN SI

FIN ProcesamientoPago
```