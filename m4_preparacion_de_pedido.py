from datetime import datetime
import random
from typing import Dict, Optional, Callable, Any, Union
from modelos.pedido import Pedido, Producto  # ✅ usamos el modelo compartido

class ModuloPreparacion:
    def __init__(self):
        
        self.preparaciones: Dict[str, Any] = {}
        self.errores = []

    # --- Función auxiliar ---
    def simular_ubicacion(self, sku: str) :
        """Devuelve una ubicación ficticia del depósito para el SKU"""
        pasillo = random.randint(1, 10)
        estante = random.randint(1, 5)
        nivel = random.choice(["A", "B", "C"])
        return f"P{pasillo}-E{estante}-{nivel}"

    def confirmar_preparacion(self, picking_list, tiempo_estimado_preparacion):
        print(f"Picking list: {picking_list}")
        print(f"Tiempo estimado de preparación: {tiempo_estimado_preparacion} minutos")

        while True:
            respuesta = input("¿Confirmar disponibilidad stock real? (s = sí / n = no / r = rechazar pedido): ").lower().strip()

            if respuesta == 's':
                print("Preparación confirmada")
                return True
            elif respuesta == 'n':
                print("Preparación no confirmada")
                # vuelve a preguntar automáticamente
                continue
            elif respuesta == 'r':
                print("Pedido rechazado")
                return "rechazado"
            else:
                print("Opción inválida. Por favor ingrese 's', 'n' o 'r'.")


    # --- Lógica principal ---
    def preparar_pedido(self, orden_pedido):

        productos = orden_pedido.productos
        # if not pedido:
        #     return {"error": "Pedido no encontrado", "order_id": order_id}

        # if pedido.estado != "PAGO_APROBADO":
        #     return {
        #         "error": "Precondición no cumplida",
        #         "order_id": order_id,
        #         "estado_actual": pedido.estado
        #     }

        # Generar picking list
        picking_list = []
        for producto in productos:
            ubicacion = self.simular_ubicacion(producto.sku)
            picking_list.append({
                "sku": producto.sku,
                "cantidad": producto.cantidad_solicitada,
                "ubicacion": ubicacion
            })

        # Calcular tiempos estimados
        tiempo_por_item = 2  # minutos
        tiempo_empaquetado = 5
        tiempo_estimado_preparacion = (len(productos) * tiempo_por_item) + tiempo_empaquetado

        # ---- ARREGLAR Confirmar preparación (pregunto en loop hasta que se confirme o se rechace el pedido)
        confirmado = self.confirmar_preparacion(picking_list, tiempo_estimado_preparacion)
        if confirmado == "rechazado":
            self.errores.append("No se pudo confirmar la preparacion")
            return False

        # ------- MAIN  Actualizar estado del pedido
        estado = "LISTO_PARA_ENVIO"

        # Guardar en base de preparaciones simulada
        self.preparaciones[orden_pedido.id] = {
            "picking_list": picking_list,
            "tiempo_estimado": tiempo_estimado_preparacion,
            "fecha_preparacion": datetime.now().isoformat()
        }

        # Retornar resultado
        return {
            "estado": estado,
            "tiempo_estimado": tiempo_estimado_preparacion,
        }

# --- Prueba local ---
def test_modulo_preparacion():
    
    pedido = Pedido(id="ORDER-001", cliente="Ana Gómez", estado="LISTO_PARA_ENVIO", productos =[Producto("SKU123", 2, 3000), Producto("SKU456", 1, 4000)])

    modulo = ModuloPreparacion()
    resultado = modulo.preparar_pedido(pedido)

    print("\n=== Resultado de preparación ===")
    for k, v in resultado.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    test_modulo_preparacion()
