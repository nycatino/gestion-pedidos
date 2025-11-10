

import random


def seleccionar_productos(productos_disponibles):
    #  Datos del cliente
    cliente = input(" Ingrese su nombre: ").strip()
    email = input(" Ingrese su email: ").strip()
    direccion = input(" Ingrese su dirección de envío: ").strip()

    # Selección de productos
    seleccionados = []
    while True:
        print("\n Lista de productos disponibles:")
        for i, producto in enumerate(productos_disponibles):
            print(f"{i}. {producto}")

        try:
            indice = int(input(" Ingrese el número del producto que desea agregar: "))
            if 0 <= indice < len(productos_disponibles):
                cantidad = int(input(" Ingrese cantidad del producto que desea comprar: "))
                if cantidad >= 0:
                    productos_disponibles[indice].cantidad_solicitada = cantidad
                    seleccionados.append(productos_disponibles[indice])
                    print(f" Agregado: {productos_disponibles[indice].nombre} x{cantidad}")
                else:
                    print(" La cantidad debe ser mayor o igual a cero.")
            else:
                print(" Índice inválido.")
        except ValueError:
            print(" Por favor, ingrese un número válido.")

        continuar = input("¿Desea agregar otro producto? (s/n): ").strip().lower()
        if continuar != "s":
            break

    #  Forma de pago (selección por número)
    total = sum(p.precio * p.cantidad_solicitada for p in seleccionados)
    forma_de_pago = ""
    while forma_de_pago == "":
        print(f"\n Total a pagar: {total}\n Formas de pago disponibles:")
        print("1. Transferencia")
        print("2. Tarjeta")
        opcion = input("Ingrese el número de la forma de pago (1 o 2): ").strip()

        if opcion == "1":
            forma_de_pago = "transferencia"
        elif opcion == "2":
            forma_de_pago = "tarjeta"
        else:
            print(" Opción inválida. Por favor, elija 1 o 2.")


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
        }
    }

    return pedido
