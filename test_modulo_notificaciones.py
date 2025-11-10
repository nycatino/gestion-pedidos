from datetime import datetime
from modulo_notificaciones import modulo_Notificaciones

def test_pedido_rechazado():
    # Crear instancia y agregar una lista interna para guardar las notificaciones
    mod = modulo_Notificaciones()
    mod.notificaciones = []

    # Datos de prueba
    cliente = "Juan Pérez"
    errores = ["Falta método de pago", "Monto inválido"]

    mensaje = mod.pedido_rechazado(errores, cliente)

    # Verificamos el mensaje
    assert "Juan Pérez" in mensaje
    assert "rechazado" in mensaje.lower()
    assert "Monto inválido" in mensaje

    # Verificamos que se haya guardado en la lista de notificaciones
    assert len(mod.notificaciones) == 1
    noti = mod.notificaciones[0]
    assert noti["cliente"] == cliente
    assert "Falta método de pago" in noti["mensaje"]
    assert isinstance(noti["fecha"], datetime)


def test_enviar_seguimiento():
    mod = modulo_Notificaciones()
    mod.notificaciones = []

    cliente = "Ana López"
    tracking = "TRK12345"
    carrier = "CarrierFast"

    mensaje = mod.enviar_seguimiento(cliente, tracking, carrier)

    # Verificamos el contenido del mensaje
    assert cliente in mensaje
    assert tracking in mensaje
    assert carrier in mensaje

    # Verificamos que se haya guardado correctamente
    assert len(mod.notificaciones) == 1
    noti = mod.notificaciones[0]
    assert noti["cliente"] == cliente
    assert tracking in noti["mensaje"]
    assert isinstance(noti["fecha"], datetime)


if __name__ == "__main__":
    test_pedido_rechazado()
    test_enviar_seguimiento()
    print("Todos los tests pasaron correctamente.")
