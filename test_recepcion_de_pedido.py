import json
from modelos.pedido import Pedido, Item
from recepcion_de_pedido import ModuloRecepcion  # ajustá el import al nombre real del archivo

def test_modulo_recepcion_con_store_externa():
    """Prueba que el módulo de recepción reciba, valide y guarde pedidos en una store externa."""

    # 1️⃣ Crear un "store" compartido que simula la base de pedidos del sistema
    pedidos_store = {}

    # 2️⃣ Crear el módulo, pasándole la referencia al store
    recepcion = ModuloRecepcion(pedidos_source=pedidos_store)

    # 3️⃣ Simular un pedido válido en formato JSON
    pedido_json = json.dumps({
        "cliente": "Juan Pérez",
        "email": "juan@example.com",
        "direccion_envio": "Av. Siempre Viva 123",
        "productos": [
            {"sku": "SKU123", "cantidad": 2},
            {"sku": "SKU456", "cantidad": 1}
        ]
    })

    # 4️⃣ Ejecutar el método principal
    resultado = recepcion.recibir_pedido(pedido_json)

    # 5️⃣ Mostrar resultado
    print("\n=== Resultado de recepción ===")
    for k, v in resultado.items():
        print(f"{k}: {v}")

    # 6️⃣ Aserciones básicas
    assert resultado["estado"] == "RECIBIDO"
    assert resultado["order_id"] in pedidos_store
    assert len(pedidos_store[resultado["order_id"]].items) == 2
    assert pedidos_store[resultado["order_id"]].estado == "RECIBIDO"

def test_modulo_recepcion_json_invalido():
    """Prueba que el módulo rechace JSON inválido."""
    recepcion = ModuloRecepcion()
    resultado = recepcion.recibir_pedido("{cliente: Juan}")  # JSON mal formado

    print("\n=== Resultado de JSON inválido ===")
    print(resultado)
    assert resultado["estado"] == "RECHAZADO"

def test_modulo_recepcion_campos_faltantes():
    """Prueba que el módulo rechace un pedido con campos faltantes."""
    recepcion = ModuloRecepcion()
    pedido_json = json.dumps({
        "cliente": "Ana Gómez",
        # Falta 'email' y 'productos'
    })
    resultado = recepcion.recibir_pedido(pedido_json)

    print("\n=== Resultado de campos faltantes ===")
    print(resultado)
    assert resultado["estado"] == "RECHAZADO"
    assert "Falta email del cliente" in resultado["errores"]

if __name__ == "__main__":
    test_modulo_recepcion_con_store_externa()
    test_modulo_recepcion_json_invalido()
    test_modulo_recepcion_campos_faltantes()
