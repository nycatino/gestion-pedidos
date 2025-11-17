import json
from datetime import datetime, timedelta
import os
import pytest

from m2_verificacion_disponibilidad import (
    Verificacion_disponibilidad_producto,
    Deposito
)

# ---------------------------------------------------------
# Helpers para generar archivos temporales
# ---------------------------------------------------------
def crear_archivos_stock_reservas(tmp_path, stock, reservas):
    stock_file = tmp_path / "stock.json"
    reservas_file = tmp_path / "reservas.json"

    with open(stock_file, "w") as f:
        json.dump(stock, f)

    with open(reservas_file, "w") as f:
        json.dump(reservas, f)

    return stock_file, reservas_file


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
# ========== PRUEBAS MANUALES (sin pytest) ================
# =========================================================

def test_manual_consultar_stock_todo_disponible():
    print("\n--- test_manual_consultar_stock_todo_disponible ---")

    class DepositoFake:
        def disponibilidad(self, sku):
            return 10  # siempre hay stock

        def reservar(self, fecha_hora_reserva, productos):
            return productos  # reserva válida

    pedido = PedidoFake([
        ProductoFake("A1", "Prod A", 2),
        ProductoFake("B1", "Prod B", 5),
    ])

    deposito = DepositoFake()
    verif = Verificacion_disponibilidad_producto(pedido, deposito)

    assert verif.consultar_stock() is True
    print("OK")


def test_manual_consultar_stock_sin_stock():
    print("\n--- test_manual_consultar_stock_sin_stock ---")

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
    print("OK")


def test_manual_reservar_exitoso():
    print("\n--- test_manual_reservar_exitoso ---")

    class DepositoFake:
        def disponibilidad(self, sku):
            return 10

        def reservar(self, fecha_hora_reserva, productos):
            return productos  # reserva correcta

    pedido = PedidoFake([
        ProductoFake("A1", "Prod A", 3),
    ])

    deposito = DepositoFake()
    verif = Verificacion_disponibilidad_producto(pedido, deposito)

    verif.consultar_stock()
    assert verif.reservar() is True
    print("OK")


def test_manual_reservar_fallido():
    print("\n--- test_manual_reservar_fallido ---")

    class DepositoFake:
        def disponibilidad(self, sku):
            return 10

        def reservar(self, fecha_hora_reserva, productos):
            return None  # no pudo reservar

    pedido = PedidoFake([
        ProductoFake("A1", "Prod A", 3),
    ])

    deposito = DepositoFake()
    verif = Verificacion_disponibilidad_producto(pedido, deposito)

    verif.consultar_stock()
    assert verif.reservar() is False
    print("OK")


# =========================================================
# ========== EJECUCIÓN MANUAL DE LOS TESTS ================
# =========================================================
if __name__ == "__main__":
    print("\n=========== EJECUTANDO TESTS MANUALES ===========")

    test_manual_consultar_stock_todo_disponible()
    test_manual_consultar_stock_sin_stock()
    test_manual_reservar_exitoso()
    test_manual_reservar_fallido()

    print("\nTODOS LOS TESTS MANUALES PASARON CORRECTAMENTE.\n")
