import json
import random

from modelos.pedido import Producto


def guardar_stock(productos_disponibles, archivo="stock.json"):
    stock_data = []

    for p in productos_disponibles:
        item = {
            "sku": p.sku,
            "nombre": p.nombre,
            "precio": p.precio,
            "stock": random.randint(0, 100)   # stock aleatorio 0–100
        }
        stock_data.append(item)

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=4, ensure_ascii=False)

    print(f"📦 Stock guardado correctamente en {archivo}")

# ---------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# ---------------------------------------------------------

if __name__ == "__main__":
    productos_disponibles = Producto.crear_productos()
    print("Productos generados:")
    for p in productos_disponibles:
        print(p)

    guardar_stock(productos_disponibles,"stock.json")