# test_integracion_preparacion_envio.py
from preparacion_de_pedido import ModuloPreparacion, Pedido as PedidoPrep, Item
from envio_y_seguimiento import ModuloEnvios
from typing import Dict
from modelos.pedido import Pedido


def test_integracion_preparacion_envio():
    # --- 1️⃣ Store compartida ---
    pedidos_store: Dict[str, PedidoPrep] = {}

    # Creamos un pedido del tipo correcto (PedidoPrep)
    pedido = PedidoPrep(
        id="ORDER-900",
        cliente="Lucía Ramírez",
        estado="PAGO_APROBADO",
        items=[Item("SKU-111", 2), Item("SKU-222", 1)]
    )

    pedidos_store[pedido.id] = pedido

    # --- 2️⃣ Módulos conectados al mismo store ---
    mod_preparacion = ModuloPreparacion(pedidos_source=pedidos_store)
    mod_envios = ModuloEnvios(pedidos_source=pedidos_store)

    print("\n=== INICIO DE PRUEBA DE INTEGRACIÓN ===")

    # --- 3️⃣ Preparación ---
    resultado_preparacion = mod_preparacion.preparar_pedido("ORDER-900")
    print("\n--- Resultado de preparación ---")
    for k, v in resultado_preparacion.items():
        print(f"{k}: {v}")

    if "error" in resultado_preparacion:
        print("❌ Error durante la preparación, se detiene la prueba.")
        return

    # --- 4️⃣ Envío ---
    resultado_envio = mod_envios.procesar_envio("ORDER-900", metodo_envio="express")
    print("\n--- Resultado del envío ---")
    for k, v in resultado_envio.items():
        print(f"{k}: {v}")

    print("\n=== ESTADO FINAL DEL PEDIDO ===")
    print(pedidos_store["ORDER-900"])

if __name__ == "__main__":
    test_integracion_preparacion_envio()
