
# Relevamiento y Análisis – TP Gestión de Pedidos Online

## 1. Alcance del proyecto
El sistema abarca el **ciclo completo de un pedido online**, desde que el cliente lo carga en la tienda hasta que recibe la confirmación de envío.  
Se desarrollará en **módulos independientes**, conectados en secuencia, permitiendo simular cada parte.  

**Suposiciones para simplificar**:
- Medio de pago: **solo tarjeta**.  
- Envío: únicamente **a domicilio particular**.  
- No hay inventario digitalizado → se simulará stock básico.  
- Base de datos simulada en memoria (sin persistencia real).  

---

## 2. Módulos y objetivos

### Módulo 1 – Recepción del pedido
- **Objetivo**: recibir un pedido en formato JSON, validar que tenga los campos mínimos (cliente, productos, dirección, pago con tarjeta) y colocarlo en la cola para continuar.  
- **Alcance**: no valida stock ni pago; solo asegura que la entrada sea válida.  

### Módulo 2 – Verificación de disponibilidad
- **Objetivo**: chequear el stock de cada producto (simulado).  
- **Alcance**:  
  - Si hay stock → reservarlo temporalmente.  
  - Si no hay stock → devolver faltante y marcar pedido como incompleto.  

### Módulo 3 – Procesamiento de pago
- **Objetivo**: simular la autorización del pago con tarjeta.  
- **Alcance**:  
  - Validar que el medio de pago sea “tarjeta”.  
  - Generar resultado de pago: “aprobado” o “rechazado”.  
  - Actualizar el estado del pedido en consecuencia.  

### Módulo 4 – Preparación del pedido
- **Objetivo**: organizar el picking list y calcular un tiempo estimado de preparación.  
- **Alcance**:  
  - Generar lista de productos con sus ubicaciones simuladas.  
  - Calcular tiempo estimado (por ítem + empaquetado).  
  - Marcar pedido como **“listo para envío”**.  

### Módulo 5 – Envío y seguimiento
- **Objetivo**: simular la generación de guía de envío y asignar un número de seguimiento.  
- **Alcance**:  
  - Cambiar estado del pedido a **“en tránsito”**.  
  - Generar tracking ID y asociar transportista simulado.  
  - Notificar al cliente con el número de seguimiento.  

---

## 3. Diseño general del sistema
- **Flujo lineal**: cada módulo procesa y actualiza el pedido → luego lo entrega al siguiente.  
- **Base de datos simulada**: objetos en memoria, sin persistencia real.  
- **Cola simulada**: lista en memoria que encadena pedidos entre módulos.  
- **Mensajes simples**: cada módulo devuelve un JSON con el estado del pedido y la información agregada.  
- **Estados principales del pedido**:  
  - RECIBIDO  
  - STOCK_RESERVADO  
  - PAGO_APROBADO / PAGO_RECHAZADO  
  - LISTO_PARA_ENVIO  
  - EN_TRANSITO  
  - FINALIZADO  
