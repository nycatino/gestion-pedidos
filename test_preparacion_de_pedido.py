from datetime import datetime
from m4_preparacion_de_pedido import ModuloPreparacion
from modelos.pedido import Producto
import builtins


def test_preparar_pedido_confirmado():
    """Simula confirmar preparación con 's'"""
    mod = ModuloPreparacion()

    # Guardamos el input original y lo reemplazamos temporalmente
    original_input = builtins.input
    builtins.input = lambda _: "s"

    productos = [
        Producto("SKU123", 2, 3000),
        Producto("SKU456", 1, 4000)
    ]

    resultado = mod.preparar_pedido(productos, order_id="ORD001")

    # Restauramos el input original
    builtins.input = original_input

    assert resultado["estado"] == "LISTO_PARA_ENVIO"
    assert "tiempo_estimado" in resultado
    assert "ORD001" in mod.preparaciones
    assert len(mod.preparaciones["ORD001"]["picking_list"]) == len(productos)
    assert isinstance(datetime.fromisoformat(mod.preparaciones["ORD001"]["fecha_preparacion"]), datetime)


def test_preparar_pedido_rechazado():
    """Simula rechazo con 'r'"""
    mod = ModuloPreparacion()

    original_input = builtins.input
    builtins.input = lambda _: "r"

    productos = [Producto("SKU789", 3, 5000)]

    resultado = mod.preparar_pedido(productos, order_id="ORD002")

    builtins.input = original_input

    assert resultado is False
    assert len(mod.errores) == 1
    assert "ORD002" not in mod.preparaciones


def test_preparar_pedido_repite_y_confirma():
    """Simula ingresar 'n' y luego 's' para confirmar"""
    respuestas = iter(["n", "s"])
    mod = ModuloPreparacion()

    original_input = builtins.input
    builtins.input = lambda _: next(respuestas)

    productos = [Producto("SKU999", 1, 2000)]

    resultado = mod.preparar_pedido(productos, order_id="ORD003")

    builtins.input = original_input

    assert resultado["estado"] == "LISTO_PARA_ENVIO"
    assert "ORD003" in mod.preparaciones


def test_simular_ubicacion_formato():
    """Verifica formato de la ubicación generada"""
    mod = ModuloPreparacion()
    ubicacion = mod.simular_ubicacion("SKU123")

    # Formato esperado: P<numero>-E<numero>-<letra>
    assert ubicacion.startswith("P")
    assert "-E" in ubicacion
    assert ubicacion[-1] in ["A", "B", "C"]


if __name__ == "__main__":
    test_preparar_pedido_confirmado()
    test_preparar_pedido_rechazado()
    test_preparar_pedido_repite_y_confirma()
    test_simular_ubicacion_formato()
    print("✅ Todos los tests de preparación pasaron correctamente.")
