import pytest
from datetime import datetime
from modelos.pedido import Pedido
from m3_procesamiento_de_pago import ModuloPago


class ApiBancoMock:
    """Simula la API bancaria devolviendo un valor fijo."""
    def __init__(self, respuesta):
        self.respuesta = respuesta
    
    def verificacion(self, numero_operacion):
        return self.respuesta


# ------------------------------------------------------
# Helpers
# ------------------------------------------------------

def crear_pedido_correcto():
    return Pedido(
        id="PED100",
        cliente="Juan",
        email="juan@test.com",
        estado="PENDIENTE_PAGO",
        metodo_envio="estandar",
        productos=[],
        fecha_recepcion=datetime.now(),
        datos_del_pago={
            "numero_operacion": "OP123",
            "total_abonado": 1500
        },
        total_a_pagar=1500
    )


def crear_pedido_incorrecto():
    return Pedido(
        id="PED200",
        cliente="Laura",
        email="laura@test.com",
        estado="PENDIENTE_PAGO",
        metodo_envio="pickup",
        productos=[],
        fecha_recepcion=datetime.now(),
        datos_del_pago={
            "numero_operacion": "OP999",
            "total_abonado": 1000
        },
        total_a_pagar=1500
    )


# ------------------------------------------------------
# TESTS PYTEST
# ------------------------------------------------------

def test_pago_correcto_con_api_ok():
    pedido = crear_pedido_correcto()
    api = ApiBancoMock(respuesta=True)

    modulo = ModuloPago(pedido, api)

    assert modulo.verificar_pago() is True
    assert modulo.errores == []


def test_pago_falla_si_api_rechaza():
    pedido = crear_pedido_correcto()
    api = ApiBancoMock(respuesta=False)

    modulo = ModuloPago(pedido, api)

    assert modulo.verificar_pago() is False
    assert "No se pudo verificar el pago" in modulo.errores


def test_pago_falla_si_monto_incorrecto():
    pedido = crear_pedido_incorrecto()
    api = ApiBancoMock(respuesta=True)  # API dice OK, pero montos no coinciden

    modulo = ModuloPago(pedido, api)

    assert modulo.verificar_pago() is False
    assert "No se pudo verificar el pago" in modulo.errores


def test_pago_falla_si_api_rechaza_y_monto_mal():
    pedido = crear_pedido_incorrecto()
    api = ApiBancoMock(respuesta=False)

    modulo = ModuloPago(pedido, api)

    assert modulo.verificar_pago() is False
    assert len(modulo.errores) == 1
    assert "No se pudo verificar el pago" in modulo.errores


def test_datos_iniciales_se_cargan_correctamente():
    pedido = crear_pedido_correcto()
    api = ApiBancoMock(respuesta=True)

    modulo = ModuloPago(pedido, api)

    assert modulo.total_a_pagar == 1500
    assert modulo.total_abonado == 1500
    assert modulo.numero_operacion == "OP123"
