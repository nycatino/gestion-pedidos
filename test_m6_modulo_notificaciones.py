import unittest
from unittest.mock import patch
from m6_modulo_notificaciones import Modulo_Notificaciones  # ajusta el nombre del archivo si es necesario

class TestModuloNotificaciones(unittest.TestCase):

    def setUp(self):
        self.modulo = Modulo_Notificaciones()

    @patch("builtins.print")
    def test_pedido_rechazado(self, mock_print):
        errores = ["Falta stock", "Dirección incorrecta"]
        self.modulo.pedido_rechazado(errores)
        # Verificar que print fue llamado con el mensaje correcto
        expected_message = "\nHola! Tu pedido ha sido rechazado por los siguientes motivos: Falta stock, Dirección incorrecta\n"
        mock_print.assert_called_with(expected_message)

    @patch("builtins.print")
    def test_enviar_seguimiento(self, mock_print):
        tracking = "12345XYZ"
        carrier = "DHL"
        self.modulo.enviar_seguimiento(tracking, carrier)
        expected_message = "Hola! Tu pedido está en camino!\nTracking: 12345XYZ\nCarrier: DHL"
        mock_print.assert_called_with(expected_message)

    @patch("builtins.print")
    def test_notificar(self, mock_print):
        mensaje = "Mensaje de prueba"
        self.modulo.notificar(mensaje)
        mock_print.assert_called_with(mensaje)

if __name__ == "__main__":
    unittest.main()
