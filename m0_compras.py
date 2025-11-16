
import json
import random
from m2_verificacion_disponibilidad import Deposito

from modelos.pedido import Producto

seleccionados = []

def cargar_productos_desde_json(deposito):
    data = deposito.cargar_stock()
    # with open(archivo, "r", encoding="utf-8") as f:
    #     data = json.load(f)

    productos = []

    for item in data:   # porque ahora data es una LISTA, no un dict
        sku = item["sku"]
        nombre = item["nombre"]
        precio = item["precio"]
        stock = item["stock"]

        producto = Producto(sku, nombre, precio)
        producto.stock = stock   # atributo agregado dinámicamente

        productos.append(producto)

    return productos


def obtener_cliente():
    #  Datos del cliente
    while True:
        cliente = input(" Ingrese su nombre: ").strip()
        if cliente.strip():
            break
        else: 
             print(" ERROR: Nombre invalido\n")
    
    while True:
        email = input(" Ingrese su email: ").strip()

        if "@" in email and "." in email.split("@")[-1]:
            break
        else:
            print(" ERROR: Email invalido\n")

    while True:
        direccion = input(" Ingrese su dirección de envío: ").strip()
        if direccion.strip():
            break
        else:
            print(" ERROR: Direccion invalido\n")
    
    return {
        "cliente": cliente,
        "email": email,
        "direccion": direccion
    }


def seleccionar_productos(deposito):
    
    #Selección de productos
    productos_disponibles = cargar_productos_desde_json(deposito)
    while True:
        print("\n ----------- Productos disponibles -----------\n")
        for i, producto in enumerate(productos_disponibles):
            print(f"{i}. {producto}")

        print()
        while True:
            try:
                indice = int(input(" Ingrese el número del producto que desea agregar: "))
                if (0 <= indice < len(productos_disponibles) ):
                    break   # si llega hasta acá → es válido → rompemos el bucle
                else:
                    print(" ERROR: Indice invalido\n")
            except ValueError:
                print(" ERROR: Valor invalido\n")
        
        while True:
            try:
                cantidad = int(input(" Ingrese cantidad del producto que desea comprar: "))
                if (0 < cantidad <= productos_disponibles[indice].stock): # MODIFIQUE PARA SEA SOLO MAYOR A CERO, NO TIENE SENTIDO QUE SEA IGUAL A CERO. LIMITÉ A CANTIDAD EXISTENTE
                    break   # si llega hasta acá → es válido → rompemos el bucle
                elif (cantidad == 0): print(" ERROR: Indique una cantidad mayor a cero\n")
                else: print(" ERROR: No hay stock disponible\n")
            except ValueError:
                print(" ERROR: Valor invalido\n")

        productos_disponibles[indice].cantidad_solicitada = cantidad
        seleccionados.append(productos_disponibles[indice])
        print(f"---Agregado: {productos_disponibles[indice].nombre}---\n---Cantidad:{cantidad}---")
        productos_disponibles[indice].stock = productos_disponibles[indice].stock - cantidad # ESTA LINEA ES LA QUE PERMITE MODIFICAR STOCK DISPONIBLE

        print()
        continuar = input("¿Desea agregar otro producto? (s/n): ").strip().lower()
        #Aca el profe ingreso x, y se procedió a la forma de pago.
        while (continuar != "n" and continuar != "s"): 
            print(" ERROR: Opcion no valida - Ingrese (s/n)\n")
            continuar = input("¿Desea agregar otro producto? (s/n): ").strip().lower()
            #LLAMAR A UNA FUNCION DE RESERVA
        if continuar == "n":
            break


def definir_pago():
    #  Forma de pago (selección por número)
    total = sum(p.precio * p.cantidad_solicitada for p in seleccionados)
    forma_de_pago = ""
    while forma_de_pago == "":
        print(f"\n----- Total a pagar: {total} -----\n Formas de pago disponibles:")
        print("1. Transferencia")
        print("2. Tarjeta")
        opcion = input("Ingrese el número de la forma de pago ( 1 / 2 ): ").strip()
        while (opcion != "1" and opcion != "2"): 
            print(" ERROR: Opcion no valida\n")
            opcion = input("Ingrese el número de la forma de pago ( 1 / 2 ): ").strip()
        if opcion == "1":
            forma_de_pago = "transferencia"
        elif opcion == "2":
            forma_de_pago = "tarjeta"

    return {
        "total": total,
        "forma_de_pago": forma_de_pago
    }


def definir_envio():
    #  Forma de envío (selección por número)
    metodo_envio = ""
    while metodo_envio == "":
        print(f"\n Metodos de envío disponibles:")
        print("1. Estándar")
        print("2. Express")
        print("3. Pickup")
        opcion = input("Ingrese el número del método de envío ( 1 / 2 / 3 ): ").strip()
        while (opcion != "1" and opcion != "2" and opcion != "3"): 
            print(" ERROR: Opcion no valida\n")
            opcion = input("Ingrese el número del método de envío ( 1 / 2 / 3 ): ").strip()
        if opcion == "1":
            metodo_envio = "estandar"
        elif opcion == "2":
            metodo_envio = "express"
        elif opcion == "3":
            metodo_envio = "pickup"
    
    return metodo_envio


def armar_pedido(deposito): #TODAS LAS FUNCIONES SE EJECUTAN DESDE ESTA FUNCION
    #  Armar datos finales
    datos = obtener_cliente()
    seleccionar_productos(deposito)
    pago = definir_pago()
    envio = definir_envio()
    pedido = {
        "cliente": datos["cliente"],
        "email": datos["email"],
        "direccion_envio": datos["direccion"],
        "productos": [
            {
                "sku": p.sku,
                "nombre": p.nombre,
                "precio": p.precio,
                "cantidad_solicitada": p.cantidad_solicitada
            } for p in seleccionados
        ],
        "datos_del_pago": {
            "metodo": pago["forma_de_pago"],
            "total_abonado": pago["total"],
            "numero_operacion": random.randint(1000, 20000)
        },
        "metodo_envio" : envio
    }

    return pedido
