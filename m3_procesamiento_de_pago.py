from datetime import datetime
import random
import uuid
from typing import Dict, Optional, Callable, Union
from modelos.pedido import Pedido

class ModuloPago:
    def __init__(self, orden_pedido):
        self.orden_pedido = orden_pedido
        self.total_a_pagar = self.orden_pedido.total_a_pagar

        self.numero_operacion = self.orden_pedido.datos_del_pago["numero_operacion"]
        self.total_abonado = self.orden_pedido.datos_del_pago["total_abonado"]

        self.errores = []


    def verificar_pago(self):
        estado_del_pago = self.api_banco.verificacion(self.numero_operacion)

        if estado_del_pago and self.total_a_pagar == self.total_abonado:
            return True
        else:
            self.errores.append("No se pudo verificar el pago")
            return False

class Api_banco:
    def verificacion(self):
        return random.choice([True, False])