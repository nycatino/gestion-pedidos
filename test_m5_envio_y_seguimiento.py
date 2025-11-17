from datetime import datetime
from m5_envio_y_seguimiento import ModuloEnvios, Envio
from modelos.pedido import Pedido, Producto


# ============================================================
# TEST 1 - Selección de carrier
# ============================================================

def test_seleccionar_carrier():
    mod = ModuloEnvios()

    assert mod.seleccionar_carrier("estandar") == "CarrierFast"
    assert mod.seleccionar_carrier("express") == "CarrierExpress"
    assert mod.seleccionar_carrier("premium") == "CarrierLocal"
    assert mod.seleccionar_carrier("inexistente") == "CarrierFast"  # default


# ============================================================
# TEST 2 - Generación de tracking: formato correcto
# ============================================================

def test_generar_tracking_formato():
    mod = ModuloEnvios()
    tracking = mod.generar_tracking()

    assert tracking.startswith("TRK-")
    assert len(tracking) == 12      # TRK-XXXXXXXX (8 chars random)


# ============================================================
# TEST 3 - Procesar envío: debe generar un Envio válido
# ============================================================

def test_procesar_envio_crea_registro():
    mod = ModuloEnvios()

    productos = [
        Producto("SKU1", "Yerba", 1000, cantidad_solicitada=2),
        Producto("SKU2", "Azúcar", 500, cantidad_solicitada=1)
    ]

    pedido = Pedido(
        id="PED001",
        cliente="Juan",
        email="juan@test.com",
        estado="LISTO_PARA_ENVIO",
        metodo_envio="express",
        productos=productos,
        fecha_recepcion=datetime.now(),
        datos_del_pago={"metodo": "tarjeta"}
    )

    envio = mod.procesar_envio(pedido)

    # Validaciones principales
    assert isinstance(envio, Envio)
    assert envio.order_id == "PED001"
    assert envio.carrier == "CarrierExpress"
    assert envio.estado == "CREADO"
    assert envio.tracking_id in mod.envios

    # Validar historial
    assert isinstance(envio.historial, list)
    assert len(envio.historial) == 1
    assert envio.historial[0]["estado"] == "CREADO"
    assert "fecha" in envio.historial[0]


# ============================================================
# TEST 4 - Verificar que el envío se guarda en el store interno
# ============================================================

def test_envio_guardado_en_store():
    mod = ModuloEnvios()

    pedido = Pedido(
        id="PED002",
        cliente="Laura",
        email="laura@test.com",
        estado="LISTO_PARA_ENVIO",
        metodo_envio="premium",
        productos=[],
        fecha_recepcion=datetime.now(),
        datos_del_pago={"metodo": "efectivo"}
    )

    envio = mod.procesar_envio(pedido)

    assert envio.tracking_id in mod.envios
    assert mod.envios[envio.tracking_id].order_id == "PED002"
    assert mod.envios[envio.tracking_id].carrier == "CarrierLocal"
