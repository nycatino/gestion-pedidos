from m1_recepcion_del_pedido import RecepcionPedido
from modelos.pedido import Producto, Pedido


# ------------------------------------------------------------
# TEST 1: validar_pedido falla si faltan campos
# ------------------------------------------------------------

def test_validar_pedido_faltan_campos():
    data_incompleta = {
        "cliente": "",
        "email": "",
        "direccion_envio": "",
        "productos": None,
        "datos_del_pago": None,
        "metodo_envio": ""
    }

    r = RecepcionPedido(data_incompleta)
    valido = r.validar_pedido()

    assert not valido
    assert len(r.errores) == 6


# ------------------------------------------------------------
# TEST 2: validar_pedido correcto
# ------------------------------------------------------------

def test_validar_pedido_correcto():
    data_ok = {
        "cliente": "Juan",
        "email": "juan@mail.com",
        "direccion_envio": "Calle 123",
        "productos": [
            {"sku": "A1", "nombre": "Prod", "cantidad_solicitada": 2, "precio": 100}
        ],
        "datos_del_pago": {
            "metodo": "transferencia",
            "total_abonado": 200,
            "numero_operacion": 999
        },
        "metodo_envio": "express"
    }

    r = RecepcionPedido(data_ok)
    valido = r.validar_pedido()

    assert valido
    assert len(r.errores) == 0


# ------------------------------------------------------------
# TEST 3: crear_pedido con datos válidos
# ------------------------------------------------------------

def test_crear_pedido_ok():
    data_ok = {
        "cliente": "Juan",
        "email": "juan@mail.com",
        "direccion_envio": "Calle 123",
        "productos": [
            {"sku": "A1", "nombre": "Yerba", "cantidad_solicitada": 2, "precio": 800},
            {"sku": "A2", "nombre": "Fideos", "cantidad_solicitada": 1, "precio": 500}
        ],
        "datos_del_pago": {
            "metodo": "transferencia",
            "total_abonado": 2100,
            "numero_operacion": 888
        },
        "metodo_envio": "express"
    }

    r = RecepcionPedido(data_ok)
    pedido = r.crear_pedido()

    assert isinstance(pedido, Pedido)
    assert pedido.cliente == "Juan"
    assert pedido.metodo_envio == "express"
    assert len(pedido.productos) == 2
    assert pedido.total_a_pagar == (2 * 800 + 1 * 500)


# ------------------------------------------------------------
# TEST 4: crear_pedido falla si un producto está mal
# ------------------------------------------------------------

def test_crear_pedido_producto_invalido():
    data_mal = {
        "cliente": "Juan",
        "email": "juan@mail.com",
        "direccion_envio": "Calle 123",
        "productos": [
            {"sku": "A1", "nombre": "Yerba", "cantidad_solicitada": "dos", "precio": 800}
        ],
        "datos_del_pago": {
            "metodo": "transferencia",
            "total_abonado": 800,
            "numero_operacion": 555
        },
        "metodo_envio": "pickup"
    }

    r = RecepcionPedido(data_mal)
    pedido = r.crear_pedido()

    assert pedido is False
    assert len(r.errores) == 1


# ------------------------------------------------------------
# TEST 5: errores se acumulan correctamente
# ------------------------------------------------------------

def test_errores_acumulados():
    data = {
        "cliente": "",
        "email": "",
        "direccion_envio": "",
        "productos": [],
        "datos_del_pago": {},
        "metodo_envio": ""
    }

    r = RecepcionPedido(data)
    r.validar_pedido()

    assert len(r.errores) == 6
