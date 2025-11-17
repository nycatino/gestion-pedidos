from datetime import datetime
import pytest

from m4_preparacion_de_pedido import ModuloPreparacion
from modelos.pedido import Pedido, Producto


# ============================================================
# TEST 1 - Confirmación directa (usuario ingresa "s")
# ============================================================

def test_preparar_pedido_confirmado(monkeypatch):
    """Simula confirmar preparación con 's'."""
    mod = ModuloPreparacion()

    # El usuario ingresa "s"
    monkeypatch.setattr("builtins.input", lambda _: "s")

    productos = [
        Producto("SKU123", 2, 3000),
        Producto("SKU456", 1, 4000)
    ]

    pedido = Pedido(
        id="ORD001",
        cliente="Juan Pérez",
        estado="PAGO_APROBADO",
        productos=productos,
        email="jperez@hotmail.com",
        metodo_envio="estandar"
    )

    resultado = mod.preparar_pedido(pedido)

    assert resultado["estado"] == "LISTO_PARA_ENVIO"
    assert "tiempo_estimado" in resultado
    assert "ORD001" in mod.preparaciones
    assert len(mod.preparaciones["ORD001"]["picking_list"]) == len(productos)

    fecha = datetime.fromisoformat(mod.preparaciones["ORD001"]["fecha_preparacion"])
    assert isinstance(fecha, datetime)


# ============================================================
# TEST 2 - Rechazo directo (usuario ingresa "r")
# ============================================================

def test_preparar_pedido_rechazado(monkeypatch):
    """Simula rechazo con 'r'."""
    mod = ModuloPreparacion()

    monkeypatch.setattr("builtins.input", lambda _: "r")

    productos = [Producto("SKU789", 3, 5000)]

    pedido = Pedido(
        id="ORD002",
        cliente="Laura",
        estado="PAGO_APROBADO",
        productos=productos,
        email="laura@test.com",
        metodo_envio="estandar"
    )

    resultado = mod.preparar_pedido(pedido)

    assert resultado is False
    assert len(mod.errores) == 1
    assert "ORD002" not in mod.preparaciones


# ============================================================
# TEST 3 - Usuario primero dice "n" y luego "s"
# ============================================================

def test_preparar_pedido_repite_y_confirma(monkeypatch):
    """Simula: usuario ingresa 'n' → luego 's'."""
    mod = ModuloPreparacion()

    # Simular secuencia de respuestas
    respuestas = iter(["n", "s"])
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

    productos = [Producto("SKU999", 1, 2000)]

    pedido = Pedido(
        id="ORD003",
        cliente="Carlos",
        estado="PAGO_APROBADO",
        productos=productos,
        email="carlos@test.com",
        metodo_envio="estandar"
    )

    resultado = mod.preparar_pedido(pedido)

    assert resultado["estado"] == "LISTO_PARA_ENVIO"
    assert "ORD003" in mod.preparaciones


# ============================================================
# TEST 4 - Validar formato de ubicación simulada
# ============================================================

def test_simular_ubicacion_formato():
    mod = ModuloPreparacion()
    ubicacion = mod.simular_ubicacion("SKU123")

    assert ubicacion.startswith("P")
    assert "-E" in ubicacion
    assert ubicacion[-1] in ["A", "B", "C"]
