import builtins
from m0_compras import (
    armar_pedido, definir_envio, definir_pago,
    obtener_cliente, vaciar_seleccionados,
    seleccionar_productos, seleccionados
)
from modelos.pedido import Producto



# -------------------------
# Helpers para simular input
# -------------------------
def simular_input(respuestas):
    """Devuelve una función que reemplaza a input"""
    respuestas_iter = iter(respuestas)
    return lambda _: next(respuestas_iter)

# -------------------------
# TESTS SIN MONKEYPATCH
# -------------------------

def test_obtener_cliente_manual():
    respuestas = [
        "", "Juan",                # nombre
        "correo_malo", "a@b.com",  # email
        "", "Calle 123"            # direccion
    ]

    original_input = builtins.input
    builtins.input = simular_input(respuestas)

    try:
        datos = obtener_cliente()
        assert datos["cliente"] == "Juan"
        assert datos["email"] == "a@b.com"
        assert datos["direccion"] == "Calle 123"
        print("test_obtener_cliente_manual: OK")
    finally:
        builtins.input = original_input



class DepositoFake:
    def cargar_stock(self):
        return [
            {"sku": "ART_1", "nombre": "Articulo1", "precio": 1000, "stock": 5}
        ]
    def _limpiar_reservas_expiradas(self):
        pass



def test_seleccionar_productos_manual():
    vaciar_seleccionados()

    respuestas = [
        "0",  # elegir producto
        "2",  # cantidad
        "n"   # terminar
    ]

    original_input = builtins.input
    builtins.input = simular_input(respuestas)

    try:
        seleccionar_productos(DepositoFake())

        assert len(seleccionados) == 1
        p = seleccionados[0]
        assert p.sku == "ART_1"
        assert p.cantidad_solicitada == 2
        print("test_seleccionar_productos_manual: OK")
    finally:
        builtins.input = original_input



def test_definir_pago_manual():
    vaciar_seleccionados()

    p = Producto("SKU1", "Prod", 1000)
    p.cantidad_solicitada = 3
    seleccionados.append(p)

    respuestas = ["1"]  # transferencia

    original_input = builtins.input
    builtins.input = simular_input(respuestas)

    try:
        pago = definir_pago()

        assert pago["total"] == 3000
        assert pago["forma_de_pago"] == "transferencia"
        print("test_definir_pago_manual: OK")
    finally:
        builtins.input = original_input



def test_definir_envio_manual():
    respuestas = ["3"]  # pickup

    original_input = builtins.input
    builtins.input = simular_input(respuestas)

    try:
        metodo = definir_envio()
        assert metodo == "pickup"
        print("test_definir_envio_manual: OK")
    finally:
        builtins.input = original_input



def test_armar_pedido_manual():
    vaciar_seleccionados()

    respuestas = [
        "Juan",           # nombre
        "a@b.com",        # email
        "Calle 123",      # direccion
        "0",              # elegir producto
        "2",              # cantidad
        "n",              # terminar
        "1",              # forma de pago
        "2",              # envío express
    ]

    original_input = builtins.input
    builtins.input = simular_input(respuestas)

    try:
        pedido = armar_pedido(DepositoFake())

        assert pedido["cliente"] == "Juan"
        assert pedido["email"] == "a@b.com"
        assert pedido["productos"][0]["cantidad_solicitada"] == 2
        assert pedido["datos_del_pago"]["metodo"] == "transferencia"
        assert pedido["metodo_envio"] == "express"

        print("test_armar_pedido_manual: OK")
    finally:
        builtins.input = original_input


if __name__ == "__main__":
    test_obtener_cliente_manual()
    test_seleccionar_productos_manual()
    test_definir_pago_manual()
    test_definir_envio_manual()
    test_armar_pedido_manual()

    print("\nTodos los tests pasaron correctamente.")
