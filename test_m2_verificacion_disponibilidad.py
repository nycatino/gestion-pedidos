import json
from datetime import datetime, timedelta
import os
import pytest

from m2_verificacion_disponibilidad import (
    Verificacion_disponibilidad_producto,
    Deposito
)

# ---------------------------------------------------------
# Mock simple de un Pedido y un Producto
# ---------------------------------------------------------
class ProductoFake:
    def __init__(self, sku, nombre, cantidad_solicitada):
        self.sku = sku
        self.nombre = nombre
        self.cantidad_solicitada = cantidad_solicitada

class PedidoFake:
    def __init__(self, productos):
        self.productos = productos


# =========================================================
# ========== TESTS USANDO PYTEST ==========================
# =========================================================

def test_consultar_stock_todo_disponible():
    class DepositoFake:
        def disponibilidad(self, sku):
            return 10  # siempre suficiente
        def reservar(self, fecha_hora_reserva, productos):
            return productos

    pedido = PedidoFake([
        ProductoFake("A1", "Prod A", 2),
        ProductoFake("B1", "Prod B", 5),
    ])

    deposito = DepositoFake()
    verif = Verificacion_disponibilidad_producto(pedido, deposito)

    assert verif.consultar_stock() is True
    assert len(verif.consulta_disponibilidad_productos) == 2


def test_consultar_stock_sin_stock():
    class DepositoFake:
        def disponibilidad(self, sku):
            return 1  # insuficiente
        def reservar(self, fecha_hora_reserva, productos):
            return None

    pedido = PedidoFake([
        ProductoFake("A1", "Prod A", 5),
    ])

    deposito = DepositoFake()
    verif = Verificacion_disponibilidad_producto(pedido, deposito)

    assert verif.consultar_stock() is False
    assert verif.consulta_disponibilidad_productos[0]["disponibilidad"] == "SIN_STOCK"


def test_reservar_exitoso():
    class DepositoFake:
        def disponibilidad(self, sku):
            return 10
        def reservar(self, fecha_hora_reserva, productos):
            return productos  # reserva ok

    pedido = PedidoFake([ProductoFake("A1", "Prod A", 3)])
    deposito = DepositoFake()
    verif = Verificacion_disponibilidad_producto(pedido, deposito)

    verif.consultar_stock()  # genera productos
    assert verif.reservar() is True


def test_reservar_fallido():
    class DepositoFake:
        def disponibilidad(self, sku):
            return 10
        def reservar(self, fecha_hora_reserva, productos):
            return None  # no se pudo reservar

    pedido = PedidoFake([ProductoFake("A1", "Prod A", 3)])
    deposito = DepositoFake()
    verif = Verificacion_disponibilidad_producto(pedido, deposito)

    verif.consultar_stock()
    assert verif.reservar() is False
