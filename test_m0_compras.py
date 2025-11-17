import builtins
import pytest

from m0_compras import (
    armar_pedido, definir_envio, definir_pago,
    obtener_cliente, vaciar_seleccionados,
    seleccionar_productos, seleccionados
)
from modelos.pedido import Producto


# ------------------------------------------------------
# Helpers
# ------------------------------------------------------
def simular_input(respuestas):
    """Devuelve una función que reemplaza input() por valores predefinidos."""
    respuestas_iter = iter(respuestas)
    return lambda _: next(respuestas_iter)


# ------------------------------------------------------
# Fake para el depósito
# ------------------------------------------------------
class DepositoFake:
    def cargar_stock(self):
        return [
            {"sku": "ART_1", "nombre": "Articulo1", "precio": 1000, "stock": 5}
        ]

    def _limpiar_reservas_expiradas(self):
        pass


# ======================================================
# ================ TESTS CON PYTEST ====================
# ======================================================

def test_obtener_cliente(monkeypatch):
    respuestas = [
        "", "Juan",                # nombre
        "correo_malo", "a@b.com",  # email
        "", "Calle 123"            # direccion
    ]

    monkeypatch.setattr(builtins, "input", simular_input(respuestas))

    datos = obtener_cliente()

    assert datos["cliente"] == "Juan"
    assert datos["email"] == "a@b.com"
    assert datos["direccion"] == "Calle 123"


def test_seleccionar_productos(monkeypatch):
    vaciar_seleccionados()

    respuestas = [
        "0",  # elegir producto
        "2",  # cantidad
        "n"   # terminar
    ]

    monkeypatch.setattr(builtins, "input", simular_input(respuestas))

    seleccionar_productos(DepositoFake())

    assert len(seleccionados) == 1
    p = seleccionados[0]
    assert p.sku == "ART_1"
    assert p.cantidad_solicitada == 2


def test_definir_pago(monkeypatch):
    vaciar_seleccionados()

    p = Producto("SKU1", "Prod", 1000)
    p.cantidad_solicitada = 3
    seleccionados.append(p)

    respuestas = ["1"]  # transferencia

    monkeypatch.setattr(builtins, "input", simular_input(respuestas))

    pago = definir_pago()

    assert pago["total"] == 3000
    assert pago["forma_de_pago"] == "transferencia"


def test_definir_envio(monkeypatch):
    respuestas = ["3"]  # pickup

    monkeypatch.setattr(builtins, "input", simular_input(respuestas))

    metodo = definir_envio()
    assert metodo == "pickup"


def test_armar_pedido(monkeypatch):
    vaciar_seleccionados()

    respuestas = [
        "Juan",           # nombre
        "a@b.com",        # email
        "Calle 123",      # direccion
        "0",              # elegir producto
        "2",              # cantidad
        "n",              # terminar productos
        "1",              # forma de pago -> transferencia
        "2",              # envío express
    ]

    monkeypatch.setattr(builtins, "input", simular_input(respuestas))

    pedido = armar_pedido(DepositoFake())

    assert pedido["cliente"] == "Juan"
    assert pedido["email"] == "a@b.com"
    assert pedido["productos"][0]["cantidad_solicitada"] == 2
    assert pedido["datos_del_pago"]["metodo"] == "transferencia"
    assert pedido["metodo_envio"] == "express"
