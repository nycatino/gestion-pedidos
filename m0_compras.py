

import random


def seleccionar_productos(productos_disponibles):
    #  Datos del cliente
    cliente = input(" Ingrese su nombre: ").strip()
    while True:
        email = input(" Ingrese su email: ").strip()

        if "@" in email and "." in email.split("@")[-1]:
            break
        else:
            print(" Email inválido. Intente nuevamente.")

    direccion = input(" Ingrese su dirección de envío: ").strip()

    # Selección de productos
    seleccionados = []
    while True:
        print("\n Lista de productos disponibles:")
        for i, producto in enumerate(productos_disponibles):
            print(f"{i}. {producto}")

        while True:
            try:
                indice = int(input(" Ingrese el número del producto que desea agregar: "))
                if (0 <= indice < len(productos_disponibles) ):
                    break   # si llega hasta acá → es válido → rompemos el bucle
                else:
                    print("Índice inválido.")
            except ValueError:
                print("Valor inválido. Intente nuevamente.")
        
        while True:
            try:
                cantidad = int(input(" Ingrese cantidad del producto que desea comprar: "))
                if (cantidad >= 0 ):
                    break   # si llega hasta acá → es válido → rompemos el bucle
                else:
                    print(" La cantidad debe ser mayor o igual a cero.")
            except ValueError:
                print("Valor inválido. Intente nuevamente.")

        productos_disponibles[indice].cantidad_solicitada = cantidad
        seleccionados.append(productos_disponibles[indice])
        print(f" Agregado: {productos_disponibles[indice].nombre} x{cantidad}")

        continuar = input("¿Desea agregar otro producto? (s/n): ").strip().lower()
        #Aca el profe ingreso x, y se procedió a la forma de pago.
        while (continuar != "n" and continuar != "s"): 
            print("Ingrese (s/n)")
            continuar = input("¿Desea agregar otro producto? (s/n): ").strip().lower()
        if continuar == "n":
            break

    #  Forma de pago (selección por número)
    total = sum(p.precio * p.cantidad_solicitada for p in seleccionados)
    forma_de_pago = ""
    while forma_de_pago == "":
        print(f"\n Total a pagar: {total}\n Formas de pago disponibles:")
        print("1. Transferencia")
        print("2. Tarjeta")
        opcion = input("Ingrese el número de la forma de pago (1 o 2): ").strip()
        while (opcion != "1" and opcion != "2"): 
            print("Ingrese (1 o 2)")
            opcion = input("Ingrese el número de la forma de pago (1 o 2): ").strip()
        if opcion == "1":
            forma_de_pago = "transferencia"
        elif opcion == "2":
            forma_de_pago = "tarjeta"


    #  Forma de envío (selección por número)
    metodo_envio = ""
    while metodo_envio == "":
        print(f"\n Metodos de envío disponibles:")
        print("1. Estándar")
        print("2. Express")
        print("3. Pickup")
        opcion = input("Ingrese el número del método de envío (1, 2 o 3): ").strip()
        while (opcion != "1" and opcion != "2" and opcion != "3"): 
            print("Ingrese (1, 2 o 3)")
            opcion = input("Ingrese el número del método de envío (1, 2 o 3): ").strip()
        if opcion == "1":
            metodo_envio = "estandar"
        elif opcion == "2":
            metodo_envio = "express"
        elif opcion == "3":
            metodo_envio = "pickup"


    #  Armar datos finales
    pedido = {
        "cliente": cliente,
        "email": email,
        "direccion_envio": direccion,
        "productos": [
            {
                "sku": p.sku,
                "nombre": p.nombre,
                "precio": p.precio,
                "cantidad_solicitada": p.cantidad_solicitada
            } for p in seleccionados
        ],
        "datos_del_pago": {
            "metodo": forma_de_pago,
            "total_abonado":total,
            "numero_operacion":random.randint(1000, 20000)
        },
        "metodo_envio" : metodo_envio
    }

    return pedido
